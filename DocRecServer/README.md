# DocRec

**DocRec** - Веб-сервер для сервиса 

### Требования

- python (3.10)
- PostgreSQL (12)

### Установка

1. Загрузим актуальную версию, перейдем в папку проекта:

    ``git clone <ссылка на этот репозиторий>``
  

2. Создадим виртуальное пространство:

    ``python3 -m venv venv``
   
    ``source venv/bin/activate``

3. Установим зависимости.

    ``pip install -r requirements.txt``

### Конфигурация сервера

Создаем файл **.env** в корне проекта

_Пример можно увидеть в .env.example_


### Запуск

1. **Терминал**:
    
   ``uvicorn app.main:app --host YOUR_HOST --port YOUR_PORT``

2. **Docker**:

   ``docker build --tag docreg-server .``
   
   ``docker run --env-file .env --network=host --name docreg-server``


###  Документация

После запуска сервера доступна две автособираемые документации.
* Swagger UI - _<SERVER_HOST:SERVER_PORT>_**/docs**
