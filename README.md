# itmo_devops_part2
Репозиторий для загрузки домашних заданий по курсу "Контейнеризация и оркестрация приложений". 

Состав команды: Воляница Елизавета, Фёдорова Инесса

12.05.2023 - ЛР 1. Airflow + Dockerfile


## Запуск проекта

- [ ] Собрать и запустить проект можно с помощью команды: docker compose up --build -d
- [ ] Данные пользователя - username: airflow_user, password: airflow_password


## Описание DAG

Данный DAG предназначен для обучения модели линейной регрессии (файл для обучения - /data/train.csv). Результат выполнения - модель, сохраненная в /data/linear_regression_model.pkl.

Этапы выполнения:
- read_csv - чтение файла для обучения
- preprocess_data - подготовка данных, разделение на тренировочную и тестовую выборки
- train_linear_regression - обучение и сохранение модели
- test_model - подсчет ошибки (MSE) на тестовой выборке 


