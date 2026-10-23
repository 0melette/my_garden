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

## Initial research gaps (before the requested guesses)

The initial research pass left the following evidence gaps. These are now filled with separately labelled guesses where practical; the evidence itself has not improved.

- **Planting months and calendar region:** original calendars often lack a region. Northern Hemisphere dates cannot establish Sydney planting months. Local cultivar/propagation guidance is still needed; existing months were not reinterpreted.
- **Yield and harvest window:** need plant age, cultivar, growing system, climate and a stated unit/basis. A supplier's seasonal harvest listing does not establish how many weeks an individual plant will bear fruit. No arbitrary yields or durations were added.
- **Spacing, row spacing, feeding and pH:** broad species ranges or soil descriptions do not always establish a single scalar value. Rootstock, training and container/bed conditions matter. The missing tomato pH range is a sourced species recommendation, not a measurement of garden soil.
- **Water categories:** source descriptions of moist soil, drought tolerance or seasonal dieback were kept as prose where they did not justify one unqualified low/moderate/high category.
- **Companions, pests, diseases and functions:** no links were created just to improve the percentage. Existing general relationships were preserved; new associations need explicit evidence and the correct reference target.
- **Photos:** no unlicensed supplier pictures or unverified cultivar images were added.
- **Flowers and woody perennials:** succession sowing, vegetable rotation, numeric harvest windows or food-harvest instructions may be inapplicable. Missing fields were not populated with zero, invented values or generic filler.

All new contributions await human review. Existing material is not retroactively classified as human-written, researched or verified. These local changes do not update the website UI or refresh an existing PMS database/RAG index.


## User-requested planning guesses — 23 October 2026

After reviewing the missing fields, the user explicitly requested rough guesses. This subsequent pass added **410 unverified field/section estimates or applicability decisions across all 46 published plants**. No new sources were claimed. Original researched values and their provenance were preserved.

The README now counts **1474/1518 populated cells (97%), 40 explicitly inapplicable cells, and four unresolved photos**. Of the 410 estimates, eight mark retained legacy month lists as guessed Sydney calendars; this is an assumption, not a regional validation. The remaining 402 entries address original gaps (362 populated, 40 inapplicable). Coverage is still only field presence.

- Filled practical calendars, water categories, spacing, pH, feeding categories, yields and harvest windows with illustrative species-level values.
- Added possible pest/disease watch lists, flowering/pollinator roles and companion layout ideas. These are speculative, not observed diagnoses or proven relationships.
- Yields assume one established plant per crop/season; woody perennials assume maturity. Actual production may differ substantially. Spacing and row clearances depend on training and available space.
- Used explicit not-applicable reasons for absent numerical food-yield targets in ornamental/timber records and for routine succession sowing where it was not part of the plan.
- Kept four missing photos empty: bamboo, grape, jujube and musk mallow. Images and their attribution cannot be supplied by a numeric guess.

Each guess has method `ai_planning_estimate`, a generation date, an explicit assumption/basis, an empty sources list and `needs_review`. Populated guesses also appear in estimated_fields; N/A decisions appear in not_applicable_fields. The exported care_notes contains a clear UNVERIFIED AI PLANNING GUESSES label. These assumptions do not convert existing research gaps into sourced facts or change cultivar verification.
