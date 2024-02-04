from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.oracle_operator import OracleOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from utils.utils import sender_email_function

oracle_password = Variable.get("oracle_password")
receiver_email = ["ujjawal.mandhani@lumiq.ai", "ujjawalmandhani97858@gmail.com"]
dagid = 'dbt-oracle-commands-using-ssh'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id = dagid,
    default_args=default_args,
    description='dbt commands using ssh',
    catchup=False,
    schedule_interval='@daily',
    tags=["dbt", "oracle", "ssh"],
    on_failure_callback=lambda context: sender_email_function(
        receiver_email,
        f'Dag {dagid} Failed',
        f'Dag {dagid} Failed Please check Airflow'
    )
)

create_usr_sql = OracleOperator(
    task_id='creating-user-using-oracle-operator',
    oracle_conn_id='oracle_default',
    sql= f'CREATE USER DBT_STAGING IDENTIFIED BY "{oracle_password}"',
    autocommit = True,
    dag=dag
)

allowing_permissions = OracleOperator(
    task_id='providing-permission-using-oracle-operator',
    oracle_conn_id='oracle_default',
    sql= 'ALTER USER DBT_STAGING quota 100M on USERS',
    autocommit = True,
    dag=dag
)

dbt_seed = SSHOperator(
    task_id='dbt-seed-using-ssh',
    ssh_conn_id='ssh_dbt_services', 
    command='cd /home/dbt_oracle/; source bin/activate; cd dbt_oracle_project/; dbt seed',
    cmd_timeout=None,
    dag=dag,
)

dbt_run = SSHOperator(
    task_id='dbt-run-using-ssh',
    ssh_conn_id='ssh_dbt_services', 
    command='cd /home/dbt_oracle/; source bin/activate; cd dbt_oracle_project/; dbt run',
    cmd_timeout=None,
    dag=dag,
)


removing_user = OracleOperator(
    task_id='removing-user-in-oracle-operator',
    oracle_conn_id='oracle_default',
    sql= 'DROP USER DBT_STAGING CASCADE',
    autocommit = True,
    dag=dag
)

send_email_task = PythonOperator(
    task_id='execute_python_function',
    python_callable=sender_email_function,  
    op_args=[receiver_email, f'Dag {dagid} Success', f'Dag {dagid} DBT commands completed'],
    provide_context=True, 
    dag=dag
)

create_usr_sql >> allowing_permissions >> dbt_seed >> dbt_run >> removing_user >> send_email_task