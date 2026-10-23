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

## Commit and publish

One-time setup for each clone (already enabled on Amy's current Mac):

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/install_hooks.py
```

Then edit Markdown, stage the changes you want, commit, and push:

```sh
git add Plants References Catalogue.md
git commit -m "Update plant guidance"
git push
```

The pre-commit hook generates and stages the JSON automatically from the **staged** Markdown. New published plants receive permanent IDs/slugs. Drafts stay excluded. Invalid records stop the commit. If a new plant needs an ID, fully stage that note first; the hook will not overwrite unstaged edits to it. Unstaged edits to the generated JSON must also be saved or staged first.

The hook never pushes automatically. It is tracked in `.githooks/`, but Git does not enable hooks automatically on another clone: run the installer there. GitHub CI independently checks the generated JSON. Do not use `--no-verify` for catalogue commits.

Manual export still works: `.venv/bin/python scripts/export_catalogue.py --assign-ids`. Update `catalogue_updated` in [[Catalogue]] when publishing reference changes. Personal Garden Notes remain ignored and are never added by the hook.

The 0melette site reads the generated JSON from main, so it receives changes after the commit is pushed. PMS reads that same format on an explicit import. **Its current importer adds missing records/fills blanks and preserves existing local values. It does not automatically overwrite previously imported fields.** This authoring change does not modify PMS code or its running database.

The former `Documents/My Garden Vault` folder is a preserved backup of the earlier snapshot. Edit this repository vault going forward.

## Care evidence for MCP and RAG

Use the topic labels in Templates/Plant inside the existing Care heading. Keep scope, conditions and source links beside the advice: these travel into care_notes in the JSON and Almanac evidence. A separate Sources & photo section is not exported as care evidence.

Distinguish species advice from verified cultivar traits. Water categories are not watering schedules; heavy-feeder categories are not fertiliser doses. Record unknowns instead of filling gaps with estimates. Keep seasonal calendars tied to their region. Use Management for checks, prevention and problem references.

Run `.venv/bin/python scripts/audit_care.py` to review published records missing care topics. This measures completeness, not horticultural correctness. Research flagged records before adding facts. After publication, existing PMS records need a reviewed refresh because its additive importer preserves populated fields; then re-index Almanac RAG. Verify the resulting evidence before claiming improved live answers.

For explicit care provenance, use `care_scope: species_guidance` or `cultivar_specific` and `cultivar_verification: not_applicable`, `not_assessed`, `unverified` or `verified`. These are exported as labelled lines in care_notes so existing consumers retain them. `not_assessed` does not mean verified or disproven. Use verified only with supporting evidence; retain source links and conditions beside each care topic.

## Completion report and AI provenance

The README tracks 27 public content properties and the six exported prose sections for each published plant. IDs, timestamps, personal links, grouping labels and provenance metadata are not completion targets. Empty lists and unknown regional labels count as gaps. Presence does not establish accuracy, applicability or a complete care answer.

Run `.venv/bin/python scripts/export_catalogue.py` to refresh both JSON and README; `--check` verifies both. The commit hook builds both from the staged notes. Fully stage or save README edits before committing so it can safely update the generated table.

For a researched AI addition, list the **Markdown property name or exact section heading** in `generated_fields`, and add matching `field_provenance`:

```yaml
generated_fields: [family]
field_provenance:
  family:
    method: ai_assisted_research
    checked_at: '2026-10-23'
    scope: species
    review_status: needs_review
    sources:
      - https://plants.ces.ncsu.edu/plants/ziziphus-jujuba/
```

Use `scope: cultivar` only for cultivar-specific evidence. Use `human_reviewed` only after a person reviews the actual value and source; AI research alone does not qualify. Keep inline source links and scope beside generated prose. When only part of a section is added, retain its existing text and visibly label the new passage. Do not retroactively label untouched material as generated or human verified. Keep provenance when editing a generated value, updating sources/date as appropriate.

The exporter validates matching flags, populated values, dates, source links, scope and review status. JSON retains the metadata and adds a short label to care_notes for existing consumers. A website badge would require a consumer UI change; this repo change supplies the data flag. Numeric planning estimates still belong in estimated_fields, independently of whether AI assisted their entry. Unsupported yields, calendar dates, relationships and photos remain empty.
