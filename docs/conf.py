from pathlib import Path
from xml.etree import ElementTree

project = 'Lebai ROS SDK for Noetic'
manifest = Path(__file__).resolve().parents[1] / 'lebai_driver' / 'package.xml'
release = ElementTree.parse(str(manifest)).findtext('version')
root_doc = 'index'
exclude_patterns = ['build']
html_theme = 'alabaster'
