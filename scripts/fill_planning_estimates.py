"""Fill blank public fields with explicitly UNSOURCED Sydney planning guesses.

Run deliberately, then review the diff. Existing populated values and researched
provenance are preserved. Photos and private notes are never touched.
"""
from copy import deepcopy
from export_markdown import ROOT, ALIASES, SECTIONS, read_note, write_note, sections

DATE = '2026-10-23'
REGION = 'Sydney / warm temperate'
ASSUMPTIONS = ('User-requested AI guess, not researched or measured. Sydney lowland home garden, '
               'outdoor soil beds, ordinary care and irrigation; avoid frost and extreme heat. '
               'Yield is total per established plant per crop/season, not per picking; '
               'woody perennials assume a mature established plant. Row spacing is a planning '
               'clearance, not a tested crop density. Pest/disease lists are possible monitoring '
               'targets, not observations. Companion/function suggestions are layout ideas, '
               'not demonstrated pest control or yield benefits.')


def profile(months, spacing=40, row=60, ph=(6.0, 7.0), water='moderate',
            feeder='light feeder', yield_qty=0.2, weeks=8, succession=None,
            layer='herbaceous', rotation='Perennials', ornamental=False):
    return dict(planting_months=months.split(), spacing_cm=spacing, row_spacing_cm=row,
                soil_ph_min=ph[0], soil_ph_max=ph[1], water=water, feeder=feeder,
                yield_qty=yield_qty, yield_unit='kg', harvest_window_weeks=weeks,
                succession_interval_days=succession, forest_layer=layer,
                rotation_group=rotation, ornamental=ornamental)


