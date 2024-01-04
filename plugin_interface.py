
class PluginInterface:
    def run(self, state):
        raise NotImplementedError("Plugin must implement this method")