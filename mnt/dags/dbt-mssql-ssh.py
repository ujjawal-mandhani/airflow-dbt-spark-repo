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
    dag_id = 'dbt-mssql-commands-using-ssh',
    default_args=default_args,
    description='dbt commands using ssh',
    catchup=False,
    schedule_interval='@daily',
    tags=["dbt", "mssql", "ssh"]
)

dbt_seed = SSHOperator(
    task_id='dbt-seed-using-ssh',
    ssh_conn_id='ssh_dbt_services', 
    command='cd /home/dbt_mssql/; source bin/activate; cd dbt_microsoft_sql_server; dbt seed',
    cmd_timeout=None,
    dag=dag,
)

dbt_run = SSHOperator(
    task_id='dbt-run-using-ssh',
    ssh_conn_id='ssh_dbt_services', 
    command='cd /home/dbt_mssql/; source bin/activate; cd dbt_microsoft_sql_server; dbt run',
    cmd_timeout=None,
    dag=dag,
)

dbt_seed >> dbt_run