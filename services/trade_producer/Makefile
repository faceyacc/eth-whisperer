build:
	docker build -t trade_producer .

run: build
	docker run --network=redpanda_network trade_producer

lint:
	poetry run ruff check --fix

format:
	poetry run ruff format
