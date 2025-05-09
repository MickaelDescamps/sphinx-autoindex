import os
import pkgutil
import sys
from pathlib import Path
from sphinx.application import Sphinx
from sphinx.util.console import bold, colorize

from sphinx_autoindex.config import ConfigSingleton
from sphinx_autoindex.package import Package


def generate_rst_files(app: Sphinx):
    """Generate rst files for each module in the package

    :param app: Sphinx application"""
    package_toindex = app.config.package_toindex
    if package_toindex is None:
        raise RuntimeError("You must set 'package_toindex' in conf.py")

    config = ConfigSingleton()

    global_autodoc_configs:dict = app.config.sai_autodoc_global_config

    if len(global_autodoc_configs) == 0:
        global_autodoc_configs = {
        "members":{},
        "undoc-members":True,
        "show-inheritance":True,
        "inherited-members":True,
        "exclude-members":{},
        "special-members":{},
        "private-members":{},
        }

    config.load_conf(package_toindex,
                     global_autodoc_configs,
                     app.config.sai_autodoc_specific_config)

    package_path = Path(package_toindex)

    sys.path.append(str(package_path.parent))

    if not package_path.is_dir():
        raise RuntimeError(f"Package '{package_toindex}' does not exist")

    doc_path = Path(app.srcdir) / "api"
    doc_path.mkdir(exist_ok=True, parents=True)

    # Clean previous files
    for file in Path(doc_path).glob("*"):
        if file.is_dir():
            continue
        file.unlink()

    # Get the package name from this path
    package_name = package_path.name
    package = Package(package_name, package_path, doc_path, package_name)
    package.scan_package()