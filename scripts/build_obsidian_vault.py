"""The repository itself is now the vault; Markdown is authoritative."""
from pathlib import Path
if __name__ == '__main__':
    print(f'Open this folder as a vault in Obsidian: {Path(__file__).resolve().parents[1]}')
    print('Edit Plants/*.md. Use Templates/Plant.md for stubs; export_catalogue.py builds JSON.')
