
import os
import locale
import sys

from kivy.lang import Builder

parent = os.path.abspath('../')
sys.path.append(parent)
import parking_lib

if os.name == "nt":
    from ctypes import windll, c_int64
    windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))

import datetime
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from DataTable import DataTable as MDDataTable, get_table
# from DataTable import KV as KVTable
# from kivymd.uix.datatables import MDDataTable





KV = """
MDDataTable:
    text-align: center
"""


class MainTableOLD(MDApp):

    parkings = parking_lib.Checking(dbname="parking.db")  # "parking.db"
    env_date = datetime.datetime.now()

    def build(self):
        locale_strings = locale.localeconv()
        self.currency = locale_strings["currency_symbol"]
        # parking_lib.test(self.parkings).add_random_data(3000,("2022-01-01", "2023-01-01"))
        self._data = self.prepare_data()

        self.column_names = self.parkings.bases.field_names_list()
        self.column_names = [[val] for val in self.column_names]
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        layout = FloatLayout()
        column_props = [
            [dp(30)],
            [dp(20)],
            [dp(30)],
            [dp(50), self.sort_on_col_3],
            [dp(50)],
            [dp(40)],
            [dp(30)],
            [dp(20)],
            [dp(30), self.sort_on_col_2]
        ]
        column_props = [tuple(val + column_props[idx]) for idx, val in enumerate(self.column_names)]
        self.data_tables = MDDataTable(
            size_hint=(1, 0.77),
            use_pagination=True,
            pagination_menu_pos="center",
            pagination_menu_height="231dp",
            # background_color="#aaccee",
            # background_color_cell="#e1f3c9",
            # background_color_selected_cell="#e1f6ef",
            rows_num=10,
            check=True,
            background_color_header="#ddeeff",
            effect_cls="DampedScrollEffect",
            elevation=1,
            column_data=column_props,
            row_data=self._data,
            pos_hint = {"center_x": .50, "center_y": .50},
        )
        layout.add_widget(self.data_tables)
        return layout

class MainTable(MDApp):

    parkings = parking_lib.Checking(dbname="parking.db")  # "parking.db"
    env_date = datetime.datetime.now()

    def build(self):
        locale_strings = locale.localeconv()
        self.currency = locale_strings["currency_symbol"]
        # parking_lib.test(self.parkings).add_random_data(3000,("2022-01-01", "2023-01-01"))
        self._data = self.prepare_data()
        screen = get_table()
        self.screen = screen
        self.column_names = self.parkings.bases.field_names_list()
        self.column_names = [[val] for val in self.column_names]
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        layout = FloatLayout()
        # layout.pos_hint = {"center_x": .50, "center_y": .50}
        # screen.pos_hint = {"center_x": 0.5, "center_y": .3}
        size_map = (0.2,1,0.2,0.5,0.5,0.5,0.4,0.17,0.17)
        column_props = [(val[0],size_map[idx]) for idx, val in enumerate(self.column_names)]
        screen.ids.data_table.rows_per_page = 5
        screen.ids.data_table.set_data(column_props, self._data)
        layout.add_widget(screen)
        return layout

    def prepare_data(self, period="day", modes: dict=None):
        if type(modes) is not dict:
            modes = {"selection_mode":"present"}
        if period == "all":
            modes = {}
        func = {"day":self.parkings.all_for_the_day,"week":self.parkings.all_for_the_week,"month":self.parkings.all_for_the_month,"year":self.parkings.all_for_the_year,"all":self.parkings.all_records}
        data = func[period](self.env_date, **modes)
        self._raw_data = data.copy()
        data = self.parkings.bases.modify_fields(
            data,
            arrival=self.verb_date,
            departure=self.verb_date,
            stay=self.verb_stay,
            price=self.currency_sign,
            left=self.is_left_icon,
            paid=self.is_paid_icon
        )
        return data


    def verb_date(self, date):
        return datetime.datetime.strftime(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"), "%d %B %Y - %H:%M")

    def verb_stay(self, stay):
        return ", ".join(self.parkings.bases.get_time(stay))

    def is_left_icon(self, left):
        if not left:
            return ("close-circle-outline", [0, 165 / 256, 0, 1])
        else:
            return ("check-circle-outline", [165 / 256, 165 / 256, 165 / 256, 0.30])

    def is_paid_icon(self, paid):
        if paid:
            return ("check-circle-outline", [0, 165 / 256, 0, 0.20])
        else:
            return ("close-circle-outline", [165 / 256, 0, 0, 1])

    def currency_sign(self, val):
        return str(val) + " " + self.currency

    def sort_on_col_3(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][3]
            )
        )

    def sort_on_col_2(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][-1]
            )
        )

    def set_rows_per_page(self, count):
        """Change the number of rows displayed per page."""
        self.screen.ids.data_table.rows_per_page = count
        self.screen.ids.data_table.current_page = 1  # Reset to first page
        self.screen.ids.data_table._update_table()

    def update_table_data(self, data):
        self.screen.ids.data_table.row_data = data
        self.screen.ids.data_table._update_table()


if __name__ == "__main__":
    MainTable().run()
