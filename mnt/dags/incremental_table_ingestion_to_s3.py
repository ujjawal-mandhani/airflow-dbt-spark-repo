from datetime import datetime, timedelta
import psycopg2
from datetime import date
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
from airflow.hooks.S3_hook import S3Hook
import pandas as pd
import json

def write_to_s3(content, **kwargs):
    aws_conn_id = 'aws_default'
    s3_hook = S3Hook(aws_conn_id)
    bucket_name = 'test-uat'
    key = f"test_folder_for_partition_data/{str(date.today())}/{str(datetime.now()).replace(':', '').replace('-', '').replace('.', '').replace(' ', '')}.json"
    s3_hook.load_string(json.dumps(content[0]), key, bucket_name)
    print("File written to S3 successfully.")

def fetch_credentials(**context):
    connection_id = "postgres_default"
    conn = BaseHook.get_connection(connection_id)
    host = str(conn.host)
    port = str(conn.port)
    schema = str(conn.schema)
    login = str(conn.login)
    password = str(conn.password)
    return host, port, schema, login, password
    
def connect_to_postgres_and_query(query, return_df = 'N'):
    host, port, schema, login, password = fetch_credentials()
    try:
        conn = psycopg2.connect(
            dbname= schema,
            user= login,
            password= password,
            host= host,
            port= port
        )
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=colnames)
        df.fillna('', inplace=True)
        cur.close()
        conn.close()
        if return_df == 'Y':
            return rows, list(df.T.to_dict().values())
        return rows

    except Exception as e:
        print("Error:", e)
        
def get_all_from_tables():
    all_required = []
    all_required_tables_data = connect_to_postgres_and_query("""
                                    SELECT table_name
                                    FROM information_schema.tables
                                    WHERE table_schema = 'incremental_data_test';
                                  """)
    for table_row in all_required_tables_data:
        table = table_row[0]
        all_required.append(table)
    print("::::::::::::::Tables are", all_required)
    return all_required
    
def ingest_table(table):
    print("::::::::::::::::Starting for table", table)
    state_value = ''
    try:
        state_value = Variable.get(f"incremental_data_test.{table}")
    except:
        print(":::::::State value not exist")
    
    print(":::::::::::State Value", state_value)
    if state_value != '':
        data, json_value = connect_to_postgres_and_query(f"""select * from incremental_data_test.{table} where edl_created_at > '{state_value}'""", return_df = 'Y')
    else:
        data, json_value = connect_to_postgres_and_query(f"""select * from incremental_data_test.{table}""", return_df = 'Y')
    print(data)
    print("::::::::::::::::Completed for table", table)
    state_value = connect_to_postgres_and_query(f"""select max(edl_created_at) from incremental_data_test.{table}""")
    Variable.set(f"incremental_data_test.{table}", state_value[0][0])
    if json_value != []:
        write_to_s3(json_value)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id = 'postgres_operator_dag',
    default_args=default_args,
    description='postgres incremental data pull to s3',
    catchup=False,
    schedule_interval='@daily',
    tags=["postgres", "incremental"]
) as dag:

    all_required_tables  = get_all_from_tables()
    with TaskGroup('ingest_in_parallel') as ingest_in_parallel:
        for table in all_required_tables:
            task_id = f'process_table_{table}'
            table_ingestion_task = PythonOperator(
                task_id=task_id,
                python_callable=ingest_table,
                op_kwargs={'table': table},
                dag=dag
            )
    
    ingest_in_parallel

