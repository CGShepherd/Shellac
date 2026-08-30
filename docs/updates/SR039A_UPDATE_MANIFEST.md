# SR-039A — dependency hotfix

SR-039 introduced a test-only `yaml` import even though PyYAML is not part of
the controlled Shellac Python environment.

This hotfix removes that unnecessary dependency. The release-evidence test now
checks the controlled YAML text directly.

No design, generator, schematic, BOM, layout, decision or manufacturing content
changes.
