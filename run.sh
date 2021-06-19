#!/bin/bash

# ...
SERVICE_CONTAINER_1="bot_stop_hate_core_ai"
SERVICE_NAME="stop-hate-ai"


# ...
clear
echo "========================== START ============================="
echo ">> CLEANS <<"
docker stop $SERVICE_CONTAINER_1 || true && docker rm $SERVICE_CONTAINER_1 || true
docker-compose --file docker-compose.yml up 
echo "========================== END ==============================="