# SR-025C — Final ERC Type and Root-Net Closure

**Trigger:** SR-025B ERC: 1 error, 11 warnings.

## SCH106 error

J901 supply pins and PWR901/PWR902 were both declared as power outputs. J901
is now passive; the explicit rail-source symbols retain responsibility for
declaring the post-link rails driven.

## Root warnings

Repeated local labels are replaced by repeated global labels, each attached
to one short isolated stub. Singleton terminal interfaces remain local labels.
This removes direct diagonal root wiring and prevents unrelated output nets
from crossing or merging.
