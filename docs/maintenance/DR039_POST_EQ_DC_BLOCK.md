# DR-039 maintenance note

AE-074 implements DR-039 as a branch-local network inside SCH107. In each DIRECT/BYPASS branch, a 1 µF PET-film capacitor is followed by a 330 kΩ / 1% return to 0VA. The FILTER branch does not use this extra network because the SCH107 high-pass capacitors already provide intrinsic DC blocking.

The direct-branch nominal time constant is approximately 0.33 s; about 2 s is more than six direct-branch time constants. This does not replace RUN12 or prototype transient qualification.

Stable physical identities are retained: C30060/R30060 (left) and C35060/R35060 (right). After replacement verify the relevant DIRECT/BYPASS branch DC behaviour, FILTER/BYPASS operation, and replay response at 20 Hz.
