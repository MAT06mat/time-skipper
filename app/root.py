from kivymd.uix.pickers import (
    MDTimePickerDialHorizontal,
    MDTimePickerDialVertical,
    MDTimePickerInput,
)
from kivy.properties import ObjectProperty, NumericProperty
from kivymd.uix.screen import MDScreen
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
        Clock.schedule_interval(self.update_progress, 1)

    def switch_theme(self):
        self.theme_cls.theme_style = (
            "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        )
        self.app.store["theme"] = {"value": self.theme_cls.theme_style}

    def open_time_picker(self, h=None, m=None):
        hour, minute = time.strftime("%H:%M", time.localtime()).split(":")
        if not self.app.store["time_edit"]["value"]:
            if self.theme_cls.device_orientation == "landscape":
                self.time_picker = MDTimePickerDialHorizontal(
                    hour=h if h else hour, minute=m if m else minute
                )
            else:
                self.time_picker = MDTimePickerDialVertical(
                    hour=h if h else hour, minute=m if m else minute
                )
        else:
            self.time_picker = MDTimePickerInput(
                hour=h if h else hour, minute=m if m else minute
            )
        self.time_picker.open()
        self.time_picker.bind(
            on_edit=self.time_switch_edit,
            on_ok=self.on_time_picker_ok,
            on_cancel=self.on_time_picker_cancel,
            on_dismiss=self.on_time_picker_dismiss,
        )

    def time_switch_edit(self, *args):
        self.app.store["time_edit"] = {
            "value": not self.app.store["time_edit"]["value"]
        }
        hour = str(self.time_picker.time.hour)
        minute = str(self.time_picker.time.minute)
        self.time_picker.dismiss()
        Clock.schedule_once(
            lambda x: self.open_time_picker(hour, minute),
            0.1,
        )

    def check_orientation(self, instance, orientation):
        if not isinstance(
            self.time_picker, (MDTimePickerDialHorizontal, MDTimePickerDialVertical)
        ):
            return
        hour = str(self.time_picker.time.hour)
        minute = str(self.time_picker.time.minute)
        self.time_picker.dismiss()
        Clock.schedule_once(
            lambda x: self.open_time_picker(hour, minute),
            0.1,
        )

    def on_time_picker_cancel(self, instance):
        instance.dismiss()

    def on_time_picker_dismiss(self, instance):
        if isinstance(instance, type(self.time_picker)):
            self.time_picker = None

    def on_time_picker_ok(self, instance):
        user_h = instance.time.hour
        user_m = instance.time.minute
        instance.dismiss()
        th, tm, ts = time.strftime("%H:%M:%S", time.localtime()).split(":")
        h = user_h - int(th)
        m = user_m - int(tm)
        time_to_wait = h * 3600 + m * 60 - int(ts)
        self.start_time = time.time()
        self.end_time = self.start_time + time_to_wait
        self.ids.progress.stop()
        self.ids.progress.running_determinate_duration = time_to_wait
        self.ids.progress.running_anim = None
        self.ids.progress.catching_anim = None
        self.ids.progress.start()
        self.update_progress()
        if self.event:
            Clock.unschedule(self.event)
        self.event = Clock.schedule_once(self.stop_bar, time_to_wait)

    def update_progress(self, *args):
        if not self.start_time:
            return
        time_to_wait = self.end_time - self.start_time
        current_relative_time = time.time() - self.start_time
        percent = current_relative_time / time_to_wait * 100
        self.ids.percent.text = f"{max(min(round(percent), 100), 0)}%"
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
