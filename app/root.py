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
    time_picker_horizontal: MDTimePickerDialHorizontal = ObjectProperty(allownone=True)
    time_picker_vertical: MDTimePickerDialVertical = ObjectProperty(allownone=True)
    time_picker_input: MDTimePickerInput = ObjectProperty(allownone=True)

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

    def select_time(self, h=None, m=None):
        hour, minutes = time.strftime("%H:%M", time.localtime()).split(":")
        if not self.app.store["time_edit"]["value"]:
            (
                self.open_time_picker_horizontal(h if h else hour, m if m else minutes)
                if self.theme_cls.device_orientation == "landscape"
                else self.open_time_picker_vertical(
                    h if h else hour, m if m else minutes
                )
            )
        else:
            self.open_time_picker_input(h if h else hour, m if m else minutes)

    def time_switch_edit(self, *args):
        if self.time_picker_input:
            self.app.store["time_edit"] = {"value": False}
            self.time_picker_input.dismiss()
            hour = str(self.time_picker_input.time.hour)
            minute = str(self.time_picker_input.time.minute)
            Clock.schedule_once(
                lambda x: self.select_time(hour, minute),
                0.1,
            )
        elif self.time_picker_horizontal:
            self.app.store["time_edit"] = {"value": True}
            self.time_picker_horizontal.dismiss()
            hour = str(self.time_picker_horizontal.time.hour)
            minute = str(self.time_picker_horizontal.time.minute)
            Clock.schedule_once(
                lambda x: self.select_time(hour, minute),
                0.1,
            )
        elif self.time_picker_vertical:
            self.app.store["time_edit"] = {"value": True}
            self.time_picker_vertical.dismiss()
            hour = str(self.time_picker_vertical.time.hour)
            minute = str(self.time_picker_vertical.time.minute)
            Clock.schedule_once(
                lambda x: self.select_time(hour, minute),
                0.1,
            )

    def check_orientation(self, instance, orientation):
        if orientation == "portrait" and self.time_picker_horizontal:
            self.time_picker_horizontal.dismiss()
            hour = str(self.time_picker_horizontal.time.hour)
            minute = str(self.time_picker_horizontal.time.minute)
            Clock.schedule_once(
                lambda x: self.open_time_picker_vertical(hour, minute),
                0.1,
            )
        elif orientation == "landscape" and self.time_picker_vertical:
            self.time_picker_vertical.dismiss()
            hour = str(self.time_picker_vertical.time.hour)
            minute = str(self.time_picker_vertical.time.minute)
            Clock.schedule_once(
                lambda x: self.open_time_picker_horizontal(hour, minute),
                0.1,
            )

    def open_time_picker_horizontal(self, hour, minute):
        self.time_picker_vertical = None
        self.time_picker_input = None
        self.time_picker_horizontal = MDTimePickerDialHorizontal(
            hour=hour, minute=minute
        )
        self.time_picker_horizontal.open()
        self.time_picker_horizontal.bind(
            on_edit=self.time_switch_edit,
            on_ok=self.on_time_picker_ok,
            on_cancel=self.on_time_picker_cancel,
            on_dismiss=self.on_time_picker_dismiss,
        )

    def open_time_picker_vertical(self, hour, minute):
        self.time_picker_horizontal = None
        self.time_picker_input = None
        self.time_picker_vertical = MDTimePickerDialVertical(hour=hour, minute=minute)
        self.time_picker_vertical.open()
        self.time_picker_vertical.bind(
            on_edit=self.time_switch_edit,
            on_ok=self.on_time_picker_ok,
            on_cancel=self.on_time_picker_cancel,
            on_dismiss=self.on_time_picker_dismiss,
        )

    def open_time_picker_input(self, hour, minute):
        self.time_picker_horizontal = None
        self.time_picker_vertical = None
        self.time_picker_input = MDTimePickerInput(hour=hour, minute=minute)
        self.time_picker_input.open()
        self.time_picker_input.bind(
            on_edit=self.time_switch_edit,
            on_ok=self.on_time_picker_ok,
            on_cancel=self.on_time_picker_cancel,
            on_dismiss=self.on_time_picker_dismiss,
        )

    def on_time_picker_cancel(self, instance):
        instance.dismiss()

    def on_time_picker_dismiss(self, instance):
        self.time_picker_horizontal = None
        self.time_picker_vertical = None
        self.time_picker_input = None

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
        h = restant_time // 60 // 60
        if h:
            self.ids.time.text = f"{h}:{m}:{s}"
        elif m or s:
            self.ids.time.text = f"{m}:{s}"
        else:
            self.ids.time.text = ""

    def stop_bar(self, *args):
        self.ids.progress.stop()
        self.ids.progress.value = 100
        self.event = None
