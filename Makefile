.PHONY: build, re-build, up, down, list, logs

DOCKER_VERSION := docker --version

docker_config_file := 'docker-compose.local.yaml'

all:
ifndef DOCKER_VERSION
    $(error "command docker is not available, please install Docker")
endif

re-build:
	docker compose -f docker-compose.yaml -f $(docker_config_file) build --no-cache

build:
	docker compose -f docker-compose.yaml -f $(docker_config_file) build

up:
	docker compose -f docker-compose.yaml -f $(docker_config_file) up -d --wait

down:
	docker compose -f docker-compose.yaml -f $(docker_config_file) down

list:
	docker compose -f docker-compose.yaml -f $(docker_config_file) ps

logs:
	docker compose -f docker-compose.yaml -f $(docker_config_file) logs