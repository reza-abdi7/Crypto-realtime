start-redpanda:
	docker-compose -f redpanda.yaml up -d

stop-redpanda:
	docker-compose -f redpanda.yaml down

add-partition-trades:
	docker compose -f redpanda.yaml exec redpanda rpk topic add-partitions trades --num 1