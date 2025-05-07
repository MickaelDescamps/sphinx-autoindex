from sphinx.application import Sphinx
from .generator import generate_rst_files

def setup(app: Sphinx):
    app.add_config_value('package_toindex', None, "env")
    app.connect('builder-inited', generate_rst_files)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }