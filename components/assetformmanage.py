import os
os.environ["FLET_SECRET_KEY"] = "mysecret123"
import flet as ft
import mysql.connector
from mysql.connector import Error

class AssetFormManage:
    def __init__(self, page: ft.Page, parent=None):
        self.page = page
        self.parent = parent  # Store the parent (AssetPage) for reload, if provided
        self.all_users = []  # Store all users for filtering later
        self.db_config = {
            "host": "200.200.200.23",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }

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

        # Form fields
        self.asset_serial_number = ft.TextField(
            label="Serial Number",
            hint_text="Asset Serial Number",
            icon=ft.Icons.DEVICE_HUB,
            disabled=True
        )
        self.asset_model = ft.TextField(
            label="Model",
            hint_text="Enter Model",
            icon=ft.Icons.MODEL_TRAINING,
            disabled=True
        )
        self.asset_company = ft.TextField(
            label="Company",
            hint_text="Enter Company",
            icon=ft.Icons.BUSINESS,
            disabled=True
        )
        self.asset_location = ft.TextField(
            label="Location",
            hint_text="Enter Location",
            icon=ft.Icons.LOCATION_ON,
            disabled=True  # Will be enabled/disabled based on status
        )
        self.asset_status = ft.Dropdown(
            label="Asset Status",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Deployed"),
                ft.dropdown.Option("Dispose"),
                ft.dropdown.Option("Sold")
            ],
            on_change=self.status_changed,
            expand=True,
        )
        self.select_deploye = ft.Dropdown(
            label="Select Deploye",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[
                ft.dropdown.Option("User"),
                ft.dropdown.Option("Department"),
            ],
            visible=False,
            on_change=self.deploy_to_changed
        )
        self.select_user_department = ft.Dropdown(
            label="Select Department",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            menu_height=200,
            options=[],
            visible=False,
            on_change=self.department_changed
        )
        self.select_user = ft.Dropdown(
            label="Select User",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[],
            visible=False
        )
        self.select_department = ft.Dropdown(
            label="Select Department",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[],
            visible=False
        )
        self.disposal_options = ft.Dropdown(
            label="Disposal Option",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[
                ft.dropdown.Option("Dispose"),
                ft.dropdown.Option("Sold")
            ],
            visible=False,
            on_change=self.disposal_option_changed
        )
        self.disposal_date_field = ft.TextField(
            label="Disposal Date",
            value="2025-06-03",  # Set to current date
            icon=ft.Icons.CALENDAR_MONTH,
            visible=False,
            disabled=True
        )
        self.deployed_date_field = ft.TextField(
            label="Deployed Date",
            value="2025-06-03",  # Set to current date
            icon=ft.Icons.CALENDAR_MONTH,
            visible=False,
            disabled=True
        )
        self.dispose_reason_field = ft.TextField(
            label="Dispose Reason",
            hint_text="Enter Dispose Reason",
            visible=False
        )
        self.sold_to_field = ft.TextField(
            label="Sold To",
            hint_text="Enter Sold To",
            visible=False
        )
        self.sold_price_field = ft.TextField(
            label="Sold Price",
            hint_text="Enter Sold Price",
            icon=ft.Icons.ATTACH_MONEY,
            visible=False,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        # Initialize the dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.BLUE_GREY_100,
            title=ft.Text("Manage Asset"),
            content=ft.Container(
                width=400,
                height=600,
                content=ft.Column(
                    controls=[
                        self.asset_serial_number,
                        self.asset_model,
                        self.asset_company,
                        self.asset_location,
                        self.asset_status,
                        self.select_deploye,
                        self.select_user_department,
                        self.select_user,
                        self.select_department,
                        self.disposal_options,
                        self.deployed_date_field,
                        self.disposal_date_field,
                        self.dispose_reason_field,
                        self.sold_to_field,
                        self.sold_price_field
                    ],
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                )
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.TextButton("Save", on_click=self.save_asset)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Add overlay components during initialization
        self.page.overlay.extend([self.error_popup, self.success_popup, self.dialog])

    def _get_db_connection(self):
        """Helper method to get a database connection."""
        try:
            return mysql.connector.connect(**self.db_config)
        except Error as e:
            self.show_snackbar(f"Database connection error: {e}", ft.Colors.RED_400)
            return None

    def show_snackbar(self, message, color):
        """Display a snackbar with the given message and color."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=color),
            duration=4000
        )
        self.page.snack_bar.open = True
        self.page.update()

    def open(self, serial_number):
        """Open the dialog with asset details based on serial number."""
        try:
            conn = self._get_db_connection()
            if not conn:
                return
            cursor = conn.cursor(dictionary=True)

            # Fetch departments
            cursor.execute("SELECT id, name FROM department")
            departments = cursor.fetchall()
            self.select_user_department.options = [
                ft.dropdown.Option(key=str(dept['id']), text=dept['name']) for dept in departments
            ] or [ft.dropdown.Option(key="0", text="No departments available")]
            self.select_department.options = [
                ft.dropdown.Option(key=str(dept['id']), text=dept['name']) for dept in departments
            ] or [ft.dropdown.Option(key="0", text="No departments available")]

            # Fetch users
            cursor.execute("SELECT id, name, department_id FROM users")
            self.all_users = cursor.fetchall()
            self.select_user.options = [
                ft.dropdown.Option(key=str(user['id']), text=user['name']) for user in self.all_users
            ] or [ft.dropdown.Option(key="0", text="No users available")]

            # Fetch asset details
            cursor.execute("SELECT * FROM assets WHERE serial_number = %s", (serial_number,))
            asset = cursor.fetchone()
            if asset:
                self.asset_serial_number.value = asset['serial_number']
                self.asset_model.value = asset['model']
                self.asset_company.value = asset['company']
                self.asset_location.value = asset['location']
                self.asset_status.value = asset['status']
                self.select_deploye.value = asset.get('deployed_type')
                self.select_user.value = str(asset.get('deployed_user_id')) if asset.get('deployed_type') == 'User' else None
                self.select_department.value = str(asset.get('deployed_department_id')) if asset.get('deployed_type') == 'Department' else None
                self.disposal_options.value = asset.get('disposed_type')
                self.deployed_date_field.value = asset['deployed_on'].strftime('%Y-%m-%d') if asset.get('deployed_on') else 'N/A'
                self.disposal_date_field.value = asset['disposed_on'].strftime('%Y-%m-%d') if asset.get('disposed_on') else 'N/A'
                self.dispose_reason_field.value = asset.get('disposed_reason', '')
                self.sold_to_field.value = asset.get('sold_to', '')
                self.sold_price_field.value = str(asset.get('sold_price', '')) if asset.get('sold_price') else ''
                self.status_changed(None)  # Update visibility based on loaded status

                # If a department is already selected for a user, filter users
                if self.select_deploye.value == "User" and self.select_user_department.value:
                    self.department_changed(None)

            # Open the dialog
            self.dialog.open = True
            self.page.update()
        except Error as e:
            self.error_popup.content = ft.Text(f"Error loading asset: {e}")
            self.error_popup.open = True
            self.page.update()
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def status_changed(self, e):
        # Reset visibility of all fields
        self.select_deploye.visible = False
        self.select_user_department.visible = False
        self.select_user.visible = False
        self.select_department.visible = False
        self.disposal_options.visible = False
        self.deployed_date_field.visible = False
        self.disposal_date_field.visible = False
        self.dispose_reason_field.visible = False
        self.sold_to_field.visible = False
        self.sold_price_field.visible = False

        status = e.control.value if e else self.asset_status.value
        if status == "Available":
            self.select_deploye.visible = False
            self.disposal_options.visible = False
            self.asset_location.disabled = False  # Enable location input for Available status
        elif status == "Deployed":
            self.select_deploye.visible = True
            self.disposal_options.visible = False
            self.deployed_date_field.visible = True
            self.asset_location.disabled = True  # Disable location input
            self.asset_location.value = "N/A"  # Set location to N/A
        elif status in ["Dispose", "Sold"]:
            self.select_deploye.visible = False
            self.disposal_options.visible = True
            self.disposal_date_field.visible = True
            if status == "Dispose":
                self.dispose_reason_field.visible = True
            elif status == "Sold":
                self.sold_to_field.visible = True
                self.sold_price_field.visible = True
            self.select_user_department.visible = False
            self.select_user.visible = False
            self.select_department.visible = False
            self.asset_location.disabled = True  # Disable location input
            self.asset_location.value = "N/A"  # Set location to N/A
        self.page.update()

    def deploy_to_changed(self, e):
        self.select_user_department.value = None
        self.select_user.value = None
        if e.control.value == "User":
            self.select_user_department.visible = True
            self.select_user.visible = True
            self.select_department.visible = False
        elif e.control.value == "Department":
            self.select_user_department.visible = False
            self.select_user.visible = False
            self.select_department.visible = True
        self.page.update()

    def department_changed(self, e):
        if self.select_deploye.value == "User" and e.control.value:
            try:
                department_id = int(e.control.value)
                filtered_users = [user for user in self.all_users if user['department_id'] == department_id]
                self.select_user.options = [
                    ft.dropdown.Option(key=str(user['id']), text=user['name']) for user in filtered_users
                ] or [ft.dropdown.Option(key="0", text="No users in this department")]
                self.select_user.value = None
            except (ValueError, TypeError):
                self.select_user.options = [ft.dropdown.Option(key="0", text="Invalid department selected")]
                self.select_user.value = None
        self.page.update()

    def disposal_option_changed(self, e):
        # Reset visibility of disposal fields
        self.dispose_reason_field.visible = False
        self.sold_to_field.visible = False
        self.sold_price_field.visible = False

        if e.control.value == "Dispose":
            self.dispose_reason_field.visible = True
        elif e.control.value == "Sold":
            self.sold_to_field.visible = True
            self.sold_price_field.visible = True
        self.page.update()

    def close_dialog(self, e):
        """Close the dialog and reset fields."""
        self.dialog.open = False
        # Reset form fields
        self.asset_serial_number.value = ""
        self.asset_model.value = ""
        self.asset_company.value = ""
        self.asset_location.value = ""
        self.asset_status.value = "Available"
        self.select_deploye.value = None
        self.select_user_department.value = None
        self.select_user.value = None
        self.select_department.value = None
        self.disposal_options.value = None
        self.deployed_date_field.value = "2025-06-03"
        self.disposal_date_field.value = "2025-06-03"
        self.dispose_reason_field.value = ""
        self.sold_to_field.value = ""
        self.sold_price_field.value = ""
        # Reset visibility
        self.select_deploye.visible = False
        self.select_user_department.visible = False
        self.select_user.visible = False
        self.select_department.visible = False
        self.disposal_options.visible = False
        self.deployed_date_field.visible = False
        self.disposal_date_field.visible = False
        self.dispose_reason_field.visible = False
        self.sold_to_field.visible = False
        self.sold_price_field.visible = False
        self.asset_location.disabled = True
        self.page.update()

    def close_error_popup(self, e):
        self.error_popup.open = False
        self.page.update()

    def close_success_popup(self, e):
        """Close the success popup, dialog, and reset form fields."""
        self.success_popup.open = False
        self.close_dialog(e)  # Close dialog and reset fields
        # Reload assets in the parent AssetPage if parent is provided
        if self.parent and hasattr(self.parent, 'load_assets'):
            self.parent.load_assets()

    def save_asset(self, e: ft.ControlEvent):
        serial_number = self.asset_serial_number.value
        model = self.asset_model.value
        company = self.asset_company.value
        location = self.asset_location.value
        status = self.asset_status.value
        deployed_type = self.select_deploye.value if self.select_deploye.visible else None
        user_id = self.select_user.value if self.select_user.visible else None
        department_id = self.select_department.value if self.select_department.visible else None
        disposed_type = self.disposal_options.value if self.disposal_options.visible else None
        dispose_reason = self.dispose_reason_field.value if self.dispose_reason_field.visible else None
        sold_to = self.sold_to_field.value if self.sold_to_field.visible else None
        sold_price = self.sold_price_field.value if self.sold_price_field.visible else None

        if not serial_number or not status or not model or not company or not location:
            self.error_popup.content = ft.Text("Please ensure serial number, status, model, company, and location are set.")
            self.error_popup.open = True
            self.page.update()
            return
        if status == "Deployed" and (not deployed_type or (deployed_type == "User" and not user_id) or (deployed_type == "Department" and not department_id)):
            self.error_popup.content = ft.Text("Please fill in all fields for deployed status.")
            self.error_popup.open = True
            self.page.update()
            return
        if status in ["Dispose", "Sold"]:
            if status == "Dispose" and not dispose_reason:
                self.error_popup.content = ft.Text("Please enter a dispose reason.")
                self.error_popup.open = True
                self.page.update()
                return
            if status == "Sold" and (not sold_to or not sold_price):
                self.error_popup.content = ft.Text("Please fill in all fields for sale.")
                self.error_popup.open = True
                self.page.update()
                return

        try:
            conn = self._get_db_connection()
            if not conn:
                return
            cursor = conn.cursor(dictionary=True)

            # Fetch the current purchase_date to ensure it doesn't change
            cursor.execute("SELECT purchase_date FROM assets WHERE serial_number = %s", (serial_number,))
            current_asset = cursor.fetchone()
            purchase_date = current_asset['purchase_date'] if current_asset else None

            cursor.execute("""
                UPDATE assets 
                SET model = %s,
                    company = %s,
                    location = %s,
                    purchase_date = %s,
                    status = %s,
                    deployed_type = %s,
                    deployed_user_id = %s,
                    deployed_department_id = %s,
                    deployed_on = CASE WHEN %s = 'Deployed' THEN CURDATE() ELSE NULL END,
                    disposed_type = %s,
                    disposed_reason = %s,
                    sold_to = %s,
                    sold_price = %s,
                    disposed_on = CASE WHEN %s IN ('Dispose', 'Sold') THEN CURDATE() ELSE NULL END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE serial_number = %s
            """, (model, company, location, purchase_date, status, deployed_type, user_id, department_id, status, disposed_type, dispose_reason, sold_to, sold_price, status, serial_number))

            conn.commit()
            self.success_popup.content = ft.Text("Asset updated successfully!")
            self.success_popup.open = True
            self.page.update()

        except Error as e:
            self.error_popup.content = ft.Text(f"Error updating asset: {e}")
            self.error_popup.open = True
            self.page.update()
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()



