from kivymd.uix.navigationbar import MDNavigationBar

KV = '''
# declaring layout/screen
MDScreen:

	# this will create a space navigation bottom
	md_bg_color: "white"
	name: "main_screen"
	
    MDScreenManager:
        id: screen_manager
        
        MDScreen:
            id: home
            name: "home"
            MDLabel:
                text: "Home Screen"
                halign: "center"
                
            # this will be triggered when screen 1 is selected
            # creates a label
            # on_tab_press: app.change_screen("screen 1")
            # on_tab_press: app.show_registry()
            # on_tab_press: app.replace_widget(app.root.ids.first, app.registry_class._load_view(8))

            MDButton:
                pos_hint: {"center_x": .9, "center_y": .765}
                width: 1
                text_color: "black"
                style: "outlined"
                line_color: "grey"
                id: submit_button
                name: 'submit_button'
                text: 'Изпрати'
                on_press: app.submit_dialog()
                
                MDButtonText:
                    text: app.messages['submit']

            MDButton:
                pos_hint: {"center_x": .1, "center_y": .765}
                width: 1
                text_color: "grey"
                style: "outlined"
                line_color: "grey"
                id: count_button
                name: 'count_button'
                on_press: app.count_menu()
                
                MDButtonText:
                    text: app.messages['rows count']

            MDButton:
                pos_hint: {"center_x": .5, "center_y": .765}
                width: 1
                text_color: "grey"
                line_color: "grey"
                style: "outlined"
                id: time_unit_button
                name: 'time_unit_button'
                on_press: app.time_unit_menu()
                
                MDButtonText:
                    text: app.messages['time unit']



            MDLabel:
                text: app.messages['register a car']
                halign: 'center'
                valign: 'bottom'
                pos_hint: {"center_x": .50, "center_y": .80}
                
            

        MDScreen:
            id: registered
            name: "registered"
            MDLabel:
                text: "Settings Screen"
                halign: "center"
            
            # this will be triggered when screen 2 is selected
            # creates a label
            # on_tab_press: app.show_table()
            
            FloatLayout:
                id: registry_content

            FloatLayout:
                id: registry_buttons
                MDButton:
                    id: button
                    name: "screen 2"
                    text: "Сортиране"
                    style: "filled"
                    pos_hint: {"center_x": .84, "center_y": 0.89}
                    on_release: app.add_sort_dialog().open()
                    
                    MDButtonText:
                        text: app.messages['sort']
    
                    MDLabel:
                        text: f"{app.messages['view registered']} {app.messages['sort by']}:"
                        halign: 'center'
                        pos_hint: {"center_x": .50, "center_y": .07}
                        index: 100
    
                    MDLabel:
                        id: sort_label
                        text: f"{app.messages['time dict'][app.sorted_by[0]]}, {app.messages['sort dict'][app.sorted_by[1]]}"
                        halign: 'center'
                        pos_hint: {"center_x": .50, "center_y": .266}
                        index: 100
        
        MDScreen:
            id: about
            name: "about"
            MDLabel:
                text: app.messages['about the app']
                halign: 'center'
                
    MDFloatLayout:
	    id: time_bar
	    MDTextField:
            id: text_field_date
            hint_text: "Helper text on error (press 'Enter')"
            pos_hint: {"center_x": .15, "center_y": .95}
            size_hint_x: .25
            mode: "filled"
            theme_line_color: "Custom"
            theme_fill_color: "Custom"
            fill_color: 1, 1, 1, 1
            line_color_normal: 1, 0, 0, 1 
            line_color_focus: 1, 0, 0, 1  
            fill_color_focus: 1, 1, 1, 1
            fill_color_normal: 1, 1, 1, 1
            hint_text: app.messages["today"] + ":"
            text: app.table_class.verb_date(str(app.table_class.parkings.bases.date_or_now())).split(" -")[0]
            on_focus: app.show_date_picker() if self.focus else None
            elevation: 105
                
            MDTextFieldHelperText:
                text: app.messages["work date error"]
                helper_text_mode: "on_error"
                
            MDTextFieldHintText:
                text: app.messages["work date hint"]

        MDTextField:
            id: text_field_time
            pos_hint: {"center_x": .35, "center_y": .95}
            size_hint_x: .10
            mode: "filled"
            theme_line_color: "Custom"
            theme_fill_color: "Custom"
            fill_color: 1, 1, 1, 1
            line_color_normal: 1, 0, 0, 1 
            line_color_focus: 1, 0, 0, 1  
            fill_color_focus: 1, 1, 1, 1
            fill_color_normal: 1, 1, 1, 1
            icon_right: "clock-outline"
            hint_text: app.messages["now"] + ":"
            text: app.table_class.verb_date(str(app.table_class.parkings.bases.date_or_now())).split(" - ")[1]
            on_focus: app.show_time_picker() if self.focus else None
                
            MDTextFieldHelperText:
                text: app.messages["work time error"]
                helper_text_mode: "on_error"
                
            MDTextFieldHintText:
                text: app.messages["work time hint"]

        MDButton:
            text: "MDTextButton"
            style: "text"
            custom_color: "red"
            on_press: app.on_date_cancel(None,None) 
            font_style: 'Subtitle1'
            font_size: '10sp'
            pos_hint: {"center_x": .45, "center_y": .95}
            size_hint_x: .30
            
            MDButtonText:
                text: app.messages["reset date"]
	
    
    MDNavigationBar:
        id: bottom_nav_bar
        panel_color: 1, 1, 1, 1
        selected_color_background: 0.1, 0.3, 0.9, 1
        text_color_active: 1, 0, 0, 1  # Red when active
        text_color_normal: 0.5, 0.5, 0.5, 1  # Gray when inactive
        icon_color_active: 1, 0, 0, 1  # Red when active
        icon_color_normal: 0.5, 0.5, 0.5, 1  # Gray when inactive
        elevation: 10
        on_switch_tabs: app.switch_tabs(*args)
        # this will create a navigation button on the bottom of screen
        
        MDNavigationItem:
            id: first_nav
            name: 'home'
            text: app.messages['register title']
            icon: 'book-arrow-up'
            MDNavigationItemIcon:
                icon: 'book-arrow-up'
                icon_color_active: 1, 0, 0, 1  # Red when active
                icon_color_normal: 0.5, 0.5, 0.5, 1  # Gray when inactive
            MDNavigationItemLabel:
                text: app.messages['register title']
                text_color_active: 1, 1, 0, 1  # Red when active
                text_color_normal: 0.5, 0.5, 0.5, 1  # Gray when inactive


        # this will create a navigation button on the bottom of screen
        MDNavigationItem:
            id: second_nav
            name: 'registered'
            text: app.messages['show registered title']
            icon: 'car'
            MDNavigationItemIcon:
                icon: 'car'
                icon_color_active: 1, 0, 0, 1  # Red when active
                icon_color_normal: 0.5, 0.5, 0.5, 1  # Gray when inactive
            MDNavigationItemLabel:
                text: app.messages['show registered title']
                text_color_active: 1, 1, 0, 1  # Red when active
                text_color_normal: 0.5, 0.5, 0.5, 1  # Gray when inactive
            





        # this will create a navigation button on the bottom of screen
        MDNavigationItem:
            id: third_nav
            name: 'about'
            MDNavigationItemIcon:
                icon: 'check-decagram'
                icon_color_active: 1, 0, 0, 1  # Red when active
                icon_color_normal: 0.5, 0.5, 0.5, 1  # Gray when inactive
            MDNavigationItemLabel:
                text: app.messages['about the app title']
                text_color_active: 1, 1, 0, 1  # Red when active
                text_color_normal: 0.5, 0.5, 0.5, 1  # Gray when inactive

    

'''

