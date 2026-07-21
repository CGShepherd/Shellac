# G3-010 — Interconnect and Harness Architecture Rev A0

## Decision

Project Shellac shall use two internal crimp-terminal families compatible with the user's SN-58B ratchet tool:

- JST VH (3.96 mm) for signal, control and indicator harnesses;
- Molex Mini-Fit Jr (4.2 mm) for regulated DC power.

The external two-box DC link remains a metal five-pin Neutrik XLR.

## Ownership ECO

J101, J201 and J901 remain electrical interface references but must not be populated as PCB-mounted XLR connectors. A controlled schematic ECO shall replace their PCB footprints with board-side harness interfaces while preserving signal names and pin assignments.

## Harness classes

- Microvolt analogue: shielded twisted pair or star-quad, AWG24, shortest route, 25 mm separation from power/control wiring.
- Line-level analogue: twisted pair, AWG22, routed in the output-side region.
- Regulated power: AWG18 Mini-Fit Jr, physically distinct, keyed by an unpopulated position.
- Control and indicator harnesses: JST VH, pin counts frozen after panel architecture.

## Shielding

Input and output XLR shells bond to chassis at panel entry. Signal returns remain separate from chassis. The external PSU cable uses both connector-shell bonding and a dedicated chassis conductor; neither shell continuity nor 0VA alone is relied upon as the chassis path.

## Crimp qualification

For every terminal/wire combination, make five samples and record:

1. terminal part number;
2. wire type and gauge;
3. SN-58B die cavity;
4. conductor-wing and insulation-wing inspection;
5. housing retention;
6. pull-test result.

Generic 'JST compatible' contacts are not approved substitutes without this qualification.
