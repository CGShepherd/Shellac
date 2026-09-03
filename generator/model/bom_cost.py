"""Controlled running BOM-cost model for Shellac."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

LEDGER = Path("config/bom/shellac_cost_ledger.yaml")

@dataclass(frozen=True)
class CostSummary:
    quoted_design_gbp: float
    quoted_build_gbp: float
    quoted_production_10_gbp: float
    priced_lines: int
    unpriced_lines: int
    total_lines: int
    confidence_pct: float

def load_ledger(repo: Path = Path(".")) -> dict[str, Any]:
    return yaml.safe_load((repo / LEDGER).read_text(encoding="utf-8"))

def _num(v):
    return float(v) if isinstance(v, (int, float)) else 0.0

def summarise(repo: Path = Path(".")) -> CostSummary:
    data = load_ledger(repo)
    items = data.get("items", [])
    priced = [x for x in items if isinstance(x.get("design_unit_cost_gbp"), (int, float))]
    return CostSummary(
        quoted_design_gbp=sum(_num(x.get("design_unit_cost_gbp")) for x in items),
        quoted_build_gbp=sum(_num(x.get("build_cost_gbp")) for x in items),
        quoted_production_10_gbp=sum(_num(x.get("production_10_unit_cost_gbp")) for x in items),
        priced_lines=len(priced),
        unpriced_lines=len(items)-len(priced),
        total_lines=len(items),
        confidence_pct=(100.0*len(priced)/len(items)) if items else 0.0,
    )

def category_subtotals(repo: Path = Path(".")):
    data=load_ledger(repo)
    out=defaultdict(float)
    for item in data.get("items",[]):
        if isinstance(item.get("design_unit_cost_gbp"),(int,float)):
            out[item["category"]] += float(item["design_unit_cost_gbp"])
    return dict(sorted(out.items()))

def validate_ledger(repo: Path = Path(".")):
    data=load_ledger(repo)
    assert data["currency"]=="GBP"
    assert data["rules"]["rejected_parts_excluded_from_current_estimate"] is True
    assert data["rules"]["prototype_samples_are_nre"] is True
    assert data["rules"]["owned_test_equipment_excluded"] is True
    ids=[x["id"] for x in data.get("items",[])]
    assert len(ids)==len(set(ids))
    for x in data.get("items",[]):
        if isinstance(x.get("design_unit_cost_gbp"),(int,float)):
            assert x.get("source")
            assert x.get("checked_date")
