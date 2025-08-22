# ========================================
# BASE DEPENDENCIES STAGE
# ========================================
FROM node:22-alpine AS deps
WORKDIR /usr/src/app

# Install system dependencies
RUN apk add --no-cache \
    libc6-compat \
    python3 \
    make \
    g++ \
    && ln -sf python3 /usr/bin/python

# Copy package files
COPY package.json ./

# Install ALL dependencies
RUN npm install

# ========================================
# DEVELOPMENT STAGE
# ========================================
FROM node:22-alpine AS development
WORKDIR /usr/src/app

# Install runtime dependencies
RUN apk add --no-cache libc6-compat curl

# Copy config files first
COPY package*.json ./
COPY tsconfig.json* ./
COPY vite.config* ./
COPY tailwind.config* ./

# Copy node_modules from deps stage
COPY --from=deps /usr/src/app/node_modules ./node_modules

# Copy source code
COPY . .

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 reactjs

# Set ownership
RUN chown -R reactjs:nodejs /usr/src/app
USER reactjs

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev"]