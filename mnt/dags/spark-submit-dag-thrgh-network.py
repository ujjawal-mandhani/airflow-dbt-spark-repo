from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id = 'spark-submit-dag-thrgh-network',
    default_args=default_args,
    description='An example DAG to submit a Spark job',
    catchup=False,
    schedule_interval='@daily',
    tags=["spark-submit", "spark-connection"]
)

# Specify the Spark job parameters
spark_task = SparkSubmitOperator(
    task_id='spark-submit-dag-thrgh-network',
    conn_id='spark_default',  # Airflow connection ID for Spark
    application='/opt/airflow/spark_scripts/spark_job.py',  # Path to your Spark application script
    name='MySparkJob',  # Spark application name
    verbose=False,
    conf={'spark.master': 'spark://spark-master:7077'},  # Spark master URL
    dag=dag,
)

# Set task dependencies if needed
# task2.set_upstream(task1)

# Define other tasks as needed

# The tasks are linked sequentially, but you can modify the dependencies based on your DAG structure.
