#!/bin/bash
export CONFIGURATION_SETUP="app.core.settings.DevelopmentConfig"
gunicorn app.app:app \
    --worker-class gevent \
    --preload \
    --reload \
    --workers 8 \
    --bind 0.0.0.0:5000 \
    --max-requests 10000 \
    --timeout 5 \
    --keep-alive 5 \
    --log-level DEBUG