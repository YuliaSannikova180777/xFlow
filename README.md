# xFlow
# Создаем новую ВМ называем xflow
# устанавливаем все необходимое (команда выполняется долго)
sudo apt-get update -y && sudo apt-get install software-properties-common -y && sudo apt-get install python-setuptools -y && sudo apt install python3-pip -y && sudo apt install libpq-dev -y && sudo apt install postgresql -y && sudo pip install psycopg2

# (Разбивка команд:
   sudo apt-get update -y: Обновляет список доступных пакетов из репозиториев.
   sudo apt-get install software-properties-common -y: Устанавливает инструмент для управления репозиториями.
   sudo apt-get install python-setuptools -y: Устанавливает setuptools, необходимые для установки некоторых Python-пакетов.
   sudo apt install python3-pip -y: Устанавливает пакетный менеджер pip для Python 3.
   sudo apt install libpq-dev -y: Устанавливает библиотеки разработки для PostgreSQL, которые необходимы для компиляции некоторых Python-пакетов, взаимодействующих с PostgreSQL.
   sudo apt install postgresql -y: Устанавливает систему управления базами данных PostgreSQL.
   sudo pip install psycopg2: Устанавливает Python-пакет psycopg2, который обеспечивает доступ к базам данных PostgreSQL из Python.)

# Установим git
sudo apt install git

# На гит создаем репозиторий xflow

# Генерируем SSH
ssh-keygen

# Копируем ssh-rsa для этого можно вывести его на экран для удобства 
cd .ssh
cat id_rsa.pub
# Вставляем в github для этого заходим в репозиторий Settings => Deploy keys => Add deploy key

cd 

# Клонируем репозиторий 
git clone git@github.com:YuliaSannikova180777/xFlow.git
yes
(клонировать обязательно по SSH)

1. AIRFLOW 
# Уазываем с помощью команды экспорт где будет храниться airflow
export AIRFLOW_HOME=~/airflow
# (Эта команда устанавливает переменную среды AIRFLOW_HOME в значение ~/airflow. Это значение указывает на каталог, в котором хранятся файлы Airflow, такие как DAG-файлы, плагины и конфигурационные файлы)

# Устанавливаем airflow
sudo pip3 install apache-airflow 

sudo -u postgres psql
# (появится следующее 
   could not change directory to "/home/angry": Permission denied
   psql (14.10 (Ubuntu 14.10-0ubuntu0.22.04.1))
   Type "help" for help.

postgres=#)

# Создаем пользователя
CREATE user airflow PASSWORD 'password';
# (пример CREATE USER angry WITH PASSWORD '1234';)

# Создаем базуданных
CREATE DATABASE airflow;

# Наделяем пользователя правами
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO angry;

# Для выхода нажимаем Ctrl + D (далее ^D)

# Инициализируем базу данных
airflow db init

cd airflow
mkdir dags
chmod 777 dags && chmod 777 logs

# Связываем airflow c базой данных postgsql (airflow.cfg лежит в корне в папке airflow)
nano airflow.cfg 
^W (поиск по файлу) пишем sql
# находим строку sql_alchemy_conn = sqlite:////home/angry/airflow/airflow.db
# Заменяем на строку
sql_alchemy_conn = postgresql+psycopg2://angry:1234@localhost/airflow 
# (postgresql+psycopg2: Директива драйвера. В данном случае используется драйвер psycopg2 для подключения к базе данных PostgreSQL.
   angry: Имя пользователя базы данных.
   1234: Пароль базы данных.
   localhost: Имя хоста базы данных.
   airflow: Имя базы данных.)

# Снова инициализируем пользователя
airflow db init

# Создаем пользователя на airflow
airflow users create --username Angry --firstname Yulia --lastname Sannikova --role Admin --email sannikovayi@gmail.com
# при установке попросит ввести пароль и повторить его

# запускаем сервер 
airflow webserver -p 8080
# выйти ^C

# Запускаем планировщик airflow (scheduler), который будет отслеживать все задачи и группы 
airflow scheduler
# выйти ^C

# Запустим airflow
airflow webserver

# переходим в браузер и вставляем там ссылку 
http://localhost:8080
# Авторизуемся

