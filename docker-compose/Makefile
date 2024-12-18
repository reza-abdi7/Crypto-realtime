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


# News Sentiment Pipeline
# for live data
build-news-sentiment-live:
	docker compose -f news-sentiment-live.yaml build

start-news-sentiment-live: build-news-sentiment-live
	docker compose -f news-sentiment-live.yaml up -d

stop-news-sentiment-live:
	docker compose -f news-sentiment-live.yaml down



clean-backfill-kakfa-topics:
	@echo "Removing all Kafka topics that contain the word historical"
	docker compose -f redpanda.yml exec redpanda rpk topic delete -r ".*historical.*"