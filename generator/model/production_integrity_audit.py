"""Current production-integrity finding oracle reconciled by AE-076D.
Historical finding identifiers are retained. CLOSED means the historical defect is resolved;
it does not close later related work. Current routing authority is the AE071 hold.
"""
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Finding:
    identifier:str; severity:str; area:str; summary:str; state:str; routing_blocker:bool; resolution_evidence:str=''
FINDINGS=(
 Finding('AE036-F01','P0','build-system','clean build can delete native PCB','CLOSED',False,'AE-036A/B preserve native PCB/design-rule artifacts during generator cleanup.'),
 Finding('AE036-F02','P0','SCH101','cartridge loading/common-mode bias/RF response not closed','CLOSED',False,'AE-037/037A/037B/037C3 establish 47.4k differential loading, explicit DC bias return and fixed 47p common-mode RF shunts; later AE-071A/AE-076C separately govern service loading.'),
 Finding('AE036-F03','P0/P1','physical-CAD','dual op-amp package/unit semantics not closed','CLOSED',False,'AE-038/039A/039B/B1/039C/C1/C2B establish real package/unit semantics and explicit follower feedback.'),
 Finding('AE036-F04','P1','controls','Grayhill remains selected in live authority after rejection','CLOSED',False,'AE-040B removes Grayhill from current authority; AE-075C/AE-076C freeze NKK/C&K current hardware while Grayhill remains provenance only.'),
 Finding('AE036-F05','P1','controls-PCB','selected seven-control direct-main-PCB architecture is not yet physically migrated into exact B.Cu PCB objects','OPEN',True),
 Finding('AE036-F06','P1','power','nominal rail operating-margin decision','CLOSED',False,'AE-076A establishes +17 V / 0VA / -17 V as current product authority and requalifies current nominal integrated/output headroom.'),
 Finding('AE036-F07','P1','governance','current decision baseline/provenance was stale','CLOSED',False,'AE-059 establishes current/historical status semantics; AE-071 onward separates historical release snapshots from current hold authority; AE-076C reconciles current decision/document/readiness authority.'),
 Finding('AE036-F08','P1','PCB-authority','native pipeline retained superseded mounting-hole ownership/freeze state','CLOSED',False,'AE-071B hardens MH1-MH4 as locked board-only objects and separates native-board integrity from routing authority. AE-076B six-support migration is a later distinct B03 activity.'),
 Finding('AE036-F09','P1','PCB-audit','native-board audits retain residual structural/text-parser limitations outside the strengthened SR-043 audit','OPEN',False),
 Finding('AE036-F10','P1/P2','procurement','BOM/approved-parts catalogue remains incomplete: timing-cap decomposition, output ferrite and other final identities remain open','OPEN',False),
 Finding('AE036-F11','P2','CI','CI runs compile/pytest but does not execute the full native KiCad build/ERC/DRC/audit production gate set','OPEN',False),
 Finding('AE036-F12','P2','mechanical','connector identities are controlled but final full-chassis placement, harness corridors and service arrangement remain to be proven in MCAD','OPEN',False),
 Finding('AE036-F13','P2','maintenance','maintenance/release pack awaits measured physical, thermal, fault-isolation and fabrication evidence','OPEN',False),
 Finding('AE071-F01','P0','product-migration','AE-042 SCH101 selected-next implementation not yet migrated into live product generator','CLOSED',False,'AE-071A migrates the fail-safe gain/service implementation into live product state; AE-076C separately selects per-channel cartridge personality as selected-next.'),
 Finding('AE071-F02','P0','product-migration','AE-067 branch-local DR-039 selected topology not yet migrated into live product generator','CLOSED',False,'AE-074 migrates branch-local DIRECT/BYPASS 1 uF / 330 kOhm topology and reconciles native PCB F8/net/metadata while retaining RUN09/RUN10/RUN12/bench qualification.'),
 Finding('AE071-F03','P1','precision-CAD','LT5400 B-grade MPN/EP are implemented; complete-stage RUN10 tolerance/CMRR/20 kHz parasitic acceptance remains open','OPEN',True),
 Finding('AE071-F04','P1','SCH108-physical','THAT1646 10uF sense-capacitor body/footprint correlation remains open','CLOSED',False,'AE-075A selects Panasonic ECEA1VN100U and validates the exact 5 x 11 mm, 2.0 mm-pitch native footprint.'),
 Finding('AE071-F05','P1','EMC-interface','XLR pin-1 local chassis termination is not yet represented as controlled physical implementation','CLOSED',False,'AE-075B controls exact Neutrik connectors with pin 1 and shell/front-panel contact locally bonded to CHASSIS and no connector-local 0VA bond.'),
 Finding('AE071-F06','P1','low-level-interconnect','cartridge input harness contact system requires low-level signal suitability review','CLOSED',False,'AE-075-B07 selects and natively validates Molex Micro-Lock Plus 5055780321 / 5055700301 / 5055721200 with controlled CHASSIS/HOT/COLD pin contract.'),
 Finding('AE071-F07','P1','simulation-model','THAT1646 output impedance model semantics require 25-ohm-per-leg / 50-ohm-balanced correction before RUN08','CLOSED',False,'AE-075G corrects live semantics to 25 ohm per leg / 50 ohm differential and records AE071-S01 RESOLVED.'),
 Finding('AE071-F08','P1','SCH101-service-hardware','gain-shunt physical pairing/orientation plus selected-next per-channel personality-interface CAD/migration/parasitic correlation remain open','OPEN',True),)
CLOSED_IDS={'AE036-F01','AE036-F02','AE036-F03','AE036-F04','AE036-F06','AE036-F07','AE036-F08','AE071-F01','AE071-F02','AE071-F04','AE071-F05','AE071-F06','AE071-F07'}
OPEN_IDS={'AE036-F05','AE036-F09','AE036-F10','AE036-F11','AE036-F12','AE036-F13','AE071-F03','AE071-F08'}
ROUTING_BLOCKER_IDS={'AE036-F05','AE071-F03','AE071-F08'}
def open_findings(): return tuple(x for x in FINDINGS if x.state=='OPEN')
def closed_findings(): return tuple(x for x in FINDINGS if x.state=='CLOSED')
def routing_blockers(): return tuple(x for x in FINDINGS if x.state=='OPEN' and x.routing_blocker)
def validate_findings():
 assert len({x.identifier for x in FINDINGS})==len(FINDINGS)
 assert {x.state for x in FINDINGS}<={'OPEN','CLOSED'}
 assert {x.identifier for x in closed_findings()}==CLOSED_IDS
 assert {x.identifier for x in open_findings()}==OPEN_IDS
 assert {x.identifier for x in routing_blockers()}==ROUTING_BLOCKER_IDS
 assert all(x.resolution_evidence for x in closed_findings())
