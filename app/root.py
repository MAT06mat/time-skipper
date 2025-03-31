from kivymd.uix.pickers import (
    MDTimePickerDialHorizontal,
    MDTimePickerDialVertical,
    MDTimePickerInput,
)
from kivy.properties import ObjectProperty, NumericProperty
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.clock import Clock

import time


class Root(MDScreen):
    time_picker: MDTimePickerDialHorizontal = ObjectProperty(allownone=True)

    start_time = NumericProperty(0)
    end_time = NumericProperty(0)
    event = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_cls.bind(device_orientation=self.check_orientation)
        self.app = MDApp.get_running_app()
        self.anim_version_in = Animation(opacity=1, d=0.4)
        self.anim_version_out = Animation(opacity=0, d=0.1)
        Clock.schedule_interval(self.update_progress, 1 / 30)

    def switch_theme(self):
        self.theme_cls.theme_style = (
            "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        )
        self.app.set("theme", self.theme_cls.theme_style)

    def switch_palette(self):
        all_palettes = ["Teal", "Olive", "Purple", "Red"]
        i = all_palettes.index(self.theme_cls.primary_palette)
        i += 1
        i %= len(all_palettes)
        self.theme_cls.primary_palette = all_palettes[i]
        self.app.set("palette", self.theme_cls.primary_palette)

    def open_time_picker(self, time_obj=None):
        self.anim_version_out.stop(self.ids.version)
        self.anim_version_in.start(self.ids.version)
        if time_obj:
            kwargs = {"hour": str(time_obj.hour), "minute": str(time_obj.minute)}
        else:
            hour, minute = time.strftime("%H:%M", time.localtime()).split(":")
            kwargs = {"hour": hour, "minute": minute}

        if not self.app.get("time_edit"):
            if self.theme_cls.device_orientation == "landscape":
                self.time_picker = MDTimePickerDialHorizontal(**kwargs)
            else:
                self.time_picker = MDTimePickerDialVertical(**kwargs)
        else:
            self.time_picker = MDTimePickerInput(**kwargs)
        self.time_picker.open()
        self.time_picker.bind(
            on_edit=self.time_switch_edit,
            on_ok=self.on_time_picker_ok,
            on_cancel=self.on_time_picker_cancel,
            on_dismiss=self.on_time_picker_dismiss,
        )

    def time_switch_edit(self, *args):
        self.app.set("time_edit", not self.app.get("time_edit"))
        Clock.schedule_once(
            lambda x: self.open_time_picker(self.time_picker.time),
            0.1,
        )
        self.time_picker.dismiss()

    def check_orientation(self, instance, orientation):
        if not isinstance(
            self.time_picker, (MDTimePickerDialHorizontal, MDTimePickerDialVertical)
        ):
            return
        Clock.schedule_once(
            lambda x: self.open_time_picker(self.time_picker.time),
            0.1,
        )
        self.time_picker.dismiss()

    def on_time_picker_cancel(self, instance):
        instance.dismiss()

    def on_time_picker_dismiss(self, instance):
        if isinstance(instance, type(self.time_picker)):
            self.time_picker = None
            self.anim_version_in.stop(self.ids.version)
            self.anim_version_out.start(self.ids.version)

    def on_time_picker_ok(self, instance):
        user_h = instance.time.hour
        user_m = instance.time.minute
        instance.dismiss()
        th, tm, ts = time.strftime("%H:%M:%S", time.localtime()).split(":")
        h = user_h - int(th)
        m = user_m - int(tm)
        time_to_wait = h * 3600 + m * 60 - int(ts)
        self.start_time = round(time.time())
        self.end_time = self.start_time + time_to_wait
        self.update_progress()
        if self.event:
            Clock.unschedule(self.event)
        self.event = Clock.schedule_once(self.stop_bar, time_to_wait)

    def update_progress(self, *args):
        self.ids.clock.text = time.strftime("%H:%M", time.localtime())
        if not self.start_time:
            return
        time_to_wait = self.end_time - self.start_time
        current_relative_time = time.time() - self.start_time
        percent = current_relative_time / time_to_wait * 100
        percent_value = max(min(percent, 100), 0)
        self.ids.progress.value = percent_value
        self.ids.percent.text = f"{round(percent_value)}%"
        restant_time = max(round(time_to_wait - current_relative_time), 0)
        s = restant_time % 60
        m = restant_time // 60 % 60
        h = (restant_time - m - s) // 3600
        if h:
            self.ids.time.text = f"{h:02}:{m:02}:{s:02}"
        elif m or s:
            self.ids.time.text = f"{m:02}:{s:02}"
        else:
            self.ids.time.text = ""

    def stop_bar(self, *args):
        self.ids.progress.stop()
        self.ids.progress.value = 100
        self.event = None
