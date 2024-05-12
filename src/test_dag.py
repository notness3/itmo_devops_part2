import joblib
import pandas as pd
import logging
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


def read_csv(train_path, test_path):
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    return train, test


def preprocess_data(target_column, **kwargs):
    task_instance = kwargs['ti']

    data_train, data_test = task_instance.xcom_pull(task_ids="read_csv")
    data_train, data_test = data_train.dropna(), data_test.dropna()

    X_train, X_test = data_train.drop(target_column, axis=1), data_test.drop(target_column, axis=1)
    y_train, y_test = data_train[target_column], data_test[target_column]

    return X_train.to_dict(), y_train.to_dict(), X_test.to_dict(), y_test.to_dict()


def train_model(**kwargs):
    task_instance = kwargs['ti']

    X_train_dict, y_train_dict, _, _ = task_instance.xcom_pull(task_ids="preprocess_data")
    logging.warning(X_train_dict)

    X_train = pd.DataFrame.from_dict(X_train_dict)
    y_train = pd.Series(y_train_dict)

    model = GradientBoostingClassifier(n_estimators=500, learning_rate=0.8, random_state=27, max_depth=6)
    model.fit(X_train, y_train)

    model_filepath = "/opt/airflow/data/model.pkl"
    joblib.dump(model, model_filepath)

    return model_filepath


def test_model(**kwargs):
    task_instance = kwargs['ti']

    model_filepath = task_instance.xcom_pull(task_ids="train_model")

    model = joblib.load(model_filepath)

    _, _, X_test_dict, y_test_dict = task_instance.xcom_pull(task_ids="preprocess_data")

    X_test = pd.DataFrame.from_dict(X_test_dict)
    y_test = pd.Series(y_test_dict)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    return report


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 5, 3),
}

dag = DAG(
    "classification_pipeline",
    default_args=default_args,
    description="A pipeline to read CSV, preprocess data, train and test a gradient boosting classification model",
    schedule_interval=timedelta(days=1),
    catchup=False,
)

train_path, test_path = "/opt/airflow/data/train.csv", "/opt/airflow/data/test.csv"
target_column = "class"

t1 = PythonOperator(
    task_id="read_csv",
    python_callable=read_csv,
    op_args=[train_path, test_path],
    dag=dag,
)

t2 = PythonOperator(
    task_id="preprocess_data",
    python_callable=preprocess_data,
    op_args=[target_column],
    provide_context=True,
    dag=dag,
)

t3 = PythonOperator(
    task_id="train_model",
    python_callable=train_model,
    provide_context=True,
    dag=dag,
)

t4 = PythonOperator(
    task_id="test_model",
    python_callable=test_model,
    provide_context=True,
    dag=dag,
)

t1 >> t2 >> t3 >> t4
