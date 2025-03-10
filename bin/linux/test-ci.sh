#!/bin/bash
docker compose -f docker-compose-test.yml build
docker compose -f docker-compose-test.yml up -d --force-recreate
docker compose -f docker-compose-test.yml exec -T api-test /bin/sh -c "pytest ./tests/"