# возвращаемся в терминал 
# останавливаем airflow webserver
^C


# открываем второй терминал и вводим, потом переходим в 1 терминал и работаем там дальше
airflow webserver

# Переходим в dags здесь буду храниться скрипты
cd dags
nano app.py

from airflow import DAG
import airflow
from datetime import datetime
from airflow.operators.python import PythonOperator

def test123():
    print("Hello world!")

args = {
    'owner': 'dimon',
    'start_date':datetime(2018, 11, 1),
    'provide_context':True
}

with DAG('Hello-world_example', description='Hello-world example', schedule='*/1 * * * *',  catchup=False, default_args=args) as dag: 
    task_1 = PythonOperator(task_id="task_1", python_callable=test123)

^ 0 enter ^X

# Выполняем скрипт 
python3 app.py

# переходим в браузер находим во вкладке DAGs Hello World example я еще слева нажимала кнопочку (у меня без этого не отобразились graph) 

# возвращаемся в терминал

# Создаем новый скрипт
nano bash.py

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

^ 0 enter ^X

# переходим в браузер находим во вкладке DAGs LS_Bash_example здесь якобы должна быть ошибка, но у меня все работало без ошибок 

# Создаем скрипт сложнее
nano model.py

from airflow import task, DAG
from datetime import datetime, timedelta
import airflow
from airflow.operators.python import PythonOperator
import json

def StepOne(ti):
    from random import randint
    import numpy as np
    from sklearn.model_selection import train_test_split

    #ti = kwargs["ti"]
    xs = np.linspace(0, 10, 50)
    ys = xs**2 + np.random.random(50) * 10

    ti.xcom_push("xs", xs.tolist())
    ti.xcom_push("ys", ys.tolist())

def StepTwo(ti):
    from random import randint
    import numpy as np
    from sklearn.model_selection import train_test_split

    xs = np.array(ti.xcom_pull(task_ids="task_1", key="xs"))
    # print(f"xcom pull {xs}")
    # print(f"type is {type(xs)}")
    xs.astype(int)

    t = 1

    if t == 0:
        xs1 = np.c_[xs]
    if t == 1:
        xs1 = np.c_[xs, pow(xs,2)]
    if t == 2:
        xs1 = np.c_[xs, pow(xs,2), pow(xs,3)]
    if t == 3:
        xs1 = np.c_[xs, pow(xs,2), pow(xs,3), pow(xs,4)]
    if t == 4:
        xs1 = np.c_[xs, pow(xs,2), pow(xs,3), pow(xs,4), pow(xs,5)]
    
    print(xs1)

    ti.xcom_push("xs1", xs1.tolist())
  

def StepThree(ti):
    from random import randint
    import numpy as np
    from sklearn.model_selection import train_test_split

    xs1 = np.array(ti.xcom_pull(task_ids="task_2", key="xs1"))
    ys = np.array(ti.xcom_pull(task_ids="task_1", key="ys"))

    X_train, X_test, y_train, y_test = train_test_split(xs1, ys, test_size=0.33, random_state=42)

    ti.xcom_push("X_train", X_train.tolist())
    ti.xcom_push("X_test", X_test.tolist())
    ti.xcom_push("y_train", y_train.tolist())
    ti.xcom_push("y_test", y_test.tolist())
    
def StepFour(ti):
    from random import randint
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import jsonpickle
    import json
    #from keras.models import model_from_json

    X_train = np.array(ti.xcom_pull(task_ids="task_3", key="X_train"))
    y_train = np.array(ti.xcom_pull(task_ids="task_3", key="y_train"))

    model = LinearRegression()
    model.fit(X_train, y_train)
    test = jsonpickle.encode(model)

    ti.xcom_push("model", test)


def StepFive(ti):

    from random import randint
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import jsonpickle

    model = jsonpickle.decode(ti.xcom_pull(task_ids="task_4", key="model"))
    X_test = np.array(ti.xcom_pull(task_ids="task_3", key="X_test"))
    y_test = np.array(ti.xcom_pull(task_ids="task_3", key="y_test"))


    score = model.score(X_test, y_test)

    ti.xcom_push("Score", score)


