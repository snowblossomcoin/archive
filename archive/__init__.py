from pathlib import Path

path = Path(__file__).parent
web_path = path / 'web'

from .archive import Archive
