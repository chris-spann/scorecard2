.PHONY: test clean help

help:
	@echo "test - run tests"
	@echo "clean - remove all generated files"

test:
	docker-compose run backend pytest -v --cov=app --cov-report term-missing

clean:
	docker-compose down --remove-orphans
