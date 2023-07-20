OPTION = PYTHONDONTWRITEBYTECODE=1

run:
	$(OPTION) python3 -m uvicorn api.main:app --reload --port 8888

migrate:
	$(OPTION) python3 -m api.db

test:
	$(OPTION) python3 -m pytest -svv

# re-test only failed tests
re:
	$(OPTION) python3 -m pytest -svv --lf


# preformance
measure:
	$(OPTION) python3 -m pytest --durations=0

cov:
	$(OPTION) python3 -m pytest --cov --cov-report=html && google-chrome ./htmlcov/index.html

profile:
	$(OPTION) python3 -m pytest --profile-svg


.PHONY: dump
dump:
	sqlite3 dev.db .dump > ./dump/database.sql

.PHONY: load
load:
	cat ./dump/database.sql | sqlite3 dev.db
