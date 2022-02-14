import sqlalchemy
import re
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



from scripts.models import MonthlyBudget, CategoryGoal, Transaction
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

def delete_fact_table_data():

    # Conenct to database
    engine = create_engine(Config.DATABASE_URL, echo=True)
    Base = declarative_base()


    # Start sessions
    Session = sessionmaker(bind=engine)
    session = Session()


    # Delete existing data in the fact tables
    session.query(MonthlyBudget).delete()
    session.query(CategoryGoal).delete()
    session.query(Transaction).delete()
    session.commit()

    return "Data deleted successfully from all fact tables"

# BELOW LOGGING CODE USED FOR LOCAL TROUBLESHOOTING

# except:
#     logger.exception('DELETE_FACT_TABLE_DATA.PY')
#     raise

# ABOVE LOGGING CODE USED FOR LOCAL TROUBLESHOOTING