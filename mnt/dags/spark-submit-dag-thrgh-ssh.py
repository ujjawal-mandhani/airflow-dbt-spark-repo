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
    dag_id = 'spark-submit-operator-using-ssh',
    default_args=default_args,
    description='Spark submit through ssh connection',
    catchup=False,
    schedule_interval='@daily',
    tags=["spark-submit", "ssh"]
)

ssh_task = SSHOperator(
    task_id='spark-submit-operator-using-ssh',
    ssh_conn_id='ssh_default', 
    command='export PATH=/usr/local/openjdk-8/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/share/spark/bin; spark-submit --master spark://spark-master:7077 --conf spark.master=spark://spark-master:7077 --name MySparkJob --queue root.default --deploy-mode client /home/spark_job.py',
    dag=dag,
)
