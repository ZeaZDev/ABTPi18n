# // ZeaZDev [Backend Dockerfile Production Build] //
# // Project: Auto Bot Trader i18n //
# // Version: 1.0.0 (Omega Scaffolding) //
# // Author: ZeaZDev Meta-Intelligence (Generated) //
# // --- DO NOT EDIT HEADER --- //

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PRISMA_SCHEMA_PATH=/app/prisma/schema.prisma

WORKDIR /app

# Install Node.js 20.x LTS for Prisma
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate Prisma client if schema exists
RUN if [ -f prisma/schema.prisma ]; then prisma generate --schema prisma/schema.prisma; fi

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
