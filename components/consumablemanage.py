import flet as ft
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class ConsumableManage(ft.Container):
    def __init__(self, page: ft.Page, parent=None):
        super().__init__()
        self.page = page
        self.parent = parent
        self.consumable_id = None

        self.error_popup = ft.AlertDialog(
            title=ft.Text("Error", color=ft.Colors.RED_800),
            content=ft.Text(""),
            actions=[ft.TextButton("OK", on_click=self.close_error_popup)]
        )
        self.success_popup = ft.AlertDialog(
            title=ft.Text("Success", color=ft.Colors.GREEN_800),
            content=ft.Text(""),
            actions=[ft.TextButton("OK", on_click=self.close_success_popup)]
        )

        self.cartridge_no = ft.TextField(
            label="Cartridge Number",
            disabled=True,
            border_color=ft.Colors.BLUE_200
        )
        self.consumable_status = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Deployed"),
                ft.dropdown.Option("Consumed")
            ],
            border_color=ft.Colors.BLUE_200,
            on_change=self.status_changed
        )
        self.select_printer = ft.Dropdown(
            label="Select Printer",
            options=[],
            border_color=ft.Colors.BLUE_200,
            visible=False
        )
        self.consumed_by = ft.TextField(
            label="Consumed By",
            border_color=ft.Colors.BLUE_200,
            visible=False
        )

        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.BLUE_100,
            title=ft.Text("Manage Consumable", color=ft.Colors.BLUE_800),
            content=ft.Container(
                width=400,
                height=600,
                content=ft.Column(
                    controls=[
                        self.cartridge_no,
                        self.consumable_status,
                        self.select_printer,
                        self.consumed_by
                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.ElevatedButton("Save", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=self.save_data)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.overlay.extend([self.error_popup, self.success_popup])

    def load_printers(self):
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        try:
            with mysql.connector.connect(**db_config) as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("""
                        SELECT p.id, p.model, d.name AS department_name
                        FROM printers p
                        LEFT JOIN department d ON p.department_id = d.id
                        ORDER BY d.name, p.model
                    """)
                    printers = cursor.fetchall()
                    self.select_printer.options = [
                        ft.dropdown.Option(
                            key=str(p["id"]),
                            text=f"{p["model"]} ({p["department_name"] or 'N/A'})"
                        ) for p in printers
                    ]
                    if self.dialog.open:
                        self.page.update()
        except Error as e:
            self.error_popup.content = ft.Text(f"Error loading printers: {e}")
            self.error_popup.open = True
            self.page.update()

    def open_dialog(self, consumable_id: int):
        self.consumable_id = consumable_id
        self.load_printers()

        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        try:
            with mysql.connector.connect(**db_config) as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("""
                        SELECT cs.status, cs.deployed_to, cs.consumed_by, cr.cartridge_no
                        FROM consumables cs
                        LEFT JOIN cartridges cr ON cs.cartridge_id = cr.id
                        WHERE cs.id = %s
                    """, (consumable_id,))
                    consumable = cursor.fetchone()
                    if not consumable:
                        self.error_popup.content = ft.Text(f"Consumable with ID {consumable_id} not found.")
                        self.error_popup.open = True
                        self.page.update()
                        return

                    self.cartridge_no.value = consumable["cartridge_no"]
                    self.consumable_status.value = consumable["status"]
                    self.select_printer.value = str(consumable["deployed_to"]) if consumable["deployed_to"] else None
                    self.consumed_by.value = consumable["consumed_by"] or ""
                    self.status_changed(None)
                    self.dialog.open = True
                    self.page.overlay.append(self.dialog)
                    self.page.update()
        except Error as e:
            self.error_popup.content = ft.Text(f"Error loading consumable: {e}")
            self.error_popup.open = True
            self.page.update()

    def status_changed(self, e):
        status = self.consumable_status.value
        self.select_printer.visible = status == "Deployed"
        self.consumed_by.visible = status == "Consumed"
        self.page.update()

    def save_data(self, e):
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        try:
            with mysql.connector.connect(**db_config) as conn:
                with conn.cursor() as cursor:
                    status = self.consumable_status.value
                    printer_id = self.select_printer.value if self.select_printer.visible and self.select_printer.value else None
                    consumed_by = self.consumed_by.value if self.consumed_by.visible else None
                    deployed_on = datetime.now().strftime("%Y-%m-%d") if status == "Deployed" else None
                    consumption_date = datetime.now().strftime("%Y-%m-%d") if status == "Consumed" else None

                    if status == "Deployed" and not printer_id:
                        raise ValueError("Please select a printer for deployment.")
                    if status == "Consumed" and not consumed_by:
                        raise ValueError("Please provide a user who consumed the cartridge.")

                    cursor.execute("SELECT cartridge_no FROM cartridges WHERE id = (SELECT cartridge_id FROM consumables WHERE id = %s)", (self.consumable_id,))
                    cartridge_no = cursor.fetchone()[0] if cursor.rowcount > 0 else None

                    cursor.execute(
                        """
                        UPDATE consumables
                        SET status = %s, deployed_to = %s, deployed_on = %s, consumed_by = %s, 
                            consumption_date = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (status, printer_id, deployed_on, consumed_by, consumption_date, self.consumable_id)
                    )
                    if cursor.rowcount == 0:
                        raise ValueError(f"Consumable with ID {self.consumable_id} not found.")

                    if status == "Deployed" and printer_id and cartridge_no:
                        cursor.execute("UPDATE printers SET cartridge_no = %s WHERE id = %s", (cartridge_no, printer_id))
                    elif status in ["Available", "Consumed"]:
                        cursor.execute("UPDATE printers SET cartridge_no = NULL WHERE id = (SELECT deployed_to FROM consumables WHERE id = %s)", (self.consumable_id,))

                    cursor.execute(
                        """
                        INSERT INTO asset_history (table_type, entity_id, data_json, action)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            'consumables',
                            self.consumable_id,
                            f'{{"cartridge_no":"{cartridge_no or ''}", "status":"{status}", "printer_id":"{printer_id or ''}"}}',
                            'Updated'
                        )
                    )

                    conn.commit()
                    self.success_popup.content = ft.Text("Consumable updated successfully!")
                    self.success_popup.open = True
                    self.page.update()
        except (Error, ValueError) as e:
            self.error_popup.content = ft.Text(f"Error saving consumable: {e}")
            self.error_popup.open = True
            self.page.update()

    def close_dialog(self, e):
        self.dialog.open = False
        self.page.overlay.remove(self.dialog)
        self.consumable_status.value = None
        self.select_printer.value = None
        self.consumed_by.value = ""
        self.page.update()

    def close_error_popup(self, e):
        self.error_popup.open = False
        self.page.update()

    def close_success_popup(self, e):
        self.success_popup.open = False
        self.close_dialog(None)
        if self.parent and hasattr(self.parent, 'refresh_after_save'):
            self.parent.refresh_after_save()
        self.page.update()