args = {
    'owner': 'dimon',
    'start_date':datetime(2018, 11, 1),
    'provide_context':True
}

with DAG('Hello-world', description='Hello-world', schedule_interval='*/1 * * * *',  catchup=False, default_args=args) as dag: #0 * * * *   */1 * * * *

    task_1 = PythonOperator(task_id="task_1", python_callable=StepOne)
    task_2 = PythonOperator(task_id="task_2", python_callable=StepTwo)
    task_3 = PythonOperator(task_id="task_3", python_callable=StepThree)
    task_4 = PythonOperator(task_id="task_4", python_callable=StepFour)
    task_5 = PythonOperator(task_id="task_5", python_callable=StepFive)


    task_1 >> task_2 >> task_3 >> task_4 >> task_5

^ 0 enter ^X

python3 model.py

# Остановим airflow
kill `pgrep airflow`

2. MLFOW

# Устанавливаемп все необходимое 
sudo apt-get install sqlite3 libsqlite3-dev -y && sudo apt install python3-pip -y && sudo pip install pysqlite3 && sudo apt install libpq-dev -y && sudo apt install gcc -y && sudo pip install psycopg2

# Устанавливаем mlflow
sudo pip install mlflow

# Устанавливаем набор пакетов postgresql для работы с базами данны
sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-all

# Создаем базу данных и пользователя, выдаем ему привилегированный доступ к базе данных
sudo -u postgres psql

CREATE DATABASE mlflow;
# пример (CREATE DATABASE mlflow;)

CREATE USER mlflow WITH ENCRYPTED PASSWORD 'mlflow';
# пример (CREATE USER yulia WITH ENCRYPTED PASSWORD '1234';)

GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow;
# пример (GRANT ALL PRIVILEGES ON DATABASE mlflow TO yulia;)

# Запускаем MLFlow
mlflow server --backend-store-uri postgresql://yulia:1234@localhost/mlflow --default-artifact-root file:/home/angry/mlruns -h 0.0.0.0 -p 5000

# В браузере запускаем вставляем
http://localhost:5000

# Создаем скрипт 
nano exa*ply.py

import warnings
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn

if __name__ == "__main__": 
    mlflow.set_tracking_uri('http://0.0.0.0:5000') # Указываем местоположение сервера
    experiment = mlflow.set_experiment("Learn MLFlow") # Задаем имя проекта, в котором будет храниться различные эксперименты
    print("mlflow tracking uri:", mlflow.tracking.get_tracking_uri())
    print("experiment:", experiment)
    warnings.filterwarnings("ignore")

    with mlflow.start_run(experiment_id=experiment.experiment_id):
        
        from random import randint
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression

        start = 0
        end = 10
        col = 50

        xs = np.linspace(start, end, col)
        ys = xs**2 + np.random.random(50) * 10

        mlflow.log_param("start", start) # Логирование гиперпараметра start
        mlflow.log_param("end", end) # Логирование гиперпараметра end
        mlflow.log_param("col", col) # Логирование гиперпараметра col

        for t in range(1, 6):

            if t == 1:
                xs1 = np.c_[xs]
            elif t == 2:
                xs1 = np.c_[xs, pow(xs,2)]
            elif t == 3:
                xs1 = np.c_[xs, pow(xs,2), pow(xs,3)]
            elif t == 4:
                xs1 = np.c_[xs, pow(xs,2), pow(xs,3), pow(xs,4)]
            elif t == 5:
                xs1 = np.c_[xs, pow(xs,2), pow(xs,3), pow(xs,4), pow(xs,5)]

            X_train, X_test, y_train, y_test = train_test_split(xs1, ys, test_size=0.33, random_state=42)

            model = LinearRegression()
            model.fit(X_train, y_train)

            score = model.score(X_test, y_test)

            mlflow.log_metric(f"score", score) # Логирование метрики

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        mlflow.sklearn.log_model(model, "model") # Логирование модели

^ 0 enter ^X

python3 exa*ply.py

# Далее заходите на страницу MLFLOW 

3. Проект по YOUTUBE

pip install --upgrade python-youtube

