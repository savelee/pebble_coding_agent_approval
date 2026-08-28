# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

export DEVELOPER_DIR ?= /Library/Developer/CommandLineTools
SHELL := /bin/bash
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
BLACK := $(VENV)/bin/black
ISORT := $(VENV)/bin/isort
FLAKE8 := $(VENV)/bin/flake8

.PHONY: help venv install run-apis test lint format clean

help:
	@echo "Available targets:"
	@echo "  venv       : Create virtual environment using uv or python venv"
	@echo "  install    : Install dependencies using uv or pip"
	@echo "  run-apis   : Start the Flask listener service"
	@echo "  test       : Run unit tests with pytest and coverage"
	@echo "  lint       : Check code formatting and style"
	@echo "  format     : Auto-format code using black and isort"
	@echo "  clean      : Remove virtual environment and temporary artifacts"

venv:
	@if command -v uv >/dev/null 2>&1; then \
		uv venv $(VENV); \
		uv pip install -r requirements.txt -r requirements-dev.txt; \
	else \
		/usr/local/bin/python3 -m venv $(VENV); \
		$(PIP) install -r requirements.txt -r requirements-dev.txt; \
	fi

install:
	@if command -v uv >/dev/null 2>&1; then \
		uv pip install -r requirements.txt -r requirements-dev.txt; \
	else \
		$(PIP) install -r requirements.txt -r requirements-dev.txt; \
	fi

run-apis:
	$(PYTHON) -m listener.app

test:
	$(PYTEST) --cov=listener tests/

lint:
	$(FLAKE8) listener tests
	$(BLACK) --check listener tests
	$(ISORT) --check-only listener tests

format:
	$(BLACK) listener tests
	$(ISORT) listener tests

clean:
	rm -rf $(VENV) .pytest_cache .coverage htmlcov
