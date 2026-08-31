"""Pure AST Reducer for Legislative Delta Consolidation.

Implements the pure function:
reduce(BaseAST, [Mutations]) -> CompiledNormativeAct

Replays statutory mutations chronologically, enforces cascading subtree revocations,
and generates pre-rendered LZ4 TOAST HTML/Markdown read models.
"""

import hashlib
import html
import uuid
from datetime import UTC, datetime

from lex.consolidation.domain.entities import CompiledNormativeAct
from lex.treatment.domain.entities import ActAst, DispositivoNode, NormativeActMutation
from lex.treatment.domain.value_objects import (
    DispositivoStatus,
    DispositivoType,
    MutationType,
)


def _cascade_revocation(node: DispositivoNode) -> None:
    """Recursively marks a provision node and all of its descendants as REVOKED."""
    node.status = DispositivoStatus.REVOKED
    for child in node.children:
        _cascade_revocation(child)


def _render_node_html(node: DispositivoNode) -> str:
    """Renders a single AST provision node and its children into semantic HTML (CWE-79 safe)."""
    lines: list[str] = []
    node_id = html.escape(node.node_path.value, quote=True)
    escaped_label = html.escape(node.label or "")
    escaped_text = html.escape(node.text or "")

    if node.status == DispositivoStatus.REVOKED:
        lines.append(
            f'<p id="{node_id}" class="dispositivo revogado">'
            f"<strike>{escaped_label} {escaped_text}</strike></p>"
        )
    elif node.status == DispositivoStatus.MODIFIED_ACTIVE:
        lines.append(
            f'<p id="{node_id}" class="dispositivo modificado">'
            f'<span class="vigente">{escaped_label} {escaped_text}</span></p>'
        )
    else:
        lines.append(
            f'<p id="{node_id}" class="dispositivo original">'
            f"<strong>{escaped_label}</strong> {escaped_text}</p>"
        )

    for child in node.children:
        lines.append(_render_node_html(child))

    return "\n".join(lines)


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


class PureAstReducer:
    """Pure functional reduction engine compiling base statutes and delta mutations."""

    @classmethod
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
        escaped_act_id = html.escape(str(base_ast.act_id or ""), quote=True)
        escaped_title = html.escape(working_ast.title or "")
        html_chunks: list[str] = [
            f'<div class="normative-act-compiled" id="{escaped_act_id}">',
            f"<h1>{escaped_title}</h1>",
        ]
        if working_ast.ementa:
            escaped_ementa = html.escape(working_ast.ementa)
            html_chunks.append(f'<p class="ementa"><em>{escaped_ementa}</em></p>')

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
