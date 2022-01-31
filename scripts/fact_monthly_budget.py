import requests
import json
import sqlalchemy
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

from models import MonthlyBudget, MonthlyBudgetSnap, Category, CategorySnap, Month, Day
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


    # Delete existing data in the FACT_MONTHLY_BUDGET table
    session.query(MonthlyBudget).delete()
    session.commit()



    # Get today's date (used to establish this month's budgets)
    today = date.today()
    this_year_month = today.strftime("%Y-%b")

    month_key = session.query(Month.month_key).\
        filter_by(year_month_name=this_year_month).\
        scalar()


    # Get today's date (used for snapshot date)
    date_id = int(today.strftime('%Y%m%d'))

    date_key = session.query(Day.date_key).\
        filter_by(date_id=date_id).\
        scalar()



    # Loop through list and insert to FACT_MONTHLY_BUDGET
    for category_group_item in category_group_list:
        
        category_group_id = category_group_item['id']

        for category_item in category_group_item['categories']:

            category_id = category_item['id']

            category_key = session.query(Category.category_key).\
                filter_by(category_id=category_id).\
                scalar()

            category_snap_key = session.query(CategorySnap.category_snap_key).\
                filter_by(category_id=category_id).\
                filter_by(snapshot_date_key=date_key).\
                scalar()

            budgeted_amount = category_item['budgeted']
            activity_amount = category_item['activity']
            balance_amount = category_item['balance']


            new_monthly_budget = MonthlyBudget(
            category_key=category_key,
            month_key=month_key,
            budgeted_amount=budgeted_amount,
            activity_amount=activity_amount,
            balance_amount=balance_amount 
            )
            
            session.add(new_monthly_budget)


            new_monthly_budget_snap = MonthlyBudgetSnap(
            snapshot_date_key=date_key,
            category_snap_key=category_snap_key,
            month_key=month_key,
            budgeted_amount=budgeted_amount,
            activity_amount=activity_amount,
            balance_amount=balance_amount 
            )
            
            session.add(new_monthly_budget_snap)


            session.commit()

except:
    logger.exception('FACT_MONTHLY_BUDGET LOAD')
    raise
