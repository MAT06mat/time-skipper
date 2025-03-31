from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.core.text import LabelBase
from root import Root
from _version import __version__
import os


class TimeSkipperApp(MDApp):
    root = ObjectProperty(None)
    store = ObjectProperty(None)
    icon = "images/icon.png"
    __version__ = __version__

    def define(self, key, default):
        if not self.store.exists(key):
            self.store[key] = {"value": default}

    def get(self, key):
        return self.store[key]["value"]

    def set(self, key, value):
        self.store[key] = {"value": value}

    def build(self):
        LabelBase.register(
            name="ShareTechMono",
            fn_regular="fonts/ShareTechMono-Regular.ttf",
        )
        os.makedirs(".cache", exist_ok=True)
        self.store = JsonStore(".cache/settings.json")

        # Define theme
        self.define("theme", "Dark")
        self.theme_cls.theme_style = self.get("theme")

        # Define palette
        self.define("palette", "Teal")
        self.theme_cls.primary_palette = self.get("palette")

        # Define time_edit
        self.define("time_edit", False)

        self.root = Root()
        return self.root


if __name__ == "__main__":
    TimeSkipperApp().run()
