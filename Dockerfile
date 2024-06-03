FROM apache/airflow:2.7.0
WORKDIR /opt/airflow

COPY --chown=airflow:root ./src/* ./dags/

USER root
RUN apt update && apt -y install procps default-jre
USER airflow

RUN pip install -r ./dags/requirements.txt
