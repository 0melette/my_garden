# Edit the garden in Obsidian

[[My Garden|Open the garden]] · [[Collections/Drafts|Plant stubs]]

**This repository is the vault. `Plants/*.md` and `References/**/*.md` are the editable source.** The JSON snapshot is generated for the website and PMS, which keep their existing import format.

## Add a plant stub

1. Open **Plants**, choose **New note**, and name the plant. You can also use **New** in a plant Base; check that the note is inside Plants.
2. Press **⌘P**, choose **Templates: Insert template**, then **Plant**. Obsidian fills the note title. Bases does not automatically insert templates.
3. Fill Properties gradually: category is Herbs, Flowers, Fruit or Vegetables (a list; overlaps are allowed). Use full sun / part shade / full shade, and low / moderate / high water. Leave unknown values empty.
4. Write under **Summary**, **Sowing**, **Care**, **Management**, **Harvest** and **Uses**. These exact headings feed the generated catalogue. Sources & photo is supporting documentation.
5. Keep **status: draft** while incomplete. Drafts appear in [[Collections/Drafts]] but are excluded from the website/PMS export. Set status to **published** when ready. A published plant needs common_name, scientific_name and a permanent slug/ID (the exporter can allocate them).

The template and starter fields are [[Templates/Plant]]. For a terminal shortcut:

```sh
.venv/bin/python scripts/create_plant.py "New herb" --category Herbs
```

## Editing existing plants

- Change sun, water, spacing, pH, calendar and categories in Properties or the editable Base table.
- The body sections are the single editable copy of descriptive text. Do not rename their headings.
- `planting_months` is a list of Jan–Dec abbreviations; `calendar_region` identifies its climate. Read Sowing to distinguish seeds from divisions/cuttings.
- Preserve catalogue_id and slug after publication. Note names may change, but update companion links with them.
- `estimated_fields` retains explicit planning estimates. Missing values stay blank, not zero.
- Pests, diseases, functions, uses and rotation groups refer to names in References.
- Companions use a list of plant / function / notes mappings in YAML source mode. Example:

```yaml
companions:
  - plant: "[[Plants/Basil - Genovese]]"
    function: pollinator attractor
    notes: Allow room for both plants and let a few basil stems flower.
```

Photos go in `localdata/plant_images/`; set photo to `[[localdata/plant_images/filename.jpg]]` and add attribution to `localdata/plant-image-sources.json`.

## Personal notes

Use **Garden Notes**, including the **Choose my plants** view in [[Collections/My growing list]]. Growing, favourite, bed and observations are stored there and ignored by Git. Public Plants pages are reference material; anything written there is intended for the public repository. Put personal pictures in **Private Attachments**.

## Generate and publish

From the my_garden folder:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/export_catalogue.py --assign-ids
.venv/bin/python scripts/export_catalogue.py --check
```

`--assign-ids` assigns IDs/slugs only to new published plants that lack them, after validating the full catalogue. Existing IDs stay stable. Export never reads the working SQLite database or imports private journal text. Edit `catalogue_updated` in [[Catalogue]] before publishing.

Commit the edited Markdown, relevant public assets and regenerated `snapshots/almanac-catalogue.json` together, then push. GitHub CI rejects stale JSON; it does not silently publish a separate generated commit. There is no background auto-push.

The 0melette site reads the generated JSON from main, so it receives changes after the commit is pushed. PMS reads that same format on an explicit import. **Its current importer adds missing records/fills blanks and preserves existing local values. It does not automatically overwrite previously imported fields.** This authoring change does not modify PMS code or its running database.

The former `Documents/My Garden Vault` folder is a preserved backup of the earlier snapshot. Edit this repository vault going forward.
