from airflow import DAG
import airflow
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import json

args = {
    'owner': 'dimon',
    'start_date':datetime(2018, 11, 1),
    'provide_context':True
}

with airflow.DAG('LS_Bash_example', description='Hello-world example', schedule='*/1 * * * *',  catchup=False, default_args=args) as dag: #0 * * * *   */1 * * * *

    task_1 = BashOperator(task_id="task_1", bash_command="ls -la ~/airflow/dags")
