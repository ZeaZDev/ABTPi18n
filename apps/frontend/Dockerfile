# // ZeaZDev [Frontend Dockerfile Production Build] //
# // Project: Auto Bot Trader i18n //
# // Version: 1.0.0 (Omega Scaffolding) //
# // Author: ZeaZDev Meta-Intelligence (Generated) //
# // --- DO NOT EDIT HEADER --- //

FROM node:18-alpine AS base

# Install dependencies stage
FROM base AS deps
WORKDIR /app

COPY package.json ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Build stage
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Set environment variable for build
ENV NEXT_TELEMETRY_DISABLED 1

RUN npm install -g pnpm && pnpm build

# Production stage
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
