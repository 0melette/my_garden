# Research pass — 23 October 2026

All 46 published records were audited; two drafts were excluded. This pass added 127 flagged properties/section contributions across 38 plants. Using the same 27-property/six-section definition, populated cells increased from 990/1518 (65%) to 1112/1518 (73%). Five additions extend already populated sections, so contribution counts differ from newly populated cells. Coverage is not a correctness or publication-readiness score.

## What changed

- Completed missing botanical families: all 46 now have a family. Families were checked against university extension species entries, Kew, NParks and ANPSA. Cultivar records inherit species-level taxonomy, not verified cultivar-specific traits.
- Supplied a source URL where missing: all 46 now have one. A new species/taxonomic URL supports the additions cited in field_provenance; it does not retrospectively support every old estimate, photo or cultivar claim in that record.
- Added basic species guidance to sparse basil, carrot, cucumber, strawberry, zucchini, eggplant, apple, lily-of-the-valley and other records. Kept original values and prose, including explicit estimates and unknowns.
- Added climbing support context for grape, moisture context for jujube, and seasonal dormancy/propagation context for musk mallow.
- Kept the source Markdown authoritative and regenerated the compatibility JSON and README from it.

## Evidence and limits

Each new field has exact URLs, checked date, species scope, method `ai_assisted_research` and status `needs_review` in the note's field_provenance. Generated prose also has inline source links. Read the individual field entries for the evidence used, rather than treating this overview as a source for every plant.

Principal sources include [NC State Extension Plant Toolbox](https://plants.ces.ncsu.edu/), [University of Minnesota carrot guidance](https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/growing-carrots-and-parsnips), [University of Maryland carrot guidance](https://www.extension.umd.edu/resource/growing-carrots-home-garden), [NParks Cyclea barbata](https://www.nparks.gov.sg/florafaunaweb/flora/5/5/5585), [Kew Bambusa oldhamii](https://powo.science.kew.org/taxon/urn%3Alsid%3Aipni.org%3Anames%3A392445-1), and [ANPSA musk mallow](https://anpsa.org.au/plant_profiles/abelmoschus-moschatus-subsp-tuberosus/).

Some NC State entries redirect to newer taxonomic names (radish and pea). Existing catalogue scientific names were preserved; the synonym relationship is explicit on those sources. ANPSA calls musk mallow Abelmoschus moschatus subsp. tuberosus; the existing supplier-style name is retained with that distinction in the prose.

## Why some fields remain blank

The README's expandable per-plant table is the remaining-work inventory. A gap can mean unknown, unresearched, or inapplicable; an empty relationship list does not assert absence.

- **Planting months and calendar region:** original calendars often lack a region. Northern Hemisphere dates cannot establish Sydney planting months. Local cultivar/propagation guidance is still needed; existing months were not reinterpreted.
- **Yield and harvest window:** need plant age, cultivar, growing system, climate and a stated unit/basis. A supplier's seasonal harvest listing does not establish how many weeks an individual plant will bear fruit. No arbitrary yields or durations were added.
- **Spacing, row spacing, feeding and pH:** broad species ranges or soil descriptions do not always establish a single scalar value. Rootstock, training and container/bed conditions matter. The missing tomato pH range is a sourced species recommendation, not a measurement of garden soil.
- **Water categories:** source descriptions of moist soil, drought tolerance or seasonal dieback were kept as prose where they did not justify one unqualified low/moderate/high category.
- **Companions, pests, diseases and functions:** no links were created just to improve the percentage. Existing general relationships were preserved; new associations need explicit evidence and the correct reference target.
- **Photos:** no unlicensed supplier pictures or unverified cultivar images were added.
- **Flowers and woody perennials:** succession sowing, vegetable rotation, numeric harvest windows or food-harvest instructions may be inapplicable. Missing fields were not populated with zero, invented values or generic filler.

All new contributions await human review. Existing material is not retroactively classified as human-written, researched or verified. These local changes do not update the website UI or refresh an existing PMS database/RAG index.
