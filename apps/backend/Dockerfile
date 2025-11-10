# // ZeaZDev [Backend Dockerfile Production Build] //
# // Project: Auto Bot Trader i18n //
# // Version: 1.0.0 (Omega Scaffolding) //
# // Author: ZeaZDev Meta-Intelligence (Generated) //
# // --- DO NOT EDIT HEADER --- //

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    NPM_CONFIG_CACHE=/tmp/npm-cache \
    PRISMA_SCHEMA_PATH=/app/prisma/schema.prisma

WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js 20.x (avoid nodeenv in prisma-python)
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && node --version && npm --version \
    && apt-get purge -y --auto-remove curl gnupg \
    && rm -rf /var/lib/apt/lists/*

# App code (includes prisma/schema.prisma)
COPY . .

# Generate Prisma client if schema exists; non-fatal on failure
RUN if [ -f "${PRISMA_SCHEMA_PATH}" ]; then \
      echo "Generating Prisma client with schema: ${PRISMA_SCHEMA_PATH}" && \
      prisma generate --schema "${PRISMA_SCHEMA_PATH}" || echo "Prisma generate failed (non-fatal)"; \
    else \
      echo "No Prisma schema found at ${PRISMA_SCHEMA_PATH}, skipping prisma generate"; \
    fi

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]