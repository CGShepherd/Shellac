"""Compatibility façade for physical component-selection policies.

New engineering policy belongs in :mod:`generator.component_selection`.
This module retains the established public imports used by the generator and
existing tests while the later approved-parts catalogue is developed.
"""

from generator.component_selection import (
    TIMING_CAPACITOR_0805,
    TIMING_CAPACITOR_1206,
    timing_capacitor_footprint,
)

__all__ = (
    "TIMING_CAPACITOR_0805",
    "TIMING_CAPACITOR_1206",
    "timing_capacitor_footprint",
)
