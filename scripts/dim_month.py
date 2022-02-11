import sqlalchemy
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from scripts.models import Month
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

def dim_month_load():
    
    counter = 0

    # Conenct to database
    engine = create_engine(Config.DATABASE_URL, echo=True)

    Base = declarative_base()

    # Start sessions
    Session = sessionmaker(bind=engine)
    session = Session()

    # Truncate existing DIM_MONTH
    #session.query(Month).delete()
    #session.commit()
    # UNDO ABOVE

    # Date info used for DIM_MONTH
    month_codes = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    month_names = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    month_days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}


    # Add dummy record
    dummy_month = Month(month_key=0, month_id=0, month_code='None', month_name='None', year_name=0, year_month_id='0000-00', year_month_name='0000-None')

    session.add(dummy_month)
    session.commit()

    # Populate DIM_MONTH table
    month_counter = 1
    year_counter = 2016

    for month in range(120):
        month_id = month_counter
        month_code = month_codes[month_counter]
        month_name = month_names[month_counter]
        year_name = year_counter
        if month_counter < 10:
            year_month_id = f"{year_counter}-0{month_counter}"
        else:
            year_month_id = f"{year_counter}-{month_counter}"
        year_month_name = str(year_name) + '-' + month_code

        if month_counter < 12:
            month_counter += 1
        else:
            month_counter = 1
            year_counter += 1

        new_month = Month(month_id=month_id, month_code=month_code, month_name=month_name, year_name=year_name, year_month_id=year_month_id, year_month_name=year_month_name)

        session.add(new_month)
        session.commit()

        counter += 1


    return f"{counter} rows inserted successfully to DIM_MONTH"

# BELOW LOGGING CODE USED FOR LOCAL TROUBLESHOOTING

# except:
#     logger.exception('DIM_MONTH LOAD')
#     raise

# ABOVE LOGGING CODE USED FOR LOCAL TROUBLESHOOTING
