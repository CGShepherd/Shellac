"""Current fail-closed pre-layout readiness oracle after AE-076D."""
from dataclasses import dataclass
from enum import Enum
class GateState(str,Enum): CLOSED='CLOSED'; READY_FOR_NEXT_ACTIVITY='READY_FOR_NEXT_ACTIVITY'; BLOCKED='BLOCKED'; HARDWARE_EVIDENCE_REQUIRED='HARDWARE_EVIDENCE_REQUIRED'
@dataclass(frozen=True,slots=True)
class ProductionGate: identifier:str; area:str; state:GateState; release_blocker:bool; evidence:str; next_action:str
GATES=(
 ProductionGate('ELEC-SIGNAL','Electrical architecture and design-driving qualification',GateState.BLOCKED,True,'AE-076C personality architecture is selected-next; physical migration and RUN08-RUN14 remain open under the AE-076D current qualification delta.','Migrate the personality/native interface, then execute RUN08-RUN14 before routing release.'),
 ProductionGate('ELEC-MEASURE','One-off hardware electrical acceptance',GateState.HARDWARE_EVIDENCE_REQUIRED,True,'Bench CMRR/noise/overload/switching/stability/PSU/fault correlation remain mandatory.','Execute on the one-off hardware after design-driving simulation and pre-fabrication recoverability closure.'),
 ProductionGate('MECH-ENCLOSURE','Enclosure and full assembly digital mock-up',GateState.BLOCKED,True,'AE-076B2C reconciles the M5502119 external body; internal datums and full service/interference assembly remain open.','Complete dimensionally controlled full assembly and service review.'),
 ProductionGate('MECH-CONTROLS','Seven direct-PCB controls and upper-cover service module',GateState.BLOCKED,True,'Exact NKK/C&K parts selected; exact B.Cu pin/pad/orientation mapping and common-plane fit remain open.','Close exact footprints/CAD, pin maps, B.Cu orientation, control XY/apertures and six-support stack.'),
 ProductionGate('MECH-TOP','Upper-cover machining and legend',GateState.BLOCKED,True,'Apertures/support datums are not frozen; R-017 legend generation remains open.','Freeze after control/support MCAD; generate legend programmatically.'),
 ProductionGate('PCB-OUTLINE','PCB outline and support ownership',GateState.READY_FOR_NEXT_ACTIVITY,True,'Current outline retained; MH1-MH4 interim while six PCB-to-cover supports remain selected-next.','Freeze six-support XY/Z/hardware/tolerance before replacing interim support geometry.'),
 ProductionGate('PCB-PLACEMENT','Pre-routing component/control placement',GateState.BLOCKED,True,'Current placement predates seven-control B.Cu and personality-interface migration.','Perform controlled migration only after exact footprints/MCAD close.'),
 ProductionGate('PCB-NATIVE','Native KiCad mechanical/model completeness',GateState.BLOCKED,True,'AE-076B2C proves H901 and capacitor model solutions; governed native binding remains open.','Bind exact models reproducibly and regenerate a zero-missing-model PCB STEP.'),
 ProductionGate('PCB-STACK','Four-layer stack, plane and DRC contract',GateState.BLOCKED,True,'Fabricator/bounded stack, In1 0VA plane and quantitative netclasses remain open.','Freeze stack/DRC/netclasses and instantiate/audit In1 0VA plane before first routing.'),
 ProductionGate('PCB-ROUTING','Native PCB routing',GateState.BLOCKED,True,'AE-076D quarantines historical SR-039/SR-041 release and SR-042 bootstrap executables; current routing authority remains false.','Release only after all design-driving/mechanical/model/stack/assurance blockers close.'),
 ProductionGate('PCB-FAB','Fabrication release',GateState.BLOCKED,True,'No routed/DRC-closed fabrication baseline exists.','After routing: DRC/ERC, Gerber/drill, return-path, fabrication and independent review.'),
 ProductionGate('BOM-CONTROLS','Control and personality hardware BOM',GateState.BLOCKED,True,'A30403RNCB is the single Matrix production part; personality interface is selected-next; physical migration remains open.','Complete exact control/personality footprints/CAD and procurement identities before BOM freeze.'),
 ProductionGate('BOM-GENERAL','General BOM/procurement',GateState.READY_FOR_NEXT_ACTIVITY,True,'Timing-cap decomposition and output ferrite selection remain open.','Complete RUN10/value engineering and exact remaining identities.'),
 ProductionGate('DOC-AUTHORITY','Decision/document/current-contract authority',GateState.CLOSED,False,'AE-076D reconciles stale findings, quarantines historical release executables, advances the current hold and publishes the qualification delta.','Maintain atomic authority updates as later work changes state.'),
 ProductionGate('DOC-COMMISSION','Commissioning / maintenance baseline',GateState.READY_FOR_NEXT_ACTIVITY,False,'Selected-next cartridge cards are not yet live maintenance authority.','Update service instructions atomically with live SCH101 migration.'),
 ProductionGate('DOC-RELEASE','Production design pack',GateState.BLOCKED,True,'Fabrication, measured acceptance, final BOM and release manifest remain incomplete.','Assemble only after routing, one-off hardware acceptance and independent assurance close.'),
 ProductionGate('REPRO-CLEANCLONE','Clean-clone reproducibility',GateState.BLOCKED,True,'Final production baseline not yet reproduced from an empty clone.','Perform after design/fabrication artefacts freeze.'),
 ProductionGate('REPO-HYGIENE','Repository production cleanup',GateState.READY_FOR_NEXT_ACTIVITY,False,'AE-076D closes the identified executable-authority debt; ordinary bounded hygiene continues.','Continue only when new evidence identifies a specific issue.'),
 ProductionGate('INFRA-EXTRACT','Foundry / Generator extraction',GateState.READY_FOR_NEXT_ACTIVITY,False,'Post-production activity only.','Defer until production clean-clone baseline.'),)
def gates_by_state(s): return tuple(g for g in GATES if g.state is s)
def release_blockers(): return tuple(g for g in GATES if g.release_blocker)
def validate_production_gates():
 assert len({g.identifier for g in GATES})==len(GATES) and len(GATES)>=15 and gates_by_state(GateState.BLOCKED) and gates_by_state(GateState.HARDWARE_EVIDENCE_REQUIRED) and all(g.next_action for g in GATES)
 assert next(g for g in GATES if g.identifier=='ELEC-SIGNAL').state is GateState.BLOCKED and next(g for g in GATES if g.identifier=='PCB-ROUTING').state is GateState.BLOCKED
 d=next(g for g in GATES if g.identifier=='DOC-AUTHORITY'); assert d.state is GateState.CLOSED and not d.release_blocker
