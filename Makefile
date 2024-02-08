list:
	clear
	@echo "Available commands:"
	@echo "up - Start the project"
	@echo "upd - Start the project in background"
	@echo "build - Build the project"
	@echo "stop - Stop the project"
	@echo "down - Stop and remove the project"
	@echo "restart - Restart the project"
	@echo "makemigrations - Create new migrations based on the changes you have made to your models"
	@echo "migrate - Apply migrations to your database"
	@echo "shell - Run the Python shell"
	@echo "logs - Show logs"
	@echo "createsuperuser - Create a superuser"

up:
	clear
	@docker-compose up

upd:
	clear
	@docker-compose up -d

build:
	clear
	@docker-compose build

stop:
	clear
	@docker-compose stop

down:
	clear
	@docker-compose down

restart:
	clear
	@docker-compose restart

makemigrations:
	clear
	@docker-compose run --rm web python manage.py makemigrations

migrate:
	clear
	@docker-compose run --rm web python manage.py migrate

shell:
	clear
	@docker-compose run --rm web python manage.py shell

logs:
	clear
	@docker-compose logs -tf

createsuperuser:
	clear
	@docker-compose run --rm web python manage.py createsuperuser

docker-stop-all:
	clear
	docker stop `docker ps -q`
	docker ps

