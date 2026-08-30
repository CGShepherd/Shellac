# DR-039 maintenance note

SCH103 is AC-coupled before rumble FILTER/BYPASS. Each channel uses 1 µF film in series followed by 330 kΩ to 0VA. Nominal time constant is approximately 0.33 s; allow about 2 s for conservative settling checks. Both rumble states must reject upstream static DC. After replacement verify DC at POST_EQ and replay response at 20 Hz.
