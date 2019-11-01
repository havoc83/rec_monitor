#!/bin/bash
docker network create -d bridge watchdog
docker run -d --rm --network=watchdog -p 6379:6379 --name=redis redis:5-alpine
docker run -it --rm --network=watchdog -v $(pwd):/usr/src/app python:3.7-alpine /bin/sh
docker stop redis
docker network rm watchdog

