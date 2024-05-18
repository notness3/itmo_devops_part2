# itmo_devops_part2
Репозиторий для загрузки домашних заданий по курсу "Контейнеризация и оркестрация приложений". 

Состав команды: Воляница Елизавета, Фёдорова Инесса

12.05.2023 - ЛР 1. Airflow + Dockerfile

18.05.2023 - ЛР 2. Docker-compose


## Запуск проекта

- [ ] Собрать и запустить проект можно с помощью команды: `docker compose up --build -d`
- [ ] Данные пользователя - username: `airflow_user`, password: `airflow_password`


## Задача
На основе `Dockerfile` из ЛР 1 создать композ проект. Обязательные требования:

- [x] минимум 1 init + 2 app сервиса (одноразовый init + приложение + бд или что-то другое, главное чтоб работало в связке)
- [x] автоматическая сборка образа из лежащего рядом `Dockerfile` и присваивание ему (образу) имени
- [x] жесткое именование получившихся контейнеров
- [x] минимум один из сервисов обязательно с `depends_on`
- [x] минимум один из сервисов обязательно с `volume`
- [x] минимум один из сервисов обязательно с прокидыванием порта наружу
- [x] минимум один из сервисов обязательно с ключом `command` и/или `entrypoint` (можно переиспользовать тот же, что в `Dockerfile`)
- [x] добавить `healthcheck`
- [x] все env-ы прописать не в сам docker-compose.yml, а в лежащий рядом файл `.env`
- [x] должна быть явно указана `network` (одна для всех)

### Вопросы

1. **Можно ли ограничивать ресурсы (например, память или CPU) для сервисов в docker-compose.yml? Если нет, то почему, если да, то как?**
- Можно, необходимо в каждом из сервисов прописать следующие настройки, согласно https://docs.docker.com/compose/compose-file/deploy/#resources:

```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 50M
    reservations:
      cpus: '0.5'
      memory: 20M
 ```
2. **Как можно запустить только определенный сервис из docker-compose.yml, не запуская остальные?**
- `docker compose start [service_name_from_compose]`
- `docker compose up [service_name_from_compose]`


## Описание DAG

Данный DAG предназначен для обучения модели градиентного бустинга на задачу бинарной классификации (файл для обучения - /data/train.csv, файл для тестирования - /data/test.csv). Результат выполнения - модель, сохраненная в /data/model.pkl.

Этапы выполнения:
- read_csv - чтение файла для обучения
- preprocess_data - подготовка данных, разделение на тренировочную и тестовую выборки
- train_model - обучение и сохранение модели
- test_model - подсчет качества на тестовой выборке 


