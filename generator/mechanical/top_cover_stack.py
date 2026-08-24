"""G3-026 upper-cover and control bushing stack contract.

The METCASE M5502119 manufacturer drawing marks 2.00 mm as a typical sheet
thickness in the cover/base detail. G3-026 accepts 2.0 mm as the nominal upper
cover thickness for stack analysis, but does not treat an unspecified tolerance
as machining authority.
"""

from __future__ import annotations

from dataclasses import dataclass

TOP_COVER_NOMINAL_MM = 2.0
TOP_COVER_TOLERANCE_MM = None


@dataclass(frozen=True, slots=True)
class BushingStack:
    identifier: str
    mpn: str
    bushing_length_mm: float
    cover_nominal_mm: float
    thread_available_above_cover_mm: float
    final_hardware_stack_verified: bool
    machining_released: bool


GRAYHILL_STACK = BushingStack(
    "STACK-SW901-903",
    "Grayhill Series 71 selected rotaries",
    7.92,
    TOP_COVER_NOMINAL_MM,
    7.92 - TOP_COVER_NOMINAL_MM,
    False,
    False,
)

CK_STACK = BushingStack(
    "STACK-SW904-905",
    "C&K 7201SYCBE",
    8.89,
    TOP_COVER_NOMINAL_MM,
    8.89 - TOP_COVER_NOMINAL_MM,
    False,
    False,
)


def validate_top_cover_stack() -> None:
    assert TOP_COVER_NOMINAL_MM == 2.0
    assert TOP_COVER_TOLERANCE_MM is None
    assert abs(GRAYHILL_STACK.thread_available_above_cover_mm - 5.92) < 1e-9
    assert abs(CK_STACK.thread_available_above_cover_mm - 6.89) < 1e-9
    assert GRAYHILL_STACK.thread_available_above_cover_mm > 5.0
    assert CK_STACK.thread_available_above_cover_mm > 6.0
    assert not GRAYHILL_STACK.final_hardware_stack_verified
    assert not CK_STACK.final_hardware_stack_verified
    assert not GRAYHILL_STACK.machining_released
    assert not CK_STACK.machining_released
