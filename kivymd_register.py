from kivy.metrics import dp
from kivymd.app import MDApp
# from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder

from layouts.layouts import Layout

layout_module = Layout("register_table")

KV =\
"""
        
            
""" + layout_module.module.KV

KVE = layout_module.module.KVE



class RegisterTable(MDApp):

    if __name__ == "__main__":
        from kivymd_main import ParkingRegister
        messages = ParkingRegister.messages

    def build(self):
        self.time_unit_check()
        return self._load_view(1)
        pass

    def define_textfields(self):
        pass

    def multiple_fields(self, count: int=1):
        kv = ""
        pos = 50
        for st in range(count):
            kv += KV.replace("%d", str(st))
            kv = kv.replace("%p", str(pos))
            # pos -= 10
        return kv

    def _load_kv(self, kv: str):
        # kv = "\nScrollView:\n\tMDList:\n" + kv
        kv = "\nScrollView:\n\tpos_hint: {\"center_x\": .49, \"center_y\": .05}\n\tMDList:\n\t" + kv + KVE
        self.layout = layout_module.build(kv)
        return self.layout

    def _load_view(self, count: int):
        self.fields_count = count
        kv = self.multiple_fields(count)
        return self._load_kv(kv)

    def time_unit_check(self):
        try:
            return self.messages["time dict"][self.time_unit]
        except:
            self.time_unit = "hour"
            return self.messages[self.time_unit]




if __name__ == "__main__":
    RegisterTable().run()