import copy
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from export_markdown import ROOT, compile_catalogue, read_note, write_note
from completion_report import render, update, present


class CompletionProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for folder in ['Plants', 'References']:
            shutil.copytree(ROOT / folder, self.root / folder)
        for name in ['Catalogue.md', 'README.md']:
            shutil.copy2(ROOT / name, self.root / name)
        (self.root / 'localdata').symlink_to(ROOT / 'localdata', target_is_directory=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_flags_and_sources_survive_export(self):
        row = next(r for r in compile_catalogue(self.root)['tables']['plant_references'] if r['slug'] == 'jujube-si-hong')
        self.assertIn('family', row['generated_fields'])
        self.assertEqual(row['field_provenance']['family']['review_status'], 'needs_review')
        self.assertIn('AI-assisted additions', row['care_notes'])
        self.assertIn('Watering:', row['care_notes'])

    def test_incomplete_provenance_blocks_export(self):
        path = self.root / 'Plants/Jujube - Si Hong.md'
        original, body = read_note(path)
        for change in ['missing', 'source', 'date', 'scope', 'empty_field']:
            with self.subTest(change=change):
                props = copy.deepcopy(original)
                evidence = props['field_provenance']['family']
                if change == 'missing': del props['field_provenance']['family']
                if change == 'source': evidence['sources'] = []
                if change == 'date': evidence['checked_at'] = 'tomorrow'
                if change == 'scope': evidence['scope'] = 'verified'
                if change == 'empty_field': props['family'] = None
                write_note(path, props, body)
                with self.assertRaises(ValueError): compile_catalogue(self.root)

    def test_report_detects_source_changes_and_excludes_drafts(self):
        update(self.root)
        update(self.root, check=True)
        self.assertNotIn('New plant', render(self.root))
        path = self.root / 'Plants/Parsley.md'
        props, body = read_note(path)
        props['photo'] = None
        write_note(path, props, body)
        with self.assertRaisesRegex(ValueError, 'stale'): update(self.root, check=True)
        self.assertFalse(present('Original region not recorded'))
        self.assertTrue(present('Pruning is not recorded; watering guidance follows.'))

    def test_planning_guesses_cannot_claim_sources_and_keep_applicability(self):
        rows = compile_catalogue(self.root)['tables']['plant_references']
        tomato = next(row for row in rows if row['slug'] == 'tomato')
        self.assertEqual(tomato['field_provenance']['water']['sources'], [])
        self.assertEqual(tomato['field_provenance']['water']['review_status'], 'needs_review')
        self.assertIn('water_needs', tomato['estimated_fields'])
        bamboo = next(row for row in rows if row['slug'] == 'bamboo-oldhamii')
        self.assertIsNone(bamboo['yield_qty'])
        self.assertIn('yield_qty', bamboo['not_applicable_fields'])
        path = self.root / 'Plants/Tomato.md'
        props, body = read_note(path)
        props['field_provenance']['water']['sources'] = ['https://example.com/pretend-source']
        write_note(path, props, body)
        with self.assertRaisesRegex(ValueError, 'no claimed sources'):
            compile_catalogue(self.root)

    def test_applicability_cannot_hide_a_populated_value(self):
        path = self.root / 'Plants/Bamboo - Oldhamii.md'
        props, body = read_note(path)
        props['yield_qty'] = 5
        write_note(path, props, body)
        with self.assertRaisesRegex(ValueError, 'not-applicable'):
            compile_catalogue(self.root)

    def test_estimate_filler_is_idempotent_and_preserves_research(self):
        from fill_planning_estimates import fill
        before = {path: path.read_bytes() for path in (self.root / 'Plants').glob('*.md')}
        self.assertEqual(fill(self.root), 0)
        self.assertEqual(before, {path: path.read_bytes() for path in before})
