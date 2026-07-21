"""SCH109 pin-aware controls and user-interface builder."""
from __future__ import annotations
from generator.core.components import Component, resistor, testpoint
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.controls import CONTROLS, INDICATORS, LED_CURRENT_A, LED_SERIES_RESISTANCE_OHM
CONTROL_NETS={"SW901":"BASS_SELECT","SW902":"TREBLE_SELECT","SW903":"MODE_SELECT","SW904":"RUMBLE_BYPASS","SW905":"MUTE_CONTROL"}
def _control_component(control,at):
    return Component(control.identifier,"ProjectShellac:Panel_Control_Block",f"{control.name.upper()} - {control.control_type}",at,footprint="",fields={"Function":control.electrical_function,"Positions":" / ".join(control.positions),"Switching":control.switching,"Mounting":control.mounting},on_board=False)
def _indicator_component(indicator,at):
    polarity="Anode fed from +18V resistor; cathode to 0VA" if indicator.rail=="+18V" else "Anode to 0VA; cathode fed through resistor from -18V"
    return Component(indicator.identifier,"ProjectShellac:Panel_LED_Block",f"{indicator.name} RAIL LED",at,footprint="",fields={"Function":f"{indicator.rail} rail-present indication","Nominal current":f"{indicator.nominal_current_a*1000:.2f} mA","Polarity":polarity,"Mounting":indicator.mounting},on_board=False,rotation=180.0 if indicator.rail == "+18V" else 0.0)
def add_controls(sheet):
    sheet.add_note("SCH109 HUMAN-REVIEWABLE: five panel controls and two independent rail indicators.")
    sheet.add_note("Control-state interfaces are arranged by function; their audio contacts remain on the owning sheets.")
    sheet.add_note("Rail indicators are shown as complete rail-resistor-LED-0VA branches with accessible test points.")
    positions=[Point(70,75),Point(190,75),Point(310,75),Point(130,165),Point(275,165)]
    for control,at in zip(CONTROLS,positions):
        c=sheet.add_component(_control_component(control,at)); sheet.connect_pin_to_net(c,"CONTROL",CONTROL_NETS[control.identifier],stub_dy=-10.0)
    for i,(indicator,x) in enumerate(zip(INDICATORS,(155,250))):
        y=230
        led=sheet.add_component(_indicator_component(indicator,Point(x,y)))
        r=sheet.add_component(resistor(
            f"R90{6+i}", f"{LED_SERIES_RESISTANCE_OHM:g}", Point(x,y-28),
            tolerance="1%", function=f"{indicator.rail} panel-LED current limiting",
            rotation=90.0,
        ))
        rail_pin = pin_position(r, "2")
        drive_pin = pin_position(r, "1")
        if indicator.rail == "+18V":
            led_drive = pin_position(led, "A")
            led_return = pin_position(led, "K")
        else:
            led_drive = pin_position(led, "K")
            led_return = pin_position(led, "A")

        # Place the test point so its electrical pin shares the resistor/LED
        # junction row. The TestPoint pin is 5.08 mm below its symbol origin in
        # sheet coordinates.
        tp=sheet.add_component(testpoint(
            f"TP990{1+i}", f"{indicator.rail}_LED_DRIVE",
            Point(x+35, led_drive.y-5.08),
        ))

        rail_start = Point(rail_pin.x, rail_pin.y - 10)
        sheet.connect_points(rail_start, rail_pin)
        sheet.add_label(indicator.rail, rail_start.x, rail_start.y)
        sheet.connect_points(drive_pin, led_drive)
        sheet.connect_points(pin_position(tp, "TP"), led_drive)

        # Both branches terminate at a clear 0VA label below the LED. For the
        # negative indicator, conventional current flows from 0VA through A-K,
        # then through the resistor to -18 V.
        return_end = Point(led_return.x, led_return.y + 10)
        sheet.connect_points(led_return, return_end)
        sheet.add_label("0VA", return_end.x, return_end.y)
    sheet.add_note(f"Nominal LED current: {LED_CURRENT_A*1000:.2f} mA.")
