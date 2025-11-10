# // ZeaZDev [Frontend Dockerfile Production Build] //
# // Project: Auto Bot Trader i18n //
# // Version: 1.0.0 (Omega Scaffolding) //
# // Author: ZeaZDev Meta-Intelligence (Generated) //
# // --- DO NOT EDIT HEADER --- //

FROM node:18-alpine AS base

# Enable corepack (pnpm) once
RUN corepack enable

# Dependencies stage
FROM base AS deps
WORKDIR /app

# Copy manifest(s); include lockfile if present
# If you use workspaces add pnpm-workspace.yaml as well
COPY package.json ./
# COPY pnpm-lock.yaml ./
# COPY pnpm-workspace.yaml ./

# If lockfile exists keep --frozen-lockfile; otherwise remove that flag
RUN [ -f pnpm-lock.yaml ] && pnpm install --frozen-lockfile || pnpm install

# Build stage
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

RUN pnpm build

# Production runner
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs \
  && adduser --system --uid 1001 nextjs

# Copy build output (Next.js standalone output + public assets)
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

CMD ["node", "server.js"]