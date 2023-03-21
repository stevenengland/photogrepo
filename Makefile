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
	@DJANGO_ENV=test pytest

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
