start-redpanda:
	docker-compose -f redpanda.yaml up -d

stop-redpanda:
	docker-compose -f redpanda.yaml down

add-partition-trades:
	docker compose -f redpanda.yaml exec redpanda rpk topic add-partitions trades --num 1

# Technical Indicators Pipeline
# for live data
build-technical-indicators-live:
	docker compose -f technical-indicators-live.yaml build

start-technical-indicators-live: build-technical-indicators-live
	docker compose -f technical-indicators-live.yaml up -d

stop-technical-indicators-live:
	docker compose -f technical-indicators-live.yaml down

# for historical data
build-technical-indicators-historical:
	docker compose -f technical-indicators-historical.yaml build
	
backfill-technical-indicators: build-technical-indicators-historical
	$(eval RUN_ID := $(shell uuidgen))
	@echo "Starting backfill with RUN_ID: $(RUN_ID)"
	RUN_ID=$(RUN_ID) docker compose -f technical-indicators-historical.yaml up -d
