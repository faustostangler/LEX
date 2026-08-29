# ADR-003: Centralized Configuration and Constant Governance

## Status
**ACCEPTED**

## Context
In early prototypes and iterations of the LEX ingestion and digestion pipeline, various operational parameters, magic numbers, URLs, timeouts, regex patterns, and retry thresholds were hardcoded inline within individual functions and coroutines. 

Leaving configuration values and operational constants scattered throughout execution logic introduces several critical architectural liabilities:
1. **Violation of 12-Factor App (Config)**: Environment-specific configurations must be strictly segregated from execution code and validated at startup.
2. **Cognitive Load & Reduced DX**: Tuning concurrency, rate limits, timeouts, or regular expressions required excavating internal business logic across multiple modules.
3. **Inconsistent Defaults**: Divergent timeout and retry thresholds between spiders, HTTP clients, and Scrapy middlewares caused unpredictable fault-tolerance behaviors.

## Decision
We enforce a strict **Two-Tier Configuration and Constant Governance Hierarchy** across the entire LEX ecosystem:

### 1. Global & Cross-Module Configuration (`shared_kernel.config` & `settings.py`)
- All parameters that control infrastructure endpoints, database connections, global concurrency, logging, telemetry, or shared crawler policies **MUST** reside in `src/lex/shared_kernel/config.py` managed via `LexSettings` (`pydantic-settings`).
- All Scrapy-specific engine settings, middleware pipelines, and extension switches **MUST** reside in `src/lex/ingestion/infrastructure/scrapy_project/settings.py`.
- Startup execution enforces **Fail-Fast Validation**: missing mandatory environment variables (such as `LEX_DATABASE_URL`) or out-of-bound numerical thresholds halt execution immediately.

### 2. Module & Adapter-Level Constant Hoisting
- Any domain-bound or adapter-bound constant, HTTP header dictionary, pre-compiled regular expression pattern, default date fallback, or connection tuning limit that is local to a specific module **MUST** be hoisted as a module-level uppercase constant (`UPPER_SNAKE_CASE`) at the very top of the respective Python file, immediately following docstrings and imports.
- Zero inline "magic literals" (numbers, URLs, regex strings) are permitted within function or method bodies.

## Consequences

### Positive
- **Single Source of Truth (SSOT)**: Operational parameters can be audited, reviewed, and modified at the file header or through environment variables without touching execution algorithms.
- **Performance Optimization**: Pre-compiling regexes (`re.compile`) at module initialization avoids recompilation overhead during high-throughput ingestion.
- **Strict 12-Factor Compliance**: Decouples code from operational tuning and deployment environments.
- **Zero Inline Cognitive Noise**: Methods and functions focus purely on domain logic and data transformations.

### Negative / Trade-offs
- Adding new configurable parameters requires updating `LexSettings` or defining formal constants at the file header rather than dropping quick inline literals.
