# API & Web Security Hardening Guide (LEX)

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
