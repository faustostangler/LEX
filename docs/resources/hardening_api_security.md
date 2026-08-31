# API & Web Security Hardening Guide (LEX)

> [!IMPORTANT]
> **DRAFT SPECIFICATION / PENDING FUTURE ARCHITECTURAL APPROVAL**
> Active feature development for the public REST API and SRE observability endpoints is currently deferred while the project focuses on ingestion, segmentation, treatment, and consolidation. The technical architectures, security mitigations, and RFC-7807 guidelines specified in this document serve as reference standards and architectural blueprints. Production expansion and deployment of API/SRE components require explicit future phase approval.

This document establishes the enterprise security, lifecycle governance, and vulnerability mitigations implemented in the LEX REST API layer.

---

## 1. Database Connection Pool Lifecycle & FastAPI Dependency Safety

### Vulnerability Identified (VULN-01 - P0)
In FastAPI applications, dependency injection functions that return a resource directly without being generator functions (`yield`) will **not** trigger cleanup when the HTTP request lifecycle concludes. 

When `session_factory()` was returned directly, the SQLAlchemy `Session` remained open, retaining its underlying connection from the `QueuePool`. Under concurrent traffic, the connection pool was quickly saturated, leading to `TimeoutError: QueuePool limit of size 5 overflow 10 reached` and complete denial of service.

### Remediated Architecture (SOTA-KISS)
FastAPI dependencies must be structured as generators wrapping the session in a context manager:

```python
from collections.abc import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from lex.shared_kernel.config import get_settings

def get_db_session() -> Generator[Session, None, None]:
    """Provides a transactional database session per HTTP request with guaranteed cleanup."""
    # Obtain session_factory from app.state or cached singleton
    session: Session = session_factory()
    try:
        yield session
    finally:
        session.close()
```

### Invariants:
1. **Never return raw sessions**: All database access in presentation endpoints must go through `Depends(get_db_session)`.
2. **Deterministic Cleanup**: `finally: session.close()` guarantees immediate connection return to the pool even if the route raises an unhandled `HTTPException` or internal error.

---

## 2. CORS Security Governance & Credential Isolation

### Vulnerability Identified (VULN-04 - P0)
Configuring `CORSMiddleware` with `allow_origins=["*"]` and `allow_credentials=True` violates the W3C Cross-Origin Resource Sharing standard and modern browser security models. If a browser reflects credentials with wildcard origins, malicious third-party origins can execute authenticated requests or capture sensitive legal data.

### Remediated Architecture (SOTA-KISS)
1. **Configurable Whitelist**: Allowed origins are managed via `LexSettings.cors_allowed_origins`.
2. **Conditional Credentials**: If `cors_allowed_origins` is set to `["*"]`, `allow_credentials` is strictly set to `False`. When specific origins are configured (e.g. `https://lex.gov.br`), credentials may be safely enabled.

```python
settings = get_settings()
is_wildcard = "*" in settings.cors_allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=not is_wildcard,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

---

## 3. Synchronous Threadpool Execution vs. Async Event Loop Starvation

### Vulnerability Identified (VULN-02 - P0)
In ASGI frameworks (FastAPI / Starlette / Uvicorn), route handlers declared as `async def` execute directly on the main single-threaded `asyncio` event loop.

When an `async def` route invokes synchronous, blocking I/O calls (such as synchronous SQLAlchemy ORM calls `session.get()`, `session.scalars()`, `session.commit()`, or pure CPU/AST reductions), the entire event loop is frozen for the duration of the database roundtrip. All other concurrent requests across all routes are stalled, producing massive latency spikes, jitter, and eventual request timeouts under moderate load.

### Remediated Architecture (SOTA-KISS)
In accordance with the Doctor Stangler architectural principles, synchronous database operations and AST reductions must **not** be masqueraded with artificial `async def` signatures that block the loop.

1. **Synchronous Route Handlers**: Declare routes using standard `def get_compiled_legislation(...)` instead of `async def`.
2. **Automatic Threadpool Offloading**: FastAPI automatically dispatches synchronous `def` route functions to an external worker threadpool (`anyio.to_thread.run_sync`), executing database I/O concurrently in worker threads while keeping the main `asyncio` event loop non-blocking and responsive.
3. **Pure Synchronous Repositories & Use Cases**: Methods in `ConsolidationRepositoryPort`, `PostgresConsolidationRepository`, `CompileNormativeActUseCase`, and `TimeTravelCompilationUseCase` are declared as pure synchronous `def`, maintaining zero cognitive overhead and exact alignment with SQLAlchemy 2.0 ORM sessions.

```python
# Presentation Layer: FastAPI Route
@router.get("/{identifier}")
def get_compiled_legislation(
    identifier: str,
    as_of: Annotated[date | None, Query(...)] = None,
    session: Annotated[Session, Depends(get_db_session)] = None,
) -> dict[str, Any]:
    """Dispatched automatically to worker threadpool by FastAPI without blocking the asyncio loop."""
    repo = PostgresConsolidationRepository(session=session)
    ...
    compiled_act = repo.get_compiled_act(act_uuid)
    return {...}
