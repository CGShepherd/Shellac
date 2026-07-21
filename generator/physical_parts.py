"""Physical component-selection policies for Project Shellac.

These policies translate electrical requirements into provisional physical
packages. Manufacturer part numbers remain controlled by the later procurement
freeze.
"""

TIMING_CAPACITOR_0805 = "Capacitor_SMD:C_0805_2012Metric"
TIMING_CAPACITOR_1206 = "Capacitor_SMD:C_1206_3216Metric"


def timing_capacitor_footprint(value_nf: float) -> str:
    """Return the provisional solderable C0G footprint for a timing capacitor.

    Values at or above 27 nF use 1206 to improve the available range of
    conventional solder-terminated C0G/NP0 components. Smaller trimming values
    use 0805.

    This policy selects only the package. It does not freeze a manufacturer
    part number, tolerance, voltage rating, or supplier.
    """
    if value_nf <= 0:
        raise ValueError("timing capacitor value must be positive")
    if value_nf >= 27.0:
        return TIMING_CAPACITOR_1206
    return TIMING_CAPACITOR_0805