# Создаем дирректори mlops_3
mkdir mlops_3
cd mlops_3

# Создаем там все необходимые дирректории
mkdir datasets && mkdir mlflow && mkdir mlruns && mkdir models && mkdir scripts && mkdir scripts_mlflow 

cd scripts

# Coздаем APIkey
https://console.cloud.google.com
# указываем страну, создаем проект, переходим во вкладку Credentials => + Create Credentials => API key
# Включаем API
https://console.cloud.google.com/apis/dashboard
Enabled Api & services => + Enabled Apis & services => YouTube Data API v3

# Заполняем скриптами дирректорию scripts
nano get_data.py

import requests
import json
from pyyoutube import Api
 
key = "AIzaSyBZyJ3tcWF9xT87mGzAtoXIRucNT381nPI"
api = Api(api_key=key)
 
query = "'Mission Impossible'"
video = api.search_by_keywords(q=query, search_type=["video"], count=10, limit=30)
 
maxResults = 100
nextPageToken = ""
s = 0
 
for id_ in [x.id.videoId for x in video.items]:
    uri = "https://www.googleapis.com/youtube/v3/commentThreads?" + \
            "key={}&textFormat=plainText&" + \
            "part=snippet&" + \
            "videoId={}&" + \
            "maxResults={}&" + \
            "pageToken={}"
    uri = uri.format(key, id_, maxResults, nextPageToken)
    content = requests.get(uri).text
    data = json.loads(content)
    for item in data['items']:
        s += int(item['snippet']['topLevelComment']['snippet']['likeCount'])
 
with open('/home/angry/mlops_3/datasets/data.csv', 'a') as f:
    f.write("{}\n".format(s))

^ 0 enter ^X

nano process_data.py

import pandas as pd
 
df = pd.read_csv('/home/angry/mlops_3/datasets/data.csv', header=None)
 
df[0] = (df[0]-df[0].min())/(df[0].max()-df[0].min())
 
with open('/home/angry/mlops_3/datasets/data_processed.csv', 'w') as f:
    for i, item in enumerate(df[0].values):
        f.write("{},{}\n".format(i, item))

^ 0 enter ^X

nano train_test_split.py

import pandas as pd
import numpy as np
 
df = pd.read_csv('/home/angry/mlops_3/datasets/data_processed.csv', header=None)
 
idxs = np.array(df.index.values)
np.random.shuffle(idxs)
l = int(len(df)*0.7)
train_idxs = idxs[:l]
test_idxs = idxs[l+1:]
 
df.loc[train_idxs, :].to_csv('/home/angry/mlops_3/datasets/data_train.csv',
                        header=None,
                        index=None)
df.loc[test_idxs, :].to_csv('/home/angry/mlops_3/datasets/data_test.csv',
                        header=None,
                        index=None)

^ 0 enter ^X

nano train_model.py

from sklearn.linear_model import LinearRegression
import pickle
import pandas as pd
 
df = pd.read_csv('/home/angry/mlops_3/datasets/data_train.csv', header=None)
df.columns = ['id', 'counts']
 
model = LinearRegression()
model.fit(df['id'].values.reshape(-1,1), df['counts'])
 
with open('/home/angry/mlops_3/models/data.pickle', 'wb') as f:
    pickle.dump(model, f)

^ 0 enter ^X

nano test_model.py

from sklearn.linear_model import LinearRegression
import pickle
import pandas as pd
 
df = pd.read_csv('/home/angry/mlops_3/datasets/data_test.csv', header=None)
df.columns = ['id', 'counts']
 
model = LinearRegression()
with open('/home/angry/mlops_3/models/data.pickle', 'rb') as f:
    model = pickle.load(f)
 
score = model.score(df['id'].values.reshape(-1,1), df['counts'])
print("score=", score)

^ 0 enter ^X

# Запустим скрипты
python3 get_data.py
python3 process_data.py
python3 train_test_split.py
python3 train_model.py
python3 test_model.py

cd

# Переходим в другую директорию
cd airflow
airflow standalone

cd dags

# Создаем скрипт для airflow
nano youtube_comments_score.py

from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
import datetime as dt
 
