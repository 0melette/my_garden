"""Rebuild the README coverage tables from Markdown (presence, not correctness)."""
from pathlib import Path
import argparse
from urllib.parse import quote
from export_markdown import ROOT, read_note, sections, SECTIONS

START = '<!-- completion:start -->'
END = '<!-- completion:end -->'
FIELDS = ('common_name scientific_name family category sun water planting_months '
          'calendar_region spacing_cm row_spacing_cm soil_ph_min soil_ph_max feeder '
          'yield_qty yield_unit succession_interval_days harvest_window_weeks '
          'forest_layer part_used rotation_group photo source_url pests diseases '
          'functions uses companions').split()


def present(value):
    return value is not None and value != [] and value != '' and (
        not isinstance(value, str) or value.strip().lower() not in {'not recorded', 'original region not recorded'})


def render(root):
    records, drafts = [], 0
    for path in sorted((root / 'Plants').glob('*.md')):
        props, body = read_note(path)
        if props.get('status') != 'published':
            drafts += 1
            continue
        parts = sections(body)
        filled = [key for key in FIELDS if present(props.get(key))]
        filled += [key for key in SECTIONS if present(parts.get(key))]
        records.append((path, props, parts, filled))
    total = len(records)
    denominator = len(FIELDS) + len(SECTIONS)
    cells = sum(len(row[3]) for row in records)
    flagged = sum(bool(p.get('generated_fields')) for _, p, _, _ in records)
    excluded = sum(len(set(p.get('not_applicable_fields') or {}) & set(FIELDS)) for _, p, _, _ in records)
    guessed = sum(sum(e['method'] == 'ai_planning_estimate' for e in (p.get('field_provenance') or {}).values()) for _, p, _, _ in records)
    lines = [START, '<details>', '<summary>Maintainer catalogue audit</summary>', '', f'**{total} published plants · {drafts} drafts excluded · '
             f'{cells}/{total * denominator} fields/sections populated '
             f'({cells / (total * denominator):.0%}) · {excluded} explicitly inapplicable · '
             f'{total * denominator-cells-excluded} unresolved · {flagged} plants with flagged AI additions.**', '',
             f'**{guessed} field/section entries are unverified AI planning guesses (including applicability decisions).** '
             'Guesses are planning placeholders, not sourced facts. See field_provenance and estimated_fields in each note.', '',
             'Presence only, not accuracy or verification. Empty lists mean no associations recorded, '
             'not “none exist”. Populated prose may still describe unknowns. '
             'Inapplicable fields stay empty and are counted separately; this is not a readiness score. '
             'Calendars without a recorded region count as gaps. Existing unflagged data is not necessarily human-written or verified.', '',
             '| Field | Populated | N/A | Gaps | AI flagged | AI guesses |', '| --- | ---: | ---: | ---: | ---: | ---: |']
    for key in FIELDS + list(SECTIONS):
        count = sum(present(p.get(key) if key in FIELDS else s.get(key)) for _, p, s, _ in records)
        generated = sum(key in (p.get('generated_fields') or []) for _, p, _, _ in records)
        na = sum(key in (p.get('not_applicable_fields') or {}) for _, p, _, _ in records)
        guesses = sum((p.get('field_provenance') or {}).get(key, {}).get('method') == 'ai_planning_estimate' for _, p, _, _ in records)
        lines.append(f'| {key} | {count}/{total} | {na} | {total-count-na} | {generated} | {guesses} |')
    lines += ['', '<details>', '<summary>Per-plant completion and remaining gaps</summary>', '',
              '| Plant | Populated | N/A | AI additions | Missing fields/sections |', '| --- | ---: | ---: | ---: | --- |']
    for path, p, _, filled in records:
        na = p.get('not_applicable_fields') or {}
        missing = [key for key in FIELDS + list(SECTIONS) if key not in filled and key not in na]
        label = p['common_name'].replace('|', '\\|')
        lines.append(f'| [{label}]({quote(path.relative_to(root).as_posix())}) | '
                     f'{len(filled)}/{denominator} | {len(na)} | {len(p.get("generated_fields") or [])} | '
                     f'{", ".join(missing) or "—"} |')
    lines += ['', '</details>', '', '</details>', '', END]
    return '\n'.join(lines)


def update(root=ROOT, check=False):
    path = root / 'README.md'
    if not path.exists():
        return
    text = path.read_text()
    if START not in text or END not in text:
        raise ValueError('README needs completion:start and completion:end markers')
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    result = before + render(root) + after
    if check:
        if result != text:
            raise ValueError('README completion is stale. Run scripts/export_catalogue.py.')
    else:
        path.write_text(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    update(check=args.check)
