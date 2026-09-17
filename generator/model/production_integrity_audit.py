from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Finding:
    identifier: str
    severity: str
    area: str
    summary: str
    state: str
    routing_blocker: bool
    resolution_evidence: str = ""

FINDINGS = (
    Finding(
        "AE036-F01","P0","build-system",
        "clean build can delete native PCB",
        "CLOSED",False,
        "AE-036A/B preserve native PCB/design-rule artifacts during generator cleanup; validated by clean build and regression."
    ),
    Finding(
        "AE036-F02","P0","SCH101",
        "cartridge loading/common-mode bias/RF response not closed",
        "CLOSED",False,
        "AE-037/037A/037B/037C3 define 47.4k differential loading, explicit DC bias return, 47p common-mode RF shunts, optional 22p differential DNP, and reconcile placement."
    ),
    Finding(
        "AE036-F03","P0/P1","physical-CAD",
        "dual op-amp package/unit semantics not closed",
        "CLOSED",False,
        "AE-038/039A/039B/B1/039C/C1/C2B establish 10 physical op-amp packages, real KiCad A/B units, actual SOIC-8 pin semantics, and explicit follower feedback."
    ),
    Finding(
        "AE036-F04","P1","controls",
        "Grayhill remains selected in live authority after rejection",
        "CLOSED",False,
        "AE-040B removes Grayhill from current control authority, preserves it only as rejected historical evidence, and makes AE-026/AE-027 Lorlin PT platform selection with exact production MPNs open the live authority."
    ),
    Finding("AE036-F05","P1","controls-PCB","PCB-mounted controls are not yet physical PCB objects","OPEN",True),
    Finding("AE036-F06","P1","power","nominal ±18 V uses top of key IC recommended range","OPEN",False),
    Finding("AE036-F07","P1","governance","decision/current baseline and indexes are stale","OPEN",False),
    Finding("AE036-F08","P1","PCB-authority","native pipeline retains superseded mounting-hole state","OPEN",False),
    Finding("AE036-F09","P1","PCB-audit","native-board text audits are structurally weak","OPEN",False),
    Finding("AE036-F10","P1/P2","procurement","BOM/approved-parts catalogue incomplete","OPEN",False),
    Finding("AE036-F11","P2","CI","CI omits production build and KiCad gates","OPEN",False),
    Finding("AE036-F12","P2","mechanical","final connector/interface arrangement needs confirmation","OPEN",False),
    Finding("AE036-F13","P2","maintenance","maintenance/release pack awaits physical evidence","OPEN",False),
    Finding("AE071-F01","P0","product-migration","AE-042 SCH101 selected-next implementation not yet migrated into live product generator","OPEN",True),
    Finding("AE071-F02","P0","product-migration","AE-067 branch-local DR-039 selected topology not yet migrated into live product generator","OPEN",True),
    Finding("AE071-F03","P1","precision-CAD","LT5400-7 B-grade RUN10 tolerance acceptance and exposed-pad disposition remain open","OPEN",True),
    Finding("AE071-F04","P1","SCH108-physical","THAT1646 10uF sense-capacitor body/footprint correlation remains open","OPEN",True),
    Finding("AE071-F05","P1","EMC-interface","XLR pin-1 local chassis termination is not yet represented as controlled physical implementation","OPEN",True),
    Finding("AE071-F06","P1","low-level-interconnect","cartridge input harness contact system requires low-level signal suitability review","OPEN",True),
    Finding("AE071-F07","P1","simulation-model","THAT1646 output impedance model semantics require 25-ohm-per-leg / 50-ohm-balanced correction before RUN08","OPEN",False),
)

def open_findings():
    return tuple(x for x in FINDINGS if x.state=="OPEN")

def closed_findings():
    return tuple(x for x in FINDINGS if x.state=="CLOSED")

def routing_blockers():
    return tuple(x for x in FINDINGS if x.state=="OPEN" and x.routing_blocker)

def validate_findings():
    assert len({x.identifier for x in FINDINGS}) == len(FINDINGS)
    assert {x.state for x in FINDINGS} <= {"OPEN","CLOSED"}
    assert {x.identifier for x in closed_findings()} == {
        "AE036-F01","AE036-F02","AE036-F03","AE036-F04"
    }
    assert all(x.resolution_evidence for x in closed_findings())
    assert {x.identifier for x in routing_blockers()} == {
        "AE036-F05",
        "AE071-F01","AE071-F02","AE071-F03",
        "AE071-F04","AE071-F05","AE071-F06",
    }