```

### Invariants:
1. **Never run blocking ORM calls in `async def`**: If a route or service uses synchronous SQLAlchemy `Session`, the route handler MUST be declared as synchronous `def`.
2. **Clean Hexagonal Signature Alignment**: Application ports and use cases interacting with synchronous persistence adapters must reflect synchronous signatures rather than exposing fake `async` promises.

---

## 4. Centralized Exception Sanitization & RFC-7807 Compliance (CWE-209 Mitigation)

### Vulnerability Identified (VULN-03 - P1)
In default FastAPI setups without global exception handlers, unhandled exceptions originating from persistence layers (`SQLAlchemyError`, `OperationalError`, `IntegrityError`) or generic runtime failures bubble up to the ASGI server. When unhandled, the server may transmit raw stack traces, database schema details, table names, or parameterized SQL queries directly to the client in HTTP 500 error responses (CWE-209: Information Exposure Through an Error Message). This violates LGPD and enterprise security hardening requirements.

### Remediated Architecture (SOTA-KISS)
A centralized exception handling and correlation system is established via [src/lex/api/errors.py](file:///home/stangler/Documents/Python/LEX/src/lex/api/errors.py):

1. **Deterministic Correlation ID (`TraceIdMiddleware`)**: Every request is tagged with a unique `trace_id` (propagating client `X-Request-ID` or generating a new UUIDv4) attached to `request.state.trace_id` and mirrored in the `X-Trace-ID` response header.
2. **RFC-7807 Problem Details**: All unhandled exceptions return a standardized RFC-7807 `application/problem+json` payload containing the generic error title, HTTP status, request path instance, and the corresponding `trace_id`.
3. **Internal SRE Logging**: Raw stack traces, error messages, and database contexts are securely logged to the internal application logger (`lex.api.errors` / Sentry / Loki) with the associated `trace_id`, enabling seamless operational debugging without exposing internals to external callers.

```python
# RFC-7807 Response Schema
{
    "type": "about:blank",
    "title": "Internal Database Error",
    "status": 500,
    "detail": "An internal database error occurred while processing the request. Please contact support with the trace_id.",
    "instance": "/api/v1/legislation/...",
    "trace_id": "018f1a2b-3c4d-7e8f-9a0b-1c2d3e4f5a6b"
}
```

### Invariants:
1. **Zero Internal Leakage**: Internal SQL statements, table identifiers, and Python stack traces must never appear in HTTP response bodies.
2. **Deterministic Traceability**: Every 500 error response MUST include a valid `trace_id` in both the JSON payload and the `X-Trace-ID` HTTP header for correlation with SRE logs.

---

## 5. Future API & SRE Observability Backlog (Pending Phase Approval)

The following capabilities are cataloged as future enhancements. They are currently in draft/placeholder status and will not be implemented until explicit phase approval is granted:

| Item | Subsystem | Classification | Scope / Description | Approval Status |
| :--- | :--- | :--- | :--- | :--- |
| **API-BACKLOG-01** | Dependency Injection | Architectural Refactoring | Migrate from `app.dependency_overrides` to application-level state provider. | `PENDING_FUTURE_APPROVAL` |
| **API-BACKLOG-02** | HTTP Caching | Performance / Optimization | Implement `ETag` and `Cache-Control` headers for compiled statutes and time-travel queries. | `PENDING_FUTURE_APPROVAL` |
| **SRE-BACKLOG-01** | Telemetry / Metrics | Golden Signals | Add `/metrics` endpoint exporting Prometheus Prometheus Golden Signals (Latency, Traffic, Errors, Saturation). | `PENDING_FUTURE_APPROVAL` |
| **SRE-BACKLOG-02** | Structured Logging | Observability | Integrate structured JSON logging formatters formatted for Grafana Loki ingestion. | `PENDING_FUTURE_APPROVAL` |
| **SRE-BACKLOG-03** | Error Tracing | Observability | Integrate Sentry distributed tracing SDK with automatic `trace_id` tag capture. | `PENDING_FUTURE_APPROVAL` |
