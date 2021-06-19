#!/bin/bash

# ...
SERVICE_CONTAINER_1="chatbot_bot_core_ai_service_1"
SERVICE_CONTAINER_2="chatbot_bot_backend_service_1"
SERVICE_IMAGE_1="chatbot_bot_core_ai_service"
SERVICE_IMAGE_2="chatbot_bot_backend_service"


# ...
clear
echo "========================== START ============================="
echo ">> CLEANS <<"
docker stop $SERVICE_CONTAINER_1 || true && docker rm $SERVICE_CONTAINER_1 || true
docker stop $SERVICE_CONTAINER_2 || true && docker rm $SERVICE_CONTAINER_2 || true
docker rmi $SERVICE_IMAGE_1 || true
docker rmi $SERVICE_IMAGE_2 || true
docker-compose down
docker-compose --file docker-compose.yml up -d
echo "========================== END ==============================="