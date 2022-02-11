import requests
import json
import sqlalchemy
import re
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

from scripts.models import Month, Category, CategorySnap, GoalType, GoalTypeSnap, CategoryGoal, CategoryGoalSnap, Day
from scripts.config import Config


# BELOW LOGGING CODE USED FOR LOCAL TROUBLESHOOTING

# Create a logging instance
# logger = logging.getLogger('sqlalchemy')
# logger.setLevel(logging.ERROR) # this can be set to DEBUG, INFO, ERROR

# # Assign a file-handler to that instance
# fh = logging.FileHandler(Config.ERROR_LOGGING_FILE)
# fh.setLevel(logging.ERROR) # this can be set to DEBUG, INFO, ERROR

# # Format logs (optional)
# formatter = logging.Formatter('\n %(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter) # This will set the format to the file handler

# # Add the handler to logging instance
# logger.addHandler(fh)


# try:

# ABOVE LOGGING CODE USED FOR LOCAL TROUBLESHOOTING

def fact_category_goal_load():

    counter = 0
    
    # Conenct to database
    engine = create_engine(Config.DATABASE_URL, echo=True)
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


    # Get today's date (used for snapshot date)
    today = date.today()
    date_id = int(today.strftime('%Y%m%d'))

    date_key = session.query(Day.date_key).\
        filter_by(date_id=date_id).\
        scalar()


    # Delete existing data in the FACT_CATEGORY_GOAL table
    session.query(CategoryGoal).delete()
    session.commit()


    # Loop through list and insert each category to DIM_CATEGORY
    for category_group_item in category_group_list:

        for category_item in category_group_item['categories']:

            goal_target_amount = category_item['goal_target']

            if goal_target_amount != 0:

                category_id = category_item['id']
                category_key = session.query(Category.category_key).\
                    filter_by(category_id=category_id).\
                    scalar()

                category_snap_key = session.query(CategorySnap.category_snap_key).\
                    filter_by(category_id=category_id).\
                    filter_by(snapshot_date_key=date_key).\
                    scalar()

                
                goal_type_code = category_item['goal_type']
                goal_type_key = session.query(GoalType.goal_type_key).\
                    filter_by(goal_type_code=goal_type_code).\
                    scalar()

                goal_type_snap_key = session.query(GoalTypeSnap.goal_type_snap_key).\
                    filter_by(goal_type_code=goal_type_code).\
                    filter_by(snapshot_date_key=date_key).\
                    scalar()


                goal_creation_month = category_item['goal_creation_month']
                if goal_creation_month:
                    goal_creation_month_key = session.query(Month.month_key).\
                        filter_by(year_month_id=goal_creation_month[:7]).\
                        scalar()
                else:
                    goal_creation_month_key = 0

                goal_target_month = category_item['goal_target_month']
                if goal_target_month:
                    goal_target_month_key = session.query(Month.month_key).\
                        filter_by(year_month_id=goal_target_month[:7]).\
                        scalar()
                else:
                    goal_target_month_key = 0

                goal_percentage_complete = category_item['goal_percentage_complete']


                new_category_goal = CategoryGoal(
                category_key=category_key,
                goal_type_key=goal_type_key,
                goal_creation_month_key=goal_creation_month_key,
                goal_target_month_key=goal_target_month_key,
                goal_target_amount=goal_target_amount,
                goal_percentage_complete=goal_percentage_complete
                )
                
                session.add(new_category_goal)


                new_category_goal_snap = CategoryGoalSnap(
                snapshot_date_key=date_key,
                category_snap_key=category_snap_key,
                goal_type_snap_key=goal_type_snap_key,
                goal_creation_month_key=goal_creation_month_key,
                goal_target_month_key=goal_target_month_key,
                goal_target_amount=goal_target_amount,
                goal_percentage_complete=goal_percentage_complete
                )
                
                session.add(new_category_goal_snap)



                session.commit()

                counter += 1


    return f"{counter} rows inserted successfully to FACT_CATEGORY_GOAL and FACT_CATEGORY_GOAL_SNAP"
        
# BELOW LOGGING CODE USED FOR LOCAL TROUBLESHOOTING

# except:
#     logger.exception('FACT_CATEGORY_GOAL LOAD')
#     raise

# ABOVE LOGGING CODE USED FOR LOCAL TROUBLESHOOTING
