# Movement Labs Exercise – Chi Ngo

This is the technical exercise project for Movement Labs.

## Tech Stack
- **Backend**: [Flask](https://flask.palletsprojects.com/) – web framework
- **Frontend**: [React](https://reactjs.org/) with Vite – user interface
- **Database**: [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) – ORM & database layer
- **AI/LLM**: [Ollama](https://ollama.ai/) – local AI model serving
- **Containerization**: Docker & Docker Compose

## Architecture
```
├── server/          # Flask backend API
├── client/          # React frontend  
├── ollama/          # AI model serving (Llama 3.2:1b)
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
   - **Ollama API**: http://localhost:11434

4. Download AI model (first time setup):
   ```bash
   # Pull the Llama 3.2:1b model
   docker-compose exec ollama ollama pull llama3.2:1b
   
   # Verify model is available
   docker-compose exec ollama ollama list
   ```

### Services
- **db**: PostgreSQL database (port 5432)
- **server**: Flask API backend with CORS enabled (port 5143)  
- **client**: React frontend with Nginx (port 3000)
- **ollama**: AI model server - Llama 3.2:1b (port 11434)

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

# Reset database and AI models
docker-compose down -v  # This removes volumes too

# Manage AI models
docker-compose exec ollama ollama list        # List installed models
docker-compose exec ollama ollama pull <model>  # Download new model
docker-compose exec ollama ollama rm <model>    # Remove model
```

## AI Features
This application integrates with Ollama to provide AI-powered message generation:
- **Model**: Llama 3.2:1b (lightweight, fast inference)
- **Features**: 
  - Generate introduction messages
  - Create follow-up communications  
  - Draft meeting requests
- **API Endpoints**:
  - `POST /messages` - Generate AI messages for contacts

## Getting Started (Local Development without Docker)

1. Clone the repo and create a virtual environment:
   ```bash
   git clone https://github.com/<your-username>/mlabs-exercise-chingo.git
   cd mlabs-exercise-chingo
   py -3.12 -m venv .venv
   .\.venv\Scripts\activate   # (Windows)
