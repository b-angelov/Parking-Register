# import packages
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItemHeadlineText

from layouts.layouts import Layout

APP_VERSION = "2.0.0"
import os
import locale
if os.name == "nt":
    from ctypes import windll, c_int64
    windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))
    locale.setlocale(locale.LC_ALL, 'bg_BG')
else:
    locale.setlocale(locale.LC_ALL, 'bg_BG.UTF-8')

from kivymd.uix.button import MDButton, MDButtonText
# from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogSupportingText
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.pickers import MDModalDatePicker, MDTimePickerDialVertical
# from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd_table import MainTable
from kivymd_register import RegisterTable
from kivy.core.window import Window
from layouts.messages import Messages

Window.fullscreen = 'auto'

# writing kv lang



# App class
class ParkingRegister(MDApp):

    messages = Messages(APP_VERSION=APP_VERSION).messages
    table_class = MainTable()
    registry_class = RegisterTable()
    now = None
    temp_date = None
    dialog = None

    def build(self, sorted_by: tuple = ("day","present")):
        # this will load kv lang
        self.icon = "my_ico.png"
        self.registry_class.messages = self.messages
        self.sorted_by = list(sorted_by)
        screen = Layout("default").build()
        # print(self.sorted_by)
        self.run_clock()
        self.register_widget = screen.ids.home.add_widget(self.registry_class.build())
        # table = self.table_class.build()
        # self.table_widget = screen.ids.registered.add_widget(table)
        # returning screen
        return screen

    def switch_tabs(self, bar,item,icon,text):
        {
            "home": lambda: self.show_registry(),
            "registered": lambda: self.show_table(),
            "about": lambda: self.change_screen(item.name)
        }.get(item.name, lambda: None)()

    def show_table(self):
        try:
            if not self.table_widget:
                raise Exception
        except:
            widget = self.table_class.build()
            self.table_class.screen.ids.data_table.pos_hint = {"center_x": 0.5, "center_y": 3.5}
            self.table_class.screen.ids.data_table.size_hint = 0.98, 4.4
            self.root.ids.registry_content.add_widget(widget)
            # self.root.ids.registered.add_widget(self.add_sort_dialog())
            self.table_widget = widget
        self.change_screen("registered")

    def show_registry(self):
        try:
            self.registry_widget
        except:
            self.root.ids.home.add_widget(self.registry_class.build())
            self.registry_widget = True
        self.change_screen("home")

    def add_sort_dialog(self):

        menu_items = [
            {
                "id": "sort_button",
                "height": dp(42),
                "width": dp(10),
                "text":f'{self.messages["sort by"]}: {self.messages["time dict"][self.sorted_by[0]]}, {self.messages["sort dict"][self.sorted_by[1]]}',
                "on_release": lambda x=f"{self.sorted_by[1]}": self.sort_menu(x)
            }
            ]
        menu_items += [
            {
                "height": dp(42),
                "width": dp(10),
                "text":f"{i}",
                "on_release": lambda x=f"{i}": self.sort_by_time(x),
            } for i in self.messages["time dict"].values()
        ]
        # print(self.root.ids.button, menu_items)
        # exit()
        self.menu = MDDropdownMenu(
            caller=self.root.ids.button,
            items=menu_items,
            width_mult=8,
        )
        return self.menu

    def sort_by_time(self, sort_time):
        if sort_time in self.messages["time dict"].values():
            sort_time = {v:k for (k,v) in self.messages["time dict"].items()}[sort_time]
        # print(sort_time)
        self.sorted_by[0] = sort_time
        # self.root.ids.sort_label.text = f"{self.messages['time dict'][self.sorted_by[0]]}, {self.messages['sort dict'][self.sorted_by[1]]}"
        mode = {"selection_mode": self.sorted_by[1]}
        self.table_class.update_table_data(self.table_class.prepare_data(sort_time, mode))

    def re_sort(self, sort_mode):
        # print(sort_mode)
        self.sorted_by[1] = sort_mode
        self.sort_by_time(self.sorted_by[0])

    def sort_menu(self, sort_mode):
        menu_items = [
            {
                "height": dp(42),
                "width": dp(10),
                "text": f"{v}",
                "on_release": lambda x=f"{k}": self.re_sort(x),
            } for k,v in self.messages["sort dict"].items()
        ]

        menu = MDDropdownMenu(
            caller=self.root.ids.button,
            items=menu_items,
            width_mult=4,
        )
        return menu.open()


    def change_screen(self, screen: str):
        # screen = self.root.ids
        self.root.ids.screen_manager.current = screen

    def clock_fields(self, date = None):
        if self.temp_date:
            date = self.temp_date
        self.now = str(self.table_class.parkings.bases.date_or_now(date))
        self.table_class.env_date = self.now
        now = self.table_class.verb_date(self.now).split(" - ")
        self.root.ids.text_field_date.text = now[0]
        self.root.ids.text_field_time.text = now[1]
        # print(self.root.ids)
        # return self.table_class.verb_date(self.now).split(" - ")

    def run_clock(self):
        self.clock_schedule_holder = Clock.schedule_interval(lambda x: self.clock_fields(), 1)

    def stop_clock(self):
        self.clock_schedule_holder.cancel()

    def on_date_save(self, *args):
        instance, = args
        value = args[1] if len(args) > 1 else instance.get_date()[0].strftime('%Y-%m-%d %H:%M:%S.%f')
        self.temp_date = str(value)
        instance.dismiss()
        pass

    def on_date_cancel(self, instance, value):
        self.temp_date = None
        pass

    def on_time_save(self, *args):
        instance,*args = args
        value = args[0] if args else instance.time
        add = 0
        if self.time_dialog.am_pm == "pm":
            add = 12
        value = str(value).split(":")
        value[0] = str(add + int(value[0]))
        self.temp_date = self.now.split(" ")[0] + " " + ":".join(value)
        # print(self.temp_date)
        instance.dismiss()
        pass

    def show_date_picker(self):
        self.date_dialog = MDModalDatePicker()
        self.date_dialog.bind(on_ok=self.on_date_save)
        self.date_dialog.open()

    def show_time_picker(self):
        self.time_dialog = MDTimePickerDialVertical()
        self.time_dialog.bind(on_ok=self.on_time_save)
        self.time_dialog.open()

    def replace_widget(self, widget_id, new_widget, trim_count=3):
        # print(widget_id.children)
        widget_id.clear_widgets(widget_id.children[:-trim_count])
        # widget_id.remove_widget(self.root.ids.registry_app)
        widget_id.add_widget(new_widget)

    def count_menu(self, max_fields=10):
        # print(self.registry_class.layout.ids)
        menu_items = [
            {
                "height": dp(42),
                "width": dp(10),
                "text": f"{i + 1}",
                "on_press": lambda x=i: self.replace_widget(self.root.ids.home, self.registry_class._load_view(x + 1),4),
            } for i in range(10)
        ]

        count_menu_list = MDDropdownMenu(
            caller=self.root.ids.count_button,
            items=menu_items,
            width_mult=1,
        )
        return count_menu_list.open()

    def submit(self):
        # print(self.dialog)
        count = self.registry_class.fields_count
        instance = self.registry_class.layout.ids
        item_list = [{"car number":instance[f"car_number_{i}"].text, "stay duration":instance[f"stay_{i}"].text, "paid":instance[f"paid_{i}"].active, "left":instance[f"left_{i}"].active} for i in range(count) if instance[f"car_number_{i}"].text and instance[f"stay_{i}"].text]
        # self.dialog_instance = self.submit_dialog()
        submit = self.dialog
        self.dialog_switch()
        date = self.now
        if self.temp_date:
            date = self.table_class.parkings.bases.filled_datetime(self.temp_date)
        if submit:
            for item in item_list:
                self.table_class.parkings.register_car(date, **item)
        pass

    def submit_dialog(self):
        cancel = MDButton(
            style="filled",
            on_release=lambda x: self.process_dialog(False)
        )
        save = MDButton(
            style="filled",
            on_release=lambda x: self.process_dialog(True)
        )
        cancel.add_widget(MDButtonText(
            text=self.messages["cancel"],
            text_color=self.theme_cls.primaryContainerColor,
        ))
        save.add_widget(MDButtonText(
            text=self.messages["save"],
            text_color=self.theme_cls.primaryContainerColor,
        ))

        self.dialog_instance = MDDialog(
            MDDialogSupportingText(text=self.messages["confirm save"]),
            MDDialogButtonContainer(save,cancel)
        )
        self.dialog_instance.open()
        return self.dialog_instance

    def dialog_switch(self, mode = None):
        self.dialog = mode

    def reload_registry_widget(self):
        # print(self.registry_class.fields_count)
        self.replace_widget(self.root.ids.home, self.registry_class._load_view(self.registry_class.fields_count),4)

    def process_dialog(self, value):
        self.dialog_switch(value)
        if value:
            self.submit()
            self.reload_registry_widget()
        self.dialog_instance.dismiss()

    def time_unit_menu(self):
        # print(self.registry_class.layout.ids)
        units_menu = self.messages["time dict"].copy()
        del units_menu["all"]
        units_menu["hour"] = self.messages["hour"]
        menu_items = [
            {
                "height": dp(42),
                "width": dp(10),
                "text": f"{v}",
                "on_press": lambda x=i: self.time_unit_func(x),
            } for (i,v) in units_menu.items()
        ]

        unit_menu_list = MDDropdownMenu(
            caller=self.root.ids.time_unit_button,
            items=menu_items,
            width_mult=2,
        )

        return unit_menu_list.open()

    def time_unit_func(self, unit):
        self.time_unit, self.registry_class.time_unit =  unit, unit
        self.table_class.parkings.time_mode = unit + "s"
        self.reload_registry_widget()

    def set_rows_per_page(self, count, widget=None):
        widget = widget or self.table_class
        widget.set_rows_per_page(count)



# running app
ParkingRegister().run()
