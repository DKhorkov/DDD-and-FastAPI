all: app

app:
	@make -s help

help:
	@echo "make help                         - show this help."
	@echo "make build                        - build docker and it's environment."
	@echo "make run							 - run docker."
	@echo "make clean                        - cleanup docker kitchen."
	@echo "make network                      - create docker network for project."
	@echo "make prod                         - run docker for production purposes."
	@echo "make local                        - run docker for local purposes."
	@echo "make makemigrations               - create alembic migration."
	@echo "make migrate                      - upgrade database according to alembic migration."
	@echo "make downgrade                    - downgrade database according to alembic migration."

network:
	sudo docker network create benefit_bistro_network

build:
	sudo docker compose build

run:
	sudo docker compose up

clean:
	sudo docker system prune -a --volumes

prod: build run

local:
	sudo docker compose -f docker-compose-local.yml up --build

makemigrations:
	sudo docker compose exec benefit_bistro scripts/makemigrations ${name}

migrate:
	 sudo docker compose exec benefit_bistro scripts/migrate

downgrade:
	sudo docker compose exec benefit_bistro scripts/downgrade ${to}
