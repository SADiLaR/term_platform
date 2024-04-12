FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

RUN apt-get update && apt-get -y upgrade

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY ./app /app/

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
