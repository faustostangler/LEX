"""Unit tests for StubHandler and Out-of-Order JIT Backfill Prioritization.

Tests Stub creation, citation counting, and hydration event triggering.
"""

from lex.consolidation.domain.events import NormativeActHydrated
from lex.consolidation.domain.services.stub_handler import StubHandler
from lex.consolidation.domain.value_objects import CanonicalUrn
from lex.shared_kernel.value_objects import (
    HierarchicalGroup,
    PublicationNature,
)


class TestStubHandler:
    """Test suite for Out-of-Order StubHandler."""

    def test_create_stub_and_backfill_task(self) -> None:
        """Asserts creation of a valid Stub NormativeAct and JIT backfill task."""
        urn = CanonicalUrn.from_string("urn:lex:br:federal:lei:1993;8666")

        stub_act, backfill_task = StubHandler.create_stub_and_task(
            canonical_urn=urn,
            territory_id="BR",
            act_type="Lei Ordinária",
            act_number="8666",
            act_year=1993,
        )

        assert stub_act.is_stub is True
        assert stub_act.canonical_urn == urn.value
        assert stub_act.act_number == "8666"
        assert stub_act.act_year == 1993
        assert stub_act.title == "Lei Ordinária nº 8666/1993"
        assert stub_act.hierarchical_group == HierarchicalGroup.GRUPO_1_PRIMARIO
        assert stub_act.publication_nature == PublicationNature.NORMATIVA_ABSTRATA

        assert backfill_task.canonical_urn == urn
        assert backfill_task.citation_count == 1
        assert backfill_task.status == "PENDING"

    def test_hydrate_stub_act_and_emit_event(self) -> None:
        """Asserts hydration of a stub act and creation of the NormativeActHydrated domain event."""
        urn = CanonicalUrn.from_string("urn:lex:br:federal:lei:1993;8666")
        stub_act, _ = StubHandler.create_stub_and_task(
            canonical_urn=urn,
            territory_id="BR",
            act_type="Lei Ordinária",
            act_number="8666",
            act_year=1993,
        )

        genuine_text = """
        Art. 1º Esta Lei estabelece normas gerais sobre licitações e contratos administrativos.
        """

        hydrated_act, event = StubHandler.hydrate_stub(
            stub_act=stub_act,
            raw_content=genuine_text,
            source_url="https://www.planalto.gov.br/ccivil_03/leis/l8666.htm",
        )

        assert hydrated_act.is_stub is False
        assert hydrated_act.raw_content == genuine_text.strip()
        assert hydrated_act.char_count == len(genuine_text.strip())
        assert isinstance(event, NormativeActHydrated)
        assert event.canonical_urn == urn
        assert event.act_id == hydrated_act.id
