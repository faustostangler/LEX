"""LC 95/1998 Abstract Syntax Tree (AST) Segmenter for Legislative Acts.

Parses raw Brazilian legislative and normative text into a strictly validated
hierarchical AST (Articles -> Paragraphs -> Incisos -> Alíneas -> Items).
"""

import re
from uuid import UUID

from lex.treatment.domain.entities import ActAst, DispositivoNode
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    DispositivoType,
)

# Hoisted compiled regex constants for provision labels
RE_ARTICLE = re.compile(
    r"^[Aa]rt\.\s*(\d+)(?:[ºo\.]|\.º)?(?:-([A-Za-z]{1,2}))?\.?\s*(.*)$",
    re.IGNORECASE,
)
RE_PARAGRAPH = re.compile(
    r"^(?:§\s*(\d+)(?:[ºo\.]|\.º)?(?:-([A-Za-z]{1,2}))?|([Pp]ar[áa]grafo\s+[úu]nico|PARÁGRAFO\s+ÚNICO))\.?\s*(.*)$",
    re.IGNORECASE,
)
RE_INCISO = re.compile(
    r"^([IVXLCDM]+)\s*[-–\.]\s*(.*)$",
)
RE_ALINEA = re.compile(
    r"^([a-z])\s*[\)\-]\s*(.*)$",
)
RE_ITEM = re.compile(
    r"^(\d+)\s*[\.\-]\s*(.*)$",
)

ROMAN_VALS: dict[str, int] = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def _roman_to_int(roman_str: str) -> int:
    """Converts a Roman numeral string into an integer."""
    roman = roman_str.upper().strip()
    total = 0
    prev = 0
    for char in reversed(roman):
        val = ROMAN_VALS.get(char, 0)
        if val < prev:
            total -= val
        else:
            total += val
            prev = val
    return total if total > 0 else 1


class ActSegmenter:
    """Deterministic segmenter converting legislative text into an ActAst tree."""

    @classmethod
    def segment_text(
        cls,
        raw_text: str,
        title: str,
        ementa: str | None = None,
        act_id: UUID | None = None,
        canonical_urn: str | None = None,
    ) -> ActAst:
        """Parses raw text into an ActAst aggregate root.

        Args:
            raw_text: Plain text of the legislative act.
            title: Title of the act.
            ementa: Optional summary / ementa.
            act_id: Optional UUID of the parent normative act.
            canonical_urn: Optional canonical LexML URN.

        Returns:
            A structured ActAst tree.
        """
        lines = [line.strip() for line in raw_text.splitlines()]
        root_nodes: list[DispositivoNode] = []

        current_art: DispositivoNode | None = None
        current_par: DispositivoNode | None = None
        current_inc: DispositivoNode | None = None
        current_ali: DispositivoNode | None = None
        current_active: DispositivoNode | None = None

        for line in lines:
            if not line:
                continue

            # 1. Check Article
            m_art = RE_ARTICLE.match(line)
            if m_art:
                num = m_art.group(1)
                suffix = m_art.group(2)
                rest = m_art.group(3).strip()
                art_code = f"art_{num}"
                if suffix:
                    art_code += f"_{suffix.lower()}"

                label = f"Art. {num}º" if int(num) <= 9 and not suffix else f"Art. {num}"
                if suffix:
                    label += f"-{suffix.upper()}"
                label += "."

                node = DispositivoNode(
                    node_path=CanonicalNodePath.from_string(art_code),
                    node_type=DispositivoType.ARTIGO,
                    label=label,
                    text=rest,
                )
                root_nodes.append(node)
                current_art = node
                current_par = None
                current_inc = None
                current_ali = None
                current_active = node
                continue

            if current_art is None:
                # Header lines before the first article (e.g. preambles, formulas)
                continue

            # 2. Check Paragraph
            m_par = RE_PARAGRAPH.match(line)
            if m_par:
                num = m_par.group(1)
                par_suffix = m_par.group(2)
                is_unico = bool(m_par.group(3))
                rest = (m_par.group(4) or "").strip()

                if is_unico or not num:
                    par_code = f"{current_art.node_path.value}.par_unico"
                    label = "Parágrafo único."
                    node_type = DispositivoType.PARAGRAFO_UNICO
                else:
                    par_code = f"{current_art.node_path.value}.par_{num}"
                    if par_suffix:
                        par_code += f"_{par_suffix.lower()}"
                    label = f"§ {num}º" if int(num) <= 9 and not par_suffix else f"§ {num}"
                    if par_suffix:
                        label += f"-{par_suffix.upper()}"
                    label += "."
                    node_type = DispositivoType.PARAGRAFO

                node = DispositivoNode(
                    node_path=CanonicalNodePath.from_string(par_code),
                    node_type=node_type,
                    label=label,
                    text=rest,
                )
                current_art.add_child(node)
                current_par = node
                current_inc = None
                current_ali = None
                current_active = node
                continue

            # 3. Check Inciso (Clause)
            m_inc = RE_INCISO.match(line)
            if m_inc:
                roman = m_inc.group(1).upper()
                rest = m_inc.group(2).strip()
                inc_num = _roman_to_int(roman)

                parent = current_par if current_par is not None else current_art
                inc_code = f"{parent.node_path.value}.inc_{inc_num}"
                label = f"{roman} -"

                node = DispositivoNode(
                    node_path=CanonicalNodePath.from_string(inc_code),
                    node_type=DispositivoType.INCISO,
                    label=label,
                    text=rest,
                )
                parent.add_child(node)
                current_inc = node
                current_ali = None
                current_active = node
                continue

            # 4. Check Alínea
            m_ali = RE_ALINEA.match(line)
            if m_ali and (current_inc is not None or current_par is not None):
                letter = m_ali.group(1).lower()
                rest = m_ali.group(2).strip()

                parent_node = current_inc if current_inc is not None else current_par
                if parent_node is None:
                    continue
                ali_code = f"{parent_node.node_path.value}.ali_{letter}"
                label = f"{letter})"

                node = DispositivoNode(
                    node_path=CanonicalNodePath.from_string(ali_code),
                    node_type=DispositivoType.ALINEA,
                    label=label,
                    text=rest,
                )
                parent_node.add_child(node)
                current_ali = node
                current_active = node
                continue

            # 5. Check Item
            m_item = RE_ITEM.match(line)
            if m_item and current_ali is not None:
                item_num = m_item.group(1)
                rest = m_item.group(2).strip()

                item_code = f"{current_ali.node_path.value}.item_{item_num}"
                label = f"{item_num}."

                node = DispositivoNode(
                    node_path=CanonicalNodePath.from_string(item_code),
                    node_type=DispositivoType.ITEM,
                    label=label,
                    text=rest,
                )
                current_ali.add_child(node)
                current_active = node
                continue

            # 6. Continuation line for the most specific active provision
            if current_active is not None:
                current_active.text = (
                    f"{current_active.text} {line}".strip() if current_active.text else line
                )

        return ActAst(
            act_id=act_id,
            canonical_urn=canonical_urn,
            title=title,
            ementa=ementa,
            nodes=root_nodes,
        )
