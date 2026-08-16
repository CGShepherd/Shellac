"""Engineering policy for selecting physical component implementations.

The policy layer describes stable engineering requirements. It deliberately
stops before manufacturer-part approval, supplier selection, pricing, or stock
status; those belong to the later approved-parts catalogue.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ComponentFunction(str, Enum):
    """Electrical function used to select an appropriate component policy."""

    TIMING = "timing"
    COUPLING = "coupling"
    DECOUPLING = "decoupling"
    FEEDBACK = "feedback"
    COMPENSATION = "compensation"


class CapacitorDielectric(str, Enum):
    """Controlled capacitor dielectric classifications."""

    C0G_NP0 = "C0G/NP0"
    X7R = "X7R"
    FILM = "film"
    ELECTROLYTIC = "electrolytic"


@dataclass(frozen=True)
class ComponentRequirements:
    """Physical requirements derived from electrical design intent.

    ``preferred_footprints`` is ordered from most to least preferred. The first
    entry is the footprint emitted by the current generator. Later catalogue
    selection may use subsequent entries only when the engineering policy and
    layout contract explicitly permit it.
    """

    function: ComponentFunction
    dielectric: CapacitorDielectric
    tolerance_percent: float
    minimum_voltage_v: float
    preferred_footprints: tuple[str, ...]
    signal_path: bool
    notes: str = ""

    def __post_init__(self) -> None:
        if self.tolerance_percent <= 0:
            raise ValueError("component tolerance must be positive")
        if self.minimum_voltage_v <= 0:
            raise ValueError("component voltage rating must be positive")
        if not self.preferred_footprints:
            raise ValueError("at least one preferred footprint is required")
        if any(not footprint.strip() for footprint in self.preferred_footprints):
            raise ValueError("preferred footprints must be non-empty")

    @property
    def selected_footprint(self) -> str:
        """Return the current first-choice footprint."""

        return self.preferred_footprints[0]


TIMING_CAPACITOR_0805 = "Capacitor_SMD:C_0805_2012Metric"
TIMING_CAPACITOR_1206 = "Capacitor_SMD:C_1206_3216Metric"


def timing_capacitor_requirements(value_nf: float) -> ComponentRequirements:
    """Return the engineering requirements for a replay timing capacitor.

    Replay timing capacitors are signal-path parts and therefore require
    C0G/NP0 dielectric and 1% tolerance. Values at or above 27 nF prefer 1206
    because conventional solder-terminated C0G/NP0 availability becomes more
    restrictive; smaller values retain the established 0805 preference.

    The 50 V minimum rating is an engineering requirement, not a manufacturer
    part-number freeze.
    """

    if value_nf <= 0:
        raise ValueError("timing capacitor value must be positive")

    if value_nf >= 27.0:
        footprints = (TIMING_CAPACITOR_1206,)
    else:
        footprints = (TIMING_CAPACITOR_0805,)

    return ComponentRequirements(
        function=ComponentFunction.TIMING,
        dielectric=CapacitorDielectric.C0G_NP0,
        tolerance_percent=1.0,
        minimum_voltage_v=50.0,
        preferred_footprints=footprints,
        signal_path=True,
        notes="Replay equalisation timing capacitor; manufacturer part pending procurement freeze.",
    )


def timing_capacitor_footprint(value_nf: float) -> str:
    """Return the current first-choice timing-capacitor footprint."""

    return timing_capacitor_requirements(value_nf).selected_footprint
