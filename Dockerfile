FROM python:3.12.0-slim

WORKDIR /app

RUN ls

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV NAME TMS

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]