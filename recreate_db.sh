#!/bin/bash
source ynab-venv/bin/activate
python3 scripts/create_schema.py 
python3 scripts/dim_month.py 
python3 scripts/dim_date.py
python3 scripts/dim_goal_type.py  
python3 scripts/dim_account.py 
python3 scripts/dim_category.py 
python3 scripts/dim_payee.py 
python3 scripts/fact_category_goal.py 
python3 scripts/fact_monthly_budget.py 
python3 scripts/fact_transaction.py 