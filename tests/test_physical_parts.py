import pytest

from generator.physical_parts import (
    TIMING_CAPACITOR_0805,
    TIMING_CAPACITOR_1206,
    timing_capacitor_footprint,
)


@pytest.mark.parametrize(
    ("value_nf", "expected"),
    (
        (0.1, TIMING_CAPACITOR_0805),
        (4.7, TIMING_CAPACITOR_0805),
        (22.0, TIMING_CAPACITOR_0805),
        (26.999, TIMING_CAPACITOR_0805),
        (27.0, TIMING_CAPACITOR_1206),
        (33.0, TIMING_CAPACITOR_1206),
    ),
)
def test_timing_capacitor_footprint_policy(value_nf, expected):
    assert timing_capacitor_footprint(value_nf) == expected


@pytest.mark.parametrize("value_nf", (0.0, -1.0))
def test_timing_capacitor_footprint_rejects_non_positive_values(value_nf):
    with pytest.raises(ValueError, match="must be positive"):
        timing_capacitor_footprint(value_nf)
