.PHONY: list up upd build stop down restart make-migrations migrate collectstatic shell logs create-super-user \
        docker-stop-all create-schema test ruff-check ruff-fix ruff-format load-fixtures pre-commit-install \
        dev-import-documents dev-quick-install lighthouse dev_update_vector_search docker-shell check make-messages \
        compile-messages fmt lint

list:
	@echo "Available commands:"
	@echo "up - Start the project"
	@echo "upd - Start the project in background"
	@echo "build - Build the project"
	@echo "stop - Stop the project"
	@echo "down - Stop and remove the project"
	@echo "restart - Restart the project"
	@echo "make-migrations - Create new migrations based on the changes you have made to your models"
	@echo "migrate - Apply migrations to your database"
	@echo "shell - Run the Python shell"
	@echo "logs - Show logs"
	@echo "create-super-user - Create a superuser"
	@echo "docker-stop-all - Stop all running containers"
	@echo "load-fixtures - Load fixtures"
	@echo "create-schema - Create a schema"
	@echo "test - Run tests"
	@echo "ruff-check - Run ruff check"
	@echo "ruff-format - Run ruff format"
	@echo "ruff-fix - Run ruff check --fix"
	@echo "pre-commit-install - Install pre-commit"
	@echo "dev-quick-install - Run all the necessary commands to start the project"
	@echo "dev-mass-pdf-upload - Run command to upload all pdf files in the media folder"
	@echo "make-messages - Run command to ensure translation .po files are created"
	@echo "compile-messages - Run command to ensure translation .mo files are created"
	@echo "docker-shell - Access the container shell"
	@echo "check - Run the Django check command"

up:
	@docker compose up

upd:
	@docker compose up -d

build:
	@docker compose build

stop:
	@docker compose stop

down:
	@docker compose down

restart:
	@docker compose restart

make-migrations:
	@docker compose run --rm web python manage.py makemigrations

migrate:
	@docker compose run --rm web python manage.py migrate

collectstatic:
	@docker compose run --rm web python manage.py collectstatic --noinput

shell:
	@docker compose run --rm web python manage.py shell

logs:
	@docker compose logs -tf

create-super-user:
	@docker compose run --rm web python manage.py createsuperuser

docker-stop-all:
	docker stop `docker ps -q`
	docker ps

create-schema:
	@docker compose run --rm web python manage.py graph_models -a -o schema/schema.png

test:
	@docker compose run --rm -e BROWSER -e JS_ENABLED  web python manage.py test $(module)

ruff-check:
	@docker compose run --rm web ruff check .

lint: ruff-check

ruff-format:
	@docker compose run --rm web ruff format .

fmt: ruff-format

ruff-fix:
	@docker compose run --rm web ruff check --fix .

load-fixtures:
	@docker compose run --rm web python manage.py loaddata fixtures/language.json
	@docker compose run --rm web python manage.py loaddata fixtures/institution.json
	@docker compose run --rm web python manage.py loaddata fixtures/projects.json
	@docker compose run --rm web python manage.py loaddata fixtures/subjects.json

pre-commit-install:
	pre-commit install

dev-quick-install:
	@make migrate
	@make load-fixtures
	echo "Creating superuser"
	@make create-super-user

dev-import-documents:
	@docker compose run --rm web python manage.py import_documents general/tests/files/

lighthouse:
	@docker compose run --rm web lhci autorun

dev_update_vector_search:
	@docker compose run --rm web python manage.py dev_update_vector_search

docker-shell:
	docker exec -it sadilar-terminology-web bash

check:
	@docker compose run --rm web python manage.py check

make-messages:
	@docker compose run --rm web python manage.py makemessages --all -e html,txt,py,js

compile-messages:
	@docker compose run --rm web python manage.py compilemessages
