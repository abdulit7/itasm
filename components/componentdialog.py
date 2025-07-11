
import os
os.environ["FLET_SECRET_KEY"] = "mysecret123"
import flet as ft
import mysql.connector
from mysql.connector import Error
import base64
from typing import Optional, List, Tuple
import datetime
import re
import asyncio
from components.fields import CustomTextField

class ComponentDialog:
    def __init__(self, page: ft.Page, parent=None):
        if page is None:
            raise ValueError("Page object must be provided to ComponentDialog")
        self.page = page
        self.parent = parent
        self.attached_images = []  # Store multiple images
        self.attached_bills = []  # Store multiple bills
        self.TEMP_DIR = os.path.join(os.getcwd(), "temp")
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        print(f"Initialized TEMP_DIR: {self.TEMP_DIR}, writable: {os.access(self.TEMP_DIR, os.W_OK)}")

        self.error_popup = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(""), actions=[ft.TextButton("OK", on_click=self.close_error_popup)])
        self.success_popup = ft.AlertDialog(title=ft.Text("Success"), content=ft.Text(""), actions=[ft.TextButton("OK", on_click=self.close_success_popup)])

        self.component_model = CustomTextField(label="Model", hint_text="Model", icon=ft.Icons.DEVICE_HUB)
        self.component_serial_number = CustomTextField(label="Serial Number", hint_text="Enter Component Serial Number", icon=ft.Icons.DEVICE_HUB)
        self.component_company = CustomTextField(label="Company Name", hint_text="Enter Company Name", icon=ft.Icons.BUSINESS)
        self.component_location = CustomTextField(label="Location", hint_text="Enter Location", icon=ft.Icons.LOCATION_ON)
        self.component_image = ft.FilePicker(on_result=self.handle_component_image, on_upload=self.handle_image_upload)
        self.component_image_button = ft.ElevatedButton("Select Image", icon=ft.Icons.IMAGE, on_click=lambda e: self.component_image.pick_files(allow_multiple=True))
        self.image_display = ft.Image(width=50, height=50, fit="contain")
        self.image_warning_text = ft.Text("", color="red")
        self.bill_image = ft.FilePicker(on_result=self.handle_bill_image, on_upload=self.handle_bill_upload)
        self.component_bill_button = ft.ElevatedButton("Upload Bill", icon=ft.Icons.ATTACH_FILE, on_click=lambda e: self.bill_image.pick_files(allow_multiple=True))
        self.bill_display = ft.Image(width=50, height=50, fit="contain")
        self.bill_warning_text = ft.Text("", color="red")
        self.purchase_date_button = ft.ElevatedButton("Purchase Date", icon=ft.Icons.DATE_RANGE, on_click=self.open_date_picker)
        self.purchase_date = ft.DatePicker(on_change=self.update_purchase_date)

        self.component_status = ft.Dropdown(
            label="Component Status",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[ft.dropdown.Option("Available"), ft.dropdown.Option("Deployed"), ft.dropdown.Option("Disposed")]
        )

        self.component_category = ft.Dropdown(
            label="Category",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            hint_text="Select Category",
            options=[],
            on_change=self.update_category
        )

        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.RED_100,
            title=ft.Text("Add/Edit Component"),
            content=ft.Container(
                width=400,
                height=600,
                content=ft.Column(
                    controls=[
                        self.component_category,
                        self.component_model,
                        self.component_serial_number,
                        self.component_company,
                        self.component_location,
                        self.component_image_button,
                        self.image_display,
                        self.image_warning_text,
                        self.component_bill_button,
                        self.bill_display,
                        self.bill_warning_text,
                        self.purchase_date_button,
                        self.purchase_date,
                        self.component_status
                    ],
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=20
            ),
            actions=[ft.TextButton("Cancel", on_click=self.close_dialog), ft.TextButton("Submit", on_click=self.submit_form)],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.overlay.extend([self.error_popup, self.success_popup, self.component_image, self.bill_image, self.purchase_date, self.dialog])

    def load_categories(self):
        try:
            conn = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="asm_sys"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM category WHERE type = 'Component'")
            categories = cursor.fetchall()
            self.component_category.options = [ft.dropdown.Option(key=str(cat[0]), text=cat[1]) for cat in categories]
            if self.dialog.open:
                self.page.update()
        except mysql.connector.Error as e:
            self.error_popup.content = ft.Text(f"Error loading categories: {e}")
            self.error_popup.open = True
            if self.dialog.open:
                self.page.update()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def update_category(self, e):
        pass

    def open_dialog(self):
        self.dialog.open = True
        self.load_categories()
        self.page.update()

    def handle_component_image(self, e: ft.FilePickerResultEvent):
        self.attached_images = e.files if e.files else []
        self.component_image_button.text = f"{len(self.attached_images)} image(s) selected."
        self.image_display.src_base64 = None
        self.image_warning_text.value = ""
        if self.attached_images:
            file = self.attached_images[0]  # Preview the first image
            if self.page.web:
                try:
                    self.attached_image_bytes = file.read_file()
                    self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
                    self.image_warning_text.value = "Image selected successfully."
                except AttributeError:
                    self.image_warning_text.value = "Web mode requires temporary upload. Initiating upload..."
                    upload_file = ft.FilePickerUploadFile(name=file.name, upload_url=self.page.get_upload_url(file.name, 600))
                    self.component_image.upload([upload_file])
                except Exception as ex:
                    self.image_warning_text.value = f"Error reading file: {ex}"
            else:
                try:
                    with open(file.path, "rb") as f:
                        self.attached_image_bytes = f.read()
                    self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
                    self.image_warning_text.value = "Image selected successfully."
                except Exception as ex:
                    self.image_warning_text.value = f"Error reading file: {ex}"
            self.image_display.update()
        self.image_warning_text.update()
        self.page.update()

    def handle_bill_image(self, e: ft.FilePickerResultEvent):
        self.attached_bills = e.files if e.files else []
        self.component_bill_button.text = f"{len(self.attached_bills)} bill(s) selected."
        self.bill_display.src_base64 = None
        self.bill_warning_text.value = ""
        if self.attached_bills:
            file = self.attached_bills[0]  # Preview the first bill
            if self.page.web:
                try:
                    self.attached_bill_bytes = file.read_file()
                    self.bill_display.src_base64 = base64.b64encode(self.attached_bill_bytes).decode('utf-8')
                    self.bill_warning_text.value = "Bill selected successfully."
                except AttributeError:
                    self.bill_warning_text.value = "Web mode requires temporary upload. Initiating upload..."
                    upload_file = ft.FilePickerUploadFile(name=file.name, upload_url=self.page.get_upload_url(file.name, 600))
                    self.bill_image.upload([upload_file])
                except Exception as ex:
                    self.bill_warning_text.value = f"Error reading file: {ex}"
            else:
                try:
                    with open(file.path, "rb") as f:
                        self.attached_bill_bytes = f.read()
                    self.bill_display.src_base64 = base64.b64encode(self.attached_bill_bytes).decode('utf-8')
                    self.bill_warning_text.value = "Bill selected successfully."
                except Exception as ex:
                    self.bill_warning_text.value = f"Error reading file: {ex}"
            self.bill_display.update()
        self.bill_warning_text.update()
        self.page.update()

    def handle_image_upload(self, e: ft.FilePickerUploadEvent):
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
                if len(file_data) > 50 * 1024 * 1024:  # 50 MB
                    self.image_warning_text.value = f"File {e.file_name} exceeds the maximum size of 50 MB."
                    self.error_popup.open = True
                else:
                    for img in self.attached_images:
                        if img.name == e.file_name:
                            self.attached_image_bytes = file_data
                            self.image_display.src_base64 = base64.b64encode(file_data).decode('utf-8')
                            self.image_warning_text.value = "Image uploaded successfully."
                            break
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

    def handle_bill_upload(self, e: ft.FilePickerUploadEvent):
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
                if len(file_data) > 50 * 1024 * 1024:  # 50 MB
                    self.bill_warning_text.value = f"File {e.file_name} exceeds the maximum size of 50 MB."
                    self.error_popup.open = True
                else:
                    for bill in self.attached_bills:
                        if bill.name == e.file_name:
                            self.attached_bill_bytes = file_data
                            self.bill_display.src_base64 = base64.b64encode(file_data).decode('utf-8')
                            self.bill_warning_text.value = "Bill uploaded successfully."
                            break
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

    def update_purchase_date(self, event):
        if event.control.value:
            self.purchase_date_button.text = f"Purchase Date: {event.control.value.strftime('%Y-%m-%d')}"
        else:
            self.purchase_date_button.text = "Purchase Date"
        self.page.update()

    def close_dialog(self, event):
        self.dialog.open = False
        self.component_category.value = None
        self.component_model.value = ""
        self.component_serial_number.value = ""
        self.component_company.value = ""
        self.component_location.value = ""
        self.attached_images = []
        self.attached_bills = []
        self.component_image_button.text = "Select Image"
        self.component_bill_button.text = "Upload Bill"
        self.purchase_date_button.text = "Purchase Date"
        self.component_status.value = None
        self.image_display.src_base64 = None
        self.bill_display.src_base64 = None
        self.image_warning_text.value = ""
        self.bill_warning_text.value = ""
        self.close_success_popup(event)
        self.page.update()

    def close_error_popup(self, event):
        self.error_popup.open = False
        self.page.update()

    def close_success_popup(self, event):
        self.success_popup.open = False
        self.dialog.open = False
        self.component_category.value = None
        self.component_model.value = ""
        self.component_serial_number.value = ""
        self.component_company.value = ""
        self.component_location.value = ""
        self.attached_images = []
        self.attached_bills = []
        self.component_image_button.text = "Select Image"
        self.component_bill_button.text = "Upload Bill"
        self.purchase_date_button.text = "Purchase Date"
        self.component_status.value = None
        self.image_display.src_base64 = None
        self.bill_display.src_base64 = None
        self.image_warning_text.value = ""
        self.bill_warning_text.value = ""
        if self.parent and hasattr(self.parent, 'load_components'):
            self.parent.load_components()
        self.page.update()

    def submit_form(self, event):
        category_id = self.component_category.value
        model = self.component_model.value
        serial_number = self.component_serial_number.value
        company = self.component_company.value
        location = self.component_location.value
        status = self.component_status.value
        purchase_date = self.purchase_date_button.text.replace("Purchase Date: ", "")

        if not all([model, serial_number, company, location, purchase_date]) or purchase_date == "Purchase Date":
            self.error_popup.content = ft.Text("All fields are required.")
            self.error_popup.open = True
            self.page.update()
            return

        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM components WHERE serial_number = %s", (serial_number,))
            existing_component = cursor.fetchone()

            if existing_component:
                cursor.execute("""
                    UPDATE components 
                    SET category_id = %s, model = %s, company = %s, location = %s, 
                        purchase_date = %s, status = %s
                    WHERE serial_number = %s
                """, (int(category_id) if category_id else None, model, company, location, purchase_date, status, serial_number))
                component_id = existing_component[0]
            else:
                cursor.execute("""
                    INSERT INTO components (
                        category_id, model, serial_number, company, location, 
                        purchase_date, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (int(category_id) if category_id else None, model, serial_number, company, location, purchase_date, status))
                component_id = cursor.lastrowid

            if self.attached_images and hasattr(self, 'attached_image_bytes'):
                for img in self.attached_images:
                    cursor.execute("""
                        INSERT INTO component_images (component_id, image_name, image_data)
                        VALUES (%s, %s, %s)
                    """, (component_id, img.name, self.attached_image_bytes))
            if self.attached_bills and hasattr(self, 'attached_bill_bytes'):
                for bill in self.attached_bills:
                    cursor.execute("""
                        INSERT INTO component_bills (component_id, bill_name, bill_data)
                        VALUES (%s, %s, %s)
                    """, (component_id, bill.name, self.attached_bill_bytes))

            cursor.execute("""
                INSERT INTO asset_history (table_type, entity_id, data_json, action)
                VALUES (%s, %s, %s, %s)
            """, ('components', component_id, f'{{"model":"{model}", "serial_number":"{serial_number}", "status":"{status}"}}', 'Updated' if existing_component else 'Added'))

            conn.commit()
            self.success_popup.content = ft.Text("Component saved successfully!")
            self.success_popup.open = True
            self.page.update()

        except Error as e:
            self.error_popup.content = ft.Text(f"Error saving component: {e}")
            self.error_popup.open = True
            self.page.update()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
