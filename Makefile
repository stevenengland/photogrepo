SHELL := /bin/bash

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

venv:
	./tools/create_venv.sh

lint:
	@echo "*********** YAMLLINT"
	@yamllint -c=.yamllint.yml . || true
	@echo "*********** BLACK"
	@black . || true
	@echo "*********** FLAKE8"
	@flake8 . || true
	@echo "*********** MYPY"
	@mypy . || true

test:
	@pytest

pyclean:
	@find . \
    | grep -E '(__pycache__|\.hypothesis|\.perm|\.cache|\.static|\.py[cod]$)' \
    | xargs rm -rf \
  || true

docker_build:
	@docker-compose -f docker-compose-dev.yml build

docker_lint:
	@docker-compose -f docker-compose-dev.yml run --rm app sh -c '\
		echo "*********** YAMLLINT" && \
		yamllint -c=.yamllint.yml . || true && \
		echo "*********** BLACK" && \
		black . || true && \
		echo "*********** FLAKE8" && \
		flake8 . || true && \
		echo "*********** MYPY" && \
		mypy . || true \
	 '

docker_test:
	@docker-compose -f docker-compose-dev.yml run --rm app sh -c "pytest"


#run:
#	python manage.py runserver
#
#migration:
#	python manage.py makemigrations
#
#migrate:
#	python manage.py migrate
#
#superuser:
#	python manage.py createsuperuser
#
#heroku:
#	git push heroku master
#
#deploy:
#	docker-compose build
#	docker-compose up -d
#
#down:
#	docker-compose down
