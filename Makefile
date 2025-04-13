.PHONY: setup run test format lint build run-prod venv

venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip

setup: venv
	. .venv/bin/activate && pip install -r requirements.txt

build: 
	docker build -t fastapi-app .

run: 
	docker run -p 8000:8000 fastapi-app

test: 
	. .venv/bin/activate && pytest -v

format: setup
	. .venv/bin/activate && black .
	. .venv/bin/activate && ruff --fix .

lint: setup
	. .venv/bin/activate && ruff check .
	. .venv/bin/activate && black --check . 