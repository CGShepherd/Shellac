import pytest

from generator.model.core import (
    Direction,
    FunctionalBlock,
    Interface,
    ProjectModel,
    Signal,
    SignalKind,
)
from generator.model.shellac import build_shellac_model
from generator.model.validation import ModelValidationError, validate_project


def test_shellac_model_is_valid():
    model = build_shellac_model()
    assert validate_project(model, raise_on_error=False) == []


def test_shellac_block_identifiers_are_unique():
    model = build_shellac_model()
    identifiers = [block.identifier for block in model.all_blocks()]
    assert len(identifiers) == len(set(identifiers))


def test_all_shellac_interfaces_reference_declared_signals():
    model = build_shellac_model()
    signals = {signal.name for signal in model.signals}
    for block in model.all_blocks():
        for interface in block.interfaces:
            assert interface.signal in signals


def test_duplicate_block_identifier_is_rejected():
    model = ProjectModel("X", "Test", "A", "Test")
    model.signals.append(Signal("S", SignalKind.ANALOG))
    for name in ("one", "two"):
        model.blocks.append(
            FunctionalBlock(
                identifier="DUP",
                name=name,
                purpose="test",
                interfaces=[Interface("in", "S", Direction.INPUT)],
            )
        )

    with pytest.raises(ModelValidationError):
        validate_project(model)


def test_unknown_signal_is_rejected():
    model = ProjectModel("X", "Test", "A", "Test")
    model.blocks.append(
        FunctionalBlock(
            identifier="B1",
            name="Block",
            purpose="test",
            interfaces=[Interface("in", "MISSING", Direction.INPUT)],
        )
    )

    issues = validate_project(model, raise_on_error=False)
    assert any(issue.code == "FM012" for issue in issues)
