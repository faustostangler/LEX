# MITRE CWE-1000: Research Concepts View & Defensive Architecture Guide

Source: [MITRE Common Weakness Enumeration - CWE-1000 (Research Concepts)](https://cwe.mitre.org/data/definitions/1000.html)

## 1. Executive Summary & Purpose
**CWE-1000 (Research Concepts)** is the foundational, top-down taxonomic view of software weaknesses. Unlike superficial vulnerability lists or operational snapshots (e.g., OWASP Top 10), CWE-1000 categorizes all software flaws based on fundamental architectural abstractions, behaviors, state transitions, and boundaries.

In the **Doctor Stangler Architecture Method**, CWE-1000 serves as the primary threat modeling catalog and defensive engineering standard across all development phases:
1. **Phase 1 (Stereoscopy - ADR)**: Architectural risk identification and trust boundary threat modeling.
2. **Phase 2 (Refractometry - Specs)**: Negative testing, boundary invariant definitions, and exception mapping.
3. **Phase 3 (Surgery - TDD)**: Secure coding, construction-time Value Object validation, and safe serialization.
4. **Phase 4 (Treatment - Quality Gate)**: Automated SAST scanning (`ruff check --select S`, Bandit, Snyk) to eliminate weakness survivors.

---

## 2. Core Weakness Pillars & Architectural Mitigations

### 2.1 Improper Input Validation & Type Confusion (CWE-20, CWE-1287)
- **Conceptual Flaw**: Processing untrusted input without validating type, length, range, syntax, or invariants.
- **Architectural Mitigations**:
  - **Value Objects**: Every business concept (e.g. `ActId`, `ArticleNumber`, `DateRange`) is wrapped in a dedicated Value Object with construction-time validation.
  - **Eliminate Primitive Obsession**: Raw `str`, `int`, or `float` are prohibited in domain signatures.
  - **Fail-Fast Invariants**: Construction of entities with invalid data raises immediate domain validation exceptions (`ValueError`, `DomainValidationError`).

### 2.2 Injections & Neutralization Flaws (CWE-74, CWE-89, CWE-78, CWE-116)
- **Conceptual Flaw**: Embedding untrusted input directly into structured command or query interpreters (SQL, Shell, HTML/Templates).
- **Architectural Mitigations**:
  - **Parameterized Queries**: Restrict database persistence to parameterized ORM/Core adapters (SQLAlchemy) in `infrastructure/`.
  - **Prohibit Raw Shell Concatenation**: Ban `shell=True` with user input.
  - **Presentation Boundary Sanitization**: Output escaping and content negotiation at the Presentation layer.

### 2.3 Deserialization of Untrusted Data (CWE-502)
- **Conceptual Flaw**: Deserializing untrusted object graphs using execution-capable serialization formats.
- **Architectural Mitigations**:
  - **Safe Binary/Data Serialization**: Use PyArrow IPC (Feather) or JSON/Pydantic schemas.
  - **Ban `pickle`**: Strictly prohibit Python `pickle` across network boundaries, file stores, and caching layers.
  - **Anti-Corruption Layer (ACL)**: All external payloads are intercepted and sanitized before entering the domain.

### 2.4 Broken Access Control & Privilege Management (CWE-285, CWE-863, CWE-250)
- **Conceptual Flaw**: Missing or flawed authorization checks at use case boundaries or running processes with root privileges.
- **Architectural Mitigations**:
  - **Application Use Case Policies**: Authorization policies (RBAC/ABAC) evaluated at the Application port.
  - **Least Privilege Containers**: Docker images run as unprivileged non-root users (UID > 1000) using Distroless/Alpine.

### 2.5 State Management, Concurrency & Race Conditions (CWE-362, CWE-662)
- **Conceptual Flaw**: Insecure shared mutable state across asynchronous coroutines, threads, or distributed systems.
- **Architectural Mitigations**:
  - **Eventual Consistency & Domain Events**: Inter-context communication via domain events.
  - **Transactional Outbox Pattern**: Atomic persistence of state mutations and events to avoid split-brain states.
  - **Idempotency Keys**: Unique event identifiers to prevent duplicate processing on at-least-once delivery.

### 2.6 Sensitive Data Exposure & Information Leakage (CWE-200, CWE-209, CWE-359)
- **Conceptual Flaw**: Emitting PII, database connection strings, or system stack traces into logs or client responses.
- **Architectural Mitigations**:
  - **LGPD/PII Redaction**: Automatic scrubbing of sensitive fields in telemetry (Sentry, Prometheus, Loki).
  - **Centralized Configuration**: All credentials stored in `.env` validated by `pydantic-settings` (`config.py`).
  - **Humble Presentation Objects**: Standardized error responses that hide internal infrastructure diagnostics.

### 2.7 Reliance on Vulnerable Third-Party Components (CWE-1395)
- **Conceptual Flaw**: Using vulnerable or unpinned third-party libraries.
- **Architectural Mitigations**:
  - **Deterministic Lockfiles**: `uv.lock` for reproducible dependency trees.
  - **Automated Security Scanning**: Real-time scanning with Snyk and SAST tools.

---

## 3. Threat Modeling Checklist by Phase

| Phase | Agent Role | CWE-1000 Activity |
|-------|------------|-------------------|
| **Phase 1** | **Stereoscopy** | Map attack surfaces, trust boundaries, and identify relevant CWE weakness categories in the ADR. |
| **Phase 2** | **Refractometry** | Specify negative test cases, adversarial boundary assertions, and exception mappings. |
| **Phase 3** | **Surgery** | Implement Value Object invariants, parameterized queries, ACL translators, and safe serializers. |
| **Phase 4** | **Treatment** | Run SAST security checks (`ruff check --select S`, Bandit, Snyk) with 0 allowed vulnerabilities. |
| **Grilling** | **Laser** | Challenge architecture decisions against Chapters 02 (AppSec) and 11 (Container/Infra Security). |
