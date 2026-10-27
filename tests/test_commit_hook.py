import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from export_markdown import ROOT,read_note,write_note
from create_plant import create
from prepare_commit import prepare

class CommitHookTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        for folder in ['Plants','References','Templates','scripts','.githooks']:
            shutil.copytree(ROOT/folder,self.root/folder,ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy2(ROOT/'Catalogue.md',self.root/'Catalogue.md')
        shutil.copy2(ROOT/'README.md',self.root/'README.md')
        shutil.copytree(ROOT/'localdata/plant_images',self.root/'localdata/plant_images')
        shutil.copy2(ROOT/'localdata/plant-image-sources.json',self.root/'localdata/plant-image-sources.json')
        (self.root/'snapshots').mkdir();shutil.copy2(ROOT/'snapshots/almanac-catalogue.json',self.root/'snapshots/almanac-catalogue.json')
        self.git('init','-q');self.git('config','user.name','Test');self.git('config','user.email','test@example.invalid')
        # Detached maintenance can race with temporary repository cleanup.
        self.git('config','maintenance.auto','false')
        self.git('add','.');self.git('commit','-qm','Fixture')
    def tearDown(self):self.temp.cleanup()
    def git(self,*args):return subprocess.check_output(['git','-C',str(self.root),*args])
    def test_partial_staging_exports_only_index(self):
        p=self.root/'Plants/Parsley.md';props,body=read_note(p)
        props['water']='high';props['yield_qty']=2;write_note(p,props,body);self.git('add','Plants/Parsley.md')
        props['water']='low';props['yield_qty']=None;write_note(p,props,body)
        prepare(self.root)
        data=json.loads(self.git('show',':snapshots/almanac-catalogue.json'))
        row=next(r for r in data['tables']['plant_references'] if r['slug']=='parsley')
        self.assertEqual(row['water_needs'],'high');self.assertEqual(read_note(p)[0]['water'],'low')
        from completion_report import render
        staged_readme=self.git('show',':README.md').decode()
        self.assertNotIn(render(self.root),staged_readme)
        self.assertEqual(row['yield_qty'],2)
        from completion_report import FIELDS, present
        current_count=sum(present(read_note(path)[0].get('yield_qty')) for path in (self.root/'Plants').glob('*.md') if read_note(path)[0]['status']=='published')
        self.assertIn(f'| yield_qty | {current_count+1}/46 |',staged_readme)

    def test_unstaged_readme_is_preserved(self):
        path=self.root/'README.md';body=path.read_text()+'\nUnstaged writing\n';path.write_text(body)
        tree=self.git('write-tree')
        with self.assertRaisesRegex(ValueError,'README has unstaged edits'):prepare(self.root)
        self.assertEqual(path.read_text(),body)
        self.assertEqual(tree,self.git('write-tree'))
    def test_new_published_id_is_staged_and_persisted(self):
        p=create('Hook test herb','Herbs',self.root);props,body=read_note(p)
        props['status']='published';props['scientific_name']='Testus herb';write_note(p,props,body)
        self.git('add','Plants/Hook test herb.md');prepare(self.root)
        self.assertIsInstance(read_note(p)[0]['catalogue_id'],int)
        self.assertEqual(self.git('show',':Plants/Hook test herb.md'),p.read_bytes())
    def test_invalid_staged_note_leaves_index_and_json_unchanged(self):
        p=self.root/'Plants/Parsley.md';props,body=read_note(p);props['planting_months']=['Invalid'];write_note(p,props,body)
        self.git('add','Plants/Parsley.md');tree=self.git('write-tree');before=(self.root/'snapshots/almanac-catalogue.json').read_bytes()
        with self.assertRaises(subprocess.CalledProcessError):prepare(self.root)
        self.assertEqual(tree,self.git('write-tree'));self.assertEqual(before,(self.root/'snapshots/almanac-catalogue.json').read_bytes())
