venv:
	test -d venv || python3.9 -m venv venv

install-dev:
	. venv/bin/activate && pip install -r dev-requirements.txt

migrate:
	my_city/manage.py migrate

up_db:
	docker compose up

run:
	my_city/manage.py runserver

fill_db:
	my_city/manage.py fill_test_data

drop_test_db:
	my_city/manage.py drop_test_data

tests:
	cd my_city && pytest .

.PHONY: venv