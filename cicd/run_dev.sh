#!/bin/bash

source .env
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d --remove-orphans
