**Sadilar Terminology**

About the project:

---

## Requirements

- Docker
- Docker-compose
- Makefile reader installed on device

## Installations guide

### Using Docker-compose

1. docker-compose up --build
2. docker-compose down

### Using Makefile

1. Clone the repository
2. Run `make build` to build the docker image
3. Run `make run` to run the docker container
4. Run `make stop` to stop the docker container

## Production

### Plugins installed

#### Django Simple History

https://django-simple-history.readthedocs.io/en/latest/

#### Basic setup for production

### environment variables

please use .env.example as example


## Production Information

Docker Volumes for production:

/media
/logging
