import requests
import json
import sqlalchemy
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date


from models import Category, CategorySnap, Day
from config import Config


# Create a logging instance
logger = logging.getLogger('sqlalchemy')
logger.setLevel(logging.ERROR) # this can be set to DEBUG, INFO, ERROR

# Assign a file-handler to that instance
fh = logging.FileHandler(Config.ERROR_LOGGING_FILE)
fh.setLevel(logging.ERROR) # this can be set to DEBUG, INFO, ERROR

# Format logs (optional)
formatter = logging.Formatter('\n %(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter) # This will set the format to the file handler

# Add the handler to logging instance
logger.addHandler(fh)


try:

    # Conenct to database
    engine = create_engine(Config.AWS_DATABASE_URL, echo=True)
    Base = declarative_base()



    # Start sessions
    Session = sessionmaker(bind=engine)
    session = Session()



    # Retrieve data from YNAB API
    url = Config.YNAB_URL + "categories"
    headers = {"authorization" : "bearer " + Config.BEARER}
    response = requests.get(url, headers=headers)


    # Parse CATEGORY data into list
    category_group_list = response.json()['data']['category_groups']


    # Delete existing data in the DIM_CATEGORY table
    session.query(Category).delete()
    session.commit()


    # Get today's date (used for snapshot date)
    today = date.today()
    date_id = int(today.strftime('%Y%m%d'))

    date_key = session.query(Day.date_key).\
        filter_by(date_id=date_id).\
        scalar()


    # Loop through list and insert each category to DIM_CATEGORY
    for category_group_item in category_group_list:
        
        category_group_id = category_group_item['id']
        category_group_name = category_group_item['name']
        
        if category_group_item['hidden'] == True:
            category_group_visibility_status = 'Category Group Hidden'
        else:
            category_group_visibility_status = 'Category Group Visible'

        if category_group_item['deleted'] == True:
            category_group_deletion_status = 'Category Group Deleted'
        else:
            category_group_deletion_status = 'Category Group Active'

        for category_item in category_group_item['categories']:

            category_id = category_item['id']
            category_name = category_item['name']
            category_note = category_item['note']

            if category_item['hidden'] == True:
                category_visibility_status = 'Category Hidden'
            else:
                category_visibility_status = 'Category Visible'

            if category_item['deleted'] == True:
                category_deletion_status = 'Category Deleted'
            else:
                category_deletion_status = 'Category Active'

            new_category = Category(category_id=category_id, 
            category_name=category_name, 
            category_visibility_status=category_visibility_status,
            category_note=category_note,
            category_deletion_status=category_deletion_status,
            category_group_id=category_group_id,
            category_group_name=category_group_name,
            category_group_visibility_status=category_group_visibility_status,
            category_group_deletion_status=category_group_deletion_status)
            
            session.add(new_category)


            new_category_snap = CategorySnap(snapshot_date_key=date_key,
            category_id=category_id, 
            category_name=category_name, 
            category_visibility_status=category_visibility_status,
            category_note=category_note,
            category_deletion_status=category_deletion_status,
            category_group_id=category_group_id,
            category_group_name=category_group_name,
            category_group_visibility_status=category_group_visibility_status,
            category_group_deletion_status=category_group_deletion_status)
            
            session.add(new_category_snap)


            session.commit()
        
except:
    logger.exception('DIM_CATEGORY LOAD')
    raise