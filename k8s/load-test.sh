#!/bin/bash
# Simulate HTTP requests to the app every 0.1 seconds for 60 seconds
END=$((SECONDS+60))
while [ $SECONDS -lt $END ]; do
  curl -s http://localhost:8080/ > /dev/null
  sleep 0.1
done
echo "Load test finished"
