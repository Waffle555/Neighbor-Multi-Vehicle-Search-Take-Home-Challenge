.PHONY: setup run test format lint build run-prod

setup:
	pip install -r requirements.txt


run: setup
	uvicorn main:app --reload --host 0.0.0.0 --port 8000


build: 
	docker build -t fastapi-app .

run-prod: 
	docker run -p 8000:8000 fastapi-app


test: setup
	pytest -v

format: setup
	black .
	ruff --fix .

lint: setup
	ruff check .
	black --check . 