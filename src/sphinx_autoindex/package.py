import pkgutil
from pathlib import Path

from sphinx_autoindex.config import ConfigSingleton


class Package:

    def __init__(self, name: str, code_path: Path, doc_path: Path, tree_path: str) -> None:
        """Constructor for the Package class

        :param name: Name of the package
        :param code_path: Path to the package code
        :param doc_path: Path to the package documentation
        :param tree_path: Path to the package tree"""
        self.name = name
        self.code_path = code_path
        self.doc_path = doc_path

        self.tree_path = tree_path
        self.modules = []
        self.packages = []

        config = ConfigSingleton()

        self.current_config = config.get_autodoc_conf(self.tree_path)

        if "no-index" in self.current_config:
            if self.current_config["no-index"]:
                return

        if not doc_path.exists():
            doc_path.mkdir(parents=True)

    def scan_package(self) -> None:
        """Method to scan the package for modules and return a list of them"""

        for module_info in pkgutil.walk_packages([str(self.code_path)], prefix=""):
            if not module_info.ispkg:
                self.modules.append(module_info)
            else:
                self.packages.append(Package(module_info.name,
                                             self.code_path / module_info.name,
                                             self.doc_path / module_info.name,
                                             f"{self.tree_path}.{module_info.name}"))

        for package in self.packages:
            package.scan_package()

        self.generate_index()

    def generate_modules(self) -> None:
        """Method to generate the modules for the package"""

        for module_info in self.modules:

            rst_filename = f"{module_info.name}.rst"

            with open(self.doc_path / rst_filename, "w", encoding="utf-8") as f:
                f.write(f"{module_info.name}\n")
                f.write(f"{'=' * len(module_info.name)}\n\n")
                f.write(f".. automodule:: {self.tree_path}.{module_info.name}\n")
                f.write(self.build_autodoc_confs(module_info.name))

    def build_autodoc_confs(self, module_name) -> str:

        options_str = ""

        config = ConfigSingleton()

        module_tree = f"{self.tree_path}.{module_name}"

        current_confs = config.get_autodoc_conf(module_tree)

        if "no-index" in current_confs:
            if current_confs["no-index"]:
                options_str = "    :no-index:\n"
                return options_str

        if "platform" in current_confs:
            options_str += f"    :platform: {current_confs['platform']}\n"

        if "deprecated" in current_confs:
            if current_confs["deprecated"]:
                options_str += "    :deprecated:\n"

        if "ignore-module-all" in current_confs:
            if current_confs["ignore-module-all"]:
                options_str += "    :ignore-module-all:\n"

        if "members" in current_confs:
            options_str += f"    :members: {', '.join(current_confs['members'])}\n"

        if "exclude-members" in current_confs:
            options_str += f"    :exclude-members: {', '.join(current_confs['exclude-members'])}\n"

        if "imported-members" in current_confs:
            options_str += f"    :imported-members: {', '.join(current_confs['imported-members'])}\n"

        if "special-members" in current_confs:
            if isinstance(current_confs["special-members"], list):
                elements = ["__init__", *current_confs["special-members"]]
            else:
                elements = ["__init__"]
            options_str += f"    :special-members: {', '.join(elements)}\n"
        else:
            options_str += f"    :special-members: __init__\n"

        if "undoc-members" in current_confs:
            if current_confs["undoc-members"]:
                options_str += "    :undoc-members:\n"

        if "private-members" in current_confs:
            if current_confs["private-members"]:
                options_str += "    :private-members:\n"

        if "member-order" in current_confs:
            options_str += f"    :member-order: {current_confs['member-order']}\n"

        if "show-inheritance" in current_confs:
            if current_confs["show-inheritance"]:
                options_str += "    :show-inheritance:\n"

        return options_str

    def generate_index(self) -> None:
        """Method to generate the index for the package"""

        if "no-index" in self.current_config:
            if self.current_config["no-index"]:
                return

        self.generate_modules()


        with open(self.doc_path / "index.rst", "w", encoding="utf-8") as f:
            f.write(f"{self.name}\n")
            f.write(f"{'=' * len(self.name)}\n\n")
            f.write(".. toctree::\n   :maxdepth: 1\n\n")
            for module_info in self.modules:
                f.write(f"   {module_info.name}\n")
            for package in self.packages:
                f.write(f"   {package.name}/index.rst\n")
