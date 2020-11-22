DC = docker-compose

build:
	$(DC) build
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

test.build:
	$(DC) -f test-docker-compose.yml build

test.abort:
	$(DC) -f test-docker-compose.yml down

test:
	$(DC) -f test-docker-compose.yml up -d test_postgres
	$(DC) -f test-docker-compose.yml run --rm test_backend
	$(DC) -f test-docker-compose.yml down
