"""Project Shellac engineering-model baseline, Revision A.

This captures architecture and interfaces only.  It intentionally does not
claim detailed circuit completion for blocks whose schematics remain pending.
"""

from __future__ import annotations

from .core import (
    Constraint,
    Direction,
    FunctionalBlock,
    GroundDomain,
    Interface,
    PowerDomain,
    ProjectModel,
    Signal,
    SignalKind,
)


def _interface(name: str, signal: str, direction: Direction, description: str = "") -> Interface:
    return Interface(name=name, signal=signal, direction=direction, description=description)


def build_shellac_model() -> ProjectModel:
    project = ProjectModel(
        identifier="PSH",
        name="Project Shellac",
        revision="Engineering Model Rev A",
        purpose="Balanced replay preamplifier for 78 rpm records with selectable replay equalisation.",
        power_domains=[
            PowerDomain("+18V", "+18 VDC", "Positive audio rail from the external regulated PSU."),
            PowerDomain("-18V", "-18 VDC", "Negative audio rail from the external regulated PSU."),
        ],
        ground_domains=[
            GroundDomain("0VA", "Audio reference and signal return."),
            GroundDomain("CHASSIS", "Protective chassis and cable-screen domain."),
        ],
        constraints=[
            Constraint(
                "PSH-C-001",
                "The Engineering Model is the single source of architectural truth.",
                "Prevents divergence between generated artefacts.",
                "Automated model-validation test.",
            ),
            Constraint(
                "PSH-C-002",
                "0VA and CHASSIS shall remain separate except at the defined bond network.",
                "Controls hum-current paths and preserves the agreed grounding architecture.",
                "Schematic review and continuity test.",
            ),
        ],
    )

    # Project-level signal catalogue.
    signal_specs = [
        ("INPUT_L_POS", SignalKind.ANALOG, "Left cartridge positive input."),
        ("INPUT_L_NEG", SignalKind.ANALOG, "Left cartridge negative input."),
        ("INPUT_R_POS", SignalKind.ANALOG, "Right cartridge positive input."),
        ("INPUT_R_NEG", SignalKind.ANALOG, "Right cartridge negative input."),
        ("PRE_EQ_L", SignalKind.ANALOG, "Left-channel signal presented to replay equalisation."),
        ("PRE_EQ_R", SignalKind.ANALOG, "Right-channel signal presented to replay equalisation."),
        ("POST_EQ_L", SignalKind.ANALOG, "Left-channel replay-equalised signal."),
        ("POST_EQ_R", SignalKind.ANALOG, "Right-channel replay-equalised signal."),
        ("FILTERED_L", SignalKind.ANALOG, "Rumble-filter output, left."),
        ("FILTERED_R", SignalKind.ANALOG, "Rumble-filter output, right."),
        ("BUFFERED_L", SignalKind.ANALOG, "Final-gain output, left."),
        ("BUFFERED_R", SignalKind.ANALOG, "Final-gain output, right."),
        ("MODE_L", SignalKind.ANALOG, "Mode-selected left-channel signal."),
        ("MODE_R", SignalKind.ANALOG, "Mode-selected right-channel signal."),
        ("OUTPUT_L_POS", SignalKind.ANALOG, "Balanced left output positive."),
        ("OUTPUT_L_NEG", SignalKind.ANALOG, "Balanced left output negative."),
        ("OUTPUT_R_POS", SignalKind.ANALOG, "Balanced right output positive."),
        ("OUTPUT_R_NEG", SignalKind.ANALOG, "Balanced right output negative."),
        ("BASS_SELECT", SignalKind.CONTROL, "Replay bass-characteristic switch state."),
        ("TREBLE_SELECT", SignalKind.CONTROL, "Replay treble-characteristic switch state."),
        ("MODE_SELECT", SignalKind.CONTROL, "Stereo/mono routing selection."),
        ("RUMBLE_BYPASS", SignalKind.CONTROL, "Rumble-filter bypass selection."),
        ("MUTE_CONTROL", SignalKind.CONTROL, "Mechanical output-mute state."),
        ("+18V", SignalKind.POWER, "Positive regulated rail."),
        ("-18V", SignalKind.POWER, "Negative regulated rail."),
        ("0VA", SignalKind.GROUND, "Audio reference."),
        ("CHASSIS", SignalKind.GROUND, "Chassis and screen domain."),
    ]
    project.signals.extend(Signal(*spec) for spec in signal_specs)

    input_block = FunctionalBlock(
        identifier="SCH101",
        name="Balanced Input and Differential Conversion",
        purpose="Receive both cartridge channels, control RF ingress and provide low-noise differential conversion.",
        implementation_ref="generator.blocks.balanced_input:add_sch101_diff_converter_slice",
        interfaces=[
            _interface("L+", "INPUT_L_POS", Direction.INPUT),
            _interface("L-", "INPUT_L_NEG", Direction.INPUT),
            _interface("R+", "INPUT_R_POS", Direction.INPUT),
            _interface("R-", "INPUT_R_NEG", Direction.INPUT),
            _interface("OUT_L", "PRE_EQ_L", Direction.OUTPUT),
            _interface("OUT_R", "PRE_EQ_R", Direction.OUTPUT),
            _interface("+V", "+18V", Direction.POWER),
            _interface("-V", "-18V", Direction.POWER),
            _interface("0VA", "0VA", Direction.GROUND),
            _interface("CHASSIS", "CHASSIS", Direction.GROUND),
        ],
        constraints=[
            Constraint("SCH101-C-001", "Present high input impedance to the cartridge."),
            Constraint("SCH101-C-002", "Provide matched left/right signal paths."),
            Constraint("SCH101-C-003", "Provide accessible test points."),
            Constraint("SCH101-C-004", "Provide matched internal 14/18/22 dB gain selection; 18 dB is default."),
        ],
    )

    eq_block = FunctionalBlock(
        identifier="SCH103",
        name="Replay Equalisation",
        purpose="Implement the agreed ESP Project 91 replay-equalisation topology and selectable curves.",
        implementation_ref="generator.blocks.replay_eq:add_replay_equalisation",
        interfaces=[
            _interface("IN_L", "PRE_EQ_L", Direction.INPUT),
            _interface("IN_R", "PRE_EQ_R", Direction.INPUT),
            _interface("OUT_L", "POST_EQ_L", Direction.OUTPUT),
            _interface("OUT_R", "POST_EQ_R", Direction.OUTPUT),
            _interface("BASS", "BASS_SELECT", Direction.INPUT),
            _interface("TREBLE", "TREBLE_SELECT", Direction.INPUT),
            _interface("+V", "+18V", Direction.POWER),
            _interface("-V", "-18V", Direction.POWER),
            _interface("0VA", "0VA", Direction.GROUND),
        ],
        constraints=[
            Constraint("SCH103-C-001", "Retain the agreed ESP P91 equalisation topology."),
            Constraint("SCH103-C-002", "Support the selected 78 rpm curves and RIAA settings."),
            Constraint("SCH103-C-003", "Provide a dedicated true-RIAA 3180/318 us bass branch paired with the 2121 Hz treble position."),
        ],
    )

    buffer_block = FunctionalBlock(
        identifier="SCH104",
        name="Post-EQ Buffer and Gain",
        purpose="Provide the final fixed gain after infrasonic filtering.",
        implementation_ref="generator.blocks.final_gain:add_final_gain",
        interfaces=[
            _interface("IN_L", "FILTERED_L", Direction.INPUT),
            _interface("IN_R", "FILTERED_R", Direction.INPUT),
            _interface("OUT_L", "BUFFERED_L", Direction.OUTPUT),
            _interface("OUT_R", "BUFFERED_R", Direction.OUTPUT),
            _interface("+V", "+18V", Direction.POWER),
            _interface("-V", "-18V", Direction.POWER),
            _interface("0VA", "0VA", Direction.GROUND),
        ],
        constraints=[
            Constraint("SCH104-C-001", "Provide unity gain in both channels; THAT1646 supplies the final 2.000x differential gain."),
            Constraint("SCH104-C-002", "Provide a low-impedance isolated drive to SCH105 without altering the signal-chain gain."),
            Constraint("SCH104-C-003", "Provide input and output test points per channel."),
        ],
    )

    mode_block = FunctionalBlock(
        identifier="SCH105",
        name="Channel Mode Matrix",
        purpose="Provide stereo, dual-left mono, dual-right mono and arithmetic-average L+R mono operation.",
        implementation_ref="generator.blocks.mode_matrix:add_mode_matrix",
        interfaces=[
            _interface("IN_L", "BUFFERED_L", Direction.INPUT),
            _interface("IN_R", "BUFFERED_R", Direction.INPUT),
            _interface("SELECT", "MODE_SELECT", Direction.INPUT),
            _interface("OUT_L", "MODE_L", Direction.OUTPUT),
            _interface("OUT_R", "MODE_R", Direction.OUTPUT),
            _interface("+V", "+18V", Direction.POWER),
            _interface("-V", "-18V", Direction.POWER),
            _interface("0VA", "0VA", Direction.GROUND),
        ],
        constraints=[
            Constraint("SCH105-C-001", "Provide the four frozen channel modes without gain in stereo or dual-mono modes."),
            Constraint("SCH105-C-002", "L+R mode shall produce the arithmetic average on both outputs."),
            Constraint("SCH105-C-003", "The mono summing network shall be disconnected outside L+R mode."),
        ],
    )

    filter_block = FunctionalBlock(
        identifier="SCH107",
        name="Rumble Filter",
        purpose="Remove infrasonic energy before the final gain and mode-routing stages.",
        implementation_ref="generator.blocks.rumble_filter:add_rumble_filter",
        interfaces=[
            _interface("IN_L", "POST_EQ_L", Direction.INPUT),
            _interface("IN_R", "POST_EQ_R", Direction.INPUT),
            _interface("BYPASS", "RUMBLE_BYPASS", Direction.INPUT),
            _interface("OUT_L", "FILTERED_L", Direction.OUTPUT),
            _interface("OUT_R", "FILTERED_R", Direction.OUTPUT),
            _interface("+V", "+18V", Direction.POWER),
            _interface("-V", "-18V", Direction.POWER),
            _interface("0VA", "0VA", Direction.GROUND),
        ],
    )

    output_block = FunctionalBlock(
        identifier="SCH108",
        name="Balanced Output and Mute",
        purpose="Drive floating balanced XLR outputs and provide the agreed mechanical input mute.",
        implementation_ref="generator.blocks.balanced_output:add_balanced_output",
        interfaces=[
            _interface("IN_L", "MODE_L", Direction.INPUT),
            _interface("IN_R", "MODE_R", Direction.INPUT),
            _interface("MUTE", "MUTE_CONTROL", Direction.INPUT),
            _interface("L+", "OUTPUT_L_POS", Direction.OUTPUT),
            _interface("L-", "OUTPUT_L_NEG", Direction.OUTPUT),
            _interface("R+", "OUTPUT_R_POS", Direction.OUTPUT),
            _interface("R-", "OUTPUT_R_NEG", Direction.OUTPUT),
            _interface("+V", "+18V", Direction.POWER),
            _interface("-V", "-18V", Direction.POWER),
            _interface("0VA", "0VA", Direction.GROUND),
            _interface("CHASSIS", "CHASSIS", Direction.GROUND),
        ],
    )

    power_entry = FunctionalBlock(
        identifier="SCH106",
        name="Audio-Box Power Entry and Ground Bond",
        purpose="Receive regulated dual rails and implement the controlled 0VA-to-chassis bond.",
        implementation_ref="generator.blocks.power_entry:add_power_entry",
        interfaces=[
            _interface("+18V_OUT", "+18V", Direction.OUTPUT),
            _interface("-18V_OUT", "-18V", Direction.OUTPUT),
            _interface("0VA_OUT", "0VA", Direction.GROUND),
            _interface("CHASSIS", "CHASSIS", Direction.GROUND),
        ],
        constraints=[
            Constraint(
                "SCH106-C-001",
                "0VA and CHASSIS shall connect only through the defined bond network.",
            ),
            Constraint("SCH106-C-002", "Provide test points for both rails and both ground domains."),
        ],
    )

    controls = FunctionalBlock(
        identifier="SCH109",
        name="Controls and User Interface",
        purpose="Represent all external operating controls and the two rail-present indicators.",
        implementation_ref="generator.blocks.controls:add_controls",
        interfaces=[
            _interface("BASS", "BASS_SELECT", Direction.OUTPUT),
            _interface("TREBLE", "TREBLE_SELECT", Direction.OUTPUT),
            _interface("MODE", "MODE_SELECT", Direction.OUTPUT),
            _interface("RUMBLE", "RUMBLE_BYPASS", Direction.OUTPUT),
            _interface("MUTE", "MUTE_CONTROL", Direction.OUTPUT),
            _interface("+V", "+18V", Direction.POWER),
            _interface("-V", "-18V", Direction.POWER),
            _interface("0VA", "0VA", Direction.GROUND),
            _interface("CHASSIS", "CHASSIS", Direction.GROUND),
        ],
    )

    project.blocks.extend([
        input_block,
        eq_block,
        filter_block,
        buffer_block,
        mode_block,
        power_entry,
        output_block,
        controls,
    ])
    return project
