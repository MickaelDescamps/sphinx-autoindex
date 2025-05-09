import copy


class Singleton:

    _instance = {}

    def __new__(cls, *args, **kwargs):
        """Method to manage instance creation."""

        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)

        return cls._instance[cls]


class ConfigSingleton(Singleton):

    _initialized = False

    def __init__(self):

        if not self._initialized:
            self.package_toindex = None
            self.loaded = False
            self.sai_autodoc_global_config = None
            self.sai_autodoc_specific_config = None
            self._initialized = True

    def load_conf(self,
                  package_toindex,
                  sai_autodoc_global_config,
                  sai_autodoc_specific_config):
        """Load configuration from conf.py file."""

        self.package_toindex = package_toindex
        self.sai_autodoc_global_config = sai_autodoc_global_config
        self.sai_autodoc_specific_config = sai_autodoc_specific_config
        self.loaded = True

    def get_autodoc_conf(self, module_tree) -> dict:
        """Method to get compiled configuration for a module

        :param module_tree: module tree string
        :return: compiled configuration
        :rtype: dict
        :raises Exception: if configuration is not loaded"""

        if not self.loaded:
            raise Exception("Configuration not loaded.")

        res_config = copy.deepcopy(self.sai_autodoc_global_config)

        if isinstance(self.sai_autodoc_specific_config, dict):
            if module_tree in self.sai_autodoc_specific_config.keys():
                for conf_name, value in self.sai_autodoc_specific_config[module_tree].items():
                    res_config[conf_name] = value

        return res_config

