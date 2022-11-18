.PHONY: venv

requirements.txt: requirements.in
	pip-compile requirements.in

venv:
	python -m venv venv
	venv/bin/pip install -r requirements.txt

lint:
	venv/bin/black --check main.py
	venv/bin/isort --check main.py
	venv/bin/flake8 main.py

format:
	venv/bin/black main.py
	venv/bin/isort main.py
