FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NODE_ENV=production
ENV PORT=3001

# Install curl for healthcheck
RUN chmod 1777 /tmp \
    && apt-get update \
    && apt-get install -y \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-dev.txt

# Copy application code
COPY . .

EXPOSE 3001

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3001/health || exit 1

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "3001"]