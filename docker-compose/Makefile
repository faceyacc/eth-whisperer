start-redpanda:
	docker compose -f redpanda.yml up -d
stop-redpanda:
	docker compose -f redpanda.yml down -v

start-feature-pipeline:
	docker compose -f feature_pipeline.yml up -d

stop-feature-pipeline:
	docker compose -f feature_pipeline.yml down -v

run: start-redpanda start-feature-pipeline

stop: stop-feature-pipeline stop-redpanda
