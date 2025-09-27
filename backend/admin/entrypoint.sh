#!/bin/sh

uvicorn main:app --host $ADMIN_SERVICE_HOST --port $ADMIN_SERVICE_PORT --reload

exec "$@"