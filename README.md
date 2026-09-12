# My Garden data

Private local data for the Plant Management System.

## What lives here

- `localdata/almanac.db` is the working SQLite database. It is intentionally ignored by Git.
- `localdata/plant_images/` stores plant photos. Images can be committed when their history is useful.
- `snapshots/almanac-catalogue.json` is a readable, versioned export of the public garden catalogue.
- `scripts/export_catalogue.py` refreshes that snapshot without exporting chat or AI-loop history.

Database schema and Alembic migrations stay in the Plant Management System repository so each app version travels with the schema it expects.

## Use it with the Almanac

```sh
export DATABASE_URL=sqlite:////Users/amyzhou/Documents/my_garden/localdata/almanac.db
export PLANT_IMAGE_FOLDER=/Users/amyzhou/Documents/my_garden/localdata/plant_images
```

Then start the Almanac normally from the application repository.

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

## Later cloud database

Point `DATABASE_URL` at PostgreSQL and continue applying migrations from the application repository. Move uploaded images to private object storage and store only their keys or URLs in PostgreSQL. Do not commit credentials or production database dumps here.
