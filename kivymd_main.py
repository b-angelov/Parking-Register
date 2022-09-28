# import packages
APP_VERSION = "Alpha 1.0.0"
import os
import locale
if os.name == "nt":
    from ctypes import windll, c_int64
    windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))
    locale.setlocale(locale.LC_ALL, 'bg_BG')
else:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd_table import MainTable
from kivymd_register import RegisterTable

# writing kv lang
KV = '''
# declaring layout/screen
MDScreen:

	# this will create a space navigation bottom
	MDBottomNavigation:

		# this will create a navigation button on the bottom of screen
		MDBottomNavigationItem:
		    id: first
			name: 'screen 1'
			text: app.messages['register title']
			icon: 'book-arrow-up'
			

			# this will be triggered when screen 1 is selected
			# creates a label
			on_tab_press: app.change_screen("screen 1")
			# on_tab_press: app.show_registry()
			# on_tab_press: app.replace_widget(app.root.ids.first, app.registry_class._load_view(8))
			
			MDRectangleFlatButton:
			    pos_hint: {"center_x": .9, "center_y": .65}
			    width: 1
			    text_color: "grey"
			    line_color: "grey"
                id: submit_button
                name: 'submit_button'
                text: 'Изпрати'
                on_press: app.submit_dialog()
			
			MDRectangleFlatButton:
			    pos_hint: {"center_x": .1, "center_y": .65}
			    width: 1
			    text_color: "grey"
			    line_color: "grey"
                id: count_button
                name: 'count_button'
                text: 'Брой полета'
                on_press: app.count_menu()
                
            MDRectangleFlatButton:
			    pos_hint: {"center_x": .5, "center_y": .65}
			    width: 1
			    text_color: "grey"
			    line_color: "grey"
                id: time_unit_button
                name: 'time_unit_button'
                text: 'Единица за време'
                on_press: app.time_unit_menu()
                
            
			
			MDLabel:
				text: app.messages['register a car']
				halign: 'center'
				valign: 'bottom'
				pos_hint: {"center_x": .50, "center_y": .80}
				

		# this will create a navigation button on the bottom of screen
		MDBottomNavigationItem:
		    id: second
			name: 'screen 2'
			text: app.messages['show registered title']
			icon: 'car'
			

			# this will be triggered when screen 2 is selected
			# creates a label
			# on_tab_press: app.show_table()
			   
			
			MDLabel:
				text: f"{app.messages['view registered']} {app.messages['sort by']}:"
				halign: 'center'
				pos_hint: {"center_x": .50, "center_y": .07}
				index: 100
			
			MDLabel:
			    id: sort_label
			    text: f"{app.messages['time dict'][app.sorted_by[0]]}, {app.messages['sort dict'][app.sorted_by[1]]}"
			    halign: 'center'
                pos_hint: {"center_x": .50, "center_y": .03}
                index: 100
				
            MDRaisedButton:
                id: button
                name: "screen 2"
                text: "Сортиране"
                pos_hint: {"center_x": .1, "center_y": .06}
                on_release: app.add_sort_dialog().open()
            
            
        
			    

		# this will create a navigation button on the bottom of screen
		MDBottomNavigationItem:
		    id: third
			name: 'screen 3'
			text: app.messages['about the app title']
			icon: 'check-decagram'

            on_tab_press: app.change_screen("screen 3")
			# this will be triggered when screen 3 is selected
			# creates a label
			MDLabel:
				text: app.messages['about the app']
				halign: 'center'
				
	MDTextField:
        id: text_field_date
        hint_text: "Helper text on error (press 'Enter')"
        helper_text: "There will always be a mistake"
        helper_text_mode: "on_error"
        pos_hint: {"center_x": .15, "center_y": .95}
        size_hint_x: .25
        hint_text: app.messages["today"] + ":"
        text: app.table_class.verb_date(str(app.table_class.parkings.bases.date_or_now())).split(" -")[0]
        on_focus: app.show_date_picker() if self.focus else None
        elevation: 105
    
    MDTextField:
        id: text_field_time
        hint_text: "Helper text on error (press 'Enter')"
        helper_text: "There will always be a mistake"
        helper_text_mode: "on_error"
        pos_hint: {"center_x": .35, "center_y": .95}
        size_hint_x: .10
        hint_text: app.messages["now"] + ":"
        text: app.table_class.verb_date(str(app.table_class.parkings.bases.date_or_now())).split(" - ")[1]
        on_focus: app.show_time_picker() if self.focus else None
        
    MDTextButton:
        text: "MDTextButton"
        custom_color: "red"
        text: app.messages["reset date"]
        on_press: app.on_date_cancel(None,None) 
        fofnt_style: 'Subtitle1'
        font_size: '10sp'
        pos_hint: {"center_x": .58, "center_y": .95}
        size_hint_x: .30
				 
'''


