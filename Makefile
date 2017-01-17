DOCKER_COMPOSE = docker-compose -f docker-compose.yml
DOCKER_COMPOSE_DEV = $(DOCKER_COMPOSE) -f docker-compose.override.yml
DOCKER_COMPOSE_PROD = $(DOCKER_COMPOSE) -f docker-compose.production.yml
DOCKER_COMPOSE_TEST = $(DOCKER_COMPOSE) -f docker-compose.test.yml
DOCKER_ARGS ?=
DOCKER_VOLUMES ?= ci_redisdata ci_pgdata dev_redisdata dev_pgdata redisdata pgdata politicaladvisor_pgdata politicaladvisor_redisdata
APP_LIST ?= django_political_advisor.test
RUN_TIME = $(shell date +%Y-%m-%dT%H:%M:%S)

.PHONY: docker-stop-all collectstatics makemigrations run test

collectstatics:
	$(DOCKER_COMPOSE_DEV) -p dev up -d $(DOCKER_ARGS)
	$(DOCKER_COMPOSE_DEV) -p dev run web python manage.py collectstatic --noinput
	$(DOCKER_COMPOSE_DEV) -p dev stop

makemigrations:
	$(DOCKER_COMPOSE_DEV) -p dev up -d $(DOCKER_ARGS)
	$(DOCKER_COMPOSE_DEV) -p dev run web python manage.py makemigrations
	$(DOCKER_COMPOSE_DEV) -p dev stop

migrate: makemigrations
	$(DOCKER_COMPOSE_DEV) -p dev up -d $(DOCKER_ARGS)
	$(DOCKER_COMPOSE_DEV) -p dev run web python manage.py migrate
	$(DOCKER_COMPOSE_DEV) -p dev stop

migrations-check:
	$(DOCKER_COMPOSE_DEV) -p dev up -d $(DOCKER_ARGS)
	$(DOCKER_COMPOSE_DEV) -p dev run web python manage.py makemigrations --check --dry-run
	$(DOCKER_COMPOSE_DEV) -p dev stop

runserver: collectstatics
	$(DOCKER_COMPOSE_DEV) -p dev up $(DOCKER_ARGS)
	$(DOCKER_COMPOSE_DEV) -p dev stop

test: migrations-check
	$(DOCKER_COMPOSE_TEST) -p ci up -d $(DOCKER_ARGS)
	docker wait ci_sut_1
	docker logs --since $(RUN_TIME) ci_sut_1
	$(DOCKER_COMPOSE_TEST) -p ci stop

flake8:
	$(DOCKER_COMPOSE_TEST) -p ci run sut flake8
	$(DOCKER_COMPOSE_TEST) -p ci stop

ci: test
	$(DOCKER_COMPOSE_TEST) -p ci run sut coverage report
	$(DOCKER_COMPOSE_TEST) -p ci stop

docker-stop-all:
	$(DOCKER_COMPOSE) stop
	$(DOCKER_COMPOSE_DEV) -p dev stop
	$(DOCKER_COMPOSE_TEST) -p ci stop

docker-down-all:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE_DEV) -p dev down
	$(DOCKER_COMPOSE_TEST) -p ci down

docker-volume-rm-all:
	docker volume rm $(DOCKER_VOLUMES)