args = {
    "owner": "admin",
    "start_date": dt.datetime(2022, 12, 1),
    "retries": 1,
    "retry_delays": dt.timedelta(minutes=1),
    "depends_on_past": False,
    "schedule": '@hourly'
}
 
with DAG(
    dag_id='youtube_comments_score',
    default_args=args,
    #schedule=None,
    tags=['youtube', 'score'],
) as dag:
    get_data = BashOperator(task_id='get_data',
                            bash_command="python3 /home/angry/mlops_3/scripts/get_data.py",
                            dag=dag)
    process_data = BashOperator(task_id='process_data',
                            bash_command="python3 /home/angry/mlops_3/scripts/process_data.py",
                            dag=dag)
    train_test_split = BashOperator(task_id='train_test_split',
                            bash_command="python3 /home/angry/mlops_3/scripts/train_test_split.py",
                            dag=dag)  
    train_model = BashOperator(task_id='train_model',
                            bash_command="python3 /home/angry/mlops_3/scripts/train_model.py",
                            dag=dag)
    test_model = BashOperator(task_id='test_model',
                            bash_command="python3 /home/angry/mlops_3/scripts/test_model.py",
                            dag=dag)
    get_data >> process_data >> train_test_split >> train_model >> test_model

^ 0 enter ^X

python3 youtube_comments_score.py
# переходим в airflow во вкладку DAGs находим youtube_comments_score нажимаем на кнопочку слева (голубая)
# нажимаем на надпись youtube_comments_score заходим в "задачу" справа есть иконка красной корзинки, а рядом стрелочка, надо на нее нажать )) не знала как еще объяснить =D

# Возвращаемся в терминал
cd 

# Запустим MLFLOW
cd airflow
cd scripts_mlflow

nano get_data.py

import requests
import json
from pyyoutube import Api
import os
 
import mlflow
from mlflow.tracking import MlflowClient
 
os.environ["MLFLOW_REGISTRY_URI"] = "/home/angry/mlops_3/"
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("get_data")
 
key = "AIzaSyBZyJ3tcWF9xT87mGzAtoXIRucNT381nPI"
api = Api(api_key=key)
query = "'Mission Impossible'"
video = api.search_by_keywords(q=query, search_type=["video"], count=10, limit=30)
maxResults = 100
nextPageToken = ""
s = 0
 
with mlflow.start_run():
    for i, id_ in enumerate([x.id.videoId for x in video.items]):
        uri = "https://www.googleapis.com/youtube/v3/commentThreads?" + \
              "key={}&textFormat=plainText&" + \
              "part=snippet&" + \
              "videoId={}&" + \
              "maxResults={}&" + \
              "pageToken={}"
        uri = uri.format(key, id_, maxResults, nextPageToken)
        content = requests.get(uri).text
        data = json.loads(content)
        for item in data['items']:
            s += int(item['snippet']['topLevelComment']['snippet']['likeCount'])
    mlflow.log_artifact(local_path="/home/angry/mlops_3/scripts/get_data.py",
                        artifact_path="get_data code")
    mlflow.end_run()
 
with open('/home/angry/mlops_3/datasets/data.csv', 'a') as f:
    f.write("{}\n".format(s))

^ 0 enter ^X

nano train_model.py

from sklearn.linear_model import LinearRegression
import pickle
import pandas as pd
import os
 
import mlflow
from mlflow.tracking import MlflowClient
 
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("train_model")
 
df = pd.read_csv('/home/angry/mlops_3/datasets/data_train.csv', header=None)
df.columns = ['id', 'counts']
model = LinearRegression()
 
with mlflow.start_run():
    mlflow.sklearn.log_model(model,
                             artifact_path="lr",
                             registered_model_name="lr")
    mlflow.log_artifact(local_path="/home/angry/mlops_3/scripts/train_model.py",
                        artifact_path="train_model code")
    mlflow.end_run()
 
model.fit(df['id'].values.reshape(-1,1), df['counts'])
 
with open('/home/angry/mlops_3/models/data.pickle', 'wb') as f:
    pickle.dump(model, f)

^ 0 enter ^X

python3 get_data.py
python3 train_model.py



