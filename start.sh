#!/bin/bash
echo "[x] Rabbit http://localhost:8080"
echo "[x] InfluxDB http://localhost:8888"
echo "[x] Grafana http://localhost:5000"
./wait-for-it.sh localhost:5672 # rabbitmq
./wait-for-it.sh localhost:8086 # influxdn
./wait-for-it.sh localhost:5000 # grafana

python ./1.ingest/twitter_ingest.py & python ./2.sentiment/sentiment.py & python ./3.persistence/persistence.py