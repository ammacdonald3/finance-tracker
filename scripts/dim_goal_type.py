import requests
import json
import sqlalchemy
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date


from models import GoalType, GoalTypeSnap, Day
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


    # Delete existing data in the DIM_GOAL_TYPE table
    session.query(GoalType).delete()
    session.commit()


    # Get today's date (used for snapshot date)
    today = date.today()
    date_id = int(today.strftime('%Y%m%d'))

    date_key = session.query(Day.date_key).\
        filter_by(date_id=date_id).\
        scalar()


    new_goaltype_1 = GoalType(goal_type_code='TB',
    goal_type_name='Target Category Balance')

    new_goaltype_2 = GoalType(goal_type_code='TBD',
    goal_type_name='Target Category Balance by Date')

    new_goaltype_3 = GoalType(goal_type_code='MF',
    goal_type_name='Monthly Funding')

    new_goaltype_4 = GoalType(goal_type_code='NEED',
    goal_type_name='Plan Your Spending')

    session.add_all([
        new_goaltype_1, 
        new_goaltype_2, 
        new_goaltype_3, 
        new_goaltype_4
        ])



    new_snap_goaltype_1 = GoalTypeSnap(snapshot_date_key=date_key, goal_type_code='TB',
    goal_type_name='Target Category Balance')

    new_snap_goaltype_2 = GoalTypeSnap(snapshot_date_key=date_key, goal_type_code='TBD',
    goal_type_name='Target Category Balance by Date')

    new_snap_goaltype_3 = GoalTypeSnap(snapshot_date_key=date_key, goal_type_code='MF',
    goal_type_name='Monthly Funding')

    new_snap_goaltype_4 = GoalTypeSnap(snapshot_date_key=date_key, goal_type_code='NEED',
    goal_type_name='Plan Your Spending')

    session.add_all([
        new_snap_goaltype_1, 
        new_snap_goaltype_2, 
        new_snap_goaltype_3, 
        new_snap_goaltype_4
        ])


    session.commit()


except:
    logger.exception('DIM_GOAL_TYPE LOAD')
    raise