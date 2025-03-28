**LwimiLinks**

This project implements a platform for hosting multilingual terminology, and
enriching data with metadata and links between relevant role players.

"Lwimi" refers to language in the Nguni languages, and "Links" emphasises the
goal of linking relevant pieces of information.

The software is implemented in Python on the Django framework.

---

## Requirements

- Docker
- Docker-compose
- Makefile reader installed on device

---

## Installations guide

### Using Docker-compose

1. docker-compose up --build
2. docker-compose down

---

### How to setup SECRET_KEY in Development

.env file

SECRET_KEY=''

To generate a new secret key, you can use the following command:

1. python3 manage.py shell
2. from django.core.management.utils import get_random_secret_key
3. print(get_random_secret_key())

---

### Using Makefile

1. Clone the repository
2. Run `make build` to build the docker image
3. Run `make up` to run the docker container
4. Run `make stop` to stop the docker container

---

### Email Settings in Development

.env file

* EMAIL_HOST='sandbo x.smtp.mailtrap.io'
* EMAIL_HOST_USER='*********'
* EMAIL_HOST_PASSWORD='******'
* EMAIL_PORT='2525'
* EMAIL_BACKEND_CONSOLE=True

By default, the email backend is set to console, so you can see the email in the console.
To send an email, you need to set the EMAIL_BACKEND_CONSOLE to False.

### Plugins installed

#### Django Simple History

* https://django-simple-history.readthedocs.io/en/latest/

#### python-magic

* https://pypi.org/project/python-magic/

---

## Production

#### Basic setup for production

### environment variables

please use .env.example as example

## Production Information

Docker Volumes for production:

* /media
* /logging
* /pdf_uploads
* /pdf_upload_completed

### Email Settings in Production

.env file

* EMAIL_BACKEND_CONSOLE=False

## Notes to Developers

- When setting up the app (from scratch or from a wipe), the following commands should be run:
  - (Optional) `make build`
  - `make up` - wait for the database to start, then hit Control-C
  - `make migrate`
  - `make up` - runs the app
- To wipe the database, use `make down`
- The Django admin interface is at `/admin/`
  - An admin user can be created through `make create-super-user`
- To run a single module of tests, you can pass the Makefile `module` variable on the command line. For instance, to run
  only tests defined in [`test_document_admin.py`](./app/general/tests/test_document_admin.py), run
  `make test module=general.tests.test_document_admin`