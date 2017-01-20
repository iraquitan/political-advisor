# Utils
.INDENT = \\t\-\>
.RUN_TIME = $(shell date +%Y-%m-%dT%H:%M:%S)

# Docker flags
.DOCKER_COMPOSE = docker-compose
.DOCKER_COMPOSE_PROD = docker-compose -f docker-compose-prod.yml
.DOCKER_COMPOSE_TEST = docker-compose -f docker-compose-test.yml
.DOCKER_OUT_TXT = > /dev/null
ifneq ($(DOCKER_OUTPUT),true)
    .DOCKER_OUT_TXT = &> /dev/null
endif
.DOCKER_VOLUMES = politicaladvisor_redisdata politicaladvisor_pgdata
.DOCKER_NETWORKS = politicaladvisor_default

# Docker args
DOCKER_ARGS ?=
DOCKER_OUTPUT ?= true

# Input args
CMD ?=
APP_LIST ?= political_advisor.test

.PHONY: collectstatics makemigrations runserver test flake8 ci

collectstatics: start-docker
	$(.DOCKER_COMPOSE) run --rm web python manage.py collectstatic --noinput

makemigrations: start-docker
	$(.DOCKER_COMPOSE) run --rm web python manage.py makemigrations

makemigrations-check: start-docker
	$(.DOCKER_COMPOSE) run --rm web python manage.py makemigrations --check --dry-run

migrate: makemigrations-check
	$(.DOCKER_COMPOSE) run --rm web python manage.py migrate

web-run: start-docker
	$(.DOCKER_COMPOSE) run --rm web $(CMD)

test-run: test
	$(.DOCKER_COMPOSE_TEST) run --rm sut $(CMD)

runserver: start-docker
	$(.DOCKER_COMPOSE) up $(DOCKER_ARGS) web

test: makemigrations-check
	@echo Running tests
	@$(.DOCKER_COMPOSE_TEST) run --rm sut

flake8: start-docker
	@echo Running python PEP8 lint
	@$(.DOCKER_COMPOSE_TEST) run --rm sut flake8

ci: test
	@echo Generating coverage report
	@$(.DOCKER_COMPOSE_TEST) run --rm sut coverage report

start-docker:
	@echo Starting docker containers
	@if [ $(shell docker ps -a | grep -ci postgres) -eq 0 ]; then \
		echo $(.INDENT) starting postgres; \
		$(.DOCKER_COMPOSE) up -d postgres $(.DOCKER_OUT_TXT); \
	elif [ $(shell docker ps | grep -ci postgres) -eq 0 ]; then \
		echo $(.INDENT) restarting postgres; \
		$(.DOCKER_COMPOSE) restart postgres $(.DOCKER_OUT_TXT); \
	fi

	@if [ $(shell docker ps -a | grep -ci redis) -eq 0 ]; then \
		echo $(.INDENT) starting redis; \
		$(.DOCKER_COMPOSE) up -d redis $(.DOCKER_OUT_TXT); \
	elif [ $(shell docker ps | grep -ci redis) -eq 0 ]; then \
		echo $(.INDENT) restarting redis; \
		$(.DOCKER_COMPOSE) restart redis $(.DOCKER_OUT_TXT); \
	fi

stop-docker:
	@echo Stopping docker containers
	@if [ $(shell docker ps -a | grep -ci postgres) -eq 1 ]; then \
		echo $(.INDENT) stopping postgres; \
		$(.DOCKER_COMPOSE) stop postgres $(.DOCKER_OUT_TXT); \
	fi

	@if [ $(shell docker ps -a | grep -ci redis) -eq 1 ]; then \
		echo $(.INDENT) stopping redis; \
		$(.DOCKER_COMPOSE) stop redis $(.DOCKER_OUT_TXT); \
	fi

docker-ps:
	@echo Showing project docker related containers
	@docker ps -a | grep politicaladvisor

clean-docker:
	@echo Removing docker containers
	@if [ $(shell docker ps -a | grep -ci postgres) -eq 1 ]; then \
		echo $(.INDENT) removing postgres; \
		$(.DOCKER_COMPOSE) stop postgres $(.DOCKER_OUT_TXT); \
		$(.DOCKER_COMPOSE) rm -f -v postgres $(.DOCKER_OUT_TXT); \
	fi

	@if [ $(shell docker ps -a | grep -ci redis) -eq 1 ]; then \
		echo $(.INDENT) removing redis; \
		$(.DOCKER_COMPOSE) stop redis $(.DOCKER_OUT_TXT); \
		$(.DOCKER_COMPOSE) rm -f -v redis $(.DOCKER_OUT_TXT); \
	fi

.clean-docker-volume:
	@echo Removing docker volumes
	@docker volume rm $(.DOCKER_VOLUMES)

.clean-docker-network:
	@echo Removing docker networks
	@docker network rm $(.DOCKER_NETWORKS)

clean: clean-docker .clean-docker-volume .clean-docker-network

help:
	@echo "    help"
	@echo "        Display help for make targets."
	@echo "    collectstatics"
	@echo "        Collect statics for Django app."
	@echo "    makemigrations"
	@echo "        Generate migrations for Django app."
	@echo "    makemigrations-check"
	@echo "        Check migrations for Django app."
	@echo "    migrate"
	@echo "        Migrate the database for Django app."
	@echo "    web-run CMD='command'"
	@echo "        Run command using the web Docker container."
	@echo "    test-run CMD='command'"
	@echo "        Run command using the sut Docker container."
	@echo "    runserver DOCKER_ARGS=-d"
	@echo "        Run Django app server."
	@echo "    test"
	@echo "        Run tests"
	@echo "    flake8"
	@echo "        Run python PEP8 lint."
	@echo "    ci"
	@echo "        Continuous integration that generates coverage report."
	@echo "    docker-ps"
	@echo "        Shows Docker containers related to project."
	@echo "    start-docker"
	@echo "        Start Docker containers."
	@echo "    stop-docker"
	@echo "        Stop Docker containers."
	@echo "    clean-docker"
	@echo "        Stops and remove Docker containers."
	@echo "    clean"
	@echo "        Clean Docker environment by removing containers, volumes and networks."
