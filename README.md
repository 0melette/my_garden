# My Garden

An Obsidian-first public plant reference catalogue for the 0melette website and Plant Management System.

**Markdown is the source of truth.** Open this repository folder as an Obsidian vault and start at [My Garden](My%20Garden.md). Edit plant pages and native Bases; no community plugin is needed.

- `Plants/*.md`: plant properties and editable Summary, Sowing, Care, Management, Harvest and Uses sections.
- `References/**/*.md`: pests, diseases, rotation groups, functions and uses.
- `Templates/Plant.md`: draft plant template. Use Obsidian’s Insert template command (⌘P → Templates: Insert template).
- `Bases/` and `Collections/`: categories, conditions, calendars and draft views.
- `snapshots/almanac-catalogue.json`: **generated compatibility output**, not an editing source.
- `localdata/plant_images/` and image manifests: attributed public photos.
- `Garden Notes/` and `Private Attachments/`: local personal material, excluded from Git and export.
- The working SQLite database remains ignored; it never overwrites the Markdown catalogue.

See [AUTHORING.md](AUTHORING.md) for the full editing and publishing workflow.

## Enable automatic export on commit

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/install_hooks.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/export_catalogue.py --check
```

Stage your Markdown, then commit normally: the pre-commit hook generates and stages matching JSON. Run `git push` when ready. Install the hook once per clone; it is already enabled on this Mac. CI checks that the JSON matches the Markdown. Drafts are excluded; invalid published records fail validation before the snapshot is replaced.

## Consumers

The 0melette site fetches the snapshot from this repository’s main branch. Pushing a complete export updates its source data.

PMS makes a local copy. With `LOAD_MY_GARDEN_SEED=true`, initial startup imports only into an empty catalogue. Existing databases can run `flask --app app import-my-garden` to add missing records and fill empty fields while preserving local values. It does **not** continually sync or overwrite existing non-empty fields. The pest/disease photo manifest still needs consumer UI/import support.

Schema and database migrations stay in the PMS repository. This repo remains public reference data, not a copy of anyone’s private garden, accounts or chat history.

## Sources and licences

See [SOURCES.md](SOURCES.md), [CATALOGUE-ADDITIONS.md](CATALOGUE-ADDITIONS.md), per-plant references, and the image/growing-source manifests. Missing numeric values are unknown; estimates are labelled. Cultivar photographs marked representative are not verified cultivar photographs.

Original catalogue text and structure: CC BY 4.0. Scripts: MIT. Third-party photos retain their individual licences. See [LICENSE.md](LICENSE.md).
