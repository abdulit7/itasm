import flet as ft
import mysql.connector
from mysql.connector import Error

class PrintersPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "Printers Management"
        self.page.window_title = "Printers Management"
        self.expand = True
        self.padding = ft.padding.all(20)
        self.printers_list = []
        self.cartridges_list = []

        # Initialize snackbar and dialog
        self.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(""),
            content=ft.Container(width=400, height=400, content=ft.Column(controls=[], spacing=20)),
            actions=[],
            bgcolor=ft.Colors.WHITE,
            content_padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=10)
        )

        # Add to overlay once
        self.page.overlay.extend([self.snack_bar, self.dialog])

        # Initialize UI
        self.add_printer_button = ft.ElevatedButton(
            "Add Printer",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.BLUE_200,
            color=ft.Colors.WHITE,
            on_click=self.show_add_printer_form
        )
        self.add_cartridge_button = ft.ElevatedButton(
            "Add Cartridge",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.GREEN_200,
            color=ft.Colors.WHITE,
            on_click=self.show_add_cartridge_form
        )

        # Initial load and build
        self.refresh_page()

    def refresh_page(self):
        """Reloads data and rebuilds the entire page content."""
        self.load_printers()
        self.load_cartridges()
        self.printer_table = self._build_printer_table()
        self.cartridge_table = self._build_cartridge_table()
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.add_printer_button,
                        self.add_cartridge_button
                    ],
                    spacing=10
                ),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Printers", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                                ft.Container(
                                    content=self.printer_table,
                                    padding=10,
                                    border=ft.border.all(1, ft.Colors.GREY_300),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=10,
                                    shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_400)
                                )
                            ],
                            expand=True
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Cartridges", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                                ft.Container(
                                    content=self.cartridge_table,
                                    padding=10,
                                    border=ft.border.all(1, ft.Colors.GREY_300),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=10,
                                    shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_400)
                                )
                            ],
                            expand=True
                        )
                    ],
                    expand=True,
                    spacing=20
                )
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
        self.page.update()

    def _build_printer_table(self):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Model", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)),
                ft.DataColumn(ft.Text("Company", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)),
                ft.DataColumn(ft.Text("Cartridge No", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)),
                ft.DataColumn(ft.Text("Location", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)),
                ft.DataColumn(ft.Text("Department", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)),
                ft.DataColumn(ft.Text("Edit", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)),
                ft.DataColumn(ft.Text("Delete", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p["model"], bgcolor=ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100)),
                        ft.DataCell(ft.Text(p["company"], bgcolor=ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100)),
                        ft.DataCell(ft.Text(p["cartridge_no"] or "N/A", bgcolor=ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100)),
                        ft.DataCell(ft.Text(p["location"], bgcolor=ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100)),
                        ft.DataCell(ft.Text(p["department_name"] or "N/A", bgcolor=ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100)),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, id=p["id"]: self.show_edit_printer_form(id))),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=p["id"]: self.delete_printer(id))),
                    ]
                ) for i, p in enumerate(self.printers_list)
            ],
            border=ft.border.all(1, ft.Colors.BLUE_200),
            heading_row_color=ft.Colors.BLUE_50,
            divider_thickness=1,
            column_spacing=20
        )

    def _build_cartridge_table(self):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Cartridge No", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800)),
                ft.DataColumn(ft.Text("Printer Model", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800)),
                ft.DataColumn(ft.Text("Company", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800)),
                ft.DataColumn(ft.Text("Edit", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800)),
                ft.DataColumn(ft.Text("Delete", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(c["cartridge_no"], bgcolor=ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100)),
                        ft.DataCell(ft.Text(c["printer_model"], bgcolor=ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100)),
                        ft.DataCell(ft.Text(c["company"], bgcolor=ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100)),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, id=c["id"]: self.show_edit_cartridge_form(id))),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=c["id"]: self.delete_cartridge(id))),
                    ]
                ) for i, c in enumerate(self.cartridges_list)
            ],
            border=ft.border.all(1, ft.Colors.GREEN_200),
            heading_row_color=ft.Colors.GREEN_50,
            divider_thickness=1,
            column_spacing=20
        )

    def load_printers(self):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.id, p.model, p.company, p.cartridge_no, p.location, p.department_id,
                       d.name AS department_name
                FROM printers p
                LEFT JOIN department d ON p.department_id = d.id
                ORDER BY p.id
            """)
            self.printers_list = cursor.fetchall()
        except Error as e:
            self.show_snack_bar(f"Error loading printers: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def load_cartridges(self):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, cartridge_no, printer_model, company FROM cartridges ORDER BY id")
            self.cartridges_list = cursor.fetchall()
        except Error as e:
            self.show_snack_bar(f"Error loading cartridges: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_add_printer_form(self, e):
        departments = self._get_departments()
        self.dialog.title = ft.Text("Add Printer", color=ft.Colors.BLUE_800)
        self.dialog.content.content.controls = [
            ft.TextField(label="Model", autofocus=True, border_color=ft.Colors.BLUE_200),
            ft.TextField(label="Company", value="HP", border_color=ft.Colors.BLUE_200),
            ft.TextField(label="Cartridge No", border_color=ft.Colors.BLUE_200),
            ft.TextField(label="Location", value="Office", border_color=ft.Colors.BLUE_200),
            ft.Dropdown(
                label="Department",
                border=ft.InputBorder.UNDERLINE,
                enable_filter=True,
                editable=True,
                menu_height=200,
                leading_icon=ft.Icons.SEARCH,
                options=[ft.dropdown.Option(key=str(d["id"]), text=d["name"]) for d in departments],
                border_color=ft.Colors.BLUE_200
            ),
        ]
        self.dialog.actions = [
            ft.ElevatedButton("Add", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=self.submit_printer),
            ft.TextButton("Cancel", on_click=self.close_dialog)
        ]
        self.dialog.open = True
        self.page.update()

    def submit_printer(self, e):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            model = self.dialog.content.content.controls[0].value
            company = self.dialog.content.content.controls[1].value
            cartridge_no = self.dialog.content.content.controls[2].value.strip() or None
            location = self.dialog.content.content.controls[3].value
            department_id = self.dialog.content.content.controls[4].value
            if not all([model, company, location, department_id]):
                raise ValueError("Required fields missing.")

            if cartridge_no:
                cursor.execute("SELECT cartridge_no FROM cartridges WHERE cartridge_no = %s", (cartridge_no,))
                if not cursor.fetchone():
                    self.show_snack_bar(f"Warning: Cartridge No '{cartridge_no}' not found in cartridges.", ft.Colors.ORANGE_800)
                cursor.execute("SELECT id FROM printers WHERE cartridge_no = %s AND id != %s", (cartridge_no, 0))
                if cursor.fetchone():
                    self.show_snack_bar(f"Warning: Cartridge No '{cartridge_no}' is already assigned to another printer.", ft.Colors.ORANGE_800)

            cursor.execute(
                "INSERT INTO printers (model, company, cartridge_no, location, department_id) "
                "VALUES (%s, %s, %s, %s, %s)",
                (model, company, cartridge_no, location, department_id)
            )
            conn.commit()
            self.show_snack_bar("Printer added successfully!", ft.Colors.GREEN_800)
            self.clear_dialog_fields()
            self.close_dialog(None)
            self.refresh_page()
        except (Error, ValueError) as err:
            self.show_snack_bar(f"Error: {err}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_edit_printer_form(self, printer_id):
        departments = self._get_departments()
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM printers WHERE id = %s", (printer_id,))
            printer = cursor.fetchone()
            if not printer:
                raise ValueError("Printer not found.")

            self.dialog.title = ft.Text("Edit Printer", color=ft.Colors.BLUE_800)
            self.dialog.content.content.controls = [
                ft.TextField(label="Model", value=printer["model"], border_color=ft.Colors.BLUE_200),
                ft.TextField(label="Company", value=printer["company"], border_color=ft.Colors.BLUE_200),
                ft.TextField(label="Cartridge No", value=printer["cartridge_no"] or "", border_color=ft.Colors.BLUE_200),
                ft.TextField(label="Location", value=printer["location"], border_color=ft.Colors.BLUE_200),
                ft.Dropdown(
                    label="Department",
                    border=ft.InputBorder.UNDERLINE,
                    enable_filter=True,
                    editable=True,
                    leading_icon=ft.Icons.SEARCH,
                    options=[ft.dropdown.Option(key=str(d["id"]), text=d["name"]) for d in departments],
                    value=str(printer["department_id"]) if printer["department_id"] else None,
                    border_color=ft.Colors.BLUE_200
                ),
            ]
            self.dialog.actions = [
                ft.ElevatedButton("Save", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=lambda e: self.update_printer(e, printer_id)),
                ft.TextButton("Cancel", on_click=self.close_dialog)
            ]
            self.dialog.open = True
            self.page.update()
        except (Error, ValueError) as e:
            self.show_snack_bar(f"Error: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_printer(self, e, printer_id):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            model = self.dialog.content.content.controls[0].value
            company = self.dialog.content.content.controls[1].value
            cartridge_no = self.dialog.content.content.controls[2].value.strip() or None
            location = self.dialog.content.content.controls[3].value
            department_id = self.dialog.content.content.controls[4].value
            if not all([model, company, location, department_id]):
                raise ValueError("Required fields missing.")

            if cartridge_no:
                cursor.execute("SELECT cartridge_no FROM cartridges WHERE cartridge_no = %s", (cartridge_no,))
                if not cursor.fetchone():
                    self.show_snack_bar(f"Warning: Cartridge No '{cartridge_no}' not found in cartridges.", ft.Colors.ORANGE_800)
                cursor.execute("SELECT id FROM printers WHERE cartridge_no = %s AND id != %s", (cartridge_no, printer_id))
                if cursor.fetchone():
                    self.show_snack_bar(f"Warning: Cartridge No '{cartridge_no}' is already assigned to another printer.", ft.Colors.ORANGE_800)

            cursor.execute(
                "UPDATE printers SET model = %s, company = %s, cartridge_no = %s, location = %s, department_id = %s "
                "WHERE id = %s",
                (model, company, cartridge_no, location, department_id, printer_id)
            )
            conn.commit()
            self.show_snack_bar("Printer updated successfully!", ft.Colors.GREEN_800)
            self.clear_dialog_fields()
            self.close_dialog(None)
            self.refresh_page()
        except (Error, ValueError) as err:
            self.show_snack_bar(f"Error: {err}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_printer(self, printer_id):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM printers WHERE id = %s", (printer_id,))
            conn.commit()
            self.show_snack_bar("Printer deleted successfully!", ft.Colors.GREEN_800)
            self.refresh_page()
        except Error as err:
            self.show_snack_bar(f"Error: {err}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_add_cartridge_form(self, e):
        self.dialog.title = ft.Text("Add Cartridge", color=ft.Colors.GREEN_800)
        self.dialog.content.content.controls = [
            ft.TextField(label="Cartridge No", autofocus=True, border_color=ft.Colors.GREEN_200),
            ft.TextField(label="Printer Model", border_color=ft.Colors.GREEN_200),
            ft.TextField(label="Company", value="HP", border_color=ft.Colors.GREEN_200),
        ]
        self.dialog.content.height = 250
        self.dialog.actions = [
            ft.ElevatedButton("Add", bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE, on_click=self.submit_cartridge),
            ft.TextButton("Cancel", on_click=self.close_dialog)
        ]
        self.dialog.open = True
        self.page.update()

    def submit_cartridge(self, e):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cartridge_no = self.dialog.content.content.controls[0].value
            printer_model = self.dialog.content.content.controls[1].value
            company = self.dialog.content.content.controls[2].value
            if not all([cartridge_no, printer_model, company]):
                raise ValueError("All fields required.")

            cursor.execute(
                "INSERT INTO cartridges (cartridge_no, printer_model, company) VALUES (%s, %s, %s)",
                (cartridge_no, printer_model, company)
            )
            conn.commit()
            self.show_snack_bar("Cartridge added successfully!", ft.Colors.GREEN_800)
            self.clear_dialog_fields()
            self.close_dialog(None)
            self.refresh_page()
        except (Error, ValueError) as err:
            self.show_snack_bar(f"Error: {err}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_edit_cartridge_form(self, cartridge_id):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cartridges WHERE id = %s", (cartridge_id,))
            cartridge = cursor.fetchone()
            if not cartridge:
                raise ValueError("Cartridge not found.")

            self.dialog.title = ft.Text("Edit Cartridge", color=ft.Colors.GREEN_800)
            self.dialog.content.content.controls = [
                ft.TextField(label="Cartridge No", value=cartridge["cartridge_no"], border_color=ft.Colors.GREEN_200),
                ft.TextField(label="Printer Model", value=cartridge["printer_model"], border_color=ft.Colors.GREEN_200),
                ft.TextField(label="Company", value=cartridge["company"], border_color=ft.Colors.GREEN_200),
            ]
            self.dialog.content.height = 250
            self.dialog.actions = [
                ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE, on_click=lambda e: self.update_cartridge(e, cartridge_id)),
                ft.TextButton("Cancel", on_click=self.close_dialog)
            ]
            self.dialog.open = True
            self.page.update()
        except (Error, ValueError) as e:
            self.show_snack_bar(f"Error: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_cartridge(self, e, cartridge_id):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cartridge_no = self.dialog.content.content.controls[0].value.strip()
            printer_model = self.dialog.content.content.controls[1].value
            company = self.dialog.content.content.controls[2].value
            if not all([cartridge_no, printer_model, company]):
                raise ValueError("All fields required.")

            cursor.execute(
                "UPDATE cartridges SET cartridge_no = %s, printer_model = %s, company = %s WHERE id = %s",
                (cartridge_no, printer_model, company, cartridge_id)
            )
            conn.commit()
            self.show_snack_bar("Cartridge updated successfully!", ft.Colors.GREEN_800)
            self.clear_dialog_fields()
            self.close_dialog(None)
            self.refresh_page()
        except (Error, ValueError) as err:
            self.show_snack_bar(f"Error: {err}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_cartridge(self, cartridge_id):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cartridges WHERE id = %s", (cartridge_id,))
            conn.commit()
            self.show_snack_bar("Cartridge deleted successfully!", ft.Colors.GREEN_800)
            self.refresh_page()
        except Error as err:
            self.show_snack_bar(f"Error: {err}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _get_departments(self):
        db_config = {"host": "200.200.201.100", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        departments = []
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name FROM department ORDER BY name")
            departments = cursor.fetchall()
        except Error as e:
            self.show_snack_bar(f"Error loading departments: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return departments

    def close_dialog(self, e):
        if self.dialog.open:
            self.dialog.open = False
            self.clear_dialog_fields()
            self.page.update()

    def clear_dialog_fields(self):
        if self.dialog.content and self.dialog.content.content.controls:
            for control in self.dialog.content.content.controls:
                if isinstance(control, ft.TextField):
                    control.value = "" if control.label not in ["Company", "Location"] else ("HP" if control.label == "Company" else "Office")
                elif isinstance(control, ft.Dropdown):
                    control.value = None
            self.page.update()

    def show_snack_bar(self, message, color=ft.Colors.BLACK):
        self.snack_bar.content.value = message
        self.snack_bar.bgcolor = color
        self.snack_bar.open = True
        self.page.update()