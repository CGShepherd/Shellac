from pathlib import Path
import json

import pytest
import yaml

from generator.model.controls import LED_CURRENT_A, NOMINAL_RAIL_VOLTAGE_V
from generator.model.final_gain import SUPPLY_RAIL_V as SCH104_RAIL_V
from generator.model.output_driver import (
    DATASHEET_MAX_OUTPUT_RMS_V,
    SUPPLY_RAIL_V as THAT1646_RAIL_V,
)

ROOT = Path(__file__).resolve().parents[1]

CURRENT_FILES = (
    "generator/blocks/balanced_input.py",
    "generator/blocks/balanced_output.py",
    "generator/blocks/controls.py",
    "generator/blocks/final_gain.py",
    "generator/blocks/mode_matrix.py",
    "generator/blocks/power_entry.py",
    "generator/blocks/replay_eq.py",
    "generator/blocks/rumble_filter.py",
    "generator/commissioning/model.py",
    "generator/component_selection.py",
    "generator/core/components.py",
    "generator/hierarchy.py",
    "generator/layout/constraints.py",
    "generator/layout/interconnect_architecture.py",
    "generator/model/controls.py",
    "generator/model/shellac.py",
    "simulation/config/integrated_baseline.yaml",
    "simulation/config/run00.yaml",
    "simulation/runs/run00_sanity/run00_sanity.cir.in",
)

FORBIDDEN = (
    "+18VA_IN", "-18VA_IN", "+18V_OUT", "-18V_OUT",
    "+18V", "-18V", "VPLUS18", "VMINUS18", "+/-18 V", "±18 V",
)


def test_ae076a_live_current_surface_has_no_stale_18v_rail_tokens():
    failures = []
    for rel in CURRENT_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token in text:
                failures.append(f"{rel}: {token}")
    assert failures == [], "\n".join(failures)


def test_ae076a_current_numeric_rail_authority_and_led_current():
    assert NOMINAL_RAIL_VOLTAGE_V == pytest.approx(17.0)
    assert SCH104_RAIL_V == pytest.approx(17.0)
    assert THAT1646_RAIL_V == pytest.approx(17.0)
    assert DATASHEET_MAX_OUTPUT_RMS_V == pytest.approx(18.0)
    assert LED_CURRENT_A * 1000 == pytest.approx(1.7804878, rel=1e-6)


def test_ae076a_current_simulation_contract_is_17v():
    baseline = yaml.safe_load(
        (ROOT / "simulation/config/integrated_baseline.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert baseline["nominal_rails_v"] == {"plus": 17.0, "minus": -17.0}
    railq = baseline["rail_authority_requalification"]
    assert railq["authority"] == "AE-076A"
    assert railq["status"] == "PASSED_17V_REQUALIFICATION"
    assert railq["historical_18v_evidence_preserved"] is True
    assert railq["routing_authority_changed"] is False

    run00 = yaml.safe_load(
        (ROOT / "simulation/config/run00.yaml").read_text(encoding="utf-8")
    )
    assert run00["parameters"]["V_RAIL"] == 17
    assert set(run00["expected_measurements"]) == {
        "RUN00_VPLUS17", "RUN00_VMINUS17", "RUN00_VMID"
    }

    acceptance = yaml.safe_load(
        (ROOT / "simulation/config/acceptance.yaml").read_text(encoding="utf-8")
    )
    assert acceptance["authority"] == "AE-076A"
    assert acceptance["historical_acceptance_basis"] == "AE-049"
    assert acceptance["criteria"]["run00_positive_rail"]["minimum"] == pytest.approx(16.999999)
    assert acceptance["criteria"]["run00_negative_rail"]["maximum"] == pytest.approx(-16.999999)


def test_ae076a_fresh_integrated_and_output_evidence_pass():
    integrated = json.loads(
        (ROOT / "simulation/results/ae076a_17v/ae076a_integrated_run00_17v.json")
        .read_text(encoding="utf-8")
    )
    output = json.loads(
        (ROOT / "simulation/results/ae076a_17v/ae076a_output_pre90_17v.json")
        .read_text(encoding="utf-8")
    )
    assert integrated["authority"] == "AE-076A"
    assert integrated["run_id"] == "RUN00_INTEGRATED_17V"
    assert integrated["configuration"]["rail_plus_v"] == pytest.approx(17.0)
    assert integrated["configuration"]["rail_minus_v"] == pytest.approx(-17.0)
    assert integrated["pass"] is True

    assert output["authority"] == "AE-076A"
    assert output["run_id"] == "OUTPUT_PRE90_17V"
    assert output["nominal_rails_v"] == {"plus": 17.0, "minus": -17.0}
    assert output["pass"] is True
    assert all(output["gates"].values())
    assert output["bench_and_future_gates_retained"][
        "run06_load_cable_stability_bench_gate_retained"
    ] is True
    assert output["bench_and_future_gates_retained"][
        "run06_dynamic_thd_bench_gate_retained"
    ] is True


def test_ae076a_native_pcb_uses_current_17v_net_identity():
    text = (ROOT / "out/kicad/ProjectShellac.kicad_pcb").read_text(
        encoding="utf-8"
    )
    for token in ("+18V", "-18V", "+18VA_IN", "-18VA_IN"):
        assert token not in text
    for token in ("+17V", "-17V", "+17VA_IN", "-17VA_IN"):
        assert token in text


def test_historical_18v_evidence_remains_historical():
    ae069 = yaml.safe_load(
        (ROOT / "simulation/config/ae069_run06_output.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert ae069["authority"] == "AE-069"
    assert ae069["execution"]["rails_v"] == pytest.approx(18.0)

    ae065 = json.loads(
        (ROOT / "simulation/results/run00_sanity/ae065_integrated_run00.json")
        .read_text(encoding="utf-8")
    )
    assert ae065["authority"] == "AE-065"
    assert ae065["configuration"]["rail_plus_v"] == pytest.approx(18.0)
    assert ae065["configuration"]["rail_minus_v"] == pytest.approx(-18.0)
