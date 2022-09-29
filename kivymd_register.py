from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder

KV = """
        
        BaseListItem:
            ripple_scale: 0.07
            height:100
            
        # MDScreen:
        #             
            MDTextField:
                mode: "round"
                id: car_number_%d
                helper_text_mode: "on_focus"
                pos_hint: {"center_x": .19, "center_y": .%p}
                size_hint_x: .20
                hint_text: app.messages['car number']
                helper_text: app.messages["car number"]
                elevation: 105
            
            MDTextField:
                mode: "round"
                id: stay_%d
                text: '1'
                hint_text_mode: "on_focus"
                pos_hint: {"center_x": .40, "center_y": .%p}
                size_hint_x: .20
                hint_text: app.messages['stay']
                helper_text: app.registry_class.time_unit_check()
                elevation: 105
            
            MDLabel:
                pos_hint: {"center_x": .61, "center_y": .%p}
                size_hint_x: .20
                text: app.messages['paid']
                
            MDSwitch:
                id: paid_%d
                pos_hint: {'center_x': .67, 'center_y': .%p}
            
            MDLabel:
                mode: "fill"
                pos_hint: {"center_x": .81, "center_y": .%p}
                size_hint_x: .20
                text: app.messages['left']
            
            MDSwitch:
                id: left_%d
                pos_hint: {'center_x': .87, 'center_y': .%p}

"""

KV =\
"""
        
            
""" + KV

KVE = "".join(["""
        BaseListItem:
            height: 100
            ripple_scale: 0.07
""" for _ in range(5)])



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
        pos = 70
        for st in range(count):
            kv += KV.replace("%d", str(st))
            kv = kv.replace("%p", str(pos))
            # pos -= 10
        return kv

    def _load_kv(self, kv: str):
        # kv = "\nScrollView:\n\tMDList:\n" + kv
        kv = "\nScrollView:\n\tpos_hint: {\"center_x\": .5, \"center_y\": .1}\n\tMDList:\n\t" + kv + KVE
        self.layout = Builder.load_string(kv)
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