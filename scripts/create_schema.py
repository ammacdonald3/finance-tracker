from scripts.models import Payee, Category, GoalType, Account, Month, Day, MonthlyBudget, Transaction
from scripts.database import engine, Base

def create_schema_function():
    # Drop all existing tables
    Base.metadata.drop_all(engine)

    # Create all tables defined in above import
    Base.metadata.create_all(engine)