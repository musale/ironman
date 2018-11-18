# commands begin with p run only in production
COMPOSE		:= docker-compose
PRODUCTION	:= -f compose/docker-compose.prod.yml
DEVELOPMENT	:= -f compose/docker-compose.dev.yml
MANAGE		:= python manage.py
NAME		:= musale/ironman
TAG			:= $$(git rev-parse --short HEAD)
IMG			:= ${NAME}:${TAG}
LATEST		:= ${NAME}:latest

.PHONY: chk
chk:
	@echo "mic check 1, 2, 3... Deployed!"

.PHONY: build
build:
	@docker build -t ${IMG} .
	@docker tag ${IMG} ${LATEST}

.PHONY: push
push:
	@docker push ${NAME}

.PHONY: pull
pull:
	@docker pull ${NAME}

.PHONY: up
up:
	@${COMPOSE} ${DEVELOPMENT} up

.PHONY: stop
stop:
	@${COMPOSE} ${DEVELOPMENT} stop

.PHONY: rm
rm:
	@${COMPOSE} ${DEVELOPMENT} rm -fsv

.PHONY: test
test:
	${COMPOSE} ${DEVELOPMENT} run --rm ironman python -m pytest


.PHONY: migrations
migrations:
	@${COMPOSE} ${DEVELOPMENT} exec ironman ${MANAGE} makemigrations

.PHONY: migrate
migrate:
	@${COMPOSE} ${DEVELOPMENT} exec ironman ${MANAGE} migrate

.PHONY: flush
flush:
	@${COMPOSE} ${DEVELOPMENT} exec ironman ${MANAGE} flush

.PHONY: collectstatic
collectstatic:
	@${COMPOSE} ${DEVELOPMENT} exec ironman ${MANAGE} collectstatic --no-input

.PHONY: shell
shell:
	@${COMPOSE} ${DEVELOPMENT} exec ironman ${MANAGE} shell

.PHONY: ssh
ssh:
	@${COMPOSE} ${DEVELOPMENT} exec ironman /bin/bash

.PHONY: pmigrations
pmigrations:
	@${COMPOSE} ${PRODUCTION} exec ironman ${MANAGE} makemigrations

.PHONY: pmigrate
pmigrate:
	@${COMPOSE} ${PRODUCTION} exec ironman ${MANAGE} migrate

.PHONY: pcollectstatic
pcollectstatic:
	@${COMPOSE} ${PRODUCTION} exec ironman ${MANAGE} collectstatic --no-input

.PHONY: pshell
pshell:
	@${COMPOSE} ${PRODUCTION} exec ironman ${MANAGE} shell

.PHONY: pstop
pstop:
	@${COMPOSE} ${PRODUCTION} stop

.PHONY: prm
prm:
	@${COMPOSE} ${PRODUCTION} rm -fsv

.PHONY: pup
pup:
	@${COMPOSE} ${PRODUCTION} up -d

.PHONY: prune
prune:
	@docker system prune -f
