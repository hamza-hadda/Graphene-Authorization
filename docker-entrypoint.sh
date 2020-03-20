#!/bin/sh
set -e


if [ -n "$CONTAINER_ENV_VARIABLE_FILE" ]
then
    aws s3 cp "$CONTAINER_ENV_VARIABLE_FILE" /tmp/env
    echo Exporting .env file
    eval $(cat /tmp/env | sed 's/^/export /')
fi

exec "$@"
