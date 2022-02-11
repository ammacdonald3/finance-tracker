import sqlalchemy
import urllib
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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


# Connect to database
engine = create_engine(Config.DATABASE_URL, echo=True)
Base = declarative_base()

# Start sessions
Session = sessionmaker(bind=engine)
session = Session()

print("The database.py file was run successfully")


# BELOW LOGGING CODE USED FOR LOCAL TROUBLESHOOTING

# except:
#     logger.exception('DATABASE.PY')
#     raise

# ABOVE LOGGING CODE USED FOR LOCAL TROUBLESHOOTING
