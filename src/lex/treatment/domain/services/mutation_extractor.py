"""LC 95/1998 Mutation Extractor for Legislative Amendments.

Extracts atomic legislative patch deltas (ALTERACAO_NR, REVOGACAO_EXPRESSA, ACRESCIMO)
from amending statutes and prepares them for the CQRS Mutation Ledger.
"""

import re
import uuid
from uuid import UUID

from lex.ingestion.domain.value_objects import DocumentHash, GazetteDate
from lex.treatment.domain.entities import NormativeActMutation
from lex.treatment.domain.services.act_segmenter import _roman_to_int
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    MutationType,
)

# Hoisted compiled regex constants
RE_ALTERATION_HEADER = re.compile(
    r"[Aa]rt\.\s*\d+[ºo]?\s+(?:O|A|Os|As)?\s*(Lei|Decreto|Medida\s+Provisória|Portaria|Resolução)"
    r"(?:\s+Complementar)?\s+(?:n[ºo°\.]?\s*)?([\d\.]+)"
    r"(?:[,\s/]+(?:de\s+)?(?:[\w\s]+(?:de\s+)?)?(\d{4}))?,?\s+passa[m]?\s+a\s+vigorar\s+com\s+a[s]?\s+seguinte[s]?\s+alteraç[ãõ]e[s]?:?",
    re.IGNORECASE,
)

RE_QUOTED_ARTICLE = re.compile(
    r'["“\']?\s*[Aa]rt\.\s*(\d+)(?:[ºo\.]|\.º)?(?:-([A-Za-z]{1,2}))?\.?\s*(.*)$',
    re.IGNORECASE,
)

RE_QUOTED_PARAGRAPH = re.compile(
    r'["“\']?\s*(?:§\s*(\d+)(?:[ºo\.]|\.º)?(?:-([A-Za-z]{1,2}))?|([Pp]ar[áa]grafo\s+[úu]nico|PARÁGRAFO\s+ÚNICO))\.?\s*(.*)$',
    re.IGNORECASE,
)

RE_QUOTED_INCISO = re.compile(
    r'["“\']?\s*([IVXLCDM]+)\s*[-–\.]\s*(.*)$',
)

RE_NR_MARKER = re.compile(
    r"\s*\(NR\)\s*[\"”\']?$",
    re.IGNORECASE,
)

RE_EXPRESS_REVOCATION_LINE = re.compile(
    r"[Rr]evoga[m]?\s*-\s*se\s+(?:expressamente\s+)?(.+)",
    re.IGNORECASE,
)

RE_REVOKE_ART = re.compile(
    r"[oa]s?\s+art(?:igo)?s?\.\s*(\d+)(?:[ºo\.]|\.º)?(?:-([A-Za-z]{1,2}))?",
    re.IGNORECASE,
)

RE_REVOKE_INCISOS = re.compile(
    r"[oa]s?\s+incisos?\s+([IVXLCDM\s,e–\-]+)\s+do\s+(?:caput\s+do\s+)?art(?:igo)?\.\s*(\d+)",
    re.IGNORECASE,
)


