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

## Save a catalogue version

```sh
python3 scripts/export_catalogue.py
git add snapshots/almanac-catalogue.json localdata/plant_images
git commit -m "data: update garden catalogue"
git push
```

The export includes plant references, planting months, image filenames, rotation groups, pests, diseases, functions, uses and their links. It deliberately excludes chat messages and model-loop records.

## Plant image sources

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
