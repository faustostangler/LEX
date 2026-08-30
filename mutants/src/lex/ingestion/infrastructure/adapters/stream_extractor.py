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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPdfStreamTextExtractorǁ_extract_pages__mutmut: MutantDict = {}  # type: ignore


class PdfStreamTextExtractor(StreamTextExtractorPort):
    """Extracts text content from PDF binary streams in memory."""

    @_mutmut_mutated(mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut)
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_orig(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_1(self, stream_bytes: bytes, max_spool_mb: int = 11) -> str:
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_2(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if stream_bytes:
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_3(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError(None)

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_4(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("XXEmpty byte stream provided for PDF extraction.XX")

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_5(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("empty byte stream provided for pdf extraction.")

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_6(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("EMPTY BYTE STREAM PROVIDED FOR PDF EXTRACTION.")

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_7(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = None

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_8(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 / 1024

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_9(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb / 1024 * 1024

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_10(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1025 * 1024

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_11(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1025

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_12(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes or threshold_bytes > 0:
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_13(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) < threshold_bytes and threshold_bytes > 0:
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_14(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes and threshold_bytes >= 0:
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_15(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes and threshold_bytes > 1:
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_16(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes and threshold_bytes > 0:
                reader = None
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_17(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes and threshold_bytes > 0:
                reader = PdfReader(None)
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_18(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes and threshold_bytes > 0:
                reader = PdfReader(io.BytesIO(None))
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_19(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes and threshold_bytes > 0:
                reader = PdfReader(io.BytesIO(stream_bytes))
                return self._extract_pages(None)

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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_20(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes and threshold_bytes > 0:
                reader = PdfReader(io.BytesIO(stream_bytes))
                return self._extract_pages(reader)

            with tempfile.SpooledTemporaryFile(max_size=None) as spool:
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

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_21(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract text from in-memory bytes with ephemeral spool fallback."""
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream provided for PDF extraction.")

        threshold_bytes = max_spool_mb * 1024 * 1024

        try:
            if len(stream_bytes) <= threshold_bytes and threshold_bytes > 0:
                reader = PdfReader(io.BytesIO(stream_bytes))
                return self._extract_pages(reader)

            with tempfile.SpooledTemporaryFile(max_size=threshold_bytes) as spool:
                spool.write(None)
                spool.seek(0)
                reader = PdfReader(spool)
                return self._extract_pages(reader)

        except (PdfReadError, ValueError, OSError) as exc:
            raise CorruptedGazettePayloadError(f"Failed to parse PDF stream: {exc}") from exc
        except Exception as exc:
            raise CorruptedGazettePayloadError(
                f"Failed to parse PDF stream due to unexpected error: {exc}"
            ) from exc

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_22(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
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
                spool.seek(None)
                reader = PdfReader(spool)
                return self._extract_pages(reader)

        except (PdfReadError, ValueError, OSError) as exc:
            raise CorruptedGazettePayloadError(f"Failed to parse PDF stream: {exc}") from exc
        except Exception as exc:
            raise CorruptedGazettePayloadError(
                f"Failed to parse PDF stream due to unexpected error: {exc}"
            ) from exc

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_23(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
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
                spool.seek(1)
                reader = PdfReader(spool)
                return self._extract_pages(reader)

        except (PdfReadError, ValueError, OSError) as exc:
            raise CorruptedGazettePayloadError(f"Failed to parse PDF stream: {exc}") from exc
        except Exception as exc:
            raise CorruptedGazettePayloadError(
                f"Failed to parse PDF stream due to unexpected error: {exc}"
            ) from exc

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_24(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
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
                reader = None
                return self._extract_pages(reader)

        except (PdfReadError, ValueError, OSError) as exc:
            raise CorruptedGazettePayloadError(f"Failed to parse PDF stream: {exc}") from exc
        except Exception as exc:
            raise CorruptedGazettePayloadError(
                f"Failed to parse PDF stream due to unexpected error: {exc}"
            ) from exc

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_25(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
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
                reader = PdfReader(None)
                return self._extract_pages(reader)

        except (PdfReadError, ValueError, OSError) as exc:
            raise CorruptedGazettePayloadError(f"Failed to parse PDF stream: {exc}") from exc
        except Exception as exc:
            raise CorruptedGazettePayloadError(
                f"Failed to parse PDF stream due to unexpected error: {exc}"
            ) from exc

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_26(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
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
                return self._extract_pages(None)

        except (PdfReadError, ValueError, OSError) as exc:
            raise CorruptedGazettePayloadError(f"Failed to parse PDF stream: {exc}") from exc
        except Exception as exc:
            raise CorruptedGazettePayloadError(
                f"Failed to parse PDF stream due to unexpected error: {exc}"
            ) from exc

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_27(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
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
            raise CorruptedGazettePayloadError(None) from exc
        except Exception as exc:
            raise CorruptedGazettePayloadError(
                f"Failed to parse PDF stream due to unexpected error: {exc}"
            ) from exc

    def xǁPdfStreamTextExtractorǁextract_text__mutmut_28(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
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
                None
            ) from exc

    @staticmethod
    @_mutmut_mutated(mutants_xǁPdfStreamTextExtractorǁ_extract_pages__mutmut)
    def _extract_pages(reader: PdfReader) -> str:
        """Extract text from all pages in a PdfReader instance."""
        extracted_pages: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)
        return "\n\n".join(extracted_pages).strip()

    @staticmethod
    def xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_orig(reader: PdfReader) -> str:
        """Extract text from all pages in a PdfReader instance."""
        extracted_pages: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)
        return "\n\n".join(extracted_pages).strip()

    @staticmethod
    def xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_1(reader: PdfReader) -> str:
        """Extract text from all pages in a PdfReader instance."""
        extracted_pages: list[str] = None
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)
        return "\n\n".join(extracted_pages).strip()

    @staticmethod
    def xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_2(reader: PdfReader) -> str:
        """Extract text from all pages in a PdfReader instance."""
        extracted_pages: list[str] = []
        for page in reader.pages:
            page_text = None
            if page_text:
                extracted_pages.append(page_text)
        return "\n\n".join(extracted_pages).strip()

    @staticmethod
    def xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_3(reader: PdfReader) -> str:
        """Extract text from all pages in a PdfReader instance."""
        extracted_pages: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(None)
        return "\n\n".join(extracted_pages).strip()

    @staticmethod
    def xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_4(reader: PdfReader) -> str:
        """Extract text from all pages in a PdfReader instance."""
        extracted_pages: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)
        return "\n\n".join(None).strip()

    @staticmethod
    def xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_5(reader: PdfReader) -> str:
        """Extract text from all pages in a PdfReader instance."""
        extracted_pages: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)
        return "XX\n\nXX".join(extracted_pages).strip()

mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['_mutmut_orig'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_1'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_2'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_3'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_4'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_5'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_6'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_7'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_8'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_9'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_10'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_11'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_12'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_13'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_14'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_15'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_16'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_17'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_18'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_19'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_20'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_21'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_22'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_23'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_24'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_25'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_26'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_27'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁextract_text__mutmut['xǁPdfStreamTextExtractorǁextract_text__mutmut_28'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁextract_text__mutmut_28 # type: ignore # mutmut generated

mutants_xǁPdfStreamTextExtractorǁ_extract_pages__mutmut['_mutmut_orig'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁ_extract_pages__mutmut['xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_1'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁ_extract_pages__mutmut['xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_2'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁ_extract_pages__mutmut['xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_3'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁ_extract_pages__mutmut['xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_4'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPdfStreamTextExtractorǁ_extract_pages__mutmut['xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_5'] = PdfStreamTextExtractor.xǁPdfStreamTextExtractorǁ_extract_pages__mutmut_5 # type: ignore # mutmut generated
