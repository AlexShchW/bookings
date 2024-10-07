# Bookings  
# Бронирование отелей  

Репозиторий учебного пет-проекта для изучения/практики FastAPI, Pydantic, PostgreSQL, SQLAlchemy, Alembic, Redis, Celery, SQLAdmin, pytest, Docker, стилизации кода, логирования и т.д. 

Задеплоен тут: https://bookings-app-26zk.onrender.com/docs  
Можно регистрироваться, аутентифицироваться, получать отели, создавать/получать/удалять бронирования и т.д.  
Одна ручка с базовым фронтом, имеет вид https://bookings-app-26zk.onrender.com/pages/hotels?location=Алтай&date_from=2022-05-05&date_to=2022-05-05  

## Если запускать локально:
Во-первых, можно раскомментить работу с celery (в бесплатном деплое не получалось его оставить)  
celery: celery --app=app.tasks.celery:celery worker -l INFO -P solo  
flower: celery --app=app.tasks.celery:celery flower  
Миграции (после создания дб): alembic upgrade head  
Само приложение: uvicorn app.main:app --reload


## Dockerfile
(При уже созданной бд)  
docker build .  
docker run [image_id] 


## Docker compose
Это запустит сразу все, и приложение, и бд, redis, celery, flower  
docker compose build  
docker compose up  
