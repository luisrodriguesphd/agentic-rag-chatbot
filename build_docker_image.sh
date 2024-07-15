#!/bin/bash

# Navigate to the directory containing the Dockerfile
cd .

# Build the Docker image
docker build -t agentic-rag-chatbot:latest . --build-arg REQUIREMENTS_PATH="./requirements.in"

# Check if the image was created successfully
docker images | agentic-rag-chatbot

# Run docker image
# docker run -it -p 7860:7860 agentic-rag-chatbot