.PHONY: install clean help
.DEFAULT_GOAL := help

install:
	@echo "\n>>> creating environment and installing dependencies\n"
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt && pip install -r requirements_dev.txt && pip install -e .

test-docker:
	@echo "\n>>> spark_version: $$SPARK_VERSION\n"
	## pip install -r requirements_dev.txt && pip install -e .
	. venv/bin/activate && tox || true

clean:
	@echo "\n>>> cleaning artifacts\n"
	rm -rf ./.mypy_cache/ ./.pytest_cache/ ./.tox/ ./logs ./output/ .coverage || true
	rm -rf ./src/spark_template/__pycache__/ ./src/spark_template.egg-info/ ./tests/__pycache__/ || true

help:
	@echo ">>> Makefile contents:\n"
	@cat Makefile