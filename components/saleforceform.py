

import os
import flet as ft
import mysql.connector
from mysql.connector import Error
import json
import base64
from datetime import datetime

class SaleForceDialog:
    def __init__(self, page: ft.Page):
        self.page = page
        self.attached_image_bytes = None
        self.attached_bill_bytes = None
        self.TEMP_DIR = os.path.join(os.getcwd(), "temp")
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        print(f"Initialized TEMP_DIR: {self.TEMP_DIR}, writable: {os.access(self.TEMP_DIR, os.W_OK)}")

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

        self.device_model = ft.TextField(
            label="Model",
            hint_text="Enter Device Model",
            border_color=ft.Colors.BLUE_200,
            icon=ft.Icons.DEVICE_HUB
        )
        self.device_serial_number = ft.TextField(
            label="Serial Number",
            hint_text="Enter Device Serial Number",
            border_color=ft.Colors.BLUE_200,
            icon=ft.Icons.DEVICE_HUB
        )
        self.device_company = ft.TextField(
            label="Company Name",
            hint_text="Enter Company Name",
            border_color=ft.Colors.BLUE_200,
            icon=ft.Icons.BUSINESS
        )
        self.device_location = ft.TextField(
            label="Location",
            hint_text="Enter Location",
            border_color=ft.Colors.BLUE_200,
            icon=ft.Icons.LOCATION_ON
        )
        self.device_image = ft.FilePicker(on_result=self.handle_device_image, on_upload=self.handle_device_image_upload)
        self.device_image_button = ft.ElevatedButton(
            "Select Image",
            icon=ft.Icons.IMAGE,
            bgcolor=ft.Colors.BLUE_300,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.device_image.pick_files(allow_multiple=True)
        )
        self.image_display = ft.Image(width=50, height=50, fit="contain")
        self.image_warning_text = ft.Text("", color="red")
        self.device_bill = ft.FilePicker(on_result=self.handle_bill_image, on_upload=self.handle_bill_image_upload)
        self.device_bill_button = ft.ElevatedButton(
            "Upload Bill",
            icon=ft.Icons.ATTACH_FILE,
            bgcolor=ft.Colors.BLUE_300,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.device_bill.pick_files(allow_multiple=True)
        )
        self.bill_display = ft.Image(width=50, height=50, fit="contain")
        self.bill_warning_text = ft.Text("", color="red")
        self.purchase_date_button = ft.ElevatedButton(
            "Purchase Date",
            icon=ft.Icons.DATE_RANGE,
            bgcolor=ft.Colors.BLUE_300,
            color=ft.Colors.WHITE,
            on_click=self.open_date_picker
        )
        self.purchase_date = ft.DatePicker(on_change=self.update_purchase_date)
        self.device_status = ft.Dropdown(
            label="Device Status",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[ft.dropdown.Option("Available")],
            value="Available",
            border_color=ft.Colors.BLUE_200
        )

        self.page.overlay.extend([
            self.error_popup, self.success_popup, self.device_image, self.device_bill, self.purchase_date
        ])

        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.WHITE,
            title=ft.Text("Add Device", color=ft.Colors.BLUE_800),
            content=ft.Container(
                width=400,
                content=ft.Column(
                    controls=[
                        self.device_model,
                        self.device_serial_number,
                        self.device_company,
                        self.device_location,
                        self.device_image_button,
                        self.image_display,
                        self.image_warning_text,
                        self.device_bill_button,
                        self.bill_display,
                        self.bill_warning_text,
                        self.purchase_date_button,
                        self.device_status
                    ],
                    spacing=15
                ),
                padding=20
            ),
            actions=[
                ft.TextButton("Submit", on_click=self.submit_form),
                ft.TextButton("Cancel", on_click=self.close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            content_padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.overlay.append(self.dialog)
        self.page.update()

    def handle_device_image(self, event: ft.FilePickerResultEvent):
        if not event.files:
            return
        self.attached_image_bytes = None
        self.device_image_button.text = f"{len(event.files)} image(s) selected."
        self.image_display.src_base64 = None
        self.image_warning_text.value = ""
        file = event.files[0]  # Preview the first image
        if file.size > 50 * 1024 * 1024:  # 50MB limit
            self.image_warning_text.value = f"File {file.name} exceeds 50 MB."
            self.error_popup.open = True
            self.page.update()
            return
        if self.page.web:
            try:
                self.attached_image_bytes = file.read_file()
                self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
                self.image_warning_text.value = "Image selected successfully."
            except AttributeError:
                self.image_warning_text.value = "Web mode requires temporary upload. Initiating upload..."
                upload_file = ft.FilePickerUploadFile(name=file.name, upload_url=self.page.get_upload_url(file.name, 600))
                self.device_image.upload([upload_file])
            except Exception as ex:
                self.image_warning_text.value = f"Error reading file: {ex}"
                self.error_popup.open = True
        else:
            try:
                with open(file.path, 'rb') as f:
                    self.attached_image_bytes = f.read()
                self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
                self.image_warning_text.value = "Image selected successfully."
            except Exception as ex:
                self.image_warning_text.value = f"Error reading file: {ex}"
                self.error_popup.open = True
        self.image_display.update()
        self.image_warning_text.update()
        self.page.update()

    def handle_bill_image(self, event: ft.FilePickerResultEvent):
        if not event.files:
            return
        self.attached_bill_bytes = None
        self.device_bill_button.text = f"{len(event.files)} bill(s) selected."
        self.bill_display.src_base64 = None
        self.bill_warning_text.value = ""
        file = event.files[0]  # Preview the first bill
        if file.size > 50 * 1024 * 1024:  # 50MB limit
            self.bill_warning_text.value = f"File {file.name} exceeds 50 MB."
            self.error_popup.open = True
            self.page.update()
            return
        if self.page.web:
            try:
                self.attached_bill_bytes = file.read_file()
                self.bill_display.src_base64 = base64.b64encode(self.attached_bill_bytes).decode('utf-8')
                self.bill_warning_text.value = "Bill selected successfully."
            except AttributeError:
                self.bill_warning_text.value = "Web mode requires temporary upload. Initiating upload..."
                upload_file = ft.FilePickerUploadFile(name=file.name, upload_url=self.page.get_upload_url(file.name, 600))
                self.device_bill.upload([upload_file])
            except Exception as ex:
                self.bill_warning_text.value = f"Error reading file: {ex}"
                self.error_popup.open = True
        else:
            try:
                with open(file.path, 'rb') as f:
                    self.attached_bill_bytes = f.read()
                self.bill_display.src_base64 = base64.b64encode(self.attached_bill_bytes).decode('utf-8')
                self.bill_warning_text.value = "Bill selected successfully."
            except Exception as ex:
                self.bill_warning_text.value = f"Error reading file: {ex}"
                self.error_popup.open = True
        self.bill_display.update()
        self.bill_warning_text.update()
        self.page.update()

    def handle_device_image_upload(self, e: ft.FilePickerUploadEvent):
        print(f"Upload event: file={e.file_name}, progress={e.progress}, error={e.error}")
        if e.progress == 1:
            upload_path = os.path.join(self.TEMP_DIR, e.file_name)
            if not os.path.exists(upload_path) and hasattr(self.page, 'upload_dir'):
                upload_path = os.path.join(self.page.upload_dir, e.file_name)
            if not os.path.exists(upload_path):
                self.image_warning_text.value = f"Uploaded file {e.file_name} not found"
                self.error_popup.open = True
                self.page.update()
                return
            try:
                with open(upload_path, "rb") as f:
                    file_data = f.read()
                if len(file_data) > 50 * 1024 * 1024:  # 50MB limit
                    self.image_warning_text.value = f"File {e.file_name} exceeds 50 MB."
                    self.error_popup.open = True
                else:
                    self.attached_image_bytes = file_data
                    self.image_display.src_base64 = base64.b64encode(file_data).decode('utf-8')
                    self.image_warning_text.value = "Image uploaded successfully."
                os.remove(upload_path)
                print(f"Deleted temporary file: {upload_path}")
            except Exception as ex:
                self.image_warning_text.value = f"Error reading uploaded file {e.file_name}: {ex}"
                self.error_popup.open = True
            self.image_display.update()
            self.image_warning_text.update()
            self.page.update()
        elif e.error:
            self.image_warning_text.value = f"Upload error for {e.file_name}: {e.error}"
            self.error_popup.open = True
            self.page.update()

    def handle_bill_image_upload(self, e: ft.FilePickerUploadEvent):
        print(f"Upload event: file={e.file_name}, progress={e.progress}, error={e.error}")
        if e.progress == 1:
            upload_path = os.path.join(self.TEMP_DIR, e.file_name)
            if not os.path.exists(upload_path) and hasattr(self.page, 'upload_dir'):
                upload_path = os.path.join(self.page.upload_dir, e.file_name)
            if not os.path.exists(upload_path):
                self.bill_warning_text.value = f"Uploaded file {e.file_name} not found"
                self.error_popup.open = True
                self.page.update()
                return
            try:
                with open(upload_path, "rb") as f:
                    file_data = f.read()
                if len(file_data) > 50 * 1024 * 1024:  # 50MB limit
                    self.bill_warning_text.value = f"File {e.file_name} exceeds 50 MB."
                    self.error_popup.open = True
                else:
                    self.attached_bill_bytes = file_data
                    self.bill_display.src_base64 = base64.b64encode(file_data).decode('utf-8')
                    self.bill_warning_text.value = "Bill uploaded successfully."
                os.remove(upload_path)
                print(f"Deleted temporary file: {upload_path}")
            except Exception as ex:
                self.bill_warning_text.value = f"Error reading uploaded file {e.file_name}: {ex}"
                self.error_popup.open = True
            self.bill_display.update()
            self.bill_warning_text.update()
            self.page.update()
        elif e.error:
            self.bill_warning_text.value = f"Upload error for {e.file_name}: {e.error}"
            self.error_popup.open = True
            self.page.update()

    def open_date_picker(self, event):
        self.purchase_date.open = True
        self.page.update()

    def update_purchase_date(self, e):
        if e.control.value:
            selected_date = e.control.value.strftime('%Y-%m-%d')
            self.purchase_date_button.text = f"Purchase Date: {selected_date}"
        else:
            self.purchase_date_button.text = "Purchase Date"
        self.purchase_date.open = False
        self.purchase_date_button.update()
        self.page.update()

    def save_data(self, event):
        model = self.device_model.value.strip()
        serial_number = self.device_serial_number.value.strip()
        company = self.device_company.value.strip()
        location = self.device_location.value.strip()
        purchase_date = self.purchase_date.value.strftime('%Y-%m-%d') if self.purchase_date.value else None
        status = self.device_status.value

        if not all([model, serial_number, company, location, purchase_date, status]):
            self.error_popup.content = ft.Text("Please fill in all required fields.")
            self.error_popup.open = True
            self.page.update()
            return

        db_config = {
            "host": "200.200.201.100",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM devices WHERE serial_number = %s", (serial_number,))
            if cursor.fetchone()[0] > 0:
                self.error_popup.content = ft.Text("Serial number already exists.")
                self.error_popup.open = True
                self.page.update()
                return

            cursor.execute(
                """
                INSERT INTO devices (model, serial_number, company, location, purchase_date, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (model, serial_number, company, location, purchase_date, status)
            )
            device_id = cursor.lastrowid

            if self.attached_image_bytes:
                for file in self.device_image.result.files if self.device_image.result else []:
                    cursor.execute(
                        "INSERT INTO device_images (device_id, image_name, image_data) VALUES (%s, %s, %s)",
                        (device_id, file.name, self.attached_image_bytes)
                    )
            if self.attached_bill_bytes:
                for file in self.device_bill.result.files if self.device_bill.result else []:
                    cursor.execute(
                        "INSERT INTO device_bills (device_id, bill_name, bill_data) VALUES (%s, %s, %s)",
                        (device_id, file.name, self.attached_bill_bytes)
                    )

            cursor.execute(
                """
                INSERT INTO asset_history (table_type, entity_id, data_json, action)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    'devices',
                    device_id,
                    json.dumps({
                        'model': model,
                        'serial_number': serial_number,
                        'company': company,
                        'location': location,
                        'purchase_date': purchase_date,
                        'status': status
                    }),
                    'Added'
                )
            )

            conn.commit()
            self.success_popup.content = ft.Text("Device added successfully.")
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

    def submit_form(self, e):
        self.save_data(e)
        self.close_dialog(e)

    def close_error_popup(self, e):
        self.error_popup.open = False
        self.page.update()

    def close_success_popup(self, e):
        self.success_popup.open = False
        self.page.update()

    def clear_fields(self):
        self.device_model.value = ""
        self.device_serial_number.value = ""
        self.device_company.value = ""
        self.device_location.value = ""
        self.attached_image_bytes = None
        self.attached_bill_bytes = None
        self.purchase_date_button.text = "Purchase Date"
        self.device_status.value = "Available"
        self.device_image_button.text = "Select Image"
        self.device_bill_button.text = "Upload Bill"
        self.device_model.update()
        self.device_serial_number.update()
        self.device_company.update()
        self.device_location.update()
        self.purchase_date_button.update()
        self.device_status.update()
        self.device_image_button.update()
        self.device_bill_button.update()
        self.purchase_date.value = None
        self.image_display.src_base64 = None
        self.bill_display.src_base64 = None
        self.image_warning_text.value = ""
        self.bill_warning_text.value = ""

    def close_dialog(self, e):
        self.clear_fields()
        self.dialog.open = False
        self.page.update()

    def open(self):
        self.dialog.open = True
        self.page.update()
