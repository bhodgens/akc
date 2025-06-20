SHELL := /bin/bash
VENV := .venv

.PHONY: help venv install deps test clean lint

help:
	@echo "Commands:"
	@echo "venv - create python venv"
	@echo "install - install the project in the venv"
	@echo "deps - install dependencies in the venv"
	@echo "test - run tests in the venv"
	@echo "lint - lint the project in the venv"
	@echo "clean - clean all unnecessary files"

venv:
	python3 -m venv $(VENV)

env:
	source $(VENV)/bin/activate

install: venv
	./$(VENV)/bin/pip install -e .

deps: venv
	./$(VENV)/bin/pip install -r requirements.txt

test: venv
	./$(VENV)/bin/python -m pytest

lint: venv
	./$(VENV)/bin/ruff check .

clean:
	rm -rf akc.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf $(VENV)
