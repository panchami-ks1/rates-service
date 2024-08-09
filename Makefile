# Makefile for Flask API with PostgreSQL

# Variables
DOCKER_COMPOSE = docker-compose
CONTAINER_NAME = flask_api
PORT = 8080

.PHONY: build run stop test build-run

# Default target
all: build run

# Build Docker images
build:
	@echo "Building Docker images..."
	$(DOCKER_COMPOSE) build

# Run the Docker containers
run:
	@echo "Starting Docker containers..."
	$(DOCKER_COMPOSE) up -d

# Build and Run the Docker containers
build-run:
	@echo "Starting Docker containers..."
	$(DOCKER_COMPOSE) up --build -d

# Stop the Docker containers
stop:
	@echo "Stopping Docker containers..."
	$(DOCKER_COMPOSE) down

# Run tests
test:
	@echo "Running tests..."
	$(DOCKER_COMPOSE) run test

# Display help
help:
	@echo "Usage:"
	@echo "  make build    - Build the Docker images"
	@echo "  make run      - Start the Docker containers"
	@echo "  make stop     - Stop the Docker containers"
	@echo "  make test     - Run the tests"
	@echo "  make help     - Display this help message"


