"""Pure AST Reducer for Legislative Delta Consolidation.

Implements the pure function:
reduce(BaseAST, [Mutations]) -> CompiledNormativeAct

Replays statutory mutations chronologically, enforces cascading subtree revocations,
and generates pre-rendered LZ4 TOAST HTML/Markdown read models.
"""

import hashlib
import uuid
from datetime import UTC, datetime

from lex.consolidation.domain.entities import CompiledNormativeAct
from lex.treatment.domain.entities import ActAst, DispositivoNode, NormativeActMutation
from lex.treatment.domain.value_objects import (
    DispositivoStatus,
    DispositivoType,
    MutationType,
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__cascade_revocation__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__cascade_revocation__mutmut)
def _cascade_revocation(node: DispositivoNode) -> None:
    """Recursively marks a provision node and all of its descendants as REVOKED."""
    node.status = DispositivoStatus.REVOKED
    for child in node.children:
        _cascade_revocation(child)


def x__cascade_revocation__mutmut_orig(node: DispositivoNode) -> None:
    """Recursively marks a provision node and all of its descendants as REVOKED."""
    node.status = DispositivoStatus.REVOKED
    for child in node.children:
        _cascade_revocation(child)


def x__cascade_revocation__mutmut_1(node: DispositivoNode) -> None:
    """Recursively marks a provision node and all of its descendants as REVOKED."""
    node.status = None
    for child in node.children:
        _cascade_revocation(child)


def x__cascade_revocation__mutmut_2(node: DispositivoNode) -> None:
    """Recursively marks a provision node and all of its descendants as REVOKED."""
    node.status = DispositivoStatus.REVOKED
    for child in node.children:
        _cascade_revocation(None)

