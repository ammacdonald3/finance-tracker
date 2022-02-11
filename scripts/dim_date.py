import sqlalchemy
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
#from datetime import datetime
import datetime
#from datetime import strftime

from scripts.models import Day, Month
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

def dim_date_load():

    counter = 0

    # Conenct to database
    engine = create_engine(Config.DATABASE_URL, echo=True)

    Base = declarative_base()

    # Start sessions
    Session = sessionmaker(bind=engine)
    session = Session()


    # Truncate existing DIM_DATE
    session.query(Day).delete()
    session.commit()


    # Date info used for DIM_MONTH and DIM_DATE
    month_codes = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    month_names = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    month_days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}


    # Populate DIM_DATE table
    day_counter = 1
    month_counter = 1
    year_counter = 2016

    for day in range(3600):
        if year_counter % 4 == 0:
            month_days[2] == 29
        else:
            month_days[2] == 28
        
        day = datetime.date(year_counter, month_counter, day_counter)
        date_id = int(day.strftime('%Y%m%d'))
        day_of_month = day_counter
        month_code = month_codes[month_counter]
        month_name = month_names[month_counter]
        year_name = year_counter
        year_month_name = str(year_name) + '-' + month_code
        year_month_day_name = str(year_name) + '-' + month_code + '-' + str(day_of_month)

        
        if month_counter <= 12 and day_counter < month_days[month_counter]:
            day_counter += 1
        elif month_counter < 12 and day_counter == month_days[month_counter]:
            day_counter = 1
            month_counter += 1
        elif month_counter == 12 and day_counter == month_days[month_counter]:
            day_counter = 1
            month_counter = 1
            year_counter += 1 

        month_key = session.query(Month.month_key).\
            filter(Month.year_month_name==year_month_name).scalar()
        

        new_day = Day(date_name=day, date_id=date_id, day_of_month=day_of_month, month_key=month_key, month_code=month_code, month_name=month_name, year_name=year_name, year_month_name=year_month_name, year_month_day_name=year_month_day_name)

        session.add(new_day)
        session.commit()

        counter += 1


    return f"{counter} rows inserted successfully to DIM_DATE"

# BELOW LOGGING CODE USED FOR LOCAL TROUBLESHOOTING

# except:
#     logger.exception('DIM_DATE LOAD')
#     raise

# ABOVE LOGGING CODE USED FOR LOCAL TROUBLESHOOTING
