from pathlib import Path
from xml.etree import ElementTree

project = 'Lebai ROS Noetic SDK'
language = 'zh_CN'
manifest = Path(__file__).resolve().parents[1] / 'lebai_driver' / 'package.xml'
release = ElementTree.parse(str(manifest)).findtext('version')
root_doc = 'index'
exclude_patterns = ['build', 'superpowers']
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'display_version': True,
    'titles_only': True,
}
html_static_path = ['_static']
html_css_files = ['launch-parameters.css']
html_js_files = ['version-switcher.js']