mutants_x__cascade_revocation__mutmut['_mutmut_orig'] = x__cascade_revocation__mutmut_orig # type: ignore # mutmut generated
mutants_x__cascade_revocation__mutmut['x__cascade_revocation__mutmut_1'] = x__cascade_revocation__mutmut_1 # type: ignore # mutmut generated
mutants_x__cascade_revocation__mutmut['x__cascade_revocation__mutmut_2'] = x__cascade_revocation__mutmut_2 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__render_node_html__mutmut)
def _render_node_html(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


def x__render_node_html__mutmut_orig(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


def x__render_node_html__mutmut_1(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = None
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


def x__render_node_html__mutmut_2(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = None

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


def x__render_node_html__mutmut_3(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status != DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


def x__render_node_html__mutmut_4(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            None
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


def x__render_node_html__mutmut_5(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status != DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


def x__render_node_html__mutmut_6(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            None
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


def x__render_node_html__mutmut_7(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            None
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


def x__render_node_html__mutmut_8(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(None)

    return "\n".join(lines)


def x__render_node_html__mutmut_9(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(None))

    return "\n".join(lines)


def x__render_node_html__mutmut_10(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(None)


def x__render_node_html__mutmut_11(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML."""
    lines: list[str] = []
    node_id = node.node_path.value

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{node.label} {node.text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{node.label} {node.text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{node.label}</strong> {node.text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "XX\nXX".join(lines)

mutants_x__render_node_html__mutmut['_mutmut_orig'] = x__render_node_html__mutmut_orig # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_1'] = x__render_node_html__mutmut_1 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_2'] = x__render_node_html__mutmut_2 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_3'] = x__render_node_html__mutmut_3 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_4'] = x__render_node_html__mutmut_4 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_5'] = x__render_node_html__mutmut_5 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_6'] = x__render_node_html__mutmut_6 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_7'] = x__render_node_html__mutmut_7 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_8'] = x__render_node_html__mutmut_8 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_9'] = x__render_node_html__mutmut_9 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_10'] = x__render_node_html__mutmut_10 # type: ignore # mutmut generated
mutants_x__render_node_html__mutmut['x__render_node_html__mutmut_11'] = x__render_node_html__mutmut_11 # type: ignore # mutmut generated
mutants_x__render_node_markdown__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__render_node_markdown__mutmut)
def _render_node_markdown(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = []
    if node.status == DispositivoStatus.REVOKED:
        lines.append(f"~~{node.label} {node.text}~~")
    else:
        lines.append(f"**{node.label}** {node.text}")

    for child in node.children:
        lines.append(_render_node_markdown(child))

    return "\n".join(lines)


def x__render_node_markdown__mutmut_orig(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = []
    if node.status == DispositivoStatus.REVOKED:
        lines.append(f"~~{node.label} {node.text}~~")
    else:
        lines.append(f"**{node.label}** {node.text}")

    for child in node.children:
        lines.append(_render_node_markdown(child))

    return "\n".join(lines)


def x__render_node_markdown__mutmut_1(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = None
    if node.status == DispositivoStatus.REVOKED:
        lines.append(f"~~{node.label} {node.text}~~")
    else:
        lines.append(f"**{node.label}** {node.text}")

    for child in node.children:
        lines.append(_render_node_markdown(child))

    return "\n".join(lines)


def x__render_node_markdown__mutmut_2(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = []
    if node.status != DispositivoStatus.REVOKED:
        lines.append(f"~~{node.label} {node.text}~~")
    else:
        lines.append(f"**{node.label}** {node.text}")

    for child in node.children:
        lines.append(_render_node_markdown(child))

    return "\n".join(lines)


def x__render_node_markdown__mutmut_3(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = []
    if node.status == DispositivoStatus.REVOKED:
        lines.append(None)
    else:
        lines.append(f"**{node.label}** {node.text}")

    for child in node.children:
        lines.append(_render_node_markdown(child))

    return "\n".join(lines)


def x__render_node_markdown__mutmut_4(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = []
    if node.status == DispositivoStatus.REVOKED:
        lines.append(f"~~{node.label} {node.text}~~")
    else:
        lines.append(None)

    for child in node.children:
        lines.append(_render_node_markdown(child))

    return "\n".join(lines)


def x__render_node_markdown__mutmut_5(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = []
    if node.status == DispositivoStatus.REVOKED:
        lines.append(f"~~{node.label} {node.text}~~")
    else:
        lines.append(f"**{node.label}** {node.text}")

    for child in node.children:
        lines.append(None)

    return "\n".join(lines)


def x__render_node_markdown__mutmut_6(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = []
    if node.status == DispositivoStatus.REVOKED:
        lines.append(f"~~{node.label} {node.text}~~")
    else:
        lines.append(f"**{node.label}** {node.text}")

    for child in node.children:
        lines.append(_render_node_markdown(None))

    return "\n".join(lines)


def x__render_node_markdown__mutmut_7(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = []
    if node.status == DispositivoStatus.REVOKED:
        lines.append(f"~~{node.label} {node.text}~~")
    else:
        lines.append(f"**{node.label}** {node.text}")

    for child in node.children:
        lines.append(_render_node_markdown(child))

    return "\n".join(None)


def x__render_node_markdown__mutmut_8(node: DispositivoNode) -> str:
    """Renders an AST provision node and its children into standard Markdown."""
    lines: list[str] = []
    if node.status == DispositivoStatus.REVOKED:
        lines.append(f"~~{node.label} {node.text}~~")
    else:
        lines.append(f"**{node.label}** {node.text}")

    for child in node.children:
        lines.append(_render_node_markdown(child))

    return "XX\nXX".join(lines)

mutants_x__render_node_markdown__mutmut['_mutmut_orig'] = x__render_node_markdown__mutmut_orig # type: ignore # mutmut generated
mutants_x__render_node_markdown__mutmut['x__render_node_markdown__mutmut_1'] = x__render_node_markdown__mutmut_1 # type: ignore # mutmut generated
mutants_x__render_node_markdown__mutmut['x__render_node_markdown__mutmut_2'] = x__render_node_markdown__mutmut_2 # type: ignore # mutmut generated
mutants_x__render_node_markdown__mutmut['x__render_node_markdown__mutmut_3'] = x__render_node_markdown__mutmut_3 # type: ignore # mutmut generated
mutants_x__render_node_markdown__mutmut['x__render_node_markdown__mutmut_4'] = x__render_node_markdown__mutmut_4 # type: ignore # mutmut generated
mutants_x__render_node_markdown__mutmut['x__render_node_markdown__mutmut_5'] = x__render_node_markdown__mutmut_5 # type: ignore # mutmut generated
mutants_x__render_node_markdown__mutmut['x__render_node_markdown__mutmut_6'] = x__render_node_markdown__mutmut_6 # type: ignore # mutmut generated
mutants_x__render_node_markdown__mutmut['x__render_node_markdown__mutmut_7'] = x__render_node_markdown__mutmut_7 # type: ignore # mutmut generated
mutants_x__render_node_markdown__mutmut['x__render_node_markdown__mutmut_8'] = x__render_node_markdown__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut: MutantDict = {}  # type: ignore


class PureAstReducer:
    """Pure functional reduction engine compiling base statutes and delta mutations."""

    @classmethod
    @_mutmut_mutated(mutants_xǁPureAstReducerǁreduce__mutmut, is_classmethod = True)
    def reduce(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_orig(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_1(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = None

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_2(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(None)

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_3(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = None

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_4(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            None,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_5(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=None,
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_6(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_7(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_8(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: None,
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_9(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(None)),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_10(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id and "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_11(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "XXXX")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_12(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = None
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_13(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 1
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_14(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = ""

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_15(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = None
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_16(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(None)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_17(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = None

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_18(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type != MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_19(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None or mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_20(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_21(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_22(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        None
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_23(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "XXold_textXX": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_24(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "OLD_TEXT": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_25(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "XXmutation_idXX": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_26(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "MUTATION_ID": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_27(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(None) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_28(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "XXauthor_act_idXX": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_29(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "AUTHOR_ACT_ID": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_30(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(None),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_31(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "XXeffective_dateXX": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_32(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "EFFECTIVE_DATE": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_33(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(None),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_34(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = None
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_35(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = None
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_36(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count = 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_37(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count -= 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_38(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 2

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_39(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type != MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_40(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_41(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(None)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_42(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count = 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_43(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count -= 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_44(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 2

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_45(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type != MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_46(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_47(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = None
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_48(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_49(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(None) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_50(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = None
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_51(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=None,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_52(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=None,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_53(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=None,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_54(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=None,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_55(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=None,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_56(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_57(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_58(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_59(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_60(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_61(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref and mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_62(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_63(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(None)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_64(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(None)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_65(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count = 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_66(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count -= 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_67(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 2

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_68(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = None
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_69(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            None
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_70(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            2
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_71(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO or n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_72(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type != DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_73(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_74(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = None

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_75(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            None
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_76(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            2
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_77(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO or n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_78(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type != DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_79(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_80(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = None
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_81(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id and ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_82(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or "XXXX"}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_83(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(None)

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_84(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = None
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_85(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(None)

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_86(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(None)
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_87(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(None))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_88(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(None)

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_89(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(None))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_90(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append(None)
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_91(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("XX</div>XX")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_92(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</DIV>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_93(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = None
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_94(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(None)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_95(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "XX\nXX".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_96(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = None

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_97(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(None)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_98(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "XX\n\nXX".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_99(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = None

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_100(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(None).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_101(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode(None)).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_102(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("XXutf-8XX")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_103(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("UTF-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_104(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=None,
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_105(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=None,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_106(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=None,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_107(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=None,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_108(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=None,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_109(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=None,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_110(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=None,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_111(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=None,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_112(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=None,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_113(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=None,
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_114(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_115(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_116(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_117(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_118(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_119(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_120(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_121(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_122(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_123(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_124(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id and uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(UTC),
        )

    @classmethod
    def xǁPureAstReducerǁreduce__mutmut_125(
        cls,
        base_ast: ActAst,
        mutations: list[NormativeActMutation],
    ) -> CompiledNormativeAct:
        """Applies a stream of mutations to a base AST in chronological sequence.

        Args:
            base_ast: Original unmodified statutory AST tree.
            mutations: Collection of NormativeActMutation items targeting this statute.

        Returns:
            A materialized, pre-rendered CompiledNormativeAct entity.
        """
        # 1. Deep copy the base AST via dictionary serialization
        working_ast = ActAst.from_dict(base_ast.to_dict())

        # 2. Chronological ordering (effective_date, publication_date, id)
        sorted_mutations = sorted(
            mutations,
            key=lambda m: (m.effective_date.value, m.publication_date.value, str(m.id or "")),
        )

        applied_count = 0
        last_effective_date = None

        # 3. Apply mutations sequentially
        for mut in sorted_mutations:
            target_node = working_ast.find_node(mut.target_node_path)
            last_effective_date = mut.effective_date.value

            if mut.mutation_type == MutationType.ALTERACAO_NR:
                if target_node is not None and mut.new_text is not None:
                    target_node.history.append(
                        {
                            "old_text": target_node.text,
                            "mutation_id": str(mut.id) if mut.id else None,
                            "author_act_id": str(mut.author_act_id),
                            "effective_date": str(mut.effective_date.value),
                        }
                    )
                    target_node.text = mut.new_text
                    target_node.status = DispositivoStatus.MODIFIED_ACTIVE
                    applied_count += 1

            elif mut.mutation_type == MutationType.REVOGACAO_EXPRESSA:
                if target_node is not None:
                    _cascade_revocation(target_node)
                    applied_count += 1

            elif mut.mutation_type == MutationType.ACRESCIMO:
                if mut.new_text is not None:
                    parent_path = mut.target_node_path.parent_path
                    parent_node = working_ast.find_node(parent_path) if parent_path else None
                    new_node = DispositivoNode(
                        node_path=mut.target_node_path,
                        node_type=DispositivoType.INCISO,
                        label=mut.author_dispositivo_ref or mut.target_node_path.leaf_name,
                        text=mut.new_text,
                        status=DispositivoStatus.MODIFIED_ACTIVE,
                    )
                    if parent_node is not None:
                        parent_node.add_child(new_node)
                    else:
                        working_ast.nodes.append(new_node)
                    applied_count += 1

        # 4. Count active vs revoked articles
        active_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status != DispositivoStatus.REVOKED
        )
        revoked_arts = sum(
            1
            for n in working_ast.nodes
            if n.node_type == DispositivoType.ARTIGO and n.status == DispositivoStatus.REVOKED
        )

        # 5. Pre-render HTML and Markdown
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{base_ast.act_id or ""}">'
            f"<h1>{working_ast.title}</h1>"
        ]
        if working_ast.ementa:
            html_chunks.append(f'<p class="ementa"><em>{working_ast.ementa}</em></p>')

        md_chunks: list[str] = [f"# {working_ast.title}\n"]
        if working_ast.ementa:
            md_chunks.append(f"> {working_ast.ementa}\n")

        for root_node in working_ast.nodes:
            html_chunks.append(_render_node_html(root_node))
            md_chunks.append(_render_node_markdown(root_node))

        html_chunks.append("</div>")
        compiled_html = "\n".join(html_chunks)
        compiled_markdown = "\n\n".join(md_chunks)

        # 6. Deterministic version hash
        version_hash = hashlib.sha256(compiled_html.encode("utf-8")).hexdigest()

        return CompiledNormativeAct(
            act_id=base_ast.act_id or uuid.uuid4(),
            compiled_version_hash=version_hash,
            total_mutations_applied=applied_count,
            last_mutation_effective_date=last_effective_date,
            compiled_ast=working_ast,
            compiled_html=compiled_html,
            compiled_markdown=compiled_markdown,
            active_articles_count=active_arts,
            revoked_articles_count=revoked_arts,
            last_compiled_at=datetime.now(None),
        )

mutants_xǁPureAstReducerǁreduce__mutmut['_mutmut_orig'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_1'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_2'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_3'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_4'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_5'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_6'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_7'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_8'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_9'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_10'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_11'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_12'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_13'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_14'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_15'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_16'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_17'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_18'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_19'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_20'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_21'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_22'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_23'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_24'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_25'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_26'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_27'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_28'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_29'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_30'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_30 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_31'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_31 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_32'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_32 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_33'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_33 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_34'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_34 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_35'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_35 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_36'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_36 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_37'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_37 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_38'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_38 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_39'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_39 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_40'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_40 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_41'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_41 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_42'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_42 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_43'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_43 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_44'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_44 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_45'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_45 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_46'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_46 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_47'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_47 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_48'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_48 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_49'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_49 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_50'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_50 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_51'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_51 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_52'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_52 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_53'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_53 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_54'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_54 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_55'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_55 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_56'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_56 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_57'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_57 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_58'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_58 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_59'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_59 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_60'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_60 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_61'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_61 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_62'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_62 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_63'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_63 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_64'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_64 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_65'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_65 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_66'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_66 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_67'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_67 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_68'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_68 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_69'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_69 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_70'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_70 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_71'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_71 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_72'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_72 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_73'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_73 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_74'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_74 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_75'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_75 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_76'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_76 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_77'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_77 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_78'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_78 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_79'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_79 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_80'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_80 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_81'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_81 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_82'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_82 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_83'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_83 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_84'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_84 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_85'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_85 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_86'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_86 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_87'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_87 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_88'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_88 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_89'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_89 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_90'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_90 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_91'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_91 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_92'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_92 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_93'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_93 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_94'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_94 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_95'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_95 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_96'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_96 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_97'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_97 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_98'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_98 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_99'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_99 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_100'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_100 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_101'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_101 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_102'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_102 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_103'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_103 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_104'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_104 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_105'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_105 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_106'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_106 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_107'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_107 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_108'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_108 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_109'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_109 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_110'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_110 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_111'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_111 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_112'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_112 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_113'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_113 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_114'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_114 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_115'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_115 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_116'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_116 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_117'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_117 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_118'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_118 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_119'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_119 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_120'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_120 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_121'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_121 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_122'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_122 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_123'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_123 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_124'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_124 # type: ignore # mutmut generated
mutants_xǁPureAstReducerǁreduce__mutmut['xǁPureAstReducerǁreduce__mutmut_125'] = PureAstReducer.xǁPureAstReducerǁreduce__mutmut_125 # type: ignore # mutmut generated
