#!/bin/bash
echo "Starting ConnectLearn"

port="8000"

if [[ "$environment" == "netlify" ]]; then
	echo "Deployed on netlify"
	port="443"
fi

echo "$port"

exec gunicorn 'src:app' \
    --bind "0.0.0.0:${port}" \
    --workers 5 \
