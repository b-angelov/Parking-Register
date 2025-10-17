import importlib

from build import BuildException
from kivy.lang import Builder


class Layout:

    def __init__(self, module_name: str):
        try:
            self.module = importlib.import_module("layouts." + module_name)
        except ModuleNotFoundError:
            raise ModuleNotFoundError(f"Module '{module_name}' not found.")

    def build(self, kv: str = None):
        kv = kv if (kv and hasattr(self.module,kv)) else kv or self.module.KV
        try:
            build = Builder.load_string(kv)
            return build
        except BuildException:
            raise BuildException(f"Error in building layout from module '{self.module.__name__}'.")
