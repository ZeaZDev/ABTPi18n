# // ZeaZDev [Backend Dockerfile Production Build] //
# // Project: Auto Bot Trader i18n //
# // Version: 1.0.0 (Omega Scaffolding) //
# // Author: ZeaZDev Meta-Intelligence (Generated) //
# // --- DO NOT EDIT HEADER --- //

FROM python:3.10-slim

WORKDIR /app

# Set PYTHONPATH to /app for proper imports
ENV PYTHONPATH=/app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Generate Prisma client (no-op if CLI not present)
RUN prisma generate || echo "Prisma CLI not available, skipping generation"

# Expose port for FastAPI
EXPOSE 8000

# Default command: run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
