# Base node image
FROM node:20-alpine AS base
WORKDIR /app
# Install system dependencies
RUN apk add --no-cache openssl ca-certificates python3 make g++

# Build stage
FROM base AS builder
# Copy local package configurations
COPY package.json package-lock.json* ./
# Copy workspace packages
COPY foundation/package.json ./foundation/
COPY chapters/brain/topic-orchestration/package.json ./chapters/brain/topic-orchestration/

# Install exact dependencies
RUN npm ci

# Copy full source
COPY . .

# Generate Prisma Client & Build TypeScript
RUN cd foundation && npx prisma generate && npm run build
RUN cd chapters/brain/topic-orchestration && npm run build

# Production stage
FROM base AS runner
ENV NODE_ENV=production
# Add non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 vtestartup

# Copy compiled output and bare dependencies
COPY --from=builder /app/package.json /app/package-lock.json* ./
COPY --from=builder /app/foundation/dist ./foundation/dist
COPY --from=builder /app/foundation/package.json ./foundation/package.json
COPY --from=builder /app/foundation/prisma ./foundation/prisma
COPY --from=builder /app/chapters/brain/topic-orchestration/dist ./chapters/brain/topic-orchestration/dist
COPY --from=builder /app/chapters/brain/topic-orchestration/package.json ./chapters/brain/topic-orchestration/package.json
COPY --from=builder /app/node_modules ./node_modules

# Switch user
USER vtestartup

# Expose orchestration port
EXPOSE 4000
CMD ["node", "chapters/brain/topic-orchestration/dist/server.js"]
