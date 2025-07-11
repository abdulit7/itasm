
import os
import flet as ft
import mysql.connector
from mysql.connector import Error
import base64
from datetime import datetime

class ConsumableForm(ft.Container):
    def __init__(self, page: ft.Page, consumable_id=None, on_save_callback=None):
        super().__init__()
        self.page = page
        self.consumable_id = consumable_id
        self.on_save_callback = on_save_callback
        self.attached_image = None
        self.attached_bill = None
        self.cartridges = []
        self.printers = []
        self.TEMP_DIR = os.path.join(os.getcwd(), "temp")
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        print(f"Initialized TEMP_DIR: {self.TEMP_DIR}, writable: {os.access(self.TEMP_DIR, os.W_OK)}")

        # Initialize snackbar (replacing popups for consistency)
        self.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

        # Initialize form fields
        self.select_cartridge = ft.Dropdown(
            label="Cartridge Type",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            border_color=ft.Colors.ORANGE_200,
            on_change=self.update_existing_info
        )
        self.consumable_qty = ft.TextField(
            label="Quantity",
            value="1",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.ORANGE_200
        )
        self.consumable_location = ft.TextField(
            label="Location",
            value="Warehouse",
            border_color=ft.Colors.ORANGE_200
        )
        self.consumable_image = ft.FilePicker(on_result=self.handle_consumable_image, on_upload=self.handle_consumable_image_upload)
        self.consumable_image_button = ft.ElevatedButton(
            "Select Image",
            icon=ft.Icons.IMAGE,
            bgcolor=ft.Colors.ORANGE_200,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.consumable_image.pick_files(allow_multiple=False)
        )
        self.image_display = ft.Image(width=50, height=50, fit="contain")
        self.image_warning_text = ft.Text("", color="red")
        self.bill_image = ft.FilePicker(on_result=self.handle_bill_image, on_upload=self.handle_bill_image_upload)
        self.bill_image_button = ft.ElevatedButton(
            "Select Bill Image",
            icon=ft.Icons.ATTACHMENT,
            bgcolor=ft.Colors.ORANGE_200,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.bill_image.pick_files(allow_multiple=False)
        )
        self.bill_display = ft.Image(width=50, height=50, fit="contain")
        self.bill_warning_text = ft.Text("", color="red")
        self.purchase_date_button = ft.ElevatedButton(
            "Purchase Date",
            icon=ft.Icons.DATE_RANGE,
            bgcolor=ft.Colors.ORANGE_200,
            color=ft.Colors.WHITE,
            on_click=self.open_date_picker
        )
        self.purchase_date = ft.DatePicker(on_change=self.update_purchase_date)
        self.consumable_status = ft.Dropdown(
            label="Consumable Status",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Deployed"),
                ft.dropdown.Option("Consumed"),
            ],
            value="Available",
            border_color=ft.Colors.ORANGE_200,
            on_change=self.toggle_fields
        )
        self.select_printer = ft.Dropdown(
            label="Deployed To",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            border_color=ft.Colors.ORANGE_200,
            visible=False
        )
        self.consumed_by = ft.TextField(
            label="Consumed By",
            border_color=ft.Colors.ORANGE_200,
            visible=False
        )

        # Initialize dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.ORANGE_50,
            title=ft.Text("Add/Edit Consumable", color=ft.Colors.ORANGE_800),
            content=ft.Container(
                width=400,
                height=550,
                content=ft.Column(
                    controls=[
                        self.select_cartridge,
                        self.consumable_qty,
                        self.consumable_location,
                        self.consumable_image_button,
                        self.image_display,
                        self.image_warning_text,
                        self.bill_image_button,
                        self.bill_display,
                        self.bill_warning_text,
                        self.purchase_date_button,
                        self.consumable_status,
                        self.select_printer,
                        self.consumed_by
                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.ElevatedButton("Save", bgcolor=ft.Colors.ORANGE_400, color=ft.Colors.WHITE, on_click=self.save_consumable)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        # Add to overlay once
        self.page.overlay.extend([self.snack_bar, self.dialog, self.consumable_image, self.bill_image, self.purchase_date])

        self.load_cartridges()
        self.load_printers()
        if self.consumable_id:
            self.load_existing_consumable()

    def load_cartridges(self):
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, cartridge_no FROM cartridges ORDER BY cartridge_no")
            self.cartridges = cursor.fetchall()
            self.select_cartridge.options = [
                ft.dropdown.Option(key=str(c["id"]), text=c["cartridge_no"]) for c in self.cartridges
            ]
            self.page.update()
        except Error as e:
            self.show_snack_bar(f"Error loading cartridges: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def load_printers(self):
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, model FROM printers ORDER BY model")
            self.printers = cursor.fetchall()
            self.select_printer.options = [
                ft.dropdown.Option(key=str(p["id"]), text=p["model"]) for p in self.printers
            ]
            self.page.update()
        except Error as e:
            self.show_snack_bar(f"Error loading printers: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def load_existing_consumable(self):
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT cs.*, cr.cartridge_no, p.model AS deployed_to_model
                FROM consumables cs
                LEFT JOIN cartridges cr ON cs.cartridge_id = cr.id
                LEFT JOIN printers p ON cs.deployed_to = p.id
                WHERE cs.id = %s
            """, (self.consumable_id,))
            consumable = cursor.fetchone()
            if consumable:
                self.select_cartridge.value = str(consumable["cartridge_id"])
                self.consumable_qty.value = str(consumable["available_quantity"])
                self.consumable_location.value = consumable["location"]
                self.purchase_date_button.text = (
                    consumable["purchase_date"].strftime("%Y-%m-%d")
                    if consumable["purchase_date"] else "Purchase Date"
                )
                self.consumable_status.value = consumable["status"]
                self.select_printer.value = str(consumable["deployed_to"]) if consumable["deployed_to"] else None
                self.consumed_by.value = consumable["consumed_by"] or ""
                self.toggle_fields(None)
                cursor.execute("SELECT image_name, image_data FROM consumable_images WHERE consumable_id = %s", (self.consumable_id,))
                image_data = cursor.fetchone()
                if image_data:
                    self.attached_image = {"name": image_data["image_name"], "data": image_data["image_data"]}
                    self.consumable_image_button.text = image_data["image_name"]
                    self.image_display.src_base64 = base64.b64encode(image_data["image_data"]).decode('utf-8')
                cursor.execute("SELECT bill_name, bill_data FROM consumable_bills WHERE consumable_id = %s", (self.consumable_id,))
                bill_data = cursor.fetchone()
                if bill_data:
                    self.attached_bill = {"name": bill_data["bill_name"], "data": bill_data["bill_data"]}
                    self.bill_image_button.text = bill_data["bill_name"]
                    self.bill_display.src_base64 = base64.b64encode(bill_data["bill_data"]).decode('utf-8')
                self.update_existing_info(None)
        except Error as e:
            self.show_snack_bar(f"Error loading consumable: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_consumable_image(self, event):
        if not event.files:
            return
        file = event.files[0]
        self.attached_image = {"name": file.name, "data": b""}
        if file.size > 5 * 1024 * 1024:  # 5MB limit
            self.show_snack_bar("Image file too large (max 5MB).", ft.Colors.RED_800)
            return
        if self.page.web:
            try:
                self.attached_image["data"] = file.read_file()
                self.image_display.src_base64 = base64.b64encode(self.attached_image["data"]).decode('utf-8')
                self.image_warning_text.value = "Image selected successfully."
            except AttributeError:
                self.image_warning_text.value = "Web mode requires temporary upload. Initiating upload..."
                upload_file = ft.FilePickerUploadFile(name=file.name, upload_url=self.page.get_upload_url(file.name, 600))
                self.consumable_image.upload([upload_file])
            except Exception as ex:
                self.image_warning_text.value = f"Error reading file: {ex}"
        else:
            try:
                with open(file.path, "rb") as f:
                    self.attached_image["data"] = f.read()
                self.image_display.src_base64 = base64.b64encode(self.attached_image["data"]).decode('utf-8')
                self.image_warning_text.value = "Image selected successfully."
            except Exception as ex:
                self.image_warning_text.value = f"Error reading file: {ex}"
        self.consumable_image_button.text = file.name
        self.image_display.update()
        self.image_warning_text.update()
        self.page.update()

    def handle_bill_image(self, event):
        if not event.files:
            return
        file = event.files[0]
        self.attached_bill = {"name": file.name, "data": b""}
        if file.size > 5 * 1024 * 1024:  # 5MB limit
            self.show_snack_bar("Bill file too large (max 5MB).", ft.Colors.RED_800)
            return
        if self.page.web:
            try:
                self.attached_bill["data"] = file.read_file()
                self.bill_display.src_base64 = base64.b64encode(self.attached_bill["data"]).decode('utf-8')
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
                    self.attached_bill["data"] = f.read()
                self.bill_display.src_base64 = base64.b64encode(self.attached_bill["data"]).decode('utf-8')
                self.bill_warning_text.value = "Bill selected successfully."
            except Exception as ex:
                self.bill_warning_text.value = f"Error reading file: {ex}"
        self.bill_image_button.text = file.name
        self.bill_display.update()
        self.bill_warning_text.update()
        self.page.update()

    def handle_consumable_image_upload(self, e: ft.FilePickerUploadEvent):
        print(f"Upload event: file={e.file_name}, progress={e.progress}, error={e.error}")
        if e.progress == 1:
            upload_path = os.path.join(self.TEMP_DIR, e.file_name)
            if not os.path.exists(upload_path) and hasattr(self.page, 'upload_dir'):
                upload_path = os.path.join(self.page.upload_dir, e.file_name)
            if not os.path.exists(upload_path):
                self.image_warning_text.value = f"Uploaded file {e.file_name} not found"
                self.page.update()
                return
            try:
                with open(upload_path, "rb") as f:
                    file_data = f.read()
                if len(file_data) > 5 * 1024 * 1024:  # 5MB limit
                    self.image_warning_text.value = f"File {e.file_name} exceeds the maximum size of 5 MB."
                    self.show_snack_bar("Image file too large (max 5MB).", ft.Colors.RED_800)
                else:
                    if self.attached_image and self.attached_image["name"] == e.file_name:
                        self.attached_image["data"] = file_data
                        self.image_display.src_base64 = base64.b64encode(file_data).decode('utf-8')
                        self.image_warning_text.value = "Image uploaded successfully."
                os.remove(upload_path)
                print(f"Deleted temporary file: {upload_path}")
            except Exception as ex:
                self.image_warning_text.value = f"Error reading uploaded file {e.file_name}: {ex}"
                self.show_snack_bar(f"Error uploading image: {ex}", ft.Colors.RED_800)
            self.image_display.update()
            self.image_warning_text.update()
            self.page.update()
        elif e.error:
            self.image_warning_text.value = f"Upload error for {e.file_name}: {e.error}"
            self.show_snack_bar(f"Upload error: {e.error}", ft.Colors.RED_800)
            self.page.update()

    def handle_bill_image_upload(self, e: ft.FilePickerUploadEvent):
        print(f"Upload event: file={e.file_name}, progress={e.progress}, error={e.error}")
        if e.progress == 1:
            upload_path = os.path.join(self.TEMP_DIR, e.file_name)
            if not os.path.exists(upload_path) and hasattr(self.page, 'upload_dir'):
                upload_path = os.path.join(self.page.upload_dir, e.file_name)
            if not os.path.exists(upload_path):
                self.bill_warning_text.value = f"Uploaded file {e.file_name} not found"
                self.page.update()
                return
            try:
                with open(upload_path, "rb") as f:
                    file_data = f.read()
                if len(file_data) > 5 * 1024 * 1024:  # 5MB limit
                    self.bill_warning_text.value = f"File {e.file_name} exceeds the maximum size of 5 MB."
                    self.show_snack_bar("Bill file too large (max 5MB).", ft.Colors.RED_800)
                else:
                    if self.attached_bill and self.attached_bill["name"] == e.file_name:
                        self.attached_bill["data"] = file_data
                        self.bill_display.src_base64 = base64.b64encode(file_data).decode('utf-8')
                        self.bill_warning_text.value = "Bill uploaded successfully."
                os.remove(upload_path)
                print(f"Deleted temporary file: {upload_path}")
            except Exception as ex:
                self.bill_warning_text.value = f"Error reading uploaded file {e.file_name}: {ex}"
                self.show_snack_bar(f"Error uploading bill: {ex}", ft.Colors.RED_800)
            self.bill_display.update()
            self.bill_warning_text.update()
            self.page.update()
        elif e.error:
            self.bill_warning_text.value = f"Upload error for {e.file_name}: {e.error}"
            self.show_snack_bar(f"Upload error: {e.error}", ft.Colors.RED_800)
            self.page.update()

    def open_date_picker(self, e):
        self.purchase_date.open = True
        self.page.update()

    def update_purchase_date(self, e):
        if self.purchase_date.value:
            self.purchase_date_button.text = self.purchase_date.value.strftime("%Y-%m-%d")
        else:
            self.purchase_date_button.text = "Purchase Date"
        self.page.update()

    def toggle_fields(self, e):
        status = self.consumable_status.value
        self.select_printer.visible = status == "Deployed"
        self.consumed_by.visible = status == "Consumed"
        self.page.update()

    def update_existing_info(self, e):
        cartridge_id = self.select_cartridge.value
        if not cartridge_id:
            self.page.update()
            return
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT available_quantity, location
                FROM consumables
                WHERE cartridge_id = %s AND status = 'Available' LIMIT 1
            """, (cartridge_id,))
            result = cursor.fetchone()
            if result:
                qty, loc = result
                self.consumable_qty.value = str(qty)
                self.consumable_location.value = loc
            self.page.update()
        except Error as e:
            self.show_snack_bar(f"Error fetching info: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def save_consumable(self, e):
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cartridge_id = self.select_cartridge.value
            qty = int(self.consumable_qty.value) if self.consumable_qty.value.isdigit() else 0
            location = self.consumable_location.value
            purchase_date = self.purchase_date_button.text if self.purchase_date_button.text != "Purchase Date" else None
            status = self.consumable_status.value
            deployed_to = self.select_printer.value if status == "Deployed" and self.select_printer.value else None
            consumed_by = self.consumed_by.value if status == "Consumed" else None
            if not all([cartridge_id, qty, location, purchase_date]):
                raise ValueError("Please fill all required fields.")
            if status == "Deployed" and not deployed_to:
                raise ValueError("Please select a printer for deployment.")
            if status == "Consumed" and not consumed_by:
                raise ValueError("Please provide a user who consumed the cartridge.")
            cursor.execute("SELECT cartridge_no, company FROM cartridges WHERE id = %s", (cartridge_id,))
            result = cursor.fetchone()
            cartridge_no, company = result[0], result[1] if result else (None, None)
            if not cartridge_no:
                raise ValueError("Invalid cartridge selected.")
            deployed_on = datetime.now().strftime("%Y-%m-%d") if status == "Deployed" else None
            consumption_date = datetime.now().strftime("%Y-%m-%d") if status == "Consumed" else None
            if self.consumable_id:
                cursor.execute(
                    """
                    UPDATE consumables 
                    SET cartridge_no = %s, company = %s, location = %s, purchase_date = %s, 
                        available_quantity = %s, status = %s, cartridge_id = %s, deployed_to = %s,
                        deployed_on = %s, consumed_by = %s, consumption_date = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (cartridge_no, company, location, purchase_date, qty, status, cartridge_id,
                     deployed_to, deployed_on, consumed_by, consumption_date, self.consumable_id)
                )
                consumable_id = self.consumable_id
            else:
                cursor.execute(
                    """
                    INSERT INTO consumables (cartridge_no, company, location, purchase_date, available_quantity,
                                            status, cartridge_id, deployed_to, deployed_on, consumed_by, consumption_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (cartridge_no, company, location, purchase_date, qty, status, cartridge_id,
                     deployed_to, deployed_on, consumed_by, consumption_date)
                )
                consumable_id = cursor.lastrowid
            if self.attached_image and self.attached_image["data"]:
                cursor.execute("DELETE FROM consumable_images WHERE consumable_id = %s", (consumable_id,))
                cursor.execute(
                    """
                    INSERT INTO consumable_images (consumable_id, image_name, image_data)
                    VALUES (%s, %s, %s)
                    """,
                    (consumable_id, self.attached_image["name"], self.attached_image["data"])
                )
            if self.attached_bill and self.attached_bill["data"]:
                cursor.execute("DELETE FROM consumable_bills WHERE consumable_id = %s", (consumable_id,))
                cursor.execute(
                    """
                    INSERT INTO consumable_bills (consumable_id, bill_name, bill_data)
                    VALUES (%s, %s, %s)
                    """,
                    (consumable_id, self.attached_bill["name"], self.attached_bill["data"])
                )
            if status == "Deployed" and deployed_to:
                cursor.execute("UPDATE printers SET cartridge_no = %s WHERE id = %s", (cartridge_no, deployed_to))
            elif status in ["Available", "Consumed"] and self.consumable_id:
                cursor.execute("UPDATE printers SET cartridge_no = NULL WHERE id = (SELECT deployed_to FROM consumables WHERE id = %s)", (self.consumable_id,))
            cursor.execute(
                """
                INSERT INTO asset_history (table_type, entity_id, data_json, action)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    'consumables',
                    consumable_id,
                    f'{{"cartridge_no":"{cartridge_no}", "status":"{status}", "printer_id":"{deployed_to or ''}"}}',
                    'Updated' if self.consumable_id else 'Added'
                )
            )
            conn.commit()
            self.show_snack_bar("Consumable saved successfully!", ft.Colors.GREEN_800)
            self.clear_dialog_fields()
            self.close_dialog(None)
            if self.on_save_callback:
                self.on_save_callback()
        except (Error, ValueError) as e:
            self.show_snack_bar(f"Error saving consumable: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def close_dialog(self, e):
        self.dialog.open = False
        self.clear_dialog_fields()
        self.page.update()

    def clear_dialog_fields(self):
        self.select_cartridge.value = None
        self.consumable_qty.value = "1"
        self.consumable_location.value = "Warehouse"
        self.consumable_image_button.text = "Select Image"
        self.attached_image = None
        self.bill_image_button.text = "Select Bill Image"
        self.attached_bill = None
        self.purchase_date_button.text = "Purchase Date"
        self.purchase_date.value = None
        self.consumable_status.value = "Available"
        self.select_printer.value = None
        self.select_printer.visible = False
        self.consumed_by.value = ""
        self.consumed_by.visible = False
        self.image_display.src_base64 = None
        self.bill_display.src_base64 = None
        self.image_warning_text.value = ""
        self.bill_warning_text.value = ""
        self.page.update()

    def show_snack_bar(self, message, color=ft.Colors.BLACK):
        self.snack_bar.content.value = message
        self.snack_bar.bgcolor = color
        self.snack_bar.open = True
        self.page.update()
