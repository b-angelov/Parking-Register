KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "10dp"

        MDLabel:
            text: "Dropdown Menu Example"
            halign: "center"

        MDRectangleFlatButton:
            id: drop_button
            text: "Choose Option"
            pos_hint: {"center_x": .5}
            on_release: app.menu.open()
'''