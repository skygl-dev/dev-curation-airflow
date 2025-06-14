from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def say_hello():
    print("Hello Airflow!")


with DAG(
    dag_id='example_hello_dag',
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False
) as dag:
    task = PythonOperator(
        task_id='say_hello',
        python_callable=say_hello
    )
