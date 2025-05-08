import pkgutil
from pathlib import Path


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

        if not doc_path.exists():
            doc_path.mkdir(parents=True)

        self.tree_path = tree_path
        self.modules = []
        self.packages = []

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
                f.write("    :members:\n")
                f.write("    :undoc-members:\n")
                f.write("    :show-inheritance:\n")
                f.write("    :special-members: __init__\n")

    def generate_index(self) -> None:
        """Method to generate the index for the package"""

        self.generate_modules()


        with open(self.doc_path / "index.rst", "w", encoding="utf-8") as f:
            f.write(f"{self.name}\n")
            f.write(f"{'=' * len(self.name)}\n\n")
            f.write(".. toctree::\n   :maxdepth: 1\n\n")
            for module_info in self.modules:
                f.write(f"   {module_info.name}\n")
            for package in self.packages:
                f.write(f"   {package.name}/index.rst\n")
