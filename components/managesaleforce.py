import flet as ft
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

class ManageSaleDialog:
    def __init__(self, page: ft.Page):
        self.page = page
        self.serial_number = ""

        self.error_popup = ft.AlertDialog(
            title=ft.Text("Error", color=ft.Colors.BLUE_800),
            content=ft.Text(""),
            actions=[ft.TextButton("OK", on_click=self.close_error_popup)],
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.success_popup = ft.AlertDialog(
            title=ft.Text("Success", color=ft.Colors.BLUE_800),
            content=ft.Text(""),
            actions=[ft.TextButton("OK", on_click=self.close_success_popup)],
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        )

        self.device_serial_number = ft.TextField(
            label="Serial Number",
            hint_text="Device Serial Number",
            border_color=ft.Colors.BLUE_200,
            icon=ft.Icons.DEVICE_HUB,
            disabled=True
        )
        self.device_status = ft.Dropdown(
            label="Device Status",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Deployed"),
                ft.dropdown.Option("Disposed")
            ],
            border_color=ft.Colors.BLUE_200,
            on_change=self.status_changed
        )
        self.distributor_name = ft.TextField(
            label="Distributor Name",
            hint_text="Enter Distributor Name",
            border_color=ft.Colors.BLUE_200,
            icon=ft.Icons.PERSON,
            visible=False
        )
        self.distributor_location = ft.TextField(
            label="Location",
            hint_text="Enter Location",
            border_color=ft.Colors.BLUE_200,
            icon=ft.Icons.LOCATION_ON,
            visible=False
        )
        self.device_tag = ft.TextField(
            label="Device Tag",
            hint_text="Enter Device Tag",
            border_color=ft.Colors.BLUE_200,
            icon=ft.Icons.TAG,
            visible=False
        )
        self.disposed_reason = ft.TextField(
            label="Disposed Reason",
            hint_text="Enter Disposed Reason",
            border_color=ft.Colors.BLUE_200,
            icon=ft.Icons.INFO,
            visible=False
        )

        self.page.overlay.extend([self.error_popup, self.success_popup])

        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.WHITE,
            title=ft.Text("Manage Device", color=ft.Colors.BLUE_800),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.device_serial_number,
                        self.device_status,
                        self.distributor_name,
                        self.distributor_location,
                        self.device_tag,
                        self.disposed_reason
                    ],
                    spacing=15
                ),
                padding=20
            ),
            actions=[
                ft.TextButton("Save", on_click=self.save_data),
                ft.TextButton("Cancel", on_click=self.close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.overlay.append(self.dialog)
        self.page.update()

    def status_changed(self, e):
        self.distributor_name.visible = self.device_status.value == "Deployed"
        self.distributor_location.visible = self.device_status.value == "Deployed"
        self.device_tag.visible = self.device_status.value == "Deployed"
        self.disposed_reason.visible = self.device_status.value == "Disposed"
        self.distributor_name.update()
        self.distributor_location.update()
        self.device_tag.update()
        self.disposed_reason.update()
        self.page.update()

    def save_data(self, e):
        serial_number = self.device_serial_number.value
        status = self.device_status.value
        distributor_name = self.distributor_name.value.strip() if self.distributor_name.visible else None
        distributor_location = self.distributor_location.value.strip() if self.distributor_location.visible else None
        device_tag = self.device_tag.value.strip() if self.device_tag.visible else None
        disposed_reason = self.disposed_reason.value.strip() if self.disposed_reason.visible else None

        if not serial_number or not status:
            self.error_popup.content = ft.Text("Serial number and status are required.")
            self.error_popup.open = True
            self.page.update()
            return

        if status == "Deployed" and not all([distributor_name, distributor_location, device_tag]):
            self.error_popup.content = ft.Text("All fields are required for Deployed status.")
            self.error_popup.open = True
            self.page.update()
            return

        if status == "Disposed" and not disposed_reason:
            self.error_popup.content = ft.Text("Disposal reason is required.")
            self.error_popup.open = True
            self.page.update()
            return

        db_config = {
            "host": "200.200.200.23",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            deployed_on = datetime.now().strftime('%Y-%m-%d') if status == "Deployed" else None
            cursor.execute(
                """
                UPDATE devices 
                SET status = %s, 
                    distributor_name = %s, 
                    distributor_location = %s, 
                    device_tag = %s, 
                    disposed_reason = %s,
                    deployed_on = %s,
                    updated_at = %s
                WHERE serial_number = %s
                """,
                (status, distributor_name, distributor_location, device_tag, disposed_reason, 
                 deployed_on, datetime.now(), serial_number)
            )
            if cursor.rowcount == 0:
                self.error_popup.content = ft.Text(f"No device found with serial number {serial_number}.")
                self.error_popup.open = True
                self.page.update()
                return

            cursor.execute("SELECT id, model FROM devices WHERE serial_number = %s", (serial_number,))
            device = cursor.fetchone()
            cursor.execute(
                """
                INSERT INTO asset_history (table_type, entity_id, data_json, action)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    'devices',
                    device['id'],
                    json.dumps({
                        'model': device['model'],
                        'serial_number': serial_number,
                        'status': status,
                        'distributor_name': distributor_name,
                        'distributor_location': distributor_location,
                        'device_tag': device_tag,
                        'disposed_reason': disposed_reason,
                        'deployed_on': deployed_on
                    }),
                    'Updated'
                )
            )

            conn.commit()
            self.success_popup.content = ft.Text("Device status updated successfully.")
            self.success_popup.open = True
            self.page.update()
        except Error as e:
            self.error_popup.content = ft.Text(f"Error: {e}")
            self.error_popup.open = True
            self.page.update()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        self.close_dialog(e)

    def close_error_popup(self, e):
        self.error_popup.open = False
        self.page.update()

    def close_success_popup(self, e):
        self.success_popup.open = False
        self.page.update()

    def clear_fields(self):
        self.device_status.value = None
        self.distributor_name.value = ""
        self.distributor_location.value = ""
        self.device_tag.value = ""
        self.disposed_reason.value = ""
        self.distributor_name.visible = False
        self.distributor_location.visible = False
        self.device_tag.visible = False
        self.disposed_reason.visible = False
        self.distributor_name.update()
        self.distributor_location.update()
        self.device_tag.update()
        self.disposed_reason.update()
        self.device_status.update()

    def close_dialog(self, e):
        self.clear_fields()
        self.dialog.open = False
        if self.dialog in self.page.overlay:
            self.page.overlay.remove(self.dialog)
        self.page.update()

    def open(self, serial_number=None):
        self.serial_number = serial_number or ""
        self.device_serial_number.value = self.serial_number
        self.clear_fields()
        if self.serial_number:
            db_config = {
                "host": "200.200.200.23",
                "user": "root",
                "password": "Pak@123",
                "database": "asm_sys"
            }
            conn = None
            cursor = None
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    """
                    SELECT status, distributor_name, distributor_location, device_tag, disposed_reason
                    FROM devices WHERE serial_number = %s
                    """,
                    (self.serial_number,)
                )
                device = cursor.fetchone()
                if device:
                    self.device_status.value = device['status']
                    self.distributor_name.value = device['distributor_name'] or ""
                    self.distributor_location.value = device['distributor_location'] or ""
                    self.device_tag.value = device['device_tag'] or ""
                    self.disposed_reason.value = device['disposed_reason'] or ""
                    self.status_changed(None)
            except Error as e:
                self.error_popup.content = ft.Text(f"Error fetching device: {e}")
                self.error_popup.open = True
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        self.dialog.open = True
        self.page.update()