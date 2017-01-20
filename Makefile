# Docker flags
.DOCKER_COMPOSE = docker-compose
.DOCKER_COMPOSE_PROD = docker-compose -f docker-compose-prod.yml
.DOCKER_COMPOSE_TEST = docker-compose -f docker-compose-test.yml
DOCKER_ARGS ?=
DOCKER_OUTPUT ?= true
.DOCKER_OUT_TXT = > /dev/null
ifneq ($(DOCKER_OUTPUT),true)
    .DOCKER_OUT_TXT = &> /dev/null
endif
.DOCKER_VOLUMES = ci_redisdata ci_pgdata dev_redisdata dev_pgdata
.DOCKER_NETWORKS = ci_default dev_default

# Utils
.INDENT = \\t\-\>
.RUN_TIME = $(shell date +%Y-%m-%dT%H:%M:%S)

#
CMD ?=
APP_LIST ?= political_advisor.test

.PHONY: docker-stop-all collectstatics makemigrations runserver test

collectstatics: start-docker-dev
	$(.DOCKER_COMPOSE) -p dev run --rm web python manage.py collectstatic --noinput

makemigrations: start-docker-dev
	$(.DOCKER_COMPOSE) -p dev run --rm web python manage.py makemigrations

makemigrations-check: start-docker-dev
	$(.DOCKER_COMPOSE) -p dev run --rm web python manage.py makemigrations --check --dry-run

migrate: makemigrations-check
	$(.DOCKER_COMPOSE) -p dev run --rm web python manage.py migrate

cmd: start-docker-dev
	$(.DOCKER_COMPOSE) -p dev run --rm web $(CMD)

runserver:
	$(.DOCKER_COMPOSE) -p dev up $(DOCKER_ARGS)
	$(.DOCKER_COMPOSE) -p dev stop

test: start-docker-test
	@echo Running tests
	@echo $(.INDENT) checking migrations;
	@$(.DOCKER_COMPOSE_TEST) -p ci run --rm sut python manage.py makemigrations --check --dry-run
	@docker wait ci_sut_1 $(.DOCKER_OUT_TXT);
	@docker logs --since $(.RUN_TIME) ci_sut_1

flake8: start-docker-test
	@echo Running python PEP8 lint
	@$(.DOCKER_COMPOSE_TEST) -p ci run --rm sut flake8

ci: test
	@echo Generating coverage report
	@$(.DOCKER_COMPOSE_TEST) -p ci run --rm sut coverage report

start-docker-test:
	@echo Starting docker test containers
	@if [ $(shell docker ps -a | grep -ci ci_sut) -eq 0 ]; then \
		echo $(.INDENT) starting test containers; \
		$(.DOCKER_COMPOSE_TEST) -p ci up -d $(.DOCKER_OUT_TXT); \
	elif [ $(shell docker ps | grep -ci ci_sut) -eq 0 ]; then \
		echo $(.INDENT) restarting test containers; \
		$(.DOCKER_COMPOSE_TEST) -p ci restart sut $(.DOCKER_OUT_TXT); \
	fi

start-docker-dev:
	@echo Starting docker dev containers
	@if [ $(shell docker ps -a | grep -ci dev) -eq 0 ]; then \
		echo $(.INDENT) starting dev containers; \
		$(.DOCKER_COMPOSE) -p dev up -d $(.DOCKER_OUT_TXT); \
	elif [ $(shell docker ps | grep -ci dev) -eq 0 ]; then \
		echo $(.INDENT) restarting dev containers; \
		$(.DOCKER_COMPOSE) -p dev restart $(.DOCKER_OUT_TXT); \
	fi

stop-docker:
	@echo Stopping docker containers
	@if [ $(shell docker ps -a | grep -ci ci) -gt 0 ]; then \
		echo $(.INDENT) stopping test containers; \
		$(.DOCKER_COMPOSE_TEST) -p ci stop $(.DOCKER_OUT_TXT); \
	fi

	@if [ $(shell docker ps -a | grep -ci dev) -gt 0 ]; then \
		echo $(.INDENT) stopping dev containers; \
		$(.DOCKER_COMPOSE) -p dev stop $(.DOCKER_OUT_TXT); \
	fi

	@if [ $(shell docker ps -a | grep -ci prod) -gt 0 ]; then \
		echo $(.INDENT) stopping prod containers; \
		$(.DOCKER_COMPOSE_PROD) -p prod stop $(.DOCKER_OUT_TXT); \
	fi

clean-docker:
	@echo Removing docker containers
	@if [ $(shell docker ps -a | grep -ci ci) -gt 0 ]; then \
		echo removing test containers; \
		$(.DOCKER_COMPOSE_TEST) -p ci down $(.DOCKER_OUT_TXT); \
	fi

	@if [ $(shell docker ps -a | grep -ci dev) -gt 0 ]; then \
		echo removing dev containers; \
		$(.DOCKER_COMPOSE) -p dev down $(.DOCKER_OUT_TXT); \
	fi

	@if [ $(shell docker ps -a | grep -ci prod) -gt 0 ]; then \
		echo removing prod containers; \
		$(.DOCKER_COMPOSE_PROD) -p prod down $(.DOCKER_OUT_TXT); \
	fi

.clean-docker-volume:
	@echo Removing docker volumes
	@docker volume rm $(.DOCKER_VOLUMES)

.clean-docker-network:
	@echo Removing docker networks
	@docker network rm $(.DOCKER_NETWORKS)

clean: clean-docker .clean-docker-volume .clean-docker-network
