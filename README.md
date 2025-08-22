# Movement Labs Exercise – Chi Ngo

This is the technical exercise project for Movement Labs.

## Tech Stack
- **Backend**: [Flask](https://flask.palletsprojects.com/) – web framework
- **Frontend**: [React](https://reactjs.org/) with Vite – user interface
- **Database**: [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) – ORM & database layer
- **Containerization**: Docker & Docker Compose

## Architecture
```
├── server/          # Flask backend API
├── client/          # React frontend
├── docker-compose.yml
└── Database (PostgreSQL)
```

## Getting Started with Docker (Recommended)

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Quick Start
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mlabs-exercise-chingo-main
   ```

2. Start all services:
   ```bash
   ./start.sh
   ```
   
   Or manually:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:5143
   - **Health Check**: http://localhost:5143/health

### Services
- **db**: PostgreSQL database (port 5432)
- **server**: Flask API backend (port 5143)  
- **client**: React frontend with Nginx (port 3000)

### Docker Commands
```bash
# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f [service_name]

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build

# Reset database
docker-compose down -v  # This removes volumes too
```

## Getting Started (Local Development without Docker)

1. Clone the repo and create a virtual environment:
   ```bash
   git clone https://github.com/<your-username>/mlabs-exercise-chingo.git
   cd mlabs-exercise-chingo
   py -3.12 -m venv .venv
   .\.venv\Scripts\activate   # (Windows)
