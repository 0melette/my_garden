#!/usr/bin/env python3
"""Make a draft plant from the same template used by Obsidian."""
import argparse
from pathlib import Path
from export_markdown import ROOT, read_note, write_note

def create(name,category=None,root=ROOT):
    if not name.strip() or any(c in name for c in '/\\:*?"<>|#[]') or name in {'.','..'}:
        raise ValueError('Use a plain plant name without filename punctuation.')
    path=root/'Plants'/f'{name}.md'
    if path.exists():raise ValueError(f'Already exists: {path}')
    p,b=read_note(root/'Templates/Plant.md')
    p['common_name']=name;p['category']=[category] if category else []
    write_note(path,p,b.replace('{{title}}',name))
    return path

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name');parser.add_argument('--category',choices=['Herbs','Flowers','Fruit','Vegetables'])
    args=parser.parse_args()
    try:print(create(args.name,args.category))
    except ValueError as e:parser.exit(1,str(e)+'\n')
