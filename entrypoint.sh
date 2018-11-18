#!/usr/bin/env bash

exec gunicorn -b unix:/apps/ironman/app.sock ironman.wsgi:application \
        --workers=2 \
        --log-level=info \
        --log-file=-\
        --access-logfile=- \
        --error-logfile=- \
        --timeout 30000 \
        --reload