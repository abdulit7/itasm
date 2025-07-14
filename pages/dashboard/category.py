
import flet as ft
import mysql.connector
from components.categoryform import CatDialog

class Category(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        if page is None:
            raise ValueError("Page reference cannot be None")
        self.page = page
        self.expand = True
        self.page.window.title = "Asset Management System - Categories"
        self.page.bgcolor = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.Colors.TEAL_50, ft.Colors.WHITE]
        )

        self.cat_dialog = CatDialog(page)

        # Add Category Button
        self.add_category_button = ft.ElevatedButton(
            icon=ft.Icons.ADD,
            text="Add a Category",
            bgcolor=ft.Colors.TEAL_600,
            width=180,
            height=55,
            color=ft.Colors.WHITE,
            elevation=4,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                overlay_color=ft.Colors.TEAL_700  # Removed hover_color
            ),
            on_click=lambda e: self.cat_dialog.open()
        )

        # Loading indicator
        self.loading_indicator = ft.ProgressRing(
            visible=False,
            color=ft.Colors.INDIGO_500,
            stroke_width=4
        )

        # Category Table
        self.category_table = ft.DataTable(
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(2, ft.Colors.INDIGO_100),
            border_radius=15,
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            heading_row_color=ft.Colors.INDIGO_50,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_800,
                weight=ft.FontWeight.BOLD,
                size=18,
                font_family="Roboto"
            ),
            data_row_color={ft.ControlState.HOVERED: ft.Colors.LIGHT_BLUE_100},
            data_row_min_height=60,
            data_text_style=ft.TextStyle(
                color=ft.Colors.GREY_900,
                size=16,
                font_family="Roboto"
            ),
            show_checkbox_column=False,
            column_spacing=40,
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.W_700)),
                ft.DataColumn(ft.Text("Type", weight=ft.FontWeight.W_700)),
                ft.DataColumn(ft.Text("Total Items", weight=ft.FontWeight.W_700)),
                ft.DataColumn(ft.Text("Description", weight=ft.FontWeight.W_700)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_700)),
            ],
            rows=[],
        )

        # Page Layout
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                self.add_category_button,
                                                self.loading_indicator,
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                        padding=ft.padding.only(top=20, left=20, right=20),
                                    ),
                                    ft.Container(
                                        content=self.category_table,
                                        padding=ft.padding.all(20),
                                        margin=ft.margin.only(top=10),
                                        border_radius=15,
                                        shadow=ft.BoxShadow(
                                            spread_radius=2,
                                            blur_radius=10,
                                            color=ft.Colors.GREY_300,
                                            offset=ft.Offset(0, 4)
                                        )
                                    ),
                                ],
                                expand=True,
                                alignment=ft.MainAxisAlignment.START,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                        expand=True,
                    ),
                    padding=ft.padding.all(10),
                ),
            ],
            spacing=10,
            expand=True,
        )

        # Load data after UI initialization
        self.load_categories()

    def _get_db_connection(self):
        """Establish and return a database connection."""
        try:
            connection = mysql.connector.connect(
                host="200.200.201.100",
                user="root",
                password="Pak@123",
                database="asm_sys",
                auth_plugin='mysql_native_password'
            )
            #print("Database connection successful")
            return connection
        except mysql.connector.Error as error:
            print(f"Database connection failed: {error}")
            if self.page is not None:
                self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))
            return None

    def load_categories(self):
        """Fetches and displays category data, including total items."""
        if self.page is None:
            print("Error: self.page is None in load_categories")
            return
        self.loading_indicator.visible = True
        self.page.update()

        connection = self._get_db_connection()
        if not connection:
            self.loading_indicator.visible = False
            self.page.update()
            return

        try:
            cur = connection.cursor()
            cur.execute("""
                SELECT id, name, type, description
                FROM category
            """)
            categories = cur.fetchall()
            self.category_table.rows.clear()

            for cat in categories:
                cat_id, name, cat_type, description = cat
                total_items = self._get_total_items(cat_id, connection)
                self.category_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(name or "N/A", font_family="Roboto")),
                            ft.DataCell(ft.Text(cat_type or "N/A", font_family="Roboto")),
                            ft.DataCell(ft.Text(str(total_items), font_family="Roboto")),
                            ft.DataCell(ft.Text(description or "N/A", font_family="Roboto")),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Edit",
                                            bgcolor=ft.Colors.LIGHT_GREEN_600,
                                            color=ft.Colors.WHITE,
                                            elevation=3,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                                overlay_color=ft.Colors.LIGHT_GREEN_700
                                            ),
                                            on_click=lambda e, cat_id=cat_id: self.edit_category(cat_id)
                                        ),
                                        ft.ElevatedButton(
                                            "Delete",
                                            bgcolor=ft.Colors.RED_600,
                                            color=ft.Colors.WHITE,
                                            elevation=3,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                                overlay_color=ft.Colors.RED_700
                                            ),
                                            on_click=lambda e, cat_id=cat_id: self.delete_category(cat_id)
                                        ),
                                    ],
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                )
                            ),
                        ]
                    )
                )
        except mysql.connector.Error as error:
            print(f"Error fetching categories: {error}")
            if self.page is not None:
                self.page.open(ft.SnackBar(ft.Text(f"Error fetching categories: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")
            self.loading_indicator.visible = False
            if self.page is not None:
                self.page.update()

    def _get_total_items(self, category_id: int, connection) -> int:
        """Calculate the total number of components in a category using COUNT(*)."""
        try:
            cur = connection.cursor()
            cur.execute("SELECT COUNT(*) FROM components WHERE category_id = %s", (category_id,))
            component_count = cur.fetchone()[0]
            print(f"Category {category_id} has {component_count} components")
            return component_count
        except mysql.connector.Error as error:
            print(f"Error calculating total items: {error}")
            return 0

    def edit_category(self, cat_id: int):
        """Handles editing a category by opening the dialog with existing data."""
        if self.page is None:
            print("Error: self.page is None in edit_category")
            return
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("SELECT name, description, type FROM category WHERE id = %s", (cat_id,))
            category = cur.fetchone()
            if category:
                name, description, cat_type = category
                self.cat_dialog.open(name=name, desc=description, cat_type=cat_type, cat_id=cat_id)
            else:
                self.page.open(ft.SnackBar(ft.Text(f"Category ID {cat_id} not found."), duration=4000))
        except mysql.connector.Error as error:
            print(f"Error fetching category: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching category: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def delete_category(self, cat_id: int):
        """Handles deleting a category from the database."""
        if self.page is None:
            print("Error: self.page is None in delete_category")
            return
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("DELETE FROM category WHERE id = %s", (cat_id,))
            connection.commit()
            print(f"Deleted category ID: {cat_id}")
            self.page.open(ft.SnackBar(ft.Text("Category deleted successfully."), duration=3000))
            self.load_categories()  # Refresh table
        except mysql.connector.Error as error:
            print(f"Error deleting category: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error deleting category: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

def CategoryPage(page: ft.Page) -> Category:
    """Factory function to create a Category instance."""
    return Category(page)