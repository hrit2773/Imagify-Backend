.PHONY: build, re-build, up, down, list, logs, test, makemigrations


DOCKER_VERSION := docker --version

docker_config_file := 'docker-compose.local.yaml'

all:
ifndef DOCKER_VERSION
    $(error "command docker is not available, please install Docker")
endif

install:
	pipenv install --categories "packages dev-packeges docs"

re-build:
	docker compose -f docker-compose.yaml -f $(docker_config_file) build --no-cache

build:
	docker compose -f docker-compose.yaml -f $(docker_config_file) build

up:
	docker compose -f docker-compose.yaml -f $(docker_config_file) up -d --wait

down:
	docker compose -f docker-compose.yaml -f $(docker_config_file) down -v

load-dummy-data:
	docker compose exec backend bash -c "python manage.py load_dummy_data"

list:
	docker compose -f docker-compose.yaml -f $(docker_config_file) ps

logs:
	docker compose -f docker-compose.yaml -f $(docker_config_file) logs

checkmigration:
	docker compose exec backend bash -c "python manage.py makemigrations --check --dry-run"

makemigrations:
	docker compose exec backend bash -c "python manage.py makemigrations"

test:
	docker compose exec backend bash -c "python manage.py test --keepdb --parallel --shuffle"