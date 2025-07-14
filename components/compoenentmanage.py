import flet as ft
import mysql.connector
import datetime
from typing import Optional
from components.fields import CustomTextField

class ComponentManage:
    def __init__(self, page: ft.Page, parent=None):
        self.page = page
        self.parent = parent
        self.serial_number = ""

        # Popups
        self.error_popup = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(""),
            actions=[ft.TextButton("OK", on_click=self.close_error_popup)]
        )
        self.success_popup = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text(""),
            actions=[ft.TextButton("OK", on_click=self.close_success_popup)]
        )

        # Fields
        self.component_serial_number = CustomTextField(
            label="Serial Number",
            hint_text="Component Serial Number",
            icon=ft.Icons.DEVICE_HUB,
            disabled=True
        )
        self.component_status = ft.Dropdown(
            label="Component Status",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Deployed"),
                ft.dropdown.Option("Disposed")
            ],
            on_change=self.status_changed,
            expand=True
        )
        self.select_deployed_type = ft.Dropdown(
            label="Deployed Type",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[
                ft.dropdown.Option("User"),
                ft.dropdown.Option("Department"),
                ft.dropdown.Option("Asset")
            ],
            on_change=self.deployed_type_changed,
            visible=False
        )
        self.select_user = ft.Dropdown(
            label="Select User",
            options=[],
            visible=False
        )
        self.select_department = ft.Dropdown(
            label="Select Department",
            options=[],
            visible=False
        )
        self.select_asset = ft.Dropdown(
            label="Select Asset",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[],
            visible=False
        )
        self.disposed_reason = CustomTextField(
            label="Disposed Reason",
            hint_text="Enter Disposed Reason",
            icon=ft.Icons.INFO,
            visible=False
        )

        # Dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.PURPLE_ACCENT_100,
            title=ft.Text("Manage Component"),
            content=ft.Container(
                width=400,
                height=600,
                content=ft.Column(
                    controls=[
                        self.component_serial_number,
                        self.component_status,
                        self.select_deployed_type,
                        self.select_user,
                        self.select_department,
                        self.select_asset,
                        self.disposed_reason
                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO,

                )
            ),
            content_padding=ft.padding.all(20),
            actions=[
                ft.TextButton("Save", on_click=self.save_data),
                ft.TextButton("Cancel", on_click=self.close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.overlay.extend([self.error_popup, self.success_popup, self.dialog])

    def load_dropdown_options(self):
        """Fetch users, departments, and assets for dropdowns."""
        try:
            conn = mysql.connector.connect(
                host="200.200.201.100",
                user="root",
                password="Pak@123",
                database="asm_sys"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT id, name FROM users")
            users = cursor.fetchall()
            self.select_user.options = [
                ft.dropdown.Option(key=str(user[0]), text=user[1]) for user in users
            ]

            cursor.execute("SELECT id, name FROM department")
            departments = cursor.fetchall()
            self.select_department.options = [
                ft.dropdown.Option(key=str(dept[0]), text=dept[1]) for dept in departments
            ]

            cursor.execute("SELECT id, serial_number FROM assets WHERE status = 'Available'")
            assets = cursor.fetchall()
            self.select_asset.options = [
                ft.dropdown.Option(key=str(asset[0]), text=asset[1]) for asset in assets
            ]

            if self.dialog.open:
                self.page.update()
        except mysql.connector.Error as e:
            self.error_popup.content = ft.Text(f"Error loading options: {e}")
            self.error_popup.open = True
            if self.dialog.open:
                self.page.update()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def open_dialog(self, serial_number: str):
        """Open the dialog and prefill with component data."""
        self.serial_number = serial_number
        self.component_serial_number.value = serial_number
        self.load_dropdown_options()

        try:
            conn = mysql.connector.connect(
                host="200.200.201.100",
                user="root",
                password="Pak@123",
                database="asm_sys"
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, status, deployed_type, deployed_user_id, deployed_department_id, 
                       deployed_asset, disposed_reason
                FROM components WHERE serial_number = %s
            """, (serial_number,))
            component = cursor.fetchone()
            if not component:
                self.error_popup.content = ft.Text(f"Component with serial number {serial_number} not found.")
                self.error_popup.open = True
                self.page.update()
                return

            self.component_status.value = component[1]
            self.select_deployed_type.value = component[2] if component[2] else None
            self.select_user.value = str(component[3]) if component[3] else None
            self.select_department.value = str(component[4]) if component[4] else None
            self.select_asset.value = str(component[5]) if component[5] else None
            self.disposed_reason.value = component[6] if component[6] else ""
            self.status_changed(None)
            self.deployed_type_changed(None)
            self.dialog.open = True
            self.page.update()
        except mysql.connector.Error as e:
            self.error_popup.content = ft.Text(f"Error loading component: {e}")
            self.error_popup.open = True
            self.page.update()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def status_changed(self, e):
        """Update UI based on status selection."""
        if self.component_status.value == "Deployed":
            self.select_deployed_type.visible = True
            self.deployed_type_changed(None)
            self.disposed_reason.visible = False
        elif self.component_status.value == "Disposed":
            self.select_deployed_type.visible = False
            self.select_user.visible = False
            self.select_department.visible = False
            self.select_asset.visible = False
            self.disposed_reason.visible = True
        else:
            self.select_deployed_type.visible = False
            self.select_user.visible = False
            self.select_department.visible = False
            self.select_asset.visible = False
            self.disposed_reason.visible = False
        self.page.update()

    def deployed_type_changed(self, e):
        """Update UI based on deployed type selection."""
        if self.select_deployed_type.value == "User":
            self.select_user.visible = True
            self.select_department.visible = False
            self.select_asset.visible = False
        elif self.select_deployed_type.value == "Department":
            self.select_user.visible = False
            self.select_department.visible = True
            self.select_asset.visible = False
        elif self.select_deployed_type.value == "Asset":
            self.select_user.visible = False
            self.select_department.visible = False
            self.select_asset.visible = True
        else:
            self.select_user.visible = False
            self.select_department.visible = False
            self.select_asset.visible = False
        self.page.update()

    def save_data(self, e: ft.ControlEvent):
        """Save component management data to the database."""
        serial_number = self.component_serial_number.value
        status = self.component_status.value
        deployed_type = self.select_deployed_type.value if self.select_deployed_type.visible else None
        user_id = int(self.select_user.value) if self.select_user.visible and self.select_user.value else None
        department_id = int(self.select_department.value) if self.select_department.visible and self.select_department.value else None
        # Use asset serial number from dropdown text
        asset_serial = self.select_asset.options[int(self.select_asset.value)].text if self.select_asset.visible and self.select_asset.value else None
        disposed_reason = self.disposed_reason.value if self.disposed_reason.visible else None
        deployed_on = datetime.date.today() if status == "Deployed" else None
        disposed_on = datetime.date.today() if status == "Disposed" else None

        # Validation
        if not serial_number or not status:
            self.error_popup.content = ft.Text("Serial number and status are required.")
            self.error_popup.open = True
            self.page.update()
            return

        if status == "Deployed" and (not deployed_type or 
                                     (deployed_type == "User" and not user_id) or 
                                     (deployed_type == "Department" and not department_id) or 
                                     (deployed_type == "Asset" and not asset_serial)):
            self.error_popup.content = ft.Text("Please select a valid deployment option.")
            self.error_popup.open = True
            self.page.update()
            return

        if status == "Disposed" and not disposed_reason:
            self.error_popup.content = ft.Text("Please provide a reason for disposal.")
            self.error_popup.open = True
            self.page.update()
            return

        try:
            conn = mysql.connector.connect(
                host="200.200.201.100",
                user="root",
                password="Pak@123",
                database="asm_sys"
            )
            cursor = conn.cursor()

            # Update component
            cursor.execute("""
                UPDATE components
                SET status = %s, deployed_type = %s, deployed_user_id = %s, 
                    deployed_department_id = %s, deployed_asset = %s, disposed_reason = %s,
                    deployed_on = %s, disposed_on = %s
                WHERE serial_number = %s
            """, (status, deployed_type, user_id, department_id, asset_serial, disposed_reason,
                  deployed_on, disposed_on, serial_number))

            # Check if component was updated
            if cursor.rowcount == 0:
                self.error_popup.content = ft.Text(f"Component with serial number {serial_number} not found.")
                self.error_popup.open = True
                self.page.update()
                return

            # Log history with separate cursor to avoid unread result
            history_cursor = conn.cursor()
            cursor.execute("SELECT id FROM components WHERE serial_number = %s", (serial_number,))
            component_id = cursor.fetchone()
            if component_id:
                history_cursor.execute("""
                    INSERT INTO asset_history (table_type, entity_id, data_json, action)
                    VALUES (%s, %s, %s, %s)
                """, (
                    'components', 
                    component_id[0],
                    f'{{"serial_number":"{serial_number}", "status":"{status}", "deployed_type":"{deployed_type or ''}"}}',
                    'Updated'
                ))
            else:
                self.error_popup.content = ft.Text(f"Failed to log history: Component ID not found.")
                self.error_popup.open = True
                self.page.update()
                return

            conn.commit()
            self.success_popup.content = ft.Text("Component updated successfully!")
            self.success_popup.open = True
            self.page.update()
        except mysql.connector.Error as e:
            self.error_popup.content = ft.Text(f"Error saving component: {e}")
            self.error_popup.open = True
            self.page.update()
        finally:
            if 'history_cursor' in locals():
                history_cursor.close()
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def close_dialog(self, e):
        """Close the dialog and reset fields."""
        self.dialog.open = False
        self.component_status.value = None
        self.select_deployed_type.value = None
        self.select_user.value = None
        self.select_department.value = None
        self.select_asset.value = None
        self.disposed_reason.value = ""
        self.page.update()

    def close_error_popup(self, e):
        self.error_popup.open = False
        self.page.update()

    def close_success_popup(self, e):
        """Close success popup, dialog, and refresh parent."""
        self.success_popup.open = False
        self.close_dialog(e)
        if self.parent and hasattr(self.parent, 'load_components'):
            self.parent.load_components()
        self.page.update()