# App class
class ParkingRegister(MDApp):

    messages = {
        "cancel": "Отказ",
        "save": "Запиши",
        "confirm save": "Желаете ли запишете посочените номера в регистъра?",
        "car number": "Номер МПС:",
        "stay": "Престой:",
        "paid": "Платено:",
        "left": "Напуснал:",
        "register a car": "Регистриране на автомобил",
        "view registered": "Преглед на регистрираните",
        "register title": "Регистрирай",
        "show registered title": "Покажи регистрираните",
        "about the app title": "За приложението",
        "about the app": f"Паркинг регистратор\n Конзолно приложение плюс графичен интерфейс \n с помощта на KivyMD 1.0.0 \n Борислав Ангелов 2022 © \n Версия: {APP_VERSION}",
        "sort by": "Сортиране по",
        "today": "Днешна дата",
        "now": "Час",
        "hour": "час",
        "reset date": "Сверяване на часовника",
        "time dict" : {"day": "Ден", "week": "Седмица", "month": "Месец", "year": "Година", "all":"Всички данни"},
        "sort dict" : {"arrival":"Пристигане", "departure":"Заминаване", "present":"Присъствали през периода", "present_strict":"Присъстващи в момента" }
    }
    table_class = MainTable()
    registry_class = RegisterTable()
    now = None
    temp_date = None
    dialog = None

    def build(self, sorted_by: tuple = ("day","present")):
        # this will load kv lang
        self.registry_class.messages = self.messages
        self.sorted_by = list(sorted_by)
        screen = Builder.load_string(KV)
        # print(self.sorted_by)
        self.run_clock()
        self.register_widget = screen.ids.first.add_widget(self.registry_class.build())
        table = self.table_class.build()
        self.table_widget = screen.ids.second.add_widget(table)
        # returning screen
        return screen

    def show_table(self):
        try:
            self.table_widget
        except:
            self.root.ids.second.add_widget(self.table_class.build())
            # self.root.ids.second.add_widget(self.add_sort_dialog())
            self.table_widget = True
        self.change_screen("screen 2")

    def show_registry(self):
        try:
            self.registry_widget
        except:
            self.root.ids.first.add_widget(self.registry_class.build())
            self.registry_widget = True
        self.change_screen("screen 1")

    def add_sort_dialog(self):

        menu_items = [
            {
                "id": "sort_button",
                "height": dp(42),
                "width": dp(10),
                "text": f'{self.messages["sort by"]}: {self.messages["time dict"][self.sorted_by[0]]}, {self.messages["sort dict"][self.sorted_by[1]]}',
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{self.sorted_by[1]}": self.sort_menu(x)
            }
            ]
        menu_items += [
            {
                "height": dp(42),
                "width": dp(10),
                "text": f"{i}",
                "viewclass": "OneLineListItem",
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
        self.root.ids.sort_label.text = f"{self.messages['time dict'][self.sorted_by[0]]}, {self.messages['sort dict'][self.sorted_by[1]]}"
        mode = {"selection_mode": self.sorted_by[1]}
        self.table_class.data_tables.update_row_data(self.table_class.data_tables, self.table_class.prepare_data(sort_time, mode))

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
                "viewclass": "OneLineListItem",
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
        screen = self.root.ids
        self.root.current = screen

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

    def on_date_save(self, instance, value, date_range):
        self.temp_date = str(value)
        pass

    def on_date_cancel(self, instance, value):
        self.temp_date = None
        pass

    def on_time_save(self, instance, value):
        add = 0
        if self.time_dialog._am_pm_selector.selected == "pm":
            add = 12
        value = str(value).split(":")
        value[0] = str(add + int(value[0]))
        self.temp_date = self.now.split(" ")[0] + " " + ":".join(value)
        # print(self.temp_date)
        pass

    def show_date_picker(self):
        self.date_dialog = MDDatePicker()
        self.date_dialog.bind(on_save=self.on_date_save)
        self.date_dialog.open()

    def show_time_picker(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(on_save=self.on_time_save)
        self.time_dialog.open()

    def replace_widget(self, widget_id, new_widget, trim_count=3):
        # print(widget_id.children)
        widget_id.clear_widgets(widget_id.children[:-trim_count])
        # widget_id.remove_widget(self.root.ids.registry_app)
        widget_id.add_widget(new_widget)

    def count_menu(self):
        # print(self.registry_class.layout.ids)
        menu_items = [
            {
                "height": dp(42),
                "width": dp(10),
                "text": f"{i + 1}",
                "viewclass": "OneLineListItem",
                "on_press": lambda x=i: self.replace_widget(self.root.ids.first, self.registry_class._load_view(x + 1)),
            } for i in range(8)
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
        self.dialog_instance = MDDialog(
            text=self.messages["confirm save"],
            buttons=[
                MDFlatButton(
                    text=self.messages["cancel"],
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.process_dialog(False)
                ),
                MDFlatButton(
                    text=self.messages["save"],
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.process_dialog(True)
                ),
            ],
        )
        self.dialog_instance.open()
        return self.dialog_instance

    def dialog_switch(self, mode = None):
        self.dialog = mode

    def reload_registry_widget(self):
        # print(self.registry_class.fields_count)
        self.replace_widget(self.root.ids.first, self.registry_class._load_view(self.registry_class.fields_count))

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
                "viewclass": "OneLineListItem",
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



# running app
ParkingRegister().run()
