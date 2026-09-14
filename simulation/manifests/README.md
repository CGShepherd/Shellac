# Simulation manifests

`model_sources.yaml` is controlled source metadata.

`model_manifest.json` is generated evidence containing SHA-256 hashes of model and
template inputs. Regenerate it with:

```cmd
python -m simulation.scripts.shellac_spice manifest
```

Never use a generated hash manifest to justify silent edits to a reference model.
