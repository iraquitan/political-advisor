DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_DEV = $(DOCKER_COMPOSE) -f docker-compose.dev.yml
DOCKER_COMPOSE_PROD = $(DOCKER_COMPOSE) -f docker-compose.production.yml
DOCKER_COMPOSE_TEST = $(DOCKER_COMPOSE) -f docker-compose.test.yml
DOCKER_ARGS ?=
APP_LIST ?= django_political_advisor.test
RUN_TIME = $(shell date +%Y-%m-%dT%H:%M:%S)

.PHONY: docker-stop-all collectstatics makemigrations run test

collectstatics:
	$(DOCKER_COMPOSE_DEV) -p dev run web python manage.py collectstatic --noinput
	$(DOCKER_COMPOSE_DEV) -p dev stop

makemigrations:
	$(DOCKER_COMPOSE_DEV) -p dev run web python manage.py makemigrations
	$(DOCKER_COMPOSE_DEV) -p dev stop

run: collectstatics
	$(DOCKER_COMPOSE_DEV) -p dev up $(DOCKER_ARGS)
	$(DOCKER_COMPOSE_DEV) -p dev stop

test:
	$(DOCKER_COMPOSE_TEST) -p ci up -d $(DOCKER_ARGS)
	docker wait ci_sut_1
	docker logs --since $(RUN_TIME) ci_sut_1
	$(DOCKER_COMPOSE_TEST) -p ci stop

ci:
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