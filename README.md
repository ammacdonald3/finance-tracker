# Personal Finance ETL Application

This ETL process is architected to retrieve data from the YNAB (You Need a Budget) API, transform it into a snowflake schema, and load into a data warehouse. Its current imeplementation is used with Google Cloud Platform. Specifically, it's synced to a Google Cloud Function and loads data into a Cloud SQL database (Postgres). Upon initial deployment, environment variables should be set for the values defined in the CONFIG.PY file. If loaded to GCP, the Cloud Scheduler can be used to load data daily.

The repo contains extra code that's useful for local execution and troubleshooting. For example, there are comments in each load script that can write errors to a log file. Additionally, the DELETE_%.py files can be used to clear existing data. Finally, the RECREATE_DB.SH and RUN_DAILY.SH files can be used to run scripts locally.

The preferred solution is to run the MAIN.PY file. If so, the "request" function input should be removed, and the "main()" function call should be uncommented.