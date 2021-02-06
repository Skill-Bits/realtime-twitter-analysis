#!/bin/bash
python ./1.ingest/twitter_ingest.py &
python ./2.sentiment/sentiment.py &
python ./3.persistence/persistence.py  &