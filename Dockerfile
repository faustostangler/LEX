# syntax=docker/dockerfile:1
# -----------------------------------------------------------------------------
# Single Source of Truth Multi-Stage Dockerfile for LEX System (ADR-009 / 12-Factor)
# Manifests multiple deployment roles: CLI, Crawler Worker, API Server.
# -----------------------------------------------------------------------------

FROM ghcr.io/astral-sh/uv:0.5.26 AS uv-bin
FROM python:3.12-slim AS base

# System runtime dependencies and non-root user setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install minimal OS dependencies for PostgreSQL and SSL
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary from official image
COPY --from=uv-bin /uv /uvx /bin/

# -----------------------------------------------------------------------------
# Dependency Builder Stage
# -----------------------------------------------------------------------------
FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cache dependency installations
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# -----------------------------------------------------------------------------
# Final Production Runtime Image
# -----------------------------------------------------------------------------
FROM base AS runner

# Create non-root system user for security isolation
RUN groupadd -r lex && useradd -r -g lex -m -d /home/lex lex

# Copy virtualenv and application source
COPY --from=builder --chown=lex:lex /app/.venv /app/.venv
COPY --chown=lex:lex . /app

# Install project root into venv
RUN uv sync --frozen --no-dev

USER lex

EXPOSE 8000

# Default entrypoint routes to lex CLI
ENTRYPOINT ["lex"]
CMD ["--help"]
