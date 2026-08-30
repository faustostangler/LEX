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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁDispositivoNodeǁadd_child__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDispositivoNodeǁfind_node__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDispositivoNodeǁto_dict__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDispositivoNodeǁfrom_dict__mutmut: MutantDict = {}  # type: ignore


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

    @_mutmut_mutated(mutants_xǁDispositivoNodeǁadd_child__mutmut)
    def add_child(self, child: "DispositivoNode") -> None:
        """Appends a child provision to this node's children collection."""
        self.children.append(child)

    def xǁDispositivoNodeǁadd_child__mutmut_orig(self, child: "DispositivoNode") -> None:
        """Appends a child provision to this node's children collection."""
        self.children.append(child)

    def xǁDispositivoNodeǁadd_child__mutmut_1(self, child: "DispositivoNode") -> None:
        """Appends a child provision to this node's children collection."""
        self.children.append(None)

    @_mutmut_mutated(mutants_xǁDispositivoNodeǁfind_node__mutmut)
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

    def xǁDispositivoNodeǁfind_node__mutmut_orig(self, target: str | CanonicalNodePath) -> "DispositivoNode | None":
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

    def xǁDispositivoNodeǁfind_node__mutmut_1(self, target: str | CanonicalNodePath) -> "DispositivoNode | None":
        """Recursively searches for a provision node by its canonical path.

        Args:
            target: The dot-separated canonical path string or CanonicalNodePath.

        Returns:
            The matching DispositivoNode if found, or None.
        """
        target_str = None
        if self.node_path.value == target_str:
            return self

        for child in self.children:
            found = child.find_node(target_str)
            if found is not None:
                return found
        return None

    def xǁDispositivoNodeǁfind_node__mutmut_2(self, target: str | CanonicalNodePath) -> "DispositivoNode | None":
        """Recursively searches for a provision node by its canonical path.

        Args:
            target: The dot-separated canonical path string or CanonicalNodePath.

        Returns:
            The matching DispositivoNode if found, or None.
        """
        target_str = target.value if isinstance(target, CanonicalNodePath) else target.strip()
        if self.node_path.value != target_str:
            return self

        for child in self.children:
            found = child.find_node(target_str)
            if found is not None:
                return found
        return None

    def xǁDispositivoNodeǁfind_node__mutmut_3(self, target: str | CanonicalNodePath) -> "DispositivoNode | None":
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
            found = None
            if found is not None:
                return found
        return None

    def xǁDispositivoNodeǁfind_node__mutmut_4(self, target: str | CanonicalNodePath) -> "DispositivoNode | None":
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
            found = child.find_node(None)
            if found is not None:
                return found
        return None

    def xǁDispositivoNodeǁfind_node__mutmut_5(self, target: str | CanonicalNodePath) -> "DispositivoNode | None":
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
            if found is None:
                return found
        return None

    @_mutmut_mutated(mutants_xǁDispositivoNodeǁto_dict__mutmut)
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

    def xǁDispositivoNodeǁto_dict__mutmut_orig(self) -> dict[str, Any]:
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

    def xǁDispositivoNodeǁto_dict__mutmut_1(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "XXnode_pathXX": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "status": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_2(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "NODE_PATH": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "status": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_3(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "XXnode_typeXX": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "status": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_4(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "NODE_TYPE": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "status": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_5(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "XXlabelXX": self.label,
            "text": self.text,
            "status": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_6(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "LABEL": self.label,
            "text": self.text,
            "status": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_7(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "XXtextXX": self.text,
            "status": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_8(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "TEXT": self.text,
            "status": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_9(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "XXstatusXX": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_10(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "STATUS": self.status.value,
            "history": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_11(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "status": self.status.value,
            "XXhistoryXX": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_12(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "status": self.status.value,
            "HISTORY": self.history,
            "children": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_13(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "status": self.status.value,
            "history": self.history,
            "XXchildrenXX": [child.to_dict() for child in self.children],
        }

    def xǁDispositivoNodeǁto_dict__mutmut_14(self) -> dict[str, Any]:
        """Serializes the AST node and its subtrees into a JSON-compatible dictionary."""
        return {
            "node_path": self.node_path.value,
            "node_type": self.node_type.value,
            "label": self.label,
            "text": self.text,
            "status": self.status.value,
            "history": self.history,
            "CHILDREN": [child.to_dict() for child in self.children],
        }

    @classmethod
    @_mutmut_mutated(mutants_xǁDispositivoNodeǁfrom_dict__mutmut, is_classmethod = True)
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

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_orig(cls, payload: dict[str, Any]) -> "DispositivoNode":
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

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_1(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=None,
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_2(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=None,
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_3(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=None,
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_4(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=None,
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_5(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=None,
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_6(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=None,
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_7(cls, payload: dict[str, Any]) -> "DispositivoNode":
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
            children=None,
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_8(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_9(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_10(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_11(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_12(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_13(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_14(cls, payload: dict[str, Any]) -> "DispositivoNode":
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
            )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_15(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(None),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_16(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["XXnode_pathXX"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_17(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["NODE_PATH"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_18(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(None),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_19(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["XXnode_typeXX"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_20(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["NODE_TYPE"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_21(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["XXlabelXX"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_22(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["LABEL"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_23(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["XXtextXX"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_24(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["TEXT"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_25(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                None
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_26(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get(None, DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_27(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", None)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_28(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get(DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_29(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", )
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_30(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("XXstatusXX", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_31(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("STATUS", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_32(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get(None, []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_33(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", None),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_34(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get([]),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_35(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("history", ),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_36(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("XXhistoryXX", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_37(cls, payload: dict[str, Any]) -> "DispositivoNode":
        """Deserializes a dictionary into a DispositivoNode hierarchy."""
        return cls(
            node_path=CanonicalNodePath.from_string(payload["node_path"]),
            node_type=DispositivoType(payload["node_type"]),
            label=payload["label"],
            text=payload["text"],
            status=DispositivoStatus(
                payload.get("status", DispositivoStatus.ORIGINAL_ACTIVE.value)
            ),
            history=payload.get("HISTORY", []),
            children=[cls.from_dict(child) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_38(cls, payload: dict[str, Any]) -> "DispositivoNode":
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
            children=[cls.from_dict(None) for child in payload.get("children", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_39(cls, payload: dict[str, Any]) -> "DispositivoNode":
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
            children=[cls.from_dict(child) for child in payload.get(None, [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_40(cls, payload: dict[str, Any]) -> "DispositivoNode":
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
            children=[cls.from_dict(child) for child in payload.get("children", None)],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_41(cls, payload: dict[str, Any]) -> "DispositivoNode":
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
            children=[cls.from_dict(child) for child in payload.get([])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_42(cls, payload: dict[str, Any]) -> "DispositivoNode":
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
            children=[cls.from_dict(child) for child in payload.get("children", )],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_43(cls, payload: dict[str, Any]) -> "DispositivoNode":
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
            children=[cls.from_dict(child) for child in payload.get("XXchildrenXX", [])],
        )

    @classmethod
    def xǁDispositivoNodeǁfrom_dict__mutmut_44(cls, payload: dict[str, Any]) -> "DispositivoNode":
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
            children=[cls.from_dict(child) for child in payload.get("CHILDREN", [])],
        )

mutants_xǁDispositivoNodeǁadd_child__mutmut['_mutmut_orig'] = DispositivoNode.xǁDispositivoNodeǁadd_child__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁadd_child__mutmut['xǁDispositivoNodeǁadd_child__mutmut_1'] = DispositivoNode.xǁDispositivoNodeǁadd_child__mutmut_1 # type: ignore # mutmut generated

mutants_xǁDispositivoNodeǁfind_node__mutmut['_mutmut_orig'] = DispositivoNode.xǁDispositivoNodeǁfind_node__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfind_node__mutmut['xǁDispositivoNodeǁfind_node__mutmut_1'] = DispositivoNode.xǁDispositivoNodeǁfind_node__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfind_node__mutmut['xǁDispositivoNodeǁfind_node__mutmut_2'] = DispositivoNode.xǁDispositivoNodeǁfind_node__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfind_node__mutmut['xǁDispositivoNodeǁfind_node__mutmut_3'] = DispositivoNode.xǁDispositivoNodeǁfind_node__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfind_node__mutmut['xǁDispositivoNodeǁfind_node__mutmut_4'] = DispositivoNode.xǁDispositivoNodeǁfind_node__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfind_node__mutmut['xǁDispositivoNodeǁfind_node__mutmut_5'] = DispositivoNode.xǁDispositivoNodeǁfind_node__mutmut_5 # type: ignore # mutmut generated

mutants_xǁDispositivoNodeǁto_dict__mutmut['_mutmut_orig'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_1'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_2'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_3'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_4'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_5'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_6'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_7'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_8'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_9'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_9 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_10'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_11'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_11 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_12'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_12 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_13'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_13 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁto_dict__mutmut['xǁDispositivoNodeǁto_dict__mutmut_14'] = DispositivoNode.xǁDispositivoNodeǁto_dict__mutmut_14 # type: ignore # mutmut generated

mutants_xǁDispositivoNodeǁfrom_dict__mutmut['_mutmut_orig'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_1'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_2'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_3'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_4'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_5'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_6'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_7'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_8'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_9'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_9 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_10'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_11'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_11 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_12'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_12 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_13'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_13 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_14'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_14 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_15'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_15 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_16'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_16 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_17'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_17 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_18'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_18 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_19'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_19 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_20'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_20 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_21'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_21 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_22'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_22 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_23'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_23 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_24'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_24 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_25'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_25 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_26'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_26 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_27'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_27 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_28'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_28 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_29'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_29 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_30'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_30 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_31'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_31 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_32'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_32 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_33'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_33 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_34'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_34 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_35'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_35 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_36'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_36 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_37'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_37 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_38'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_38 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_39'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_39 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_40'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_40 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_41'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_41 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_42'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_42 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_43'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_43 # type: ignore # mutmut generated
mutants_xǁDispositivoNodeǁfrom_dict__mutmut['xǁDispositivoNodeǁfrom_dict__mutmut_44'] = DispositivoNode.xǁDispositivoNodeǁfrom_dict__mutmut_44 # type: ignore # mutmut generated
mutants_xǁActAstǁfind_node__mutmut: MutantDict = {}  # type: ignore
mutants_xǁActAstǁto_dict__mutmut: MutantDict = {}  # type: ignore
mutants_xǁActAstǁfrom_dict__mutmut: MutantDict = {}  # type: ignore


class ActAst(BaseModel):
    """Aggregate Root representing the complete Abstract Syntax Tree of a Normative Act."""

    model_config = ConfigDict(frozen=True)

    act_id: UUID | None = None
    canonical_urn: str | None = None
    title: str
    ementa: str | None = None
    nodes: list[DispositivoNode] = Field(default_factory=list)

    @_mutmut_mutated(mutants_xǁActAstǁfind_node__mutmut)
    def find_node(self, target: str | CanonicalNodePath) -> DispositivoNode | None:
        """Searches across all top-level articles for a matching provision node."""
        target_str = target.value if isinstance(target, CanonicalNodePath) else target.strip()
        for root_node in self.nodes:
            found = root_node.find_node(target_str)
            if found is not None:
                return found
        return None

    def xǁActAstǁfind_node__mutmut_orig(self, target: str | CanonicalNodePath) -> DispositivoNode | None:
        """Searches across all top-level articles for a matching provision node."""
        target_str = target.value if isinstance(target, CanonicalNodePath) else target.strip()
        for root_node in self.nodes:
            found = root_node.find_node(target_str)
            if found is not None:
                return found
        return None

    def xǁActAstǁfind_node__mutmut_1(self, target: str | CanonicalNodePath) -> DispositivoNode | None:
        """Searches across all top-level articles for a matching provision node."""
        target_str = None
        for root_node in self.nodes:
            found = root_node.find_node(target_str)
            if found is not None:
                return found
        return None

    def xǁActAstǁfind_node__mutmut_2(self, target: str | CanonicalNodePath) -> DispositivoNode | None:
        """Searches across all top-level articles for a matching provision node."""
        target_str = target.value if isinstance(target, CanonicalNodePath) else target.strip()
        for root_node in self.nodes:
            found = None
            if found is not None:
                return found
        return None

    def xǁActAstǁfind_node__mutmut_3(self, target: str | CanonicalNodePath) -> DispositivoNode | None:
        """Searches across all top-level articles for a matching provision node."""
        target_str = target.value if isinstance(target, CanonicalNodePath) else target.strip()
        for root_node in self.nodes:
            found = root_node.find_node(None)
            if found is not None:
                return found
        return None

    def xǁActAstǁfind_node__mutmut_4(self, target: str | CanonicalNodePath) -> DispositivoNode | None:
        """Searches across all top-level articles for a matching provision node."""
        target_str = target.value if isinstance(target, CanonicalNodePath) else target.strip()
        for root_node in self.nodes:
            found = root_node.find_node(target_str)
            if found is None:
                return found
        return None

    @_mutmut_mutated(mutants_xǁActAstǁto_dict__mutmut)
    def to_dict(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_orig(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_1(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "XXact_idXX": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_2(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "ACT_ID": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_3(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(None) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_4(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "XXcanonical_urnXX": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_5(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "CANONICAL_URN": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_6(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "XXtitleXX": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_7(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "TITLE": self.title,
            "ementa": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_8(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "XXementaXX": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_9(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "EMENTA": self.ementa,
            "nodes": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_10(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "XXnodesXX": [node.to_dict() for node in self.nodes],
        }

    def xǁActAstǁto_dict__mutmut_11(self) -> dict[str, Any]:
        """Serializes the complete AST into a JSON-compatible structure."""
        return {
            "act_id": str(self.act_id) if self.act_id else None,
            "canonical_urn": self.canonical_urn,
            "title": self.title,
            "ementa": self.ementa,
            "NODES": [node.to_dict() for node in self.nodes],
        }

    @classmethod
    @_mutmut_mutated(mutants_xǁActAstǁfrom_dict__mutmut, is_classmethod = True)
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

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_orig(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_1(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = None
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_2(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get(None)
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_3(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("XXact_idXX")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_4(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("ACT_ID")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_5(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_6(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=None,
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_7(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=None,
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_8(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=None,
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_9(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=None,
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_10(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_11(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_12(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_13(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_14(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_15(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(None) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_16(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get(None),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_17(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("XXcanonical_urnXX"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_18(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("CANONICAL_URN"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_19(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get(None, ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_20(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", None),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_21(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get(""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_22(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_23(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("XXtitleXX", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_24(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("TITLE", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_25(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", "XXXX"),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_26(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get(None),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_27(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("XXementaXX"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_28(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("EMENTA"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_29(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(None) for node in payload.get("nodes", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_30(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get(None, [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_31(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", None)],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_32(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get([])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_33(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("nodes", )],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_34(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("XXnodesXX", [])],
        )

    @classmethod
    def xǁActAstǁfrom_dict__mutmut_35(cls, payload: dict[str, Any]) -> "ActAst":
        """Deserializes a dictionary into an ActAst aggregate root."""
        act_id_val = payload.get("act_id")
        return cls(
            act_id=UUID(act_id_val) if act_id_val else None,
            canonical_urn=payload.get("canonical_urn"),
            title=payload.get("title", ""),
            ementa=payload.get("ementa"),
            nodes=[DispositivoNode.from_dict(node) for node in payload.get("NODES", [])],
        )

mutants_xǁActAstǁfind_node__mutmut['_mutmut_orig'] = ActAst.xǁActAstǁfind_node__mutmut_orig # type: ignore # mutmut generated
mutants_xǁActAstǁfind_node__mutmut['xǁActAstǁfind_node__mutmut_1'] = ActAst.xǁActAstǁfind_node__mutmut_1 # type: ignore # mutmut generated
mutants_xǁActAstǁfind_node__mutmut['xǁActAstǁfind_node__mutmut_2'] = ActAst.xǁActAstǁfind_node__mutmut_2 # type: ignore # mutmut generated
mutants_xǁActAstǁfind_node__mutmut['xǁActAstǁfind_node__mutmut_3'] = ActAst.xǁActAstǁfind_node__mutmut_3 # type: ignore # mutmut generated
mutants_xǁActAstǁfind_node__mutmut['xǁActAstǁfind_node__mutmut_4'] = ActAst.xǁActAstǁfind_node__mutmut_4 # type: ignore # mutmut generated

mutants_xǁActAstǁto_dict__mutmut['_mutmut_orig'] = ActAst.xǁActAstǁto_dict__mutmut_orig # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_1'] = ActAst.xǁActAstǁto_dict__mutmut_1 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_2'] = ActAst.xǁActAstǁto_dict__mutmut_2 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_3'] = ActAst.xǁActAstǁto_dict__mutmut_3 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_4'] = ActAst.xǁActAstǁto_dict__mutmut_4 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_5'] = ActAst.xǁActAstǁto_dict__mutmut_5 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_6'] = ActAst.xǁActAstǁto_dict__mutmut_6 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_7'] = ActAst.xǁActAstǁto_dict__mutmut_7 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_8'] = ActAst.xǁActAstǁto_dict__mutmut_8 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_9'] = ActAst.xǁActAstǁto_dict__mutmut_9 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_10'] = ActAst.xǁActAstǁto_dict__mutmut_10 # type: ignore # mutmut generated
mutants_xǁActAstǁto_dict__mutmut['xǁActAstǁto_dict__mutmut_11'] = ActAst.xǁActAstǁto_dict__mutmut_11 # type: ignore # mutmut generated

mutants_xǁActAstǁfrom_dict__mutmut['_mutmut_orig'] = ActAst.xǁActAstǁfrom_dict__mutmut_orig # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_1'] = ActAst.xǁActAstǁfrom_dict__mutmut_1 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_2'] = ActAst.xǁActAstǁfrom_dict__mutmut_2 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_3'] = ActAst.xǁActAstǁfrom_dict__mutmut_3 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_4'] = ActAst.xǁActAstǁfrom_dict__mutmut_4 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_5'] = ActAst.xǁActAstǁfrom_dict__mutmut_5 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_6'] = ActAst.xǁActAstǁfrom_dict__mutmut_6 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_7'] = ActAst.xǁActAstǁfrom_dict__mutmut_7 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_8'] = ActAst.xǁActAstǁfrom_dict__mutmut_8 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_9'] = ActAst.xǁActAstǁfrom_dict__mutmut_9 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_10'] = ActAst.xǁActAstǁfrom_dict__mutmut_10 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_11'] = ActAst.xǁActAstǁfrom_dict__mutmut_11 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_12'] = ActAst.xǁActAstǁfrom_dict__mutmut_12 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_13'] = ActAst.xǁActAstǁfrom_dict__mutmut_13 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_14'] = ActAst.xǁActAstǁfrom_dict__mutmut_14 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_15'] = ActAst.xǁActAstǁfrom_dict__mutmut_15 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_16'] = ActAst.xǁActAstǁfrom_dict__mutmut_16 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_17'] = ActAst.xǁActAstǁfrom_dict__mutmut_17 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_18'] = ActAst.xǁActAstǁfrom_dict__mutmut_18 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_19'] = ActAst.xǁActAstǁfrom_dict__mutmut_19 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_20'] = ActAst.xǁActAstǁfrom_dict__mutmut_20 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_21'] = ActAst.xǁActAstǁfrom_dict__mutmut_21 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_22'] = ActAst.xǁActAstǁfrom_dict__mutmut_22 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_23'] = ActAst.xǁActAstǁfrom_dict__mutmut_23 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_24'] = ActAst.xǁActAstǁfrom_dict__mutmut_24 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_25'] = ActAst.xǁActAstǁfrom_dict__mutmut_25 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_26'] = ActAst.xǁActAstǁfrom_dict__mutmut_26 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_27'] = ActAst.xǁActAstǁfrom_dict__mutmut_27 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_28'] = ActAst.xǁActAstǁfrom_dict__mutmut_28 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_29'] = ActAst.xǁActAstǁfrom_dict__mutmut_29 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_30'] = ActAst.xǁActAstǁfrom_dict__mutmut_30 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_31'] = ActAst.xǁActAstǁfrom_dict__mutmut_31 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_32'] = ActAst.xǁActAstǁfrom_dict__mutmut_32 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_33'] = ActAst.xǁActAstǁfrom_dict__mutmut_33 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_34'] = ActAst.xǁActAstǁfrom_dict__mutmut_34 # type: ignore # mutmut generated
mutants_xǁActAstǁfrom_dict__mutmut['xǁActAstǁfrom_dict__mutmut_35'] = ActAst.xǁActAstǁfrom_dict__mutmut_35 # type: ignore # mutmut generated


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
