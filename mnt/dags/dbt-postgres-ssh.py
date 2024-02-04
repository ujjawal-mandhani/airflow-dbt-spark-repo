from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id = 'dbt-postgres-commands-using-ssh',
    default_args=default_args,
    description='dbt commands using ssh',
    catchup=False,
    schedule_interval='@daily',
    tags=["dbt", "postgres", "ssh"]
)

dbt_seed = SSHOperator(
    task_id='dbt-seed-using-ssh',
    ssh_conn_id='ssh_dbt_services', 
    command='cd /home/dbt_postgres/; source bin/activate; cd dbt_project; dbt seed',
    cmd_timeout=None,
    dag=dag,
)

dbt_run = SSHOperator(
    task_id='dbt-run-using-ssh',
    ssh_conn_id='ssh_dbt_services', 
    command='cd /home/dbt_postgres/; source bin/activate; cd dbt_project; dbt run',
    cmd_timeout=None,
    dag=dag,
)

dbt_seed >> dbt_run