class MutationExtractor:
    """Deterministic extractor for statutory amendments and express revocations."""

    @classmethod
    def extract_mutations(
        cls,
        raw_text: str,
        author_act_id: UUID,
        publication_date: GazetteDate,
        effective_date: GazetteDate,
        target_act_id: UUID | None = None,
        default_territory_id: str = "BR",
    ) -> list[NormativeActMutation]:
        """Parses amending text and returns all extracted NormativeActMutation items.

        Args:
            raw_text: Full text of the amending statute.
            author_act_id: UUID of the amending act.
            publication_date: Publication date of the amending act.
            effective_date: Effective date of the amending act.
            target_act_id: Optional UUID of target act if already resolved.
            default_territory_id: Territory code fallback.

        Returns:
            List of validated NormativeActMutation entities.
        """
        resolved_target_id = target_act_id or uuid.uuid5(
            uuid.NAMESPACE_DNS, f"{default_territory_id}:target_placeholder"
        )
        mutations: list[NormativeActMutation] = []
        lines = [line.strip() for line in raw_text.splitlines()]

        in_alteration_block = False
        current_art_code: str | None = None
        current_par_code: str | None = None

        for line in lines:
            if not line:
                continue

            # 1. Check for express revocations
            if "revoga-se" in line.lower() or "revogam-se" in line.lower():
                m_rev_inc = RE_REVOKE_INCISOS.search(line)
                if m_rev_inc:
                    incisos_str = m_rev_inc.group(1)
                    art_num = m_rev_inc.group(2)
                    # Extract Roman numerals
                    romans = re.findall(r"\b[IVXLCDM]+\b", incisos_str.upper())
                    for roman in romans:
                        inc_num = _roman_to_int(roman)
                        node_path_str = f"art_{art_num}.inc_{inc_num}"
                        mut_hash = DocumentHash.from_text(
                            f"REVOGACAO_EXPRESSA:{node_path_str}:{author_act_id}"
                        )
                        mutations.append(
                            NormativeActMutation(
                                target_act_id=resolved_target_id,
                                target_node_path=CanonicalNodePath.from_string(node_path_str),
                                author_act_id=author_act_id,
                                mutation_type=MutationType.REVOGACAO_EXPRESSA,
                                new_text=None,
                                publication_date=publication_date,
                                effective_date=effective_date,
                                extraction_source="lc95_deterministic_regex",
                                confidence_score=1.0,
                                mutation_sha256=mut_hash,
                            )
                        )
                    continue

                m_rev_art = RE_REVOKE_ART.search(line)
                if m_rev_art:
                    art_num = m_rev_art.group(1)
                    suffix = m_rev_art.group(2)
                    art_code = f"art_{art_num}"
                    if suffix:
                        art_code += f"_{suffix.lower()}"
                    mut_hash = DocumentHash.from_text(
                        f"REVOGACAO_EXPRESSA:{art_code}:{author_act_id}"
                    )
                    mutations.append(
                        NormativeActMutation(
                            target_act_id=resolved_target_id,
                            target_node_path=CanonicalNodePath.from_string(art_code),
                            author_act_id=author_act_id,
                            mutation_type=MutationType.REVOGACAO_EXPRESSA,
                            new_text=None,
                            publication_date=publication_date,
                            effective_date=effective_date,
                            extraction_source="lc95_deterministic_regex",
                            confidence_score=1.0,
                            mutation_sha256=mut_hash,
                        )
                    )
                    continue

            # 2. Check for alteration header
            if RE_ALTERATION_HEADER.search(line):
                in_alteration_block = True
                current_art_code = None
                current_par_code = None
                continue

            if in_alteration_block:
                # Check for article anchor in quoted section
                m_art = RE_QUOTED_ARTICLE.match(line)
                if m_art:
                    num = m_art.group(1)
                    suffix = m_art.group(2)
                    current_art_code = f"art_{num}"
                    if suffix:
                        current_art_code += f"_{suffix.lower()}"
                    current_par_code = None
                    rest = m_art.group(3).strip()
                    if RE_NR_MARKER.search(rest):
                        mut_hash = DocumentHash.from_text(f"ALTERACAO_NR:{current_art_code}:{rest}")
                        mutations.append(
                            NormativeActMutation(
                                target_act_id=resolved_target_id,
                                target_node_path=CanonicalNodePath.from_string(current_art_code),
                                author_act_id=author_act_id,
                                mutation_type=MutationType.ALTERACAO_NR,
                                new_text=rest,
                                publication_date=publication_date,
                                effective_date=effective_date,
                                extraction_source="lc95_deterministic_regex",
                                confidence_score=1.0,
                                mutation_sha256=mut_hash,
                            )
                        )
                    continue

                # Check for paragraph in quoted section
                m_par = RE_QUOTED_PARAGRAPH.match(line)
                if m_par and current_art_code is not None:
                    num = m_par.group(1)
                    par_suffix = m_par.group(2)
                    is_unico = bool(m_par.group(3))
                    rest = (m_par.group(4) or "").strip()

                    if is_unico or not num:
                        current_par_code = f"{current_art_code}.par_unico"
                    else:
                        current_par_code = f"{current_art_code}.par_{num}"
                        if par_suffix:
                            current_par_code += f"_{par_suffix.lower()}"

                    if RE_NR_MARKER.search(rest):
                        mut_hash = DocumentHash.from_text(f"ALTERACAO_NR:{current_par_code}:{rest}")
                        mutations.append(
                            NormativeActMutation(
                                target_act_id=resolved_target_id,
                                target_node_path=CanonicalNodePath.from_string(current_par_code),
                                author_act_id=author_act_id,
                                mutation_type=MutationType.ALTERACAO_NR,
                                new_text=rest,
                                publication_date=publication_date,
                                effective_date=effective_date,
                                extraction_source="lc95_deterministic_regex",
                                confidence_score=1.0,
                                mutation_sha256=mut_hash,
                            )
                        )
                    continue

                # Check for inciso in quoted section
                m_inc = RE_QUOTED_INCISO.match(line)
                if m_inc and current_art_code is not None:
                    roman = m_inc.group(1).upper()
                    rest = m_inc.group(2).strip()
                    inc_num = _roman_to_int(roman)

                    parent = current_par_code if current_par_code is not None else current_art_code
                    inc_code = f"{parent}.inc_{inc_num}"

                    if RE_NR_MARKER.search(rest):
                        mut_hash = DocumentHash.from_text(f"ALTERACAO_NR:{inc_code}:{rest}")
                        mutations.append(
                            NormativeActMutation(
                                target_act_id=resolved_target_id,
                                target_node_path=CanonicalNodePath.from_string(inc_code),
                                author_act_id=author_act_id,
                                mutation_type=MutationType.ALTERACAO_NR,
                                new_text=rest,
                                publication_date=publication_date,
                                effective_date=effective_date,
                                extraction_source="lc95_deterministic_regex",
                                confidence_score=1.0,
                                mutation_sha256=mut_hash,
                            )
                        )
                    continue

        return mutations
