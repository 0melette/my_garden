# My Garden

A public, reusable plant-almanac dataset for developing the Plant Management
System and other garden tools. It includes plants, planting months, pests,
diseases, garden functions, uses, companion relationships, and attributed
reference images.

This repository is a curated reference dataset, not a live copy of anyone's
garden. Personal planting history, locations, accounts, chat history,
credentials, and the working SQLite database are deliberately excluded.

## What lives here

- `localdata/almanac.db` can be used as a private working SQLite database. It is intentionally ignored by Git and is not part of the public dataset.
- `localdata/plant_images/` stores plant photos. Images can be committed when their history is useful.
- `localdata/plant-growing-sources.json` records sources, estimates and Sydney calendar context for the seven October additions.
- `localdata/reference_images/` stores pest and disease photos; their record links, captions and licences are in `localdata/reference-image-sources.json`.
- `snapshots/almanac-catalogue.json` is a readable, versioned export of the public garden catalogue.
- `scripts/export_catalogue.py` refreshes that snapshot without exporting chat or AI-loop history.

Database schema and Alembic migrations stay in the Plant Management System repository so each app version travels with the schema it expects.

## Use it with the Almanac

```sh
export DATABASE_URL=sqlite:////path/to/my_garden/localdata/almanac.db
export PLANT_IMAGE_FOLDER=/path/to/my_garden/localdata/plant_images
```

Then start the Almanac normally from the application repository.

Plant Management System can also import the versioned JSON snapshot as optional
starter data. Importing makes a local copy: edits made in the application do
not write back to this repository. Publishing a new public dataset version is a
separate, deliberate export and Git commit.

### Updates and existing PMS databases

PMS does not continuously download catalogue changes. With
`LOAD_MY_GARDEN_SEED=true`, it fetches the snapshot on startup only when its
Almanac plant catalogue is empty. Existing databases can explicitly run the
Almanac `flask --app app import-my-garden` command to add missing records and
fill empty fields while preserving existing local values. Publishing here does
not run that command or modify any PMS database.

The current PMS importer understands plant photos. The separate pest/disease
image manifest is ready for consumers, but PMS needs explicit importer and UI
support before those pictures appear there.

See [the October catalogue additions](CATALOGUE-ADDITIONS.md) for the seven new
plants and illustrated pest/disease references. Variety photographs marked
“representative” are not verified photographs of that particular cultivar.

The October additions were edited in the public JSON snapshot; the ignored
working database was not changed. Do not export an older database over this
snapshot without first reconciling those additions.

## Save a catalogue version

```sh
python3 scripts/export_catalogue.py
git add snapshots/almanac-catalogue.json localdata/plant_images
git commit -m "data: update garden catalogue"
git push
```

The export includes plant references, planting months, image filenames, rotation groups, pests, diseases, functions, uses and their links. It deliberately excludes chat messages and model-loop records.

## Plant image sources

Pest and disease description references are recorded in [SOURCES.md](SOURCES.md).

Catalogue photos are stored in `localdata/plant_images/`. Their creator, licence,
source page and original URL are recorded in `localdata/plant-image-sources.json`.
To fill missing catalogue images from reusable Wikimedia Commons photography:

```sh
python3 scripts/fetch_plant_images.py
python3 scripts/export_catalogue.py
```

## Licence and attribution

Original dataset structure, original catalogue text, and documentation are
available under CC BY 4.0. Scripts are available under the MIT License.
Third-party images retain their individual licences and attribution recorded in
`localdata/plant-image-sources.json`. See [LICENSE.md](LICENSE.md) for the full
boundary.

## Later cloud database

Point `DATABASE_URL` at PostgreSQL and continue applying migrations from the application repository. Move uploaded images to private object storage and store only their keys or URLs in PostgreSQL. Do not commit credentials or production database dumps here.
