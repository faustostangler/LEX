"""Centralized Exception Handlers and RFC-7807 Error Responses for the LEX API.

NOTE (ADR-009 / Status: PENDING_FUTURE_APPROVAL):
Mitigates CWE-209 (Information Exposure Through an Error Message) by ensuring that
unhandled database queries, internal server traces, and infrastructure details are
sanitized before transmission to HTTP clients, while preserving structured diagnostic
telemetry (trace_id / correlation_id) for internal SRE log aggregation. Active production
SRE routing is deferred pending explicit future phase approval.
"""

import logging
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = logging.getLogger("lex.api.errors")


def _get_or_create_trace_id(request: Request) -> str:
    """Extracts existing trace_id from request state/headers or generates a new UUIDv4."""
    state_trace = getattr(request.state, "trace_id", None)
    if state_trace:
        return str(state_trace)

    header_trace = request.headers.get("X-Request-ID") or request.headers.get("X-Trace-ID")
    if header_trace:
        return header_trace

    return str(uuid.uuid4())


class TraceIdMiddleware(BaseHTTPMiddleware):
    """Middleware attaching a deterministic trace_id to incoming requests and outgoing responses."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        trace_id = _get_or_create_trace_id(request)
        request.state.trace_id = trace_id

        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        return response


def create_problem_details_response(
    status_code: int,
    title: str,
    detail: str,
    instance: str,
    trace_id: str,
    error_type: str = "about:blank",
    extra: dict[str, Any] | None = None,
) -> JSONResponse:
    """Constructs an RFC-7807 compliant problem details JSON response."""
    payload: dict[str, Any] = {
        "type": error_type,
        "title": title,
        "status": status_code,
        "detail": detail,
        "instance": instance,
        "trace_id": trace_id,
    }
    if extra:
        payload.update(extra)

    return JSONResponse(
        status_code=status_code,
        content=payload,
        media_type="application/problem+json",
        headers={"X-Trace-ID": trace_id},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registers global exception handlers for SQLAlchemyError and generic unhandled exceptions."""

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError,
    ) -> JSONResponse:
        trace_id = _get_or_create_trace_id(request)
        logger.error(
            "Database exception occurred on path '%s' [trace_id=%s]: %s",
            request.url.path,
            trace_id,
            exc,
            exc_info=True,
        )
        return create_problem_details_response(
            status_code=500,
            title="Internal Database Error",
            detail=(
                "An internal database error occurred while processing the request. "
                "Please contact support with the trace_id."
            ),
            instance=request.url.path,
            trace_id=trace_id,
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        trace_id = _get_or_create_trace_id(request)
        logger.error(
            "Unhandled server exception occurred on path '%s' [trace_id=%s]: %s",
            request.url.path,
            trace_id,
            exc,
            exc_info=True,
        )
        return create_problem_details_response(
            status_code=500,
            title="Internal Server Error",
            detail=(
                "An unexpected internal server error occurred. "
                "Please contact support with the trace_id."
            ),
            instance=request.url.path,
            trace_id=trace_id,
        )
