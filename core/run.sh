#!/bin/bash

# ...
SERVICE_IMAGE="bot_stop_hate_core_ai_image"
SERVICE_CONTAINER="bot_stop_hate_core_ai"
PORT_IN=5005
PORT_OUT=5006

# ...
clear
echo "========================== START ============================="
echo ">> CLEANS <<"
rm -fr build/
rm -fr dist/
rm -fr .eggs/
find . -name '*.egg-info' -exec rm -fr {} +
find . -name '*.egg' -exec rm -f {} +
find . -name "*.pyc" -exec rm -f {} \;
find . -name "*.pyo" -exec rm -f {} \;
find . -name '*~' -exec rm -f {} +
find . -name '__pycache__' -exec rm -fr {} +
rm -fr .tox/
rm -f .coverage
rm -fr htmlcov/
rm -fr app.egg-info/
echo ">> STOP & DELETE CONTAINER <<"
docker stop $SERVICE_CONTAINER || true && docker rm $SERVICE_CONTAINER || true
# TODO remove rasa-chitchat-image
echo ">> BUILD IMAGE <<"
docker build -t $SERVICE_IMAGE --no-cache .
echo ">> RUN CONTAINER <<"
# docker run --name $SERVICE_CONTAINER -p $PORT_OUT:$PORT_IN $SERVICE_IMAGE
docker run --name $SERVICE_CONTAINER -d -p $PORT_OUT:$PORT_IN $SERVICE_IMAGE
echo "========================== END ==============================="