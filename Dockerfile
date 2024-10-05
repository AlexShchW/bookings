FROM python:3.11

RUN mkdir /bookings

WORKDIR /bookings

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /bookings/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
