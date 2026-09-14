from generator.model.control_architecture import (
    EQ_CONTROLS,
    MATRIX,
    MATRIX_KNOB,
    MUTE,
    OPEN_QUALIFICATION,
    REG08_ROLE,
    RELATIVE_GEOMETRY,
    RUMBLE,
    SIGNAL_FLOW,
    validate_control_architecture,
)

def main() -> None:
    validate_control_architecture()
    print("Project Shellac AE-041 control architecture")
    print("Signal flow:", " -> ".join(SIGNAL_FLOW))
    print("EQ controls:")
    for c in EQ_CONTROLS:
        print(f"  {c.function} {c.channel}: {c.manufacturer} {c.family_or_mpn}, knob {c.knob_colour}")
    print("Rumble:", RUMBLE.mpn, RUMBLE.left_label, "/", RUMBLE.right_label)
    print("Matrix:", MATRIX.mpn, " / ".join(MATRIX.mode_order_ccw_to_cw))
    print("Matrix knob:", MATRIX_KNOB["mpn"])
    print("Mute:", MUTE.mpn, MUTE.left_label, "/", MUTE.right_label)
    print("REG-08:", REG08_ROLE)
    print("Relative geometry:", RELATIVE_GEOMETRY)
    print("Open qualification:")
    for item in OPEN_QUALIFICATION:
        print(" -", item)

if __name__ == "__main__":
    main()
