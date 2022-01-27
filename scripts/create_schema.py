from models import Payee, Category, GoalType, Account, Month, Day, MonthlyBudget, Transaction
from database import engine, Base


# Drop all existing tables
Base.metadata.drop_all(engine)

# CREATE ALL TABLES DEFINED ABOVE
Base.metadata.create_all(engine)