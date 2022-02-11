import sqlalchemy
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


from models import Account, AccountSnap, Category, CategorySnap, Payee, PayeeSnap, CategoryGoal, CategoryGoalSnap, Transaction, TransactionSnap, MonthlyBudget, MonthlyBudgetSnap, GoalType, GoalTypeSnap
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


    # Delete data in non-static tables
    session.query(CategoryGoal).delete()
    session.query(CategoryGoalSnap).delete()
    session.query(Transaction).delete()
    session.query(TransactionSnap).delete()
    session.query(MonthlyBudget).delete()
    session.query(MonthlyBudgetSnap).delete()
    session.query(Account).delete()
    session.query(AccountSnap).delete()
    session.query(Category).delete()
    session.query(CategorySnap).delete()
    session.query(Payee).delete()
    session.query(PayeeSnap).delete()
    session.query(GoalType).delete()
    session.query(GoalTypeSnap).delete()



    session.commit()


except:
    logger.exception('DELETE_DATA.PY')
    raise