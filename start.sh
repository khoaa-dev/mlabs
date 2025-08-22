#!/bin/bash

# Build and start all services
echo "Building and starting all services..."
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

# Wait for services to be healthy
echo "Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "Checking service status..."
docker compose ps

echo "Setup complete! Your application should be available at:"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:5143"
echo "Database: localhost:5432"
echo ""
echo "To view logs: docker compose logs -f [service_name]"
echo "To stop: docker compose down"
echo "To rebuild: docker compose up --build"
