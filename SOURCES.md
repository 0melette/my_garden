# Catalogue reference notes

The pest and disease descriptions are short recognition notes, paraphrased from
the references below. They are general guidance, not a diagnosis of a particular
plant. References checked on 1 October 2026.

| Record | Reference | Details supported |
| --- | --- | --- |
| Aphids | [RHS: Aphids](https://www.rhs.org.uk/biodiversity/aphids) | Sap feeding, colonies on young growth, distorted leaves and honeydew |
| Slugs and snails | [RHS: Slugs and snails](https://www.rhs.org.uk/biodiversity/slugs-and-snails) | Night feeding, holes in seedlings and soft leaves, and slime trails |
| Powdery mildew | [UC IPM: Powdery mildew on ornamentals](https://ipm.ucanr.edu/home-and-landscape/powdery-mildew-on-ornamentals/) | Pale powdery growth, spacing and air movement |

Existing plant source links remain in each plant's `source_url` field. Missing
plant descriptions remain blank until a suitable reference is checked.

## Plant additions — 2 October 2026

The seven additions now include structured growing fields and a **Sydney / warm-temperate** planting calendar. UK calendar months are not copied. Australian mild-climate sowing guidance is used for parsley, okra and Lazy Housewife; local seasons are explicitly translated for runner beans and mint propagation. General tomato guidance is labelled as such for Sweet 1000.

Spacing choices, qualitative badges and other estimates are labelled in each record’s care notes and `estimated_fields`. Exact yield weights and inapplicable repeat-sowing intervals stay null; harvest guidance is supplied as text. Maturity days are not entered as harvest-window weeks. Additional references and per-plant source IDs are recorded in [plant-growing-sources.json](localdata/plant-growing-sources.json).

| Record | Reference | Details supported |
| --- | --- | --- |
| Parsley | [RHS growing guide](https://www.rhs.org.uk/herbs/parsley/grow-your-own) | Biennial habit, curly/flat forms, sun or partial shade, slow germination, leaf harvest |
| Okra | [RHS growing guide](https://www.rhs.org.uk/vegetables/okra/grow-your-own) | Warm growing conditions, immature pods, frost protection |
| Bean - Lazy Housewife | [Greenpatch Organic Seeds](https://greenpatchseeds.com.au/products/bean-climbing-lazy-housewife) | Phaseolus vulgaris, climbing habit, young stringless pods, Australian spring/summer sowing |
| Bean - Scarlet Runner | [Yates](https://www.yates.com.au/heirloom-beans-climbing-scarlet-runner/) | Climbing support, perennial habit, red flowers, temperate/cool sowing guidance |
| Tomato - Sweet 1000 | [HRSeeds variety list](https://www.hrseeds.com/pepper-and-tomato-seed-list) | Name appears in the supplier list; exact packet identity and cultivar traits remain unverified. Kept separate from Sweet 100 and Sweet Million. |
| Vietnamese Mint | [RHS profile](https://www.rhs.org.uk/plants/118209/persicaria-odorata/details) and [Gardening Australia](https://www.abc.net.au/gardening/plant-finder/vietnamese-mint/9672278) | Persicaria odorata, Polygonaceae, culinary leaves, moisture, spreading roots and cuttings. Taxonomy follows RHS; the ABC page has a conflicting family label. |
| Chocolate Mint | [RHS Plants](https://www.rhsplants.co.uk/plants/_/mentha--piperita-f-citrata-chocolate/classid.2000012671/) | Cultivar name, moist soil, sun/light shade, root containment, division and leaf harvest |

“Red scarlet bean” is interpreted as Scarlet Runner. Reusable photographs and
their individual licence/source records are stored in the two image manifests.
The common bean and cherry tomato pictures are representative species images,
not evidence of the named cultivars' appearance. Powdery mildew is shown on a
maple leaf as an example of visible symptoms, not as a crop-specific diagnosis.

## Structured field sources and interpretation

| Records | Additional reference | Fields / interpretation |
| --- | --- | --- |
| Parsley | [Eden Seeds](https://www.edenseeds.com.au/Product-Info-seeds?product=parsley-italian), [UMN parsley sheet](https://rvs.umn.edu/Uploads/EducationalMaterials/35181a07-10a3-4430-a86d-8222ab716801..pdf) | Mild-climate months, sowing depth, spacing range and pH. Single spacing values use the wider end of the range. |
| Okra | [Eden Seeds](https://www.edenseeds.com.au/Product-Info-Seeds?product=okra-emerald), [USU Extension](https://extension.usu.edu/yardandgarden/research/okra-in-the-garden) | General okra calendar/spacing, pH, water, nitrogen and pod harvest; not Emerald-specific traits. |
| Lazy Housewife | [Eden Seeds](https://www.edenseeds.com.au/Product-Info-Seeds?product=bean-climbing-lazy-wife), [UMN beans](https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/growing-beans), [Yates beans](https://www.yates.com.au/how-to-grow/beans/) | Australian calendar, spacing, pH, legume category and care. A 21-day optional succession is an interpretation of “every few weeks”. |
| Scarlet Runner | [RHS runner beans](https://www.rhs.org.uk/vegetables/runner-beans/grow-your-own) and the bean references above | Harvest-window baseline, water and pests. Climbing-bean spacing/pH is marked provisional; heat may reduce Sydney pod set. |
| Sweet 1000 | [Eden Australian calendar](https://edenseeds.com.au/flux-content/eden/pdf/EdenSeedsCatalogue2021-WEB.pdf), [Maryland tomatoes](https://www.extension.umd.edu/resource/growing-tomatoes-home-garden), [UMN tomatoes](https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/growing-tomatoes) | General tomato months, spacing, feeding, water and pH, not verified cultivar performance. |
| Vietnamese Mint | [Mudbrick Herb Cottage](https://www.herbcottage.com.au/products/vietnamese-mint) | Australian light, moisture and cutting season. Spacing is an explicit provisional layout allowance; numeric pH limits remain unknown. |
| Chocolate Mint | [Mudbrick Herb Cottage](https://www.herbcottage.com.au/products/chocolate-mint), [USU mint](https://extension.usu.edu/yardandgarden/research/mint-in-the-garden), [UMN herbs](https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/growing-herbs) | Containment, moisture and propagation. Single spacing and general herb pH are marked estimates; spring/autumn translated to Australian months. |

No arbitrary companion or disease links are added merely to fill a panel. The
new bean records carry the nitrogen-fixer function; Scarlet Runner also has an
ornamental use. Pest links are added where the cited growing guides support them.
