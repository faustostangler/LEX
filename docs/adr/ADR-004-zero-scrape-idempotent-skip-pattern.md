# ADR-004: Zero-Scrape Idempotent Skip Pattern

## Status
**ACCEPTED**

## Context
In government gazette ingestion pipelines, scraping hundreds or thousands of discrete normative acts (e.g. 3,618 acts per daily edition of the Federal Official Gazette DOU) consumes substantial network bandwidth, CDN requests, and compute resources.

When running backfills, scheduled cron triggers, or recovery jobs, spiders frequently encounter dates that have already been 100% ingested into PostgreSQL. Re-downloading every discrete HTML article without verification causes unnecessary network load on government servers and slows pipeline execution from milliseconds to several minutes.

## Decision
We implement the **Zero-Scrape Idempotent Early-Exit Pattern** directly in Gazette Spiders:

1. **Index-Level Ingestion Check**:
   - Spiders fetch the lightweight journal edition metadata page (`leiturajornal`) to obtain the official `total_acts` count.
   - Before spawning concurrent worker tasks or downloading discrete article bodies, the spider queries `GazetteRepositoryPort.get_by_territory_and_date(territory_id, date, section)`.

2. **Early-Exit Condition**:
   - If an existing edition record is found in PostgreSQL with `ingestion_status == COMPLETED` and `existing.total_acts == total_acts`, the spider logs an info message and immediately returns without downloading individual article bodies.
   - Pipeline execution for already ingested editions completes in **under 1 second**.

3. **Force Override**:
   - An explicit `--force` CLI flag (`spider_args["force"] = True`) bypasses the early-exit check, allowing manual re-scraping and data refreshing when necessary.

## Consequences

### Positive
- **Near-Instant Re-runs**: Re-running a crawler on existing data completes in milliseconds rather than 5+ minutes.
- **Respect for Government CDNs**: Drastically reduces network traffic and avoids triggering rate limits (429) or Cloudflare/Azion blocks.
- **Seamless Recovery**: Idempotent by design, allowing daily batch jobs to safely re-run without duplicate workload.

### Negative / Trade-offs
- The spider requires access to `GazetteRepositoryPort` (injected via `from_crawler` or constructor) to verify existing database status.
