"""G3-027 Foundry audit for the independent optional 3180 us RIAA pole.

The third RIAA pole is an independent operator-controlled ON/BYPASS function.
It is intentionally NOT interlocked with Bass or Treble selector positions.

The integration blocker is narrower: the legacy TRUE RIAA bass branch still
contains an approximately 3180 us pole as well as the 318 us zero. If the
separate G3-026 3180 us stage is switched ON while that legacy branch is selected,
the 3180 us pole would be applied twice.

G3-027 therefore requires the TRUE-RIAA bass contribution to be resynthesised so
it no longer contains the 3180 us term. The independent downstream 3180 us stage
then remains free for the operator to combine with any Bass/Treble selection.
"""
from dataclasses import dataclass
from enum import Enum
from .replay_eq import RIAA_BASS_NETWORK
from .replay_eq_transfer import active_network_response

class IntegrationStatus(str, Enum):
    READY = 'ready'
    BLOCKED_DUPLICATED_3180 = 'blocked_duplicated_3180'

@dataclass(frozen=True)
class IntegrationAudit:
    status: IntegrationStatus
    legacy_true_riaa_pole_hz: float
    legacy_true_riaa_zero_hz: float
    independent_3180_stage_frozen: bool
    independent_operator_control_required: bool
    bass_treble_interlock_required: bool
    double_3180_possible_if_unmodified: bool
    required_action: str

def audit() -> IntegrationAudit:
    n = RIAA_BASS_NETWORK
    x = active_network_response(n.rf_ohm, n.rs_ohm, n.rg_ohm, n.capacitance_nf * 1e-9)
    legacy_has_3180 = abs(x.pole_hz - 50.0) < 1.0
    legacy_has_318 = abs(x.zero_hz - 500.0) < 10.0
    duplicated = legacy_has_3180 and legacy_has_318
    return IntegrationAudit(
        status=IntegrationStatus.BLOCKED_DUPLICATED_3180 if duplicated else IntegrationStatus.READY,
        legacy_true_riaa_pole_hz=x.pole_hz,
        legacy_true_riaa_zero_hz=x.zero_hz,
        independent_3180_stage_frozen=True,
        independent_operator_control_required=True,
        bass_treble_interlock_required=False,
        double_3180_possible_if_unmodified=duplicated,
        required_action=(
            'Resynthesise the TRUE-RIAA bass contribution without the 3180 us term; '
            'preserve the required 318 us behaviour, then place the independent '
            'operator-controlled 3180 us stage later in the chain.'
            if duplicated else 'Proceed to complete independent-control transfer verification.'
        ),
    )

def validate_integration_audit() -> None:
    a = audit()
    assert a.status is IntegrationStatus.BLOCKED_DUPLICATED_3180
    assert 49.0 < a.legacy_true_riaa_pole_hz < 51.0
    assert 490.0 < a.legacy_true_riaa_zero_hz < 510.0
    assert a.independent_3180_stage_frozen
    assert a.independent_operator_control_required
    assert not a.bass_treble_interlock_required
    assert a.double_3180_possible_if_unmodified
