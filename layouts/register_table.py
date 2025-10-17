from kivymd.uix.list import MDListItem

KV = """

        MDListItem:
            ripple_scale: 0.07
            height:150
            

        # MDScreen:
        #           
            MDTextField:
                mode: "outlined"
                id: car_number_%d
                helper_text_mode: "on_focus"
                pos_hint: {"center_x": .19, "center_y": .%p}
                size_hint_x: .20
                hint_text: app.messages['car number']
                helper_text: app.messages["car number"]
                elevation: 105
                
                MDTextFieldHintText:
                    text: app.messages['car number']
                
                MDTextFieldHelperText:
                    helper_text_mode: "on_focus"
                    text: app.messages['car number']

            MDTextField:
                mode: "outlined"
                id: stay_%d
                text: '1'
                hint_text_mode: "on_focus"
                pos_hint: {"center_x": .40, "center_y": .%p}
                size_hint_x: .20
                hint_text: app.messages['stay']
                helper_text: app.registry_class.time_unit_check()
                elevation: 105
                
                MDTextFieldHintText:
                    hint_text_mode: "on_focus"
                    text: app.messages['stay']
                
                MDTextFieldHelperText:
                    helper_text_mode: "on_focus"
                    text: app.registry_class.time_unit_check()

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

KVE = "".join(["""
        MDListItem:
            height: 100
            ripple_scale: 0.07
""" for _ in range(5)])