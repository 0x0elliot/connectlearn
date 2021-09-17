#!/bin/bash
echo "Starting ConnectLearn"
exec gunicorn 'src:app' \
    --bind '0.0.0.0:8000' \
    --workers 5 \