"""SR-040 full schematic-population BOM/footprint census."""
from __future__ import annotations
from collections import Counter
from dataclasses import asdict, dataclass, field

from generator.layout.footprint_contract import PopulationStatus, build_footprint_contract

@dataclass(frozen=True, slots=True)
class BomCensusItem:
    ref: str
    sheet_id: str
    value: str
    footprint: str
    population: str
    procurement_state: str

@dataclass(slots=True)
class FullBomCensus:
    identifier: str
    revision: str
    status: str
    board_item_count: int
    panel_item_count: int
    footprint_count: int
    procurement_pending_count: int
    package_family_counts: dict[str,int] = field(default_factory=dict)
    items: list[BomCensusItem] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

def _procurement_state(ref: str, value: str) -> str:
    exact_tokens=("LT5400","OPA1656","OPA1612","LM4562","THAT1646")
    if any(token in value.upper() for token in exact_tokens):
        return "FUNCTIONAL_IDENTITY_KNOWN__MPN_GRADE_REVIEW"
    if ref.startswith(("R","C","D")):
        return "VALUE_AND_FOOTPRINT_FROZEN__MANUFACTURER_MPN_PENDING"
    if ref.startswith("TP"):
        return "STANDARD_FOOTPRINT__MPN_OPTIONAL"
    return "PART_IDENTITY_REVIEW_REQUIRED"

def build_full_bom_census() -> FullBomCensus:
    contract=build_footprint_contract()
    items=[]
    for e in contract.entries:
        state=_procurement_state(e.ref,e.value)
        items.append(BomCensusItem(
            ref=e.ref,
            sheet_id=e.sheet_id,
            value=e.value,
            footprint=e.footprint,
            population=e.population_status.value,
            procurement_state=state,
        ))
    board=[i for i in items if i.population==PopulationStatus.APPROVED.value]
    panel=[i for i in items if i.population==PopulationStatus.PANEL_EXCLUDED.value]
    pending=[i for i in board if "PENDING" in i.procurement_state or "REVIEW" in i.procurement_state]
    counts=Counter(
        e.package_family for e in contract.entries
        if e.population_status is PopulationStatus.APPROVED
    )
    return FullBomCensus(
        identifier="SR-040-BOM-CENSUS",
        revision="Rev A0",
        status="FULL_POPULATION_IDENTIFIED__PROCUREMENT_MPN_FREEZE_PENDING",
        board_item_count=len(board),
        panel_item_count=len(panel),
        footprint_count=len({i.footprint for i in board}),
        procurement_pending_count=len(pending),
        package_family_counts=dict(sorted(counts.items())),
        items=items,
    )
