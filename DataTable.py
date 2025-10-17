from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel

from layouts.layouts import Layout

KV = Layout("data_table").module.KV


class DataTableRow(RecycleDataViewBehavior, MDBoxLayout):
    """Row for data table with selection support."""
    index = NumericProperty(0)
    selected = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.selected = data.get('selected', False)
        self.clear_widgets()

        # Add cells based on column data
        for i, col_data in enumerate(data['cells']):
            # Create a container for each cell
            from kivymd.uix.boxlayout import MDBoxLayout
            cell_container = MDBoxLayout(
                size_hint_x=data['col_widths'][i],
                padding=("16dp", 0, 0, 0)
            )

            # Check if cell data is a tuple (icon_name, color)
            if isinstance(col_data, tuple) and len(col_data) == 2:
                # Create icon widget
                from kivymd.uix.label import MDIcon
                icon = MDIcon(
                    icon=col_data[0],
                    theme_icon_color="Custom",
                    icon_color=col_data[1],
                    pos_hint={"center_y": 0.5}
                )
                cell_container.add_widget(icon)
            else:
                # Create regular text label
                lbl = MDLabel(
                    text=str(col_data),
                )
                cell_container.add_widget(lbl)

            self.add_widget(cell_container)

        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return self.parent.parent.parent.select_row(self.index)
        return super().on_touch_down(touch)


class DataTableHeader(MDBoxLayout):
    """Header row for data table."""
    pass


class DataTable(MDBoxLayout):
    """Custom data table with RecycleView, header, and pagination."""

    columns = ListProperty([])
    row_data = ListProperty([])
    rows_per_page = NumericProperty(10)
    current_page = NumericProperty(1)
    page_info_text = StringProperty("")
    total_pages = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_rows = []

    def set_data(self, columns, rows):
        """Set table data with columns and rows.

        Args:
            columns: List of tuples [(column_name, width_ratio), ...]
            rows: List of lists [[cell1, cell2, ...], ...]
        """
        self.columns = columns
        self.row_data = rows
        self.current_page = 1
        self._update_header()
        self._update_table()

    def _update_header(self):
        """Update header with column names."""
        header = self.ids.header
        header.clear_widgets()

        col_widths = [col[1] if len(col) > 1 else 1 for col in self.columns]
        total = sum(col_widths)
        col_widths = [w / total for w in col_widths]

        for i, col in enumerate(self.columns):
            col_name = col[0] if isinstance(col, (list, tuple)) else col

            # Create a container for header cell to match row cell structure
            from kivymd.uix.boxlayout import MDBoxLayout
            header_cell = MDBoxLayout(
                size_hint_x=col_widths[i],
                padding=("16dp", 0, 0, 0)
            )

            lbl = MDLabel(
                text=str(col_name),
                bold=True,
            )
            header_cell.add_widget(lbl)
            header.add_widget(header_cell)

    def _update_table(self):
        """Update table data based on current page."""
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = start_idx + self.rows_per_page
        page_data = self.row_data[start_idx:end_idx]

        # Calculate column widths
        col_widths = [col[1] if len(col) > 1 else 1 for col in self.columns]
        total = sum(col_widths)
        col_widths = [w / total for w in col_widths]

        # Prepare data for RecycleView
        rv_data = []
        for i, row in enumerate(page_data):
            rv_data.append({
                'cells': row,
                'col_widths': col_widths,
                'selected': (start_idx + i) in self.selected_rows
            })

        self.ids.rv.data = rv_data

        # Update RecycleView height based on actual rows displayed
        actual_rows = len(page_data)
        self.ids.rv.height = actual_rows * 48  # 48dp per row

        # Update pagination info
        self.total_pages = max(1, (len(self.row_data) + self.rows_per_page - 1) // self.rows_per_page)
        total_rows = len(self.row_data)
        start = start_idx + 1 if total_rows > 0 else 0
        end = min(end_idx, total_rows)
        self.page_info_text = f"Showing {start}-{end} of {total_rows} rows"

    def next_page(self):
        """Navigate to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._update_table()

    def previous_page(self):
        """Navigate to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_table()

    def select_row(self, index):
        """Handle row selection."""
        actual_index = (self.current_page - 1) * self.rows_per_page + index
        if actual_index in self.selected_rows:
            self.selected_rows.remove(actual_index)
        else:
            self.selected_rows.append(actual_index)
        self._update_table()
        return True


class DataTableApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        # Sample data with icons
        columns = [
            ("Icon", 0.8),
            ("Name", 2),
            ("Email", 2.5),
            ("Status", 1)
        ]

        # Rows can now include tuples for icons: (icon_name, color)
        rows = [
            [
                ("account", [0.2, 0.6, 1, 1]),  # Icon with blue color
                f"User {i}",
                f"user{i}@example.com",
                "Active" if i % 2 == 0 else "Inactive"
            ]
            for i in range(1, 51)
        ]

        self.root.ids.data_table.set_data(columns, rows)
        self.root.ids.data_table.rows_per_page = 10  # Default

    def set_rows_per_page(self, count):
        """Change the number of rows displayed per page."""
        self.root.ids.data_table.rows_per_page = count
        self.root.ids.data_table.current_page = 1  # Reset to first page
        self.root.ids.data_table._update_table()



def get_table():
    return Builder.load_string(KV)

if __name__ == "__main__":
    DataTableApp().run()