APP_NAME=app_financial_investment
SERVER_HOST=0.0.0.0
SERVER_PORT=8010
COVERAGE_OPTS=--cov=app --cov-report=term --cov-report=html
DOCKER_COMPOSE=docker-compose

.PHONY: build start start-detached stop test run-local run-local-detached test-local generate-coverage lint clean-docker help remove-unused-volumes

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  build                  to build the Docker image using docker-compose"
	@echo "  start                  to start the Docker container in attached mode (logs visible in console)"
	@echo "  start-build            to start and build the Docker container in detached mode (runs in background)"
	@echo "  start-detached         to start the Docker container in detached mode (runs in background)"
	@echo "  stop                   to stop the running Docker container"
	@echo "  test                   to run tests inside the Docker container"
	@echo "  run-local              to run the application locally in attached mode (logs visible in console)"
	@echo "  run-local-detached     to run the application locally in detached mode (runs in background)"
	@echo "  test-local             to run tests locally"
	@echo "  generate-coverage      to generate a coverage report"
	@echo "  lint                   to format the code according to the standard style"
	@echo "  clean-docker           to remove containers, networks, and unused volumes"
	@echo "  remove-unused-volumes  to remove all unused local volumes"

build:
	$(DOCKER_COMPOSE) build

start:
	$(DOCKER_COMPOSE) up

start-build:
	$(DOCKER_COMPOSE) up -d --build

start-detached:
	$(DOCKER_COMPOSE) up -d

stop:
	$(DOCKER_COMPOSE) down

test:
	$(DOCKER_COMPOSE) exec $(APP_NAME) pytest

run-local:
	uvicorn src.main:app --host $(SERVER_HOST) --port $(SERVER_PORT)

run-local-detached:
	uvicorn src.main:app --host $(SERVER_HOST) --port $(SERVER_PORT) &

test-local:
	python3 -m pytest -vv

generate-coverage:
	python -m pytest $(COVERAGE_OPTS) ${1:-tests}

lint:
	isort .
	black .

clean-docker:
	$(DOCKER_COMPOSE) down --remove-orphans
	docker system prune -a -f --volumes

remove-unused-volumes:
	docker volume prune -f
