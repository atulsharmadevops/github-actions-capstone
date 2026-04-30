#!/bin/bash
set -e

docker build -t myapp:latest .
docker run -d -p 5000:5000 --name myapp myapp:latest

sleep 10

STATUS=$(curl -s http://localhost:5000/health | grep -o "ok")

if [ "$STATUS" == "ok" ]; then
  echo "Health Check PASSED"
else
  echo "Health Check FAILED"
  docker logs myapp 
  exit 1
fi

docker stop myapp
docker rm myapp
