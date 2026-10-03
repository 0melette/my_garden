"""Enable the tracked hooks for this clone only."""
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]
old=subprocess.run(['git','-C',str(root),'config','--local','--get','core.hooksPath'],capture_output=True,text=True).stdout.strip()
if old and old!='.githooks':
    raise SystemExit(f'Existing hooksPath {old!r}; combine your hooks before changing it.')
default=root/'.git/hooks/pre-commit'
if not old and default.exists():
    raise SystemExit('An existing .git/hooks/pre-commit needs to be combined with this hook first.')
subprocess.run(['git','-C',str(root),'config','--local','core.hooksPath','.githooks'],check=True)
print('Enabled My Garden pre-commit hook for this clone.')
