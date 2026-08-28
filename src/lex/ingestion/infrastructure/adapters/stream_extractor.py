"""In-Memory PDF and Stream Text Extractor Adapter.

Implements StreamTextExtractorPort to extract plain text from in-memory byte streams
using io.BytesIO and pypdf with SpooledTemporaryFile fallback for oversized streams,
guaranteeing zero permanent binary retention on disk.
"""

import io
import tempfile

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from lex.ingestion.application.ports import StreamTextExtractorPort
from lex.ingestion.domain.exceptions import CorruptedGazettePayloadError


class PdfStreamTextExtractor(StreamTextExtractorPort):
    """Extracts text content from PDF binary streams in memory."""

    def extract_text(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes and threshold_bytes > 0:
                reader = PdfReader(io.BytesIO(stream_bytes))
                return self._extract_pages(reader)

            with tempfile.SpooledTemporaryFile(max_size=threshold_bytes) as spool:
                spool.write(stream_bytes)
                spool.seek(0)
                reader = PdfReader(spool)
                return self._extract_pages(reader)

        except (PdfReadError, ValueError, OSError) as exc:
            raise CorruptedGazettePayloadError(f"Failed to parse PDF stream: {exc}") from exc
        except Exception as exc:
            raise CorruptedGazettePayloadError(
                f"Failed to parse PDF stream due to unexpected error: {exc}"
            ) from exc

    @staticmethod
    def _extract_pages(reader: PdfReader) -> str:
        """Extract text from all pages in a PdfReader instance."""
        extracted_pages: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)
        return "\n\n".join(extracted_pages).strip()
