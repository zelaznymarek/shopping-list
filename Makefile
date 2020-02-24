DC = docker-compose

build:
	$(DC) build

build.scratch:
	$(DC) build --no-cache

up:
	$(DC) up

start:
	$(DC) up -d

stop:
	$(DC) down

stop.unmount:
	$(DC) down -v

restart: stop build start

restart.scratch: stop.unmount build.scratch start

status:
	$(DC) ps
