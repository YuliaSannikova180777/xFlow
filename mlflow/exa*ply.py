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

        mlflow.sklearn.log_model(model, "model") # Логирование модел
