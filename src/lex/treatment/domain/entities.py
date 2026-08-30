"""Domain Entities and AST Representation for the Treatment Bounded Context.

Implements the structured legislative tree (DispositivoNode / ActAst) and the
immutable mutation event (NormativeActMutation) following LC 95/1998 standards.
"""

from typing import Any, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from lex.ingestion.domain.value_objects import DocumentHash, GazetteDate
from lex.treatment.domain.exceptions import InvalidMutationPayloadError
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    DispositivoStatus,
    DispositivoType,
    MutationType,
)


class DispositivoNode(BaseModel):
    """Hierarchical node in a statutory Abstract Syntax Tree (AST).

    Represents an article, paragraph, clause (inciso), alínea, or item.
    """

    model_config = ConfigDict(frozen=False)

    node_path: CanonicalNodePath
    node_type: DispositivoType
    label: str
    text: str
    status: DispositivoStatus = DispositivoStatus.ORIGINAL_ACTIVE
    history: list[dict[str, Any]] = Field(default_factory=list)
    children: list["DispositivoNode"] = Field(default_factory=list)

    def add_child(self, child: "DispositivoNode") -> None:
        """Appends a child provision to this node's children collection."""
        self.children.append(child)

    def find_node(self, target: str | CanonicalNodePath) -> "DispositivoNode | None":
        """Recursively searches for a provision node by its canonical path.

        Args:
            target: The dot-separated canonical path string or CanonicalNodePath.

        Returns:
            The matching DispositivoNode if found, or None.
        """
        target_str = target.value if isinstance(target, CanonicalNodePath) else target.strip()
        if self.node_path.value == target_str:
            return self

        for child in self.children:
            found = child.find_node(target_str)
            if found is not None:
                return found
        return None

    def to_dict(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "status": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )


class ActAst(BaseModel):
    """Aggregate Root representing the complete Abstract Syntax Tree of a Normative Act."""

    model_config = ConfigDict(frozen=True)

    act_id: UUID | None = None
    canonical_urn: str | None = None
    title: str
    ementa: str | None = None
    nodes: list[DispositivoNode] = Field(default_factory=list)

    def find_node(self, target: str | CanonicalNodePath) -> DispositivoNode | None:
        """Searches across all top-level articles for a matching provision node."""
        target_str = target.value if isinstance(target, CanonicalNodePath) else target.strip()
        for root_node in self.nodes:
            found = root_node.find_node(target_str)
            if found is not None:
                return found
        return None

    def to_dict(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )


class NormativeActMutation(BaseModel):
    """Write Model entity representing an atomic legislative amendment patch (LC 95/1998)."""

    model_config = ConfigDict(frozen=True)

    id: UUID | None = None
    target_act_id: UUID
    target_node_path: CanonicalNodePath
    author_act_id: UUID
    author_dispositivo_ref: str | None = None
    mutation_type: MutationType
    new_text: str | None = None
    new_structured_payload: dict[str, Any] | None = None
    publication_date: GazetteDate
    effective_date: GazetteDate
    extraction_source: str
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    mutation_sha256: DocumentHash

    @model_validator(mode="after")
    def _validate_mutation_invariants(self) -> Self:
        """Enforces domain invariants on the amendment payload."""
        if self.mutation_type in (MutationType.ALTERACAO_NR, MutationType.ACRESCIMO):
            if not self.new_text or not self.new_text.strip():
                raise InvalidMutationPayloadError(
                    f"Mutation type '{self.mutation_type}' requires non-empty new_text."
                )
        return self
