from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

PROJECT_PATH = "/opt/airflow/project"
DBT_DIR = f"{PROJECT_PATH}/dbt_transformation"

with DAG(
    'sap_clothing_production_v1',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

 
    task_ingestion = BashOperator(
        task_id='lake_to_bronze',
        bash_command=f'python {PROJECT_PATH}/scripts/03_ingestion.py'
    )


    task_freshness = BashOperator(
        task_id='dbt_source_freshness',
        bash_command=f'cd {DBT_DIR} && dbt source freshness --profiles-dir .'
    )


    task_dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'cd {DBT_DIR} && dbt test --profiles-dir .'
    )


    task_dbt_run = BashOperator(
        task_id='dbt_run_silver',
        bash_command=f'cd {DBT_DIR} && dbt run --profiles-dir .'
    )

    task_ingestion >> task_freshness >> task_dbt_test >> task_dbt_run