.PHONY: test

test:
	@pytest --cov=rubato --cov-report term-missing rubato/tests
	@echo "Linting Code"
	@pylint rubato
