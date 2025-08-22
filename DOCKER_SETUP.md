# Docker Setup Guide

## Yêu cầu hệ thống
- Docker Desktop (Windows/Mac) hoặc Docker Engine (Linux)
- Docker Compose

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
