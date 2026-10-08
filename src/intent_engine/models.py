from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class IntentClassification(BaseModel):
    """Classification of user intent with structured reasoning.

    Attributes:
        chain_of_thought: Step-by-step reasoning before determining the intent.
        intent: Primary category of the user request.
        confidence_score: Estimated confidence score from 0.0 to 1.0.
    """

    chain_of_thought: str = Field(
        ...,
        description="Step-by-step reasoning before determining the primary intent.",
    )
    intent: Literal[
        "TECHNICAL_QUERY",
        "CODE_EXECUTION",
        "SYSTEM_COMMAND",
        "UNKNOWN",
    ] = Field(
        ...,
        description="Primary category of the user request.",
    )
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Estimated confidence score (0.0 to 1.0).",
    )


class Ambiguity(BaseModel):
    """Represents an ambiguity identified in the input request."""

    field: str = Field(..., description="The field or aspect that is ambiguous.")
    description: str = Field(..., description="Explanation of the ambiguity.")
    suggested_clarification: str = Field(
        ..., description="Suggested clarification question or phrasing."
    )


class IntentContract(BaseModel):
    """Structured contract extracted from unstructured natural language input."""

    original_input: str = Field(..., description="The original unstructured input.")
    classification: IntentClassification = Field(
        ..., description="Intent classification with reasoning and confidence."
    )
    requirements: list[str] = Field(
        default_factory=list,
        description="Key requirements extracted from the input.",
    )
    ambiguities: list[Ambiguity] = Field(
        default_factory=list,
        description="Identified ambiguities requiring clarification.",
    )
