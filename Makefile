export FLASK_APP=run.py
CURRENT_DIR := $(shell pwd)

VIRTUALENV_DIR = .env

help:
	@echo "Usage: $ make <target>"
	@echo " > deps   : install dependencies"
	@echo " > run    : run project "
	@echo " > test   : run tests "

env:
	@echo "[RUN]: create/activate virtualenv"
	@virtualenv -p python3 $(VIRTUALENV_DIR) && \
	. $(VIRTUALENV_DIR)/bin/activate

deps: env
	@echo "[RUN]: install dependencies"
	$(VIRTUALENV_DIR)/bin/pip install -r $(CURRENT_DIR)/requirements.txt

run:
	@echo "[RUN]: run"
	FLASK_DEBUG=1 .env/bin/python -m flask run

test:
	@echo "[RUN]: tests"
	.env/bin/pytest tests
