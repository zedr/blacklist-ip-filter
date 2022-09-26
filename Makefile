.PHONY: default clean test lint

ENV := .env
_PYTHON := python3
PYTHON_VERSION := $(shell ${_PYTHON} -V | cut -d " " -f 2 | cut -d "." -f1-2)
PYTHON := ${ENV}/bin/python3
SITE_PACKAGES := ${ENV}/lib/python${PYTHON_VERSION}/site-packages
APP := ${SITE_PACKAGES}/blipgrep.egg-link
SOURCES := blipgrep.py tests
DEV_REQUIREMENTS := ${SITE_PACKAGES}/pytest ${ENV}/bin/mypy ${ENV}/bin/flake8

default: ${APP}

${PYTHON}:
	@echo "Creating Python ${PYTHON_VERSION} environment..." >&2
	@${_PYTHON} -m venv ${ENV}
	@${PYTHON} -m pip install -U pip setuptools

${APP}: ${PYTHON}
	@${PYTHON} -m pip install -e .

${DEV_REQUIREMENTS}: ${PYTHON}
	@${PYTHON} -m pip install -U pip
	@${PYTHON} -m pip install -r dev-requirements.txt

test: ${DEV_REQUIREMENTS}
	@${PYTHON} -m pytest tests

lint: ${DEV_REQUIREMENTS}
	@flake8 ${SOURCES}
	@${PYTHON} -m mypy ${SOURCES}

clean:
	@rm -rf ${ENV}
