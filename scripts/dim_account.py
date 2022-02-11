import requests
import json
import sqlalchemy
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date


from scripts.models import Account, AccountSnap, Day
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

def dim_account_load():

    counter = 0

    # Conenct to database
    engine = create_engine(Config.DATABASE_URL, echo=True)
    Base = declarative_base()



    # Start sessions
    Session = sessionmaker(bind=engine)
    session = Session()



    # Retrieve data from YNAB API
    url = Config.YNAB_URL + "accounts"
    headers = {"authorization" : "bearer " + Config.BEARER}
    response = requests.get(url, headers=headers)


    # Parse ACCOUNT data into list
    account_list = response.json()['data']['accounts']


    # Delete existing data in the DIM_account table
    session.query(Account).delete()
    session.commit()


    # Get today's date (used for snapshot date)
    today = date.today()
    date_id = int(today.strftime('%Y%m%d'))

    date_key = session.query(Day.date_key).\
        filter_by(date_id=date_id).\
        scalar()


    # Loop through list and insert each account to DIM_ACCOUNT
    for account_item in account_list:
        
        account_id = account_item['id']
        account_name = account_item['name']
        account_type = account_item['type']

        if account_item['on_budget'] == True:
            account_budget_status = 'Account On Budget'
        else:
            account_budget_status = 'Account Off Budget'
        
        if account_item['closed'] == True:
            account_open_status = 'Account Closed'
        else:
            account_open_status = 'Account Open'

        account_note = account_item['note']
        account_balance = account_item['balance']
        account_cleared_balance = account_item['cleared_balance']
        account_uncleared_balance = account_item['uncleared_balance']

        if account_item['deleted'] == True:
            account_deletion_status = 'Account Deleted'
        else:
            account_deletion_status = 'Account Active'
        
        new_account = Account(account_id=account_id, 
        account_name=account_name, 
        account_type=account_type, 
        account_budget_status=account_budget_status, 
        account_open_status=account_open_status, 
        account_note=account_note, 
        account_balance=account_balance, 
        account_cleared_balance=account_cleared_balance, 
        account_uncleared_balance=account_uncleared_balance, 
        account_deletion_status=account_deletion_status)
        
        session.add(new_account)


        new_account_snap = AccountSnap(snapshot_date_key=date_key,
        account_id=account_id, 
        account_name=account_name, 
        account_type=account_type, 
        account_budget_status=account_budget_status, 
        account_open_status=account_open_status, 
        account_note=account_note, 
        account_balance=account_balance, 
        account_cleared_balance=account_cleared_balance, 
        account_uncleared_balance=account_uncleared_balance, 
        account_deletion_status=account_deletion_status)
        
        session.add(new_account_snap)


        session.commit()

        counter += 1

    return f"{counter} rows inserted successfully to DIM_ACCOUNT and DIM_ACCOUNT_SNAP"


# BELOW LOGGING CODE USED FOR LOCAL TROUBLESHOOTING

# except:
#     logger.exception('DIM_ACCOUNT LOAD')
#     raise

# ABOVE LOGGING CODE USED FOR LOCAL TROUBLESHOOTING
