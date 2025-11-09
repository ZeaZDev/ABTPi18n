# // ZeaZDev [Backend Dockerfile Production Build] //
# // Project: Auto Bot Trader i18n //
# // Version: 1.0.0 (Omega Scaffolding) //
# // Author: ZeaZDev Meta-Intelligence (Generated) //
# // --- DO NOT EDIT HEADER --- //

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for psycopg2 and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Generate Prisma client
RUN prisma generate

# Expose port for FastAPI
EXPOSE 8000

# Default command: run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
