from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

def task1(**context):
    result = "Task1 Result"
    context['ti'].xcom_push(key='task1_result', value=result)

def task2(**context):
    task1_result = context['ti'].xcom_pull(task_ids='task1', key='task1_result')
    print("Result from Task1:", task1_result)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 31),
    'retries': 1
}

with DAG('xcom_example', default_args=default_args, schedule_interval=None) as dag:
    start = EmptyOperator(task_id='start')
    task1 = PythonOperator(
        task_id='task1',
        python_callable=task1
    )
    task2 = PythonOperator(
        task_id='task2',
        python_callable=task2
    )

    end = EmptyOperator(task_id='end')

    start >> task1 >> task2 >> end