PROFILES = {
    'Lobularia maritima': profile('Mar Apr May Aug Sep Oct', 20, 30, ornamental=True, rotation='Anywhere'),
    'Bambusa oldhamii': profile('Sep Oct Nov Mar Apr', 400, 500, layer='canopy', ornamental=True),
    'Ocimum basilicum': profile('Sep Oct Nov Dec Jan Feb', 30, 40, ph=(6, 7.5), yield_qty=0.2, weeks=16, succession=28),
    'Phaseolus vulgaris': profile('Sep Oct Nov Dec Jan Feb', 20, 90, yield_qty=1, weeks=8, succession=21, layer='vine', rotation='Legumes'),
    'Phaseolus coccineus': profile('Sep Oct Nov Dec Jan', 30, 120, yield_qty=1.5, weeks=12, layer='vine', rotation='Legumes'),
    'Monarda citriodora': profile('Mar Apr Sep Oct', 30, 45, yield_qty=0.1, weeks=8),
    'Brassica oleracea': profile('Feb Mar Apr May', 60, 75, feeder='heavy feeder', yield_qty=0.5, weeks=6, rotation='Brassicas'),
    'Allium fistulosum': profile('Feb Mar Apr May Aug Sep Oct', 10, 30, yield_qty=0.1, weeks=8, succession=21, rotation='Alliums'),
    'Daucus carota': profile('Feb Mar Apr May Aug Sep Oct Nov', 5, 30, ph=(6, 7), yield_qty=0.1, weeks=4, succession=21, layer='rhizosphere', rotation='Roots'),
    'Mentha × piperita f. citrata \'Chocolate\'': profile('Mar Apr Sep Oct Nov', 40, 60, yield_qty=0.3, weeks=24),
    'Solanum melongena': profile('Sep Oct Nov Dec', 60, 90, water='high', feeder='heavy feeder', yield_qty=1.5, weeks=12, rotation='Solanums'),
    'Vitis vinifera': profile('Jun Jul Aug Sep', 200, 250, ph=(6, 7.5), yield_qty=8, weeks=4, layer='vine'),
    'Cyclea barbata': profile('Sep Oct Nov Dec', 100, 150, yield_qty=0.5, weeks=20, layer='vine'),
    'Armoracia rusticana': profile('Jul Aug Sep', 45, 60, yield_qty=0.3, weeks=4, layer='rhizosphere'),
    'Hyssopus officinalis': profile('Mar Apr Sep Oct', 40, 50, water='low', yield_qty=0.1, weeks=16, layer='shrub'),
    'Hovenia dulcis': profile('Jun Jul Aug Sep', 600, 800, yield_qty=5, weeks=4, layer='canopy'),
    'Ziziphus jujuba': profile('Jun Jul Aug Sep', 400, 500, yield_qty=10, weeks=6, layer='canopy'),
    'Cucumis sativus': profile('Sep Oct Nov Dec Jan Feb', 60, 100, ph=(6, 7), water='high', feeder='heavy feeder', yield_qty=3, weeks=8, succession=28, layer='vine', rotation='Cucurbits'),
    'Cucurbita pepo': profile('Sep Oct Nov Dec Jan', 90, 120, ph=(6, 7.5), water='moderate', feeder='heavy feeder', yield_qty=3, weeks=8, succession=28, rotation='Cucurbits'),
    'Lactuca sativa': profile('Feb Mar Apr May Jun Jul Aug Sep Oct', 25, 35, yield_qty=0.25, weeks=4, succession=14, rotation='Anywhere'),
    'Convallaria majalis': profile('Jun Jul Aug', 20, 30, layer='groundcover', ornamental=True),
    'Tagetes patula': profile('Sep Oct Nov Dec Jan', 25, 35, ornamental=True, rotation='Anywhere'),
    'Abelmoschus moschatus tuberosus': profile('Sep Oct Nov', 75, 100, layer='herbaceous', ornamental=True),
    'Abelmoschus esculentus': profile('Oct Nov Dec Jan', 40, 75, water='moderate', yield_qty=0.5, weeks=10, rotation='Anywhere'),
    'Petroselinum crispum': profile('Feb Mar Apr Aug Sep Oct', 25, 40, yield_qty=0.2, weeks=24),
    'Pisum sativum': profile('Mar Apr May Jun Jul Aug', 10, 60, yield_qty=0.25, weeks=6, succession=21, rotation='Legumes'),
    'Raphanus sativus': profile('Mar Apr May Aug Sep', 10, 30, yield_qty=0.2, weeks=3, succession=21, layer='rhizosphere', rotation='Brassicas'),
    'Malus domestica': profile('Jun Jul Aug', 200, 150, yield_qty=5, weeks=4, layer='shrub'),
    'Fragaria × ananassa': profile('Apr May Jun Jul Aug', 30, 60, ph=(5.5, 6.5), yield_qty=0.4, weeks=12, layer='groundcover'),
    'Helianthus annuus': profile('Sep Oct Nov Dec Jan', 45, 60, succession=21, ornamental=True, rotation='Anywhere'),
    'Zea mays': profile('Sep Oct Nov Dec Jan', 30, 60, feeder='heavy feeder', yield_qty=0.3, weeks=3, succession=21, rotation='Anywhere'),
    'Ipomoea batatas': profile('Oct Nov Dec Jan', 40, 100, yield_qty=1, weeks=4, layer='groundcover'),
    'Solanum lycopersicum': profile('Sep Oct Nov Dec', 60, 90, water='moderate', feeder='heavy feeder', yield_qty=3, weeks=12, rotation='Solanums'),
    'Persicaria odorata': profile('Sep Oct Nov Dec Mar Apr', 40, 60, ph=(5.5, 7), water='high', yield_qty=0.3, weeks=24),
    'Zinnia elegans': profile('Sep Oct Nov Dec Jan', 30, 45, succession=28, ornamental=True, rotation='Anywhere'),
}
PROFILES['Daucus carota subsp. sativus'] = PROFILES['Daucus carota']


def fill(root=ROOT):
    changed = 0
    for path in sorted((root / 'Plants').glob('*.md')):
        p, body = read_note(path)
        if p.get('status') != 'published':
            continue
        plan = deepcopy(PROFILES[p['scientific_name']])
        if path.stem == 'Radish - French Breakfast':
            plan.update(yield_qty=0.03, spacing_cm=5, succession_interval_days=14)
        flags = p.setdefault('generated_fields', [])
        provenance = p.setdefault('field_provenance', {})
        estimates = p.setdefault('estimated_fields', [])
        na = p.setdefault('not_applicable_fields', {})
        added = []

        def record(key, basis, inapplicable=False):
            if key not in flags:
                flags.append(key)
            provenance[key] = dict(method='ai_planning_estimate', generated_at=DATE,
                                   scope='species', review_status='needs_review', sources=[],
                                   basis=basis + ' ' + ASSUMPTIONS)
            exported_key = ALIASES.get(key, SECTIONS.get(key, key))
            if not inapplicable and exported_key not in estimates:
                estimates.append(exported_key)
            added.append(key)

        original_region = p.get('calendar_region')
        if original_region != REGION:
            p['calendar_region'] = REGION
            record('calendar_region', f'Assume Sydney for planning; former region label: {original_region}.')
            if p.get('planting_months'):
                record('planting_months', 'Existing month list retained but now explicitly treated as a rough Sydney planning assumption, not a verified regional calendar.')
        for key, value in plan.items():
            if key == 'ornamental' or p.get(key) not in (None, '', []):
                continue
            if key in na:
                continue
            if value is None or (plan['ornamental'] and key in {'yield_qty', 'yield_unit', 'harvest_window_weeks'}):
                reason = ('No numeric crop-yield or food-harvest target for this ornamental/timber planning record.'
                          if key != 'succession_interval_days' else
                          'No routine repeated sowing assumed for this established perennial or single long-season planting.')
                na[key] = reason
                record(key, reason, inapplicable=True)
            else:
                p[key] = value
                record(key, 'Representative species planning value chosen by AI; no cultivar-specific evidence. '
                       + ('Months mean outdoor sowing/transplanting for annuals or planting nursery stock/divisions for perennials.' if key == 'planting_months' else ''))

        # These are watch-list/layout suggestions only. Never create a diagnosis.
        suggestions = {
            'pests': ['Spider mites'] if p['scientific_name'] == 'Bambusa oldhamii' else ['Aphids', 'Slugs and snails'],
            'diseases': ['Root rot'] if plan['forest_layer'] in {'canopy', 'rhizosphere', 'groundcover'} else ['Powdery mildew'],
            'functions': ['windbreak'] if p['scientific_name'] == 'Bambusa oldhamii' else ['pollinator attractor'],
            'companions': [dict(plant='[[Plants/Alyssum]]' if path.stem != 'Alyssum' else '[[Plants/Zinnia]]',
                                function='pollinator attractor',
                                notes='try a separate flowering edge for visiting insects; allow light, airflow and root space. Not evidence of pest control, compatibility or increased yield.')],
        }
        if not p.get('part_used'):
            suggestions['part_used'] = 'culm' if p['scientific_name'] == 'Bambusa oldhamii' else 'flower (ornamental only)'
        if not p.get('uses'):
            suggestions['uses'] = ['timber'] if p['scientific_name'] == 'Bambusa oldhamii' else ['ornamental']
        for key, value in suggestions.items():
            if p.get(key) in (None, '', []):
                p[key] = value
                record(key, 'Speculative monitoring target or garden layout/use category. Pollinator value assumes the plant is allowed to flower; do not infer medicinal or food safety advice.')

        for heading in ['Sowing', 'Harvest']:
            if sections(body).get(heading):
                continue
            text = ('Try the months in planting_months as a rough Sydney starting point; use seed/transplants for annual crops and nursery plants or divisions for perennials. Adjust to weather and establishment.'
                    if heading == 'Sowing' else
                    '' + ('This is ornamental/timber planning, with no edible-harvest target. Do not treat flowers, shoots or other parts as safe food based on this record.' if plan['ornamental'] else 'Use harvest_window_weeks as a rough picking/lifting period; yield_qty is a total per established plant per crop/season, not per picking. Harvest at suitable maturity and adjust after observing your plants.'))
            marker = '## ' + heading + '\n'
            start = body.index(marker)
            end = body.find('\n## ', start + len(marker))
            end = len(body) if end < 0 else end
            body = body[:start] + marker + '\n' + text + '\n' + body[end:]
            record(heading, 'Unverified planning text requested by the user.')
        if not added:
            continue
        if 'Internal Planning estimates' not in body:
            body += '\n\n<!-- Internal Planning estimates\nUNVERIFIED AI GUESSES, generated 23 October 2026 at the user’s request. '
            body += ASSUMPTIONS + '\n\n'
            body += 'Fields/sections guessed in this pass: ' + ', '.join(added) + '. '
            body += 'All need review. Exact guesses, dates and assumptions are in field_provenance; fields without an applicable value are explained in not_applicable_fields. '
            body += 'Existing sourced text remains as historical research and may still describe these values as unknown; the new guesses do not resolve that evidence gap. No photos were invented.\n-->\n'
        write_note(path, p, body)
        changed += len(added)
    return changed


if __name__ == '__main__':
    print(f'Added {fill()} explicitly unverified planning guesses; regenerate the catalogue next.')
