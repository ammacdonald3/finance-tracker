import sqlalchemy

from sqlalchemy import Column, Integer, String, Numeric, Table, ForeignKey, Date
from sqlalchemy.orm import relationship

from scripts.config import Config
from scripts.database import Base


class Month(Base):
    __tablename__ = 'dim_month'

    month_key = Column(Integer, primary_key=True)
    month_id = Column(Integer)
    month_code = Column(String)
    month_name = Column(String)
    year_name = Column(Integer)
    year_month_id = Column(String)
    year_month_name = Column(String)

    month_day = relationship('Day', backref='month')
    month_budget = relationship('MonthlyBudget', backref='month')
    month_budget_snap = relationship('MonthlyBudgetSnap', backref='month')
    #month_goal_creation = relationship('CategoryGoal', backref='month')
    #month_goal_creation_snap = relationship('CategoryGoalSnap', backref='month')
    #month_goal_target = relationship('CategoryGoal', backref='month')
    #month_goal_target_snap = relationship('CategoryGoalSnap', backref='month')

    #month_goal_creation = relationship('CategoryGoal', foreign_keys='fact_category_goal.goal_creation_month_key')
    #month_goal_target = relationship('CategoryGoal', foreign_keys='fact_category_goal.goal_target_month_key')
    #month_goal_creation_snap = relationship('CategoryGoalSnap', foreign_keys='fact_category_goal_snap.goal_creation_month_key')
    #month_goal_target_snap = relationship('CategoryGoalSnap', foreign_keys='fact_category_goal_snap.goal_target_month_key')

    def __repr__(self):
        return "<(month_name='%s')" % (self.month_name)


class Day(Base):
    __tablename__ = 'dim_date'

    date_key = Column(Integer, primary_key=True)
    date_id = Column(Integer)
    date_name = Column(Date)
    day_of_month = Column(Integer)
    month_key = Column(Integer, ForeignKey('dim_month.month_key'))
    month_code = Column(String)
    month_name = Column(String)
    year_name = Column(Integer)
    year_month_name = Column(String)
    year_month_day_name = Column(String)

    day_transaction = relationship('Transaction', backref='day')
    #day_transaction_snap = relationship('TransactionSnap', backref='day')
    day_account_snapshot_date = relationship('AccountSnap', backref='day')
    day_category_snapshot_date = relationship('CategorySnap', backref='day')
    day_payee_snapshot_date = relationship('PayeeSnap', backref='day')
    day_goaltype_snapshot_date = relationship('GoalTypeSnap', backref='day')
    day_monthlybudget_snapshot_date = relationship('MonthlyBudgetSnap', backref='day')
    #day_transaction_snapshot_date = relationship('TransactionSnap', backref='day')
    day_categorygoal_snapshot_date = relationship('CategoryGoalSnap', backref='day')

    #day_transaction_snap = relationship('TransactionSnap', foreign_keys='fact_transaction_snap.date_key')
    #day_transaction_snapshot_date = relationship('TransactionSnap', foreign_keys='fact_transaction_snap.snapshot_date_key')

    def __repr__(self):
        return "<(month_name='%s')" % (self.month_name)


class Account(Base):
    __tablename__ = 'dim_account'

    account_key = Column(Integer, primary_key=True)
    account_id = Column(String)
    account_name = Column(String)
    account_type = Column(String)
    account_budget_status = Column(String)
    account_open_status = Column(String)
    account_note = Column(String)
    account_balance = Column(Numeric)
    account_cleared_balance = Column(Numeric)
    account_uncleared_balance = Column(Numeric)
    account_deletion_status = Column(String)

    account_transaction = relationship('Transaction', backref='account')

    def __repr__(self):
        return "<(account_name='%s')" % (self.account_name)


class Category(Base):
    __tablename__ = 'dim_category'

    category_key = Column(Integer, primary_key=True)
    category_id = Column(String)
    category_name = Column(String)
    category_visibility_status = Column(String)
    category_note = Column(String)
    category_deletion_status = Column(String)
    category_group_id = Column(String)
    category_group_name = Column(String)
    category_group_visibility_status = Column(String)
    category_group_deletion_status = Column(String)

    monthly_budget_category = relationship('MonthlyBudget', backref='category')
    category_transaction = relationship('Transaction', backref = 'category')
    category_goal = relationship('CategoryGoal', backref = 'category')

    def __repr__(self):
        return "<('category_name'='%s')" % (self.category_name)


class Payee(Base):
    __tablename__ = 'dim_payee'
    
    payee_key = Column(Integer, primary_key=True)
    payee_id = Column(String)
    payee_name = Column(String)
    payee_deletion_status = Column(String)

    payee_transaction = relationship('Transaction', backref='payee')
    
    def __repr__(self):
        return "<(payee_name='%s')" % (self.payee_name)


class GoalType(Base):
    __tablename__ = 'dim_goal_type'

    goal_type_key = Column(Integer, primary_key=True)
    goal_type_code = Column(String)
    goal_type_name = Column(String)

    goaltype_goal = relationship('CategoryGoal', backref = 'goaltype')

    def __repr__(self):
        return "<(goal_type_name='%s')" % (self.goal_type_name)


class MonthlyBudget(Base):
    __tablename__ = 'fact_monthly_budget'

    monthly_budget_key = Column(Integer, primary_key=True)
    category_key = Column(Integer, ForeignKey('dim_category.category_key'))
    month_key = Column(Integer, ForeignKey('dim_month.month_key'))
    budgeted_amount = Column(Numeric)
    activity_amount = Column(Numeric)
    balance_amount = Column(Numeric)

    def __repr__(self):
        return "<(monthly_budget='%s')" % (self.monthly_budget_key)

    
class Transaction(Base):
    __tablename__ = 'fact_transaction'

    transaction_key = Column(Integer, primary_key=True)
    transaction_id = Column(String)
    account_key = Column(Integer, ForeignKey('dim_account.account_key'))
    payee_key = Column(Integer, ForeignKey('dim_payee.payee_key'))
    category_key = Column(Integer, ForeignKey('dim_category.category_key'))
    date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    transaction_amount = Column(Numeric)

    def __repr__(self):
        return "<(transaction='%s')" % (self.transaction_id)


class CategoryGoal(Base):
    __tablename__ = 'fact_category_goal'

    category_goal_key = Column(Integer, primary_key=True)
    category_key = Column(Integer, ForeignKey('dim_category.category_key'))
    goal_creation_month_key = Column(Integer, ForeignKey('dim_month.month_key'))
    goal_target_month_key = Column(Integer, ForeignKey('dim_month.month_key'))
    goal_type_key = Column(Integer, ForeignKey('dim_goal_type.goal_type_key'))
    goal_target_amount = Column(Numeric)
    goal_percentage_complete = Column(Numeric)

    goal_creation_month = relationship("Month", foreign_keys=[goal_creation_month_key])
    goal_target_month = relationship("Month", foreign_keys=[goal_target_month_key])

    def __repr__(self):
        return "<(category_goal='%s')" % (self.category_goal_key)


class AccountSnap(Base):
    __tablename__ = 'dim_account_snap'

    snapshot_date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    account_snap_key = Column(Integer, primary_key=True)
    account_id = Column(String)
    account_name = Column(String)
    account_type = Column(String)
    account_budget_status = Column(String)
    account_open_status = Column(String)
    account_note = Column(String)
    account_balance = Column(Numeric)
    account_cleared_balance = Column(Numeric)
    account_uncleared_balance = Column(Numeric)
    account_deletion_status = Column(String)

    account_transaction_snap = relationship('TransactionSnap', backref='account_snap')

    def __repr__(self):
        return "<(account_name='%s')" % (self.account_name)


