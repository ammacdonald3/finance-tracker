from scripts.dim_account import dim_account_load
from scripts.dim_category import dim_category_load
from scripts.dim_date import dim_date_load
from scripts.dim_goal_type import dim_goal_type_load
from scripts.dim_month import dim_month_load
from scripts.dim_payee import dim_payee_load
from scripts.fact_category_goal import fact_category_goal_load
from scripts.fact_monthly_budget import fact_monthly_budget_load
from scripts.fact_transaction import fact_transaction_load


def main():

    dim_account_load()
    dim_category_load()
    dim_goal_type_load()
    dim_payee_load()
    fact_category_goal_load()
    fact_monthly_budget_load()
    fact_transaction_load()

    return "All load scripts run successfully"

