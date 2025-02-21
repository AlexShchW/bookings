# Bookings  
# Бронирование отелей  

Репозиторий учебного пет-проекта для изучения/практики FastAPI, Pydantic, PostgreSQL, SQLAlchemy, Alembic, Redis, Celery, SQLAdmin, pytest, Docker, стилизации кода, логирования и т.д. 

~~Задеплоен тут: https://bookings-app-26zk.onrender.com/docs~~ (На данный момент раздеплоен, доступен локальный запуск, нужные .env файлы уже в наличии).
#
### Запуск
docker compose build  
docker compose up  
#
После запуска доступен на http://localhost:7777/docs

Можно регистрироваться, аутентифицироваться, получать отели, создавать/получать/удалять бронирования и т.д.

Одна ручка с базовым фронтом, имеет вид http://localhost:7777/pages/hotels?location=Алтай&date_from=2020-02-02&date_to=2030-03-03
