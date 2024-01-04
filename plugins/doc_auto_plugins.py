from plugin_interface import PluginInterface

class FetchDocumentPlugin(PluginInterface):
    def run(self, state):
        state["document_fetched"] = True
        print("Running Fetch Document Plugin")

class OCRDocumentPlugin(PluginInterface):
    def run(self, state):
        state["ocr_document"] = True
        print("Running OCR Document Plugin")

class ExtractLabelsPlugin(PluginInterface):
    def run(self, state):
        state["labels_extracted"] = True
        print("Running Extract Labels Plugin")

class ApplyRulesPlugin(PluginInterface):
    def run(self, state):
        state["rules_applied"] = True
        print("Running Apply Rules Plugin")

class CaptureDataPlugin(PluginInterface):
    def run(self, state):
        state["data_captured"] = True
        print("Running Capture Data Plugin")

class DataStoragePlugin(PluginInterface):
    def run(self, state):
        state["data_stored"] = True
        state["document_processed"] = True
        print("Running Data Storage Plugin")

class TestPlugin(PluginInterface):
    def run(self, state):
        print("Running Test Plugin")
