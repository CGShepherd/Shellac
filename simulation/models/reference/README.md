# Reference models

Unchanged vendor/reference models belong here.

For every added model:
- retain the original file unchanged;
- record source/vendor, retrieval/version information, licence/use note and limitations;
- regenerate `simulation/manifests/model_manifest.json`;
- do not silently patch the reference file.

Compatibility changes belong in `simulation/models/wrappers/` or as explicit,
separately recorded patches.
