KV = '''
<DataTableRow>:
    size_hint_y: None
    height: "48dp"
    canvas.before:
        Color:
            rgba: app.theme_cls.surfaceContainerColor if not self.selected else app.theme_cls.primaryContainerColor
        Rectangle:
            pos: self.pos
            size: self.size

<DataTableHeader>:
    size_hint_y: None
    height: "56dp"
    canvas.before:
        Color:
            rgba: app.theme_cls.surfaceContainerHighColor
        Rectangle:
            pos: self.pos
            size: self.size

<DataTable>:
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height

    # Header
    DataTableHeader:
        id: header

    # Data rows
    RecycleView:
        id: rv
        size_hint_y: None
        height: root.rows_per_page * 48  # 48dp per row
        viewclass: "DataTableRow"
        RecycleBoxLayout:
            default_size: None, "48dp"
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: "vertical"

    # Footer with pagination
    MDBoxLayout:
        size_hint_y: None
        height: "56dp"
        padding: "16dp"
        spacing: "8dp"
        canvas.before:
            Color:
                rgba: app.theme_cls.surfaceContainerHighColor
            Rectangle:
                pos: self.pos
                size: self.size

        MDLabel:
            id: page_info
            text: root.page_info_text
            size_hint_x: 0.7
            adaptive_height: True

        MDBoxLayout:
            size_hint_x: 0.3
            spacing: "4dp"

            MDIconButton:
                icon: "chevron-left"
                on_release: root.previous_page()
                disabled: root.current_page == 1

            MDLabel:
                text: f"{root.current_page}/{root.total_pages}"
                halign: "center"
                size_hint_x: None
                width: "60dp"

            MDIconButton:
                icon: "chevron-right"
                on_release: root.next_page()
                disabled: root.current_page >= root.total_pages

MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDBoxLayout:
        orientation: "vertical"
        padding: "16dp"
        spacing: "16dp"
        pos_hint: {"center_x": 0.5, "center_y": .43}

        # MDLabel:
        #     text: "Data Table with Adaptive Height"
        #     font_style: "Display"
        #     role: "small"
        #     halign: "center"
        #     size_hint_y: None
        #     adaptive_height: True

        # Rows per page selector
        MDBoxLayout:
            size_hint_y: None
            height: "48dp"
            spacing: "8dp"

            MDLabel:
                text: app.messages['rows per page']
                size_hint_x: None
                width: "165dp"
                halign: "left"
                valign: "middle"
                adaptive_height: True

            MDButton:
                style: "outlined"
                on_release: app.set_rows_per_page(5)

                MDButtonText:
                    text: "5"

            MDButton:
                style: "outlined"
                on_release: app.set_rows_per_page(10)

                MDButtonText:
                    text: "10"

            MDButton:
                style: "outlined"
                on_release: app.set_rows_per_page(20)

                MDButtonText:
                    text: "20"

            Widget:  # Spacer

        # Spacer to center the table vertically
        Widget:

        # Data table (centered)
        DataTable:
            id: data_table
            pos_hint: {"center_x": 0.5}

        # Spacer below table
        Widget:
'''