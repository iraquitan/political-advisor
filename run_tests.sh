#!/usr/bin/env bash
docker-compose -f docker-compose.test.yml -p ci down
docker-compose -f docker-compose.test.yml -p ci build
docker-compose -f docker-compose.test.yml -p ci up -d
docker logs -f ci_sut_1
docker wait ci_sut_1
