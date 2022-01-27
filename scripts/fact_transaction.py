import requests
import json
import sqlalchemy
import re
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date


from models import Account, AccountSnap, Payee, PayeeSnap, Category, CategorySnap, Day, Transaction, TransactionSnap
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
    engine = create_engine(Config.DATABASE_URL, echo=True)
    Base = declarative_base()



    # Start sessions
    Session = sessionmaker(bind=engine)
    session = Session()



    # Retrieve data from YNAB API
    url = Config.YNAB_URL + "transactions"
    headers = {"authorization" : "bearer " + Config.BEARER}
    response = requests.get(url, headers=headers)


    # Parse TRANSACTION data into list
    transaction_list = response.json()['data']['transactions']



    # Get today's date (used for snapshot date)
    today = date.today()
    date_id = int(today.strftime('%Y%m%d'))

    today_date_key = session.query(Day.date_key).\
        filter_by(date_id=date_id).\
        scalar()


    # Delete existing data in the FACT_TRANSACTION table
    session.query(Transaction).delete()
    session.commit()


    # Loop through list and insert each category to FACT_TRANSACTION
    for transaction in transaction_list:

        transaction_id = transaction['id']

        account_id = transaction['account_id']
        account_key = session.query(Account.account_key).\
            filter_by(account_id=account_id).\
                scalar()

        account_snap_key = session.query(AccountSnap.account_snap_key).\
            filter_by(account_id=account_id).\
            filter_by(snapshot_date_key=today_date_key).\
                scalar()


        payee_id = transaction['payee_id']
        payee_key = session.query(Payee.payee_key).\
            filter_by(payee_id=payee_id).\
                scalar()

        payee_snap_key = session.query(PayeeSnap.payee_snap_key).\
            filter_by(payee_id=payee_id).\
            filter_by(snapshot_date_key=today_date_key).\
                scalar()


        category_id = transaction['category_id']
        category_key = session.query(Category.category_key).\
            filter_by(category_id=category_id).\
            scalar()

        category_snap_key = session.query(CategorySnap.category_snap_key).\
            filter_by(category_id=category_id).\
            filter_by(snapshot_date_key=today_date_key).\
            scalar()


        transaction_date = re.sub('[^0-9]+', '', transaction['date'])
        date_key = session.query(Day.date_key).\
            filter_by(date_id=transaction_date).\
            scalar()

        transaction_amount = transaction['amount']


        new_transaction = Transaction(
        transaction_id=transaction_id,
        account_key=account_key,
        payee_key=payee_key,
        category_key=category_key,
        date_key=date_key,
        transaction_amount=transaction_amount 
        )
        
        session.add(new_transaction)


        new_transaction_snap = TransactionSnap(
        snapshot_date_key=today_date_key,
        transaction_id=transaction_id,
        account_snap_key=account_snap_key,
        payee_snap_key=payee_snap_key,
        category_snap_key=category_snap_key,
        date_key=date_key,
        transaction_amount=transaction_amount 
        )
        
        session.add(new_transaction_snap)


        session.commit()
        

except:
    logger.exception('FACT_TRANSACTION LOAD')
    raise