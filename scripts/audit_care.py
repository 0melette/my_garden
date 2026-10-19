"""Report missing care topics without changing catalogue data."""
import json
from pathlib import Path
from export_markdown import read_note, sections

TOPICS = ('Sunlight', 'Watering', 'Fertiliser', 'Support', 'Pruning', 'Unknowns')


def audit(root):
    records = []
    for path in sorted((root / 'Plants').glob('*.md')):
        props, body = read_note(path)
        if props.get('status') != 'published':
            continue
        care = sections(body).get('Care') or ''
        missing = [topic for topic in TOPICS if not any(
            line.startswith(topic + ':') and line.partition(':')[2].strip()
            for line in care.splitlines())]
        records.append({'plant': props.get('common_name', path.stem),
                        'missing_topics': missing,
                        'has_inline_source': 'https://' in care})
    return {'meaning': 'Topic coverage only; not verification of advice or source quality.',
            'published_plants': len(records), 'records': records}


if __name__ == '__main__':
    print(json.dumps(audit(Path(__file__).resolve().parents[1]), indent=2))
