#!/bin/bash
airflow db upgrade

airflow webserver
wait
