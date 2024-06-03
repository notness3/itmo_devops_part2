# itmo_devops_part2
Репозиторий для загрузки домашних заданий по курсу "Контейнеризация и оркестрация приложений". 

Состав команды: Воляница Елизавета, Фёдорова Инесса

12.05.2023 - ЛР 1. Airflow + Dockerfile

18.05.2023 - ЛР 2. Docker-compose

25.05.2023 - ЛР 3. Kubernetes

03.06.2023 - ЛР 4. More Kubernetes

## Ход работы

### Шаг 0 - Запускаем minikube

```
minikube start --force
```

### Шаг 1 - Собираем кастомный докер в minikube

```
eval $(minikube docker-env)
docker build -t my/airflow_custom_build:local .
```

<img src="screenshots/build_custom_image.jpg" height=300 align = "center"/>

### Шаг 2 - Добавляем манифесты

```
kubectl create -f postgres_configmap.yml
kubectl create -f postgres_secret.yml
kubectl create -f airflow_configmap.yml
kubectl create -f airflow_secret.yml
kubectl create -f airflow_postgres.yml
kubectl create -f airflow_init.yml
kubectl create -f airflow_scheduler.yml
kubectl create -f airflow_webserver.yml
```

<img src="screenshots/pods_status.jpg" height=300 align = "center"/>

### Шаг 3 - Запускаем на remote хосте, поэтому прокидываем порты

```
kubectl port-forward --address localhost,147.45.252.106 deployment/airflow-webserver 8080
```

<img src="screenshots/port_forwarding.jpg" height=300 align = "center"/>

### Шаг 4 - Проверяем сервис

<img src="screenshots/service.jpg" height=300 align = "center"/>