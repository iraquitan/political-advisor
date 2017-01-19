DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_PROD = docker-compose -f docker-compose-prod.yml
DOCKER_COMPOSE_TEST = docker-compose -f docker-compose-test.yml
DOCKER_ARGS ?=
DOCKER_VOLUMES ?= ci_redisdata ci_pgdata dev_redisdata dev_pgdata redisdata pgdata politicaladvisor_pgdata politicaladvisor_redisdata
CMD ?=
APP_LIST ?= political_advisor.test
RUN_TIME = $(shell date +%Y-%m-%dT%H:%M:%S)

.PHONY: docker-stop-all collectstatics makemigrations runserver test

collectstatics:
	$(DOCKER_COMPOSE) -p dev up -d $(DOCKER_ARGS)
	$(DOCKER_COMPOSE) -p dev run web python manage.py collectstatic --noinput
	$(DOCKER_COMPOSE) -p dev stop

makemigrations:
	$(DOCKER_COMPOSE) -p dev up -d $(DOCKER_ARGS)
	$(DOCKER_COMPOSE) -p dev run web python manage.py makemigrations
	$(DOCKER_COMPOSE) -p dev stop

migrate: makemigrations
	$(DOCKER_COMPOSE) -p dev up -d $(DOCKER_ARGS)
	$(DOCKER_COMPOSE) -p dev run web python manage.py migrate
	$(DOCKER_COMPOSE) -p dev stop

cmd:
	$(DOCKER_COMPOSE) -p dev up -d $(DOCKER_ARGS)
	$(DOCKER_COMPOSE) -p dev run web $(CMD)
	$(DOCKER_COMPOSE) -p dev stop

migrations-check:
	$(DOCKER_COMPOSE) -p dev up -d $(DOCKER_ARGS)
	$(DOCKER_COMPOSE) -p dev run web python manage.py makemigrations --check --dry-run
	$(DOCKER_COMPOSE) -p dev stop

runserver: collectstatics
	$(DOCKER_COMPOSE) -p dev up $(DOCKER_ARGS)
	$(DOCKER_COMPOSE) -p dev stop

test:
	@echo running tests
	@echo
	$(DOCKER_COMPOSE_TEST) -p ci up -d $(DOCKER_ARGS) &> /dev/null;
	$(DOCKER_COMPOSE_TEST) -p ci run sut python manage.py makemigrations --check --dry-run
	@docker wait ci_sut_1 &> /dev/null;
	@docker logs --since $(RUN_TIME) ci_sut_1
	$(DOCKER_COMPOSE_TEST) -p ci stop &> /dev/null;
	@echo
	@echo done.

flake8:
	$(DOCKER_COMPOSE_TEST) -p ci run sut flake8
	$(DOCKER_COMPOSE_TEST) -p ci stop

ci: test
	$(DOCKER_COMPOSE_TEST) -p ci run sut coverage report
	$(DOCKER_COMPOSE_TEST) -p ci stop &> /dev/null;

docker-compose-up:
	$(DOCKER_COMPOSE) -p dev up $(DOCKER_ARGS)

docker-stop-all:
	$(DOCKER_COMPOSE) -p dev stop
	$(DOCKER_COMPOSE_TEST) -p ci stop

docker-down-all:
	$(DOCKER_COMPOSE) -p dev down
	$(DOCKER_COMPOSE_TEST) -p ci down

docker-volume-rm-all:
	docker volume rm $(DOCKER_VOLUMES)

start-docker-test:
	@echo Starting docker test containers
	@if [ $(shell docker ps -a | grep -ci ci) -eq 0 ]; then \
		echo starting test containers; \
		$(DOCKER_COMPOSE_TEST) -p ci up -d; \
	elif [ $(shell docker ps | grep -ci ci) -eq 0 ]; then \
		echo restarting test containers; \
		$(DOCKER_COMPOSE_TEST) -p ci restart; \
	fi

start-docker-dev:
	@echo Starting docker dev containers
	@if [ $(shell docker ps -a | grep -ci dev) -eq 0 ]; then \
		echo starting dev containers; \
		$(DOCKER_COMPOSE) -p dev up -d; \
	elif [ $(shell docker ps | grep -ci dev) -eq 0 ]; then \
		echo restarting dev containers; \
		$(DOCKER_COMPOSE) -p dev restart; \
	fi

stop-docker:
	@echo Stopping docker containers
	@if [ $(shell docker ps -a | grep -ci ci) -gt 0 ]; then \
		echo stopping test containers; \
		$(DOCKER_COMPOSE_TEST) -p ci stop; \
	fi

	@if [ $(shell docker ps -a | grep -ci dev) -gt 0 ]; then \
		echo stopping dev containers; \
		$(DOCKER_COMPOSE) -p dev stop; \
	fi

	@if [ $(shell docker ps -a | grep -ci prod) -gt 0 ]; then \
		echo stopping prod containers; \
		$(DOCKER_COMPOSE_PROD) -p prod stop; \
	fi

clean-docker:
	@echo Removing docker containers
	@if [ $(shell docker ps -a | grep -ci ci) -gt 0 ]; then \
		echo removing test containers; \
		$(DOCKER_COMPOSE_TEST) -p ci down; \
	fi

	@if [ $(shell docker ps -a | grep -ci dev) -gt 0 ]; then \
		echo removing dev containers; \
		$(DOCKER_COMPOSE) -p ci down; \
	fi

	@if [ $(shell docker ps -a | grep -ci prod) -gt 0 ]; then \
		echo removing prod containers; \
		$(DOCKER_COMPOSE_PROD) -p prod down; \
	fi
