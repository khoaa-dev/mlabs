# Docker Setup Guide

## Yêu cầu hệ thống
- Docker Desktop (Windows/Mac) hoặc Docker Engine (Linux)
- Docker Compose  
- Tối thiểu 8GB RAM (khuyến nghị 16GB cho Ollama)
- Tối thiểu 4GB dung lượng ổ cứng trống (cho AI models)

## Cài đặt Docker

### Windows (WSL2)
1. Tải và cài đặt [Docker Desktop](https://docs.docker.com/desktop/install/windows/)
2. Trong Docker Desktop Settings, bật WSL 2 integration
3. Restart WSL terminal

### Linux
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again
```

### macOS
```bash
# Install via Homebrew
brew install docker docker-compose

# Or download Docker Desktop
```

## Kiểm tra cài đặt
```bash
docker --version
docker-compose --version
```

## Chạy dự án
```bash
# Khởi động tất cả services
docker-compose up --build

# Hoặc chạy background
docker-compose up -d --build

# Kiểm tra status
docker-compose ps

# Xem logs
docker-compose logs -f

# Download AI model (first time setup)
docker-compose exec ollama ollama pull llama3.2:1b

# Verify model installation
docker-compose exec ollama ollama list
```

## Troubleshooting

### Lỗi permission denied
```bash
sudo chmod +x start.sh
```

### Port đã được sử dụng
Thay đổi ports trong docker-compose.yml:
```yaml
services:
  client:
    ports:
      - "3001:80"  # Thay vì 3000:80
  server:
    ports:  
      - "5144:5143"  # Thay vì 5143:5143
```

### Database connection errors
Đảm bảo PostgreSQL container đã start hoàn toàn trước khi backend connect:
```bash
docker-compose up db
# Đợi vài giây
docker-compose up server client
```

### Ollama model errors
Nếu gặp lỗi AI model:
```bash
# Kiểm tra Ollama container
docker-compose logs ollama

# Download model manually
docker-compose exec ollama ollama pull llama3.2:1b

# Test Ollama API
curl http://localhost:11434/api/tags
```

### Memory issues with Ollama
Nếu hệ thống không đủ RAM:
```bash
# Use smaller model
docker-compose exec ollama ollama pull llama3.2:1b  # ~1.3GB
# instead of llama3:latest (~4GB)

# Monitor resource usage
docker stats
```

### Slow AI response times
```bash
# Check if model is loaded
docker-compose exec ollama ollama ps

# Warm up the model
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2:1b", "prompt": "Hello", "stream": false}'
```

## Development Commands

### Service Management
```bash
# Start specific services
docker-compose up db ollama          # Start database and AI only
docker-compose up db server          # Start backend only
docker-compose up --scale ollama=0   # Start without AI service

# Restart specific service
docker-compose restart server
docker-compose restart ollama
```

### Model Management
```bash
# List all available models
docker-compose exec ollama ollama list

# Download different models
docker-compose exec ollama ollama pull codellama:7b    # For code generation
docker-compose exec ollama ollama pull mistral:7b     # Alternative model

# Remove unused models to free space
docker-compose exec ollama ollama rm <model-name>

# Check model info
docker-compose exec ollama ollama show llama3.2:1b
```

### Testing AI Integration
```bash
# Test message generation endpoint
curl -X POST http://localhost:5143/messages \
  -H "Content-Type: application/json" \
  -d '{"contact_id": 1, "message_type": "intro", "prompt_hint": "software engineer"}'

# Test health endpoints
curl http://localhost:5143/health     # Backend health
curl http://localhost:11434/api/tags  # Ollama health
```
