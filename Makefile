DC = docker-compose

build:
	$(DC) build

up:
	$(DC) up

start:
	$(DC) up -d

stop:
	$(DC) down

restart: stop start

restart.scratch: stop build start

status:
	$(DC) ps
