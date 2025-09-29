#!/bin/bash

set -e

if [ "$DEV" = "True" ]; then
    fastapi dev src/main.py --host 0.0.0.0 --port $ADMIN_SERVICE_PORT --reload
else
    fastapi run src/main.py --port $ADMIN_SERVICE_PORT
fi
