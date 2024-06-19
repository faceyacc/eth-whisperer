build:
	docker build -t kafka_to_fs .


run: build
	docker run \
    	--network=redpanda_network \
    	--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
    	kafka_to_fs

lint:
	poetry run ruff check --fix

format:
	poetry run ruff format
