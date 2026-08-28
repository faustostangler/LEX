"""Precision Unit Tests for PdfStreamTextExtractor.

Verifies in-memory stream processing, empty/corrupted payload error handling,
and ephemeral spooling boundaries specified in SPEC-001 (Section 4 Scenario 1).
"""

import io

import pytest
from pypdf import PdfWriter

from lex.ingestion.domain.exceptions import CorruptedGazettePayloadError
from lex.ingestion.infrastructure.adapters.stream_extractor import PdfStreamTextExtractor


def create_synthetic_pdf(num_pages: int = 1) -> bytes:
    """Helper to generate a valid PDF byte stream in memory without disk files."""
    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


class TestPdfStreamTextExtractor:
    """Acceptance tests for PdfStreamTextExtractor."""

    def test_extract_text_from_valid_pdf_stream(self) -> None:
        """Scenario: Extract text from valid in-memory PDF stream."""
        pdf_bytes = create_synthetic_pdf(num_pages=2)
        extractor = PdfStreamTextExtractor()
        extracted = extractor.extract_text(pdf_bytes)
        assert isinstance(extracted, str)

    def test_extract_text_from_empty_bytes_raises(self) -> None:
        """Boundary condition: Empty byte stream raises CorruptedGazettePayloadError."""
        extractor = PdfStreamTextExtractor()
        with pytest.raises(CorruptedGazettePayloadError, match="Empty byte stream"):
            extractor.extract_text(b"")

    def test_extract_text_from_corrupted_bytes_raises(self) -> None:
        """Boundary condition: Non-PDF garbage raises CorruptedGazettePayloadError."""
        extractor = PdfStreamTextExtractor()
        garbage = b"NOT_A_REAL_PDF_HEADER_12345"
        with pytest.raises(CorruptedGazettePayloadError, match="Failed to parse PDF stream"):
            extractor.extract_text(garbage)

    def test_extract_text_with_spool_fallback(self) -> None:
        """Scenario: Oversized payloads (> max_spool_mb) trigger spooling without error."""
        pdf_bytes = create_synthetic_pdf(num_pages=3)
        extractor = PdfStreamTextExtractor()
        # Force spool fallback with tiny max_spool_mb=0
        extracted = extractor.extract_text(pdf_bytes, max_spool_mb=0)
        assert isinstance(extracted, str)
