#!/usr/bin/env python3
"""Build from the Git index, so unstaged Markdown never leaks into a commit."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def git(root,*args,**kwargs):
    return subprocess.run(['git','-C',str(root),*args],check=True,stdout=subprocess.PIPE,**kwargs).stdout


def prepare(root):
    root=Path(root)
    output='snapshots/almanac-catalogue.json'
    # A generated file may be replaced, but never silently discard manual edits.
    if git(root,'diff','--name-only','--',output).strip():
        raise ValueError('JSON has unstaged edits. Stage or save those edits before committing.')
    with tempfile.TemporaryDirectory(prefix='garden-commit-') as folder:
        snapshot=Path(folder)
        git(root,'checkout-index','--all',f'--prefix={snapshot}{os.sep}')
        before={p.relative_to(snapshot):p.read_bytes() for p in (snapshot/'Plants').glob('*.md')}
        subprocess.run([sys.executable,str(snapshot/'scripts/export_catalogue.py'),'--root',str(snapshot),'--assign-ids'],check=True)
        assigned={path:(snapshot/path).read_bytes() for path,body in before.items() if (snapshot/path).read_bytes()!=body}
        # Assigning an ID rewrites frontmatter; stop rather than overwrite a partial edit.
        for path in assigned:
            if not (root/path).is_file() or (root/path).read_bytes()!=before[path]:
                raise ValueError(f'{path}: new ID needed, but the note has unstaged edits. Fully stage this note first.')
        updates={**assigned,Path(output):(snapshot/output).read_bytes()}
        for path,body in updates.items():
            destination=root/path;destination.parent.mkdir(parents=True,exist_ok=True)
            destination.write_bytes(body)
            git(root,'add','--',str(path))
    print('My Garden: generated catalogue staged from committed Markdown.')


if __name__=='__main__':
    try:
        root=subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()
        prepare(root)
    except (ValueError,subprocess.CalledProcessError) as exc:
        sys.exit(f'My Garden commit stopped: {exc}')
