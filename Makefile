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

test.build:
	$(DC) -f test-docker-compose.yml build

test:
	$(DC) -f test-docker-compose.yml run -d --rm test_postgres
	$(DC) -f test-docker-compose.yml run --rm test_backend
	$(DC) -f test-docker-compose.yml down