class CategorySnap(Base):
    __tablename__ = 'dim_category_snap'

    snapshot_date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    category_snap_key = Column(Integer, primary_key=True)
    category_id = Column(String)
    category_name = Column(String)
    category_visibility_status = Column(String)
    category_note = Column(String)
    category_deletion_status = Column(String)
    category_group_id = Column(String)
    category_group_name = Column(String)
    category_group_visibility_status = Column(String)
    category_group_deletion_status = Column(String)

    monthly_budget_category_snap = relationship('MonthlyBudgetSnap', backref='category_snap')
    category_transaction_snap = relationship('TransactionSnap', backref = 'category_snap')
    category_goal_snap = relationship('CategoryGoalSnap', backref = 'category_snap')

    def __repr__(self):
        return "<(category_name='%s')" % (self.category_name)


class PayeeSnap(Base):
    __tablename__ = 'dim_payee_snap'
    
    snapshot_date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    payee_snap_key = Column(Integer, primary_key=True)
    payee_id = Column(String)
    payee_name = Column(String)
    payee_deletion_status = Column(String)
    payee_transaction = relationship('TransactionSnap', backref='payee_snap')
    
    def __repr__(self):
        return "<(payee_name='%s')" % (self.payee_name)


class GoalTypeSnap(Base):
    __tablename__ = 'dim_goal_type_snap'

    snapshot_date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    goal_type_snap_key = Column(Integer, primary_key=True)
    goal_type_code = Column(String)
    goal_type_name = Column(String)

    goaltype_snap_goal = relationship('CategoryGoalSnap', backref = 'goaltypesnap')

    def __repr__(self):
        return "<(goal_type_name='%s')" % (self.goal_type_snap_name)


class MonthlyBudgetSnap(Base):
    __tablename__ = 'fact_monthly_budget_snap'

    snapshot_date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    monthly_budget_snap_key = Column(Integer, primary_key=True)
    category_snap_key = Column(Integer, ForeignKey('dim_category_snap.category_snap_key'))
    month_key = Column(Integer, ForeignKey('dim_month.month_key'))
    budgeted_amount = Column(Numeric)
    activity_amount = Column(Numeric)
    balance_amount = Column(Numeric)

    def __repr__(self):
        return "<(monthly_budget='%s')" % (self.monthly_budget_snap_key)


class TransactionSnap(Base):
    __tablename__ = 'fact_transaction_snap'

    snapshot_date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    transaction_snap_key = Column(Integer, primary_key=True)
    transaction_id = Column(String)
    account_snap_key = Column(Integer, ForeignKey('dim_account_snap.account_snap_key'))
    payee_snap_key = Column(Integer, ForeignKey('dim_payee_snap.payee_snap_key'))
    category_snap_key = Column(Integer, ForeignKey('dim_category_snap.category_snap_key'))
    date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    transaction_amount = Column(Numeric)

    def __repr__(self):
        return "<(transaction='%s')" % (self.transaction_id)


class CategoryGoalSnap(Base):
    __tablename__ = 'fact_category_goal_snap'

    snapshot_date_key = Column(Integer, ForeignKey('dim_date.date_key'))
    category_goal_snap_key = Column(Integer, primary_key=True)
    category_snap_key = Column(Integer, ForeignKey('dim_category_snap.category_snap_key'))
    goal_creation_month_key = Column(Integer, ForeignKey('dim_month.month_key'))
    goal_target_month_key = Column(Integer, ForeignKey('dim_month.month_key'))
    goal_type_snap_key = Column(Integer, ForeignKey('dim_goal_type_snap.goal_type_snap_key'))
    goal_target_amount = Column(Numeric)
    goal_percentage_complete = Column(Numeric)

    goal_creation_month = relationship("Month", foreign_keys=[goal_creation_month_key])
    goal_target_month = relationship("Month", foreign_keys=[goal_target_month_key])

    def __repr__(self):
        return "<(category_goal='%s')" % (self.category_goal_snap_key)