#!/usr/bin/env bash
docker-compose -f docker-compose.dev.yml -p dev down
docker-compose -f docker-compose.dev.yml -p dev build
docker-compose -f docker-compose.dev.yml -p dev up