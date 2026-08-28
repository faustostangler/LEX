# LEX — Legislação, Extração e Estruturação

Modular Monolith for Brazilian Legislation Ingestion, Digestion, and Structured API.

## Architecture

- **Bounded Contexts**: `ingestion`, `treatment`, `api`, `shared_kernel`
- **Methodology**: Doctor Stangler Method (DDD + Clean & Hexagonal Architecture)
- **Ingestion Engine**: Scrapy Spiders with In-Memory Stream Processing
- **Persistence**: PostgreSQL 16 (Two-Tier Model: `gazette_editions` 1 ──< N `normative_acts`)

## Development

```bash
# Sync dependencies
uv sync

# Run tests
uv run pytest

# Run type checker
uv run mypy src tests

# Run linter
uv run ruff check .
```
