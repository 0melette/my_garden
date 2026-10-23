import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from export_markdown import ROOT,compile_catalogue,export,read_note,write_note
from create_plant import create

class MarkdownCatalogueTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        for folder in ['Plants','References','Templates']:shutil.copytree(ROOT/folder,self.root/folder)
        shutil.copy2(ROOT/'Catalogue.md',self.root/'Catalogue.md')
        (self.root/'localdata').symlink_to(ROOT/'localdata',target_is_directory=True)
    def tearDown(self):self.tmp.cleanup()
    def test_body_and_properties_are_authoritative(self):
        path=self.root/'Plants/Parsley.md';p,b=read_note(path)
        p['water']='high';p['spacing_cm']=42
        start=b.index('## Care\n');end=b.index('## Management\n',start)
        b=b[:start]+'## Care\n\nUnique updated care text.\n\n'+b[end:]
        write_note(path,p,b)
        row=next(r for r in compile_catalogue(self.root)['tables']['plant_references'] if r['slug']=='parsley')
        self.assertEqual(row['water_needs'],'high');self.assertEqual(row['in_row_spacing_cm'],42)
        self.assertTrue(row['care_notes'].endswith('Unique updated care text.'))
    def test_draft_template_then_stable_publish_id(self):
        baseline=len(compile_catalogue(self.root)['tables']['plant_references'])
        next_id=max(read_note(p)[0].get('catalogue_id') or 0 for p in (self.root/'Plants').glob('*.md'))+1
        path=create('Test Herb','Herbs',self.root)
        self.assertEqual(len(compile_catalogue(self.root)['tables']['plant_references']),baseline)
        p,b=read_note(path);p['status']='published';p['scientific_name']='Testus example';write_note(path,p,b)
        with self.assertRaisesRegex(ValueError,'assign-ids'):compile_catalogue(self.root)
        first=compile_catalogue(self.root,True);self.assertEqual(len(first['tables']['plant_references']),baseline+1)
        p,_=read_note(path);self.assertEqual(p['catalogue_id'],next_id);self.assertEqual(p['slug'],'test-herb')
        self.assertEqual(first,compile_catalogue(self.root))
    def test_duplicate_identity_and_broken_relations_fail(self):
        path=self.root/'Plants/Parsley.md';p,b=read_note(path);p['catalogue_id']=1;write_note(path,p,b)
        with self.assertRaisesRegex(ValueError,'duplicate/invalid catalogue_id'):compile_catalogue(self.root)
        p['catalogue_id']=35;p['pests']=['Missing pest'];write_note(path,p,b)
        with self.assertRaisesRegex(ValueError,'unknown pests'):compile_catalogue(self.root)
    def test_invalid_calendar_does_not_replace_output(self):
        output=self.root/'result.json';output.write_text('keep me')
        path=self.root/'Plants/Parsley.md';p,b=read_note(path);p['planting_months']=['Smarch'];write_note(path,p,b)
        with self.assertRaises(ValueError):export(self.root,output)
        self.assertEqual(output.read_text(),'keep me')
    def test_private_notes_never_export(self):
        private=self.root/'Garden Notes';private.mkdir();(private/'Secret.md').write_text('PRIVATE-CANARY')
        path=self.root/'Plants/Parsley.md';p,b=read_note(path);p['bed']='PRIVATE-CANARY';write_note(path,p,b+'\n## My observations\n\nPRIVATE-CANARY\n')
        self.assertNotIn('PRIVATE-CANARY',json.dumps(compile_catalogue(self.root)))
    def test_check_detects_stale_json_and_export_is_deterministic(self):
        out=self.root/'result.json';export(self.root,out);before=out.read_bytes();export(self.root,out)
        self.assertEqual(before,out.read_bytes());export(self.root,out,check=True)
        out.write_text('{}')
        with self.assertRaisesRegex(ValueError,'stale'):export(self.root,out,check=True)

    def test_additive_ailments_keep_categories_and_credits(self):
        result=compile_catalogue(self.root)['tables']
        self.assertEqual(len(result['ailments']),30)
        self.assertEqual(len({g['id'] for g in result['ailments']}),30)
        wilting=next(g for g in result['ailments'] if g['name']=='Wilting')
        self.assertEqual(wilting['category'],'symptom')
        self.assertIn('Water and environment/Underwatering',wilting['possible_causes'])
        self.assertNotIn('Underwatering',[g['name'] for g in result['diseases']])
        photo=next(g for g in result['ailments'] if g['name']=='Grey mould')['image']
        self.assertTrue(photo['creator'])
        self.assertTrue(photo['license_url'].startswith('https://'))

    def test_tomato_scope_survives_export_without_schema_changes(self):
        plants=compile_catalogue(self.root)['tables']['plant_references']
        by_slug={p['slug']:p for p in plants}
        for slug,status in [('tomato','not_applicable'),('tomato-black-krim','not_assessed'),('tomato-sweet-1000','unverified')]:
            row=by_slug[slug]
            self.assertIn('Care scope: species_guidance.',row['care_notes'])
            self.assertIn(f'Cultivar verification: {status}.',row['care_notes'])
            self.assertNotIn('care_scope',row)
            self.assertNotIn('cultivar_verification',row)
        self.assertEqual(by_slug['tomato']['water_needs'],'moderate')
        self.assertEqual(by_slug['tomato']['field_provenance']['water']['method'],'ai_planning_estimate')
        self.assertIn('UNVERIFIED AI PLANNING GUESSES',by_slug['tomato']['care_notes'])

    def test_invalid_care_scope_rejected(self):
        path=self.root/'Plants/Tomato.md';p,b=read_note(path)
        p['care_scope']='made_up';write_note(path,p,b)
        with self.assertRaisesRegex(ValueError,'invalid care_scope'):
            compile_catalogue(self.root)

if __name__=='__main__':unittest.main()
