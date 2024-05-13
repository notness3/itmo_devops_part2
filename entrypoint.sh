#!/bin/bash
airflow db upgrade

airflow webserver -p 8080 &

airflow scheduler &

wait
