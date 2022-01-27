import requests
import json
import sqlalchemy
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date


from models import Payee, PayeeSnap, Day
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
    url = Config.YNAB_URL + "payees"
    headers = {"authorization" : "bearer " + Config.BEARER}
    response = requests.get(url, headers=headers)


    # Parse PAYEE data into list
    payee_list = response.json()['data']['payees']


    # Delete existing data in the DIM_PAYEE table
    session.query(Payee).delete()
    session.commit()


    # Get today's date (used for snapshot date)
    today = date.today()
    date_id = int(today.strftime('%Y%m%d'))

    date_key = session.query(Day.date_key).\
        filter_by(date_id=date_id).\
        scalar()


    # Loop through list and insert each payee to DIM_PAYEE
    for payee_item in payee_list:
        #print(payee_item['name'])
        
        payee_id = payee_item['id']
        payee_name = payee_item['name']
        
        if payee_item['deleted'] == True:
            payee_deletion_status = 'Payee Deleted'
        else:
            payee_deletion_status = 'Payee Active'
        
        new_payee = Payee(payee_id=payee_id, 
        payee_name=payee_name, 
        payee_deletion_status=payee_deletion_status)

        session.add(new_payee)


        new_payee_snap = PayeeSnap(snapshot_date_key=date_key,
        payee_id=payee_id, 
        payee_name=payee_name, 
        payee_deletion_status=payee_deletion_status
        )
        
        session.add(new_payee_snap)

        
        session.commit()


except:
    logger.exception('DIM_PAYEE LOAD')
    raise