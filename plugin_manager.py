
from plugin_interface import PluginInterface

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.test_mode = False

    def register_plugin(self, name, plugin):
        if not issubclass(plugin, PluginInterface):
            raise TypeError("plugin must be a subclass of PluginInterface")
        self.plugins[name] = plugin

    def get_plugin(self, name):
        if self.test_mode:
            return self.plugins["test"]
        else:
            if name in self.plugins:
                return self.plugins[name]
            else:
                print(f"No plugin found for name: {name}")
                return None

    def plugin_exists(self, name):
        return name in self.plugins