__version__ = "0.0.0"

if __name__ == "__main__":
    from kivymd.app import MDApp
    from kivy.properties import ObjectProperty
    from kivy.storage.jsonstore import JsonStore
    from kivy.core.text import LabelBase
    from kivy.metrics import sp
    from root import Root
    import os

    class TimeSkipperApp(MDApp):
        root = ObjectProperty(None)
        store = ObjectProperty(None)

        def build(self):
            LabelBase.register(
                name="ShareTechMono",
                fn_regular="fonts/ShareTechMono-Regular.ttf",
            )
            self.store = JsonStore(".cache/settings.json")
            if not self.store.exists("theme"):
                self.theme_cls.theme_style = "Light"
                self.store["theme"] = {"value": "Light"}
            else:
                self.theme_cls.theme_style = self.store["theme"]["value"]
            if not self.store.exists("time_edit"):
                self.store["time_edit"] = {"value": False}

            self.theme_cls.primary_palette = "Teal"

            self.root = Root()
            return self.root

    os.makedirs(".cache", exist_ok=True)
    TimeSkipperApp().run()
