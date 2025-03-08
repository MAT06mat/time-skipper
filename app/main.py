__version__ = "1.0"

if __name__ == "__main__":
    from kivymd.app import MDApp
    from kivy.properties import ObjectProperty
    from kivy.storage.jsonstore import JsonStore
    from kivy.core.text import LabelBase
    from root import Root
    import os

    class TimeSkipperApp(MDApp):
        root = ObjectProperty(None)
        store = ObjectProperty(None)
        icon = "images/icon.png"

        def build(self):
            LabelBase.register(
                name="ShareTechMono",
                fn_regular="fonts/ShareTechMono-Regular.ttf",
            )
            os.makedirs(".cache", exist_ok=True)
            self.store = JsonStore(".cache/settings.json")
            if not self.store.exists("theme"):
                self.theme_cls.theme_style = "Dark"
                self.store["theme"] = {"value": "Dark"}
            else:
                self.theme_cls.theme_style = self.store["theme"]["value"]
            if not self.store.exists("time_edit"):
                self.store["time_edit"] = {"value": False}

            self.theme_cls.primary_palette = "Teal"

            self.root = Root()
            return self.root

    TimeSkipperApp().run()
