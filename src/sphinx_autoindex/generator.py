import os
import pkgutil
from pathlib import Path
from sphinx.application import Sphinx
from sphinx.util.console import bold, colorize

def generate_rst_files(app: Sphinx):
    """Generate rst files for each module in the package

    :param app: Sphinx application"""
    package_toindex = app.config.package_toindex
    if package_toindex is None:
        raise RuntimeError("You must set 'package_toindex' in conf.py")

    package_path = Path(package_toindex)
    if not package_path.is_dir():
        raise RuntimeError(f"Package '{package_toindex}' does not exist")

    doc_path = Path(app.srcdir) / "api"
    doc_path.mkdir(exist_ok=True, parents=True)

    # Clean previous files
    for file in Path(doc_path).glob("*.rst"):
        file.unlink()

    for module_info in pkgutil.walk_packages([package_toindex], prefix=""):
        if module_info.ispkg:
            continue

        package_name = Path(package_toindex).name  # ex: sphinx_autoindex
        full_module_name = f"{package_name}.{module_info.name}"
        module_rst_path = os.path.join(doc_path, f"{module_info.name}.rst")

        with open(module_rst_path, "w", encoding="utf-8") as f:
            f.write(f"{full_module_name}\n")
            f.write(f"{'=' * len(full_module_name)}\n\n")
            f.write(f".. automodule:: {full_module_name}\n")
            f.write("    :members:\n")
            f.write("    :undoc-members:\n")
            f.write("    :show-inheritance:\n")
            f.write("    :special-members: __init__\n")

    index_path = os.path.join(doc_path, "api.rst")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("API\n===\n\n")
        f.write(".. toctree::\n   :maxdepth: 2\n\n")
        for module_info in pkgutil.walk_packages([package_toindex]):
            if not module_info.ispkg:
                f.write(f"   {module_info.name}\n")