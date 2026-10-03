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
        self.assertEqual(row['care_notes'],'Unique updated care text.')
    def test_draft_template_then_stable_publish_id(self):
        path=create('Test Herb','Herbs',self.root)
        self.assertEqual(len(compile_catalogue(self.root)['tables']['plant_references']),41)
        p,b=read_note(path);p['status']='published';p['scientific_name']='Testus example';write_note(path,p,b)
        with self.assertRaisesRegex(ValueError,'assign-ids'):compile_catalogue(self.root)
        first=compile_catalogue(self.root,True);self.assertEqual(len(first['tables']['plant_references']),42)
        p,_=read_note(path);self.assertEqual(p['catalogue_id'],42);self.assertEqual(p['slug'],'test-herb')
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

if __name__=='__main__':unittest.main()
