from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Finding:
    identifier: str
    severity: str
    area: str
    summary: str
    routing_blocker: bool

FINDINGS = (
    Finding("AE036-F01","P0","build-system","clean build can delete native PCB",True),
    Finding("AE036-F02","P0","SCH101","cartridge loading/common-mode bias/RF response not closed",True),
    Finding("AE036-F03","P0/P1","physical-CAD","dual op-amp package/unit semantics not closed",True),
    Finding("AE036-F04","P1","controls","Grayhill remains selected in live authority after rejection",False),
    Finding("AE036-F05","P1","controls-PCB","PCB-mounted controls are not yet physical PCB objects",False),
    Finding("AE036-F06","P1","power","nominal ±18 V uses top of key IC recommended range",False),
    Finding("AE036-F07","P1","governance","decision/current baseline and indexes are stale",False),
    Finding("AE036-F08","P1","PCB-authority","native pipeline retains superseded mounting-hole state",False),
    Finding("AE036-F09","P1","PCB-audit","native-board text audits are structurally weak",False),
    Finding("AE036-F10","P1/P2","procurement","BOM/approved-parts catalogue incomplete",False),
    Finding("AE036-F11","P2","CI","CI omits production build and KiCad gates",False),
    Finding("AE036-F12","P2","mechanical","final connector/interface arrangement needs confirmation",False),
    Finding("AE036-F13","P2","maintenance","maintenance/release pack awaits physical evidence",False),
)

def routing_blockers():
    return tuple(x for x in FINDINGS if x.routing_blocker)

def validate_findings():
    assert len({x.identifier for x in FINDINGS}) == len(FINDINGS)
    assert len(routing_blockers()) == 3
    assert all(x.severity.startswith("P0") for x in routing_blockers())
