from __future__ import annotations

from pydantic import ValidationError

from intent_engine.models import Ambiguity, IntentClassification, IntentContract


def test_intent_classification_valid() -> None:
    data = {
        "chain_of_thought": "The user requests to execute a Python script.",
        "intent": "CODE_EXECUTION",
        "confidence_score": 0.95,
    }
    instance = IntentClassification(**data)
    assert instance.intent == "CODE_EXECUTION"
    assert instance.confidence_score == 0.95


def test_intent_classification_invalid_score() -> None:
    data = {
        "chain_of_thought": "Analysis failed",
        "intent": "TECHNICAL_QUERY",
        "confidence_score": 1.5,  # invalid (> 1.0)
    }
    try:
        IntentClassification(**data)
        assert False, "Expected ValidationError"
    except ValidationError:
        pass


def test_intent_classification_invalid_intent() -> None:
    data = {
        "chain_of_thought": "Unknown",
        "intent": "INVALID_INTENT",
        "confidence_score": 0.5,
    }
    try:
        IntentClassification(**data)
        assert False, "Expected ValidationError"
    except ValidationError:
        pass


def test_intent_contract_with_defaults() -> None:
    contract = IntentContract(
        original_input="Build a REST API",
        classification=IntentClassification(
            chain_of_thought="Technical request",
            intent="TECHNICAL_QUERY",
            confidence_score=0.9,
        ),
    )
    assert contract.original_input == "Build a REST API"
    assert contract.requirements == []
    assert contract.ambiguities == []


def test_ambiguity_model() -> None:
    amb = Ambiguity(
        field="scope",
        description="Scope is unclear",
        suggested_clarification="What endpoints are needed?",
    )
    assert amb.field == "scope"
    assert amb.suggested_clarification
