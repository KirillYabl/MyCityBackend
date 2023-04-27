venv:
	test -d venv || python3.9 -m venv venv

install-dev:
	. venv/bin/activate && pip install -r dev-requirements.txt

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose run --rm api sh -c './manage.py migrate'

fill_db:
	docker compose run --rm api sh -c './manage.py fill_test_data'

drop_test_db:
	docker compose run --rm api sh -c './manage.py drop_test_data'

tests:
	docker compose run --rm api sh -c 'pytest .'

tests-ci:
	docker compose --file docker-compose.ci.yaml run --rm api sh -c 'pytest ./my_city'

lint-ci:
	docker compose --file docker-compose.ci.yaml run --rm api sh -c 'ruff check ./my_city'

lint:
	ruff check ./my_city

isort:
	ruff --select I ./my_city --fix

.PHONY: venv tests