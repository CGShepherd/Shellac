# Project Shellac — Engineering Design Rules

**Status:** CONTROLLED BASELINE  
**Introduced:** SR-035

## Electrical and PCB
- Keep low-level and timing-critical signal paths short and preserve left/right symmetry where the function is symmetrical.
- Prevent sensitive input nodes from sharing uncontrolled return-current paths.
- Avoid signal-path electrolytics where a practical superior implementation exists; where an approved topology explicitly requires one, its technology is controlled by the relevant evidence.
- Provide appropriate local decoupling, useful test points and staged commissioning by functional block.
- Use consistent component orientation where it improves assembly, inspection or service.
- Use replaceable connectors for service interfaces where practical; avoid PCB removal for routine adjustment where practical.
- Physical footprints follow controlled component/footprint policy; a convenient library footprint is not evidence of an approved part.

## Mechanical and controls
- PCB/standoffs establish board position. Threaded control hardware may support/locate only after natural alignment and must not pull PCB or enclosure into position.
- Prefer PCB-mounted controls when electrical and mechanical requirements permit. Indicator implementation follows the selected mechanical architecture: PCB LEDs/light pipes are preferred when geometry is robust, while deliberately selected panel-bezel LEDs may use short serviceable flying leads.
- Manufacturing drilling coordinates require exact selected hardware, verified panel thickness/Z datum, PCB/control coordinates and washer/nut/knob stack.
- Prefer datum-based drilling dimensions to chained dimensions.
- Preserve deliberate mains, PE and SELV/analogue segregation and service-safe wiring.

## Procurement and BOM
- Select by engineering function/tier, not brand prestige.
- Exploit commonality and quantity pricing where every hard requirement is met.
- Record manufacturer, MPN, function, selection status, commonality group, rationale and evidence for approved physical parts.
- Distributor price and stock are dated procurement evidence, not permanent design invariants.
- Maintain credible second-source/substitution strategy where practical.
- Never silently substitute contact timing, pole count, dielectric, tolerance, voltage rating or mechanical interface.

## Change control
- Material changes record what changed, why, evidence, affected risks and the release where they became authoritative.
- Contradictions between historical intent and controlled artefacts are logged explicitly, not silently reconciled.
- Each package advances one primary engineering objective and ends with deterministic acceptance criteria.
