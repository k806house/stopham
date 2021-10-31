#!/bin/bash

set -e

source .env

if [ -z "$1" ]; then
    docker-compose -f docker-compose.dev.yml build
    docker-compose -f docker-compose.dev.yml up -d --remove-orphans
elif [ "$1" = "--app" ]; then
    docker-compose -f docker-compose.dev.yml build core
    docker-compose -f docker-compose.dev.yml up -d --remove-orphans core
elif [ "$1" = "--celeblur" ]; then
    docker-compose -f docker-compose.dev.yml build storage
    docker-compose -f docker-compose.dev.yml up -d --remove-orphans storage
elif [ "$1" = "--help" ]; then
    echo "Flags:"
    echo "--app		    up app"
    echo "--celeblur	up celeblur"
fi
