start-redpanda:
	docker-compose -f redpanda.yaml up -d

stop-redpanda:
	docker-compose -f redpanda.yaml down

add-partition-trades:
	docker compose -f redpanda.yaml exec redpanda rpk topic add-partitions trades --num 1

# Technical Indicators Pipeline
build-technical-indicators-pipeline:
	docker-compose -f technical-indicators-pipeline.yaml build

start-technical-indicators-pipeline: build-technical-indicators-pipeline
	docker-compose -f technical-indicators-pipeline.yaml up -d

stop-technical-indicators-pipeline:
	docker-compose -f technical-indicators-pipeline.yaml down