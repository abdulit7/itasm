# # import os
# # os.environ["FLET_SECRET_KEY"] = "mysecret123"
# # import flet as ft
# # import mysql.connector
# # from mysql.connector import Error
# # import base64

# # class AssetFormPage:
# #     def __init__(self, page: ft.Page, parent=None):
# #         self.page = page
# #         self.parent = parent  # Store the parent (AssetPage) for reload
# #         self.attached_image = None
# #         self.attached_bill = []
# #         self.TEMP_DIR = os.path.join(os.getcwd(), "temp")
# #         os.makedirs(self.TEMP_DIR, exist_ok=True)

# #         # Initialize error and success popups
# #         self.error_popup = ft.AlertDialog(
# #             title=ft.Text("Error"),
# #             content=ft.Text(""),
# #             actions=[ft.TextButton("OK", on_click=self.close_error_popup)]
# #         )
# #         self.success_popup = ft.AlertDialog(
# #             title=ft.Text("Success"),
# #             content=ft.Text(""),
# #             actions=[ft.TextButton("OK", on_click=self.close_success_popup)]
# #         )

# #         # Form fields
# #         self.asset_model = ft.TextField(label="Model", hint_text="Model", icon=ft.Icons.DEVICE_HUB)
# #         self.asset_serial_number = ft.TextField(label="Serial Number", hint_text="Enter Asset Serial Number", icon=ft.Icons.DEVICE_HUB)
# #         self.asset_company = ft.TextField(label="Company Name", hint_text="Enter Company Name", icon=ft.Icons.BUSINESS)
# #         self.asset_location = ft.TextField(label="Location", hint_text="Enter Location", icon=ft.Icons.LOCATION_ON)
# #         self.asset_image = ft.FilePicker(on_result=self.handle_asset_image, on_upload=self.handle_image_upload)
# #         self.asset_image_button = ft.ElevatedButton("Select Image", icon=ft.Icons.IMAGE, on_click=lambda e: self.asset_image.pick_files(allow_multiple=True))
# #         self.image_display = ft.Image(width=150, height=150, fit="contain")
# #         self.warning_text = ft.Text("", color="red")
# #         self.bill_image = ft.FilePicker()
# #         self.asset_bill_button = ft.ElevatedButton("Upload Bill", icon=ft.Icons.ATTACH_FILE, on_click=lambda e: self.bill_image.pick_files(allow_multiple=True))
# #         self.purchase_date_button = ft.ElevatedButton("Purchase Date", icon=ft.Icons.DATE_RANGE, on_click=self.open_date_picker)
# #         self.purchase_date = ft.DatePicker(on_change=self.update_purchase_date)

# #         self.asset_status = ft.Dropdown(
# #             label="Asset Status",
# #             options=[
# #                 ft.dropdown.Option("Available"),
# #                 ft.dropdown.Option("Deployed"),
# #                 ft.dropdown.Option("Disposed/Sold")
# #             ]
# #         )

# #         # Initialize the dialog
# #         self.dialog = ft.AlertDialog(
# #             modal=True,
# #             bgcolor=ft.Colors.RED_100,
# #             title=ft.Text("Add/Edit Asset"),
# #             content=ft.Container(
# #                 width=400,
# #                 height=550,
# #                 content=ft.Column(
# #                     controls=[
# #                         self.asset_model,
# #                         self.asset_serial_number,
# #                         self.asset_company,
# #                         self.asset_location,
# #                         self.asset_image_button,
# #                         self.image_display,
# #                         self.asset_bill_button,
# #                         self.purchase_date_button,
# #                         self.asset_status
# #                     ],
# #                     spacing=10
# #                 ),
# #                 padding=20
# #             ),
# #             actions=[
# #                 ft.TextButton("Cancel", on_click=self.close_dialog),
# #                 ft.TextButton("Save", on_click=self.save_asset)
# #             ],
# #             actions_alignment=ft.MainAxisAlignment.END,
# #         )

# #         # Add overlay components only once during initialization
# #         self.page.overlay.extend([self.error_popup, self.success_popup, self.asset_image, self.bill_image, self.purchase_date, self.dialog])

# #     def open_dialog(self):
# #         """Open the dialog for adding/editing an asset."""
# #         self.dialog.open = True
# #         self.page.update()


# #     def handle_asset_image(self, e:ft.FilePickerResultEvent):
        
# #         self.attached_image = None
# #         self.asset_image_button.text = "Select Image"

# #         if e.files:
# #             self.attached_image = e.files[0]
# #             self.asset_image_button.text = self.attached_image.name
# #             if self.page.web:
# #                 try:
# #                     self.attached_image_bytes = self.attached_image.read_file()
# #                     self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
# #                     self.warning_text.value = "Image selected successfully."

# #                 except AttributeError:
# #                     self.warning_text.value = "Failed to read file. Please try again."
# #                     self.asset_image.upload([ft.FilePickerUploadFile(name=self.attached_image.name, upload_url=(self.attached_image.name, 600) )])

# #                 except Exception as e:
# #                     self.warning_text.value = f"Error reading file: {e}"
# #                     self.attached_image_bytes = b""


# #             else:
# #                 try:
# #                     with open(self.attached_image.path, "rb") as f:
# #                         self.attached_image_bytes = f.read()
# #                         self.image_display.src = f"file://{self.attached_image.path}"
# #                         self.warning_text.value = "Image selected successfully."
# #                 except Exception as e:
# #                     self.warning_text.value = f"Error reading file: {e}"
# #                     self.attached_image_bytes = b""

# #             self.image_display.update()

# #         self.asset_image_button.text = f"{self.attached_image.name} selected." if self.attached_image else "Select Image"
# #         self.warning_text.update()
# #         self.page.update()
    
# #     def handle_image_upload(self, e: ft.FilePickerUploadEvent):
# #         if e.progress == 1:
# #             try:
# #                 upload_path = os.path.join(self.TEMP_DIR, e.file.name)
# #                 with open(upload_path, "wb") as f:
# #                     self.attached_image_bytes = f.read()
# #                     self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
# #                     self.warning_text.value = "Image uploaded successfully."
# #                     try:
# #                         os.remove(upload_path)  # Clean up temporary file
# #                     except Exception as ex:
# #                         self.warning_text.value = f"Error deleting temporary file: {ex}"
# #             except Exception as ex:
# #                 self.warning_text.value = f"Error uploading file: {ex}"
# #                 self.attached_image_bytes = b""
# #             self.image_display.update()
# #             self.warning_text.update()

# #         elif e.error:
# #             self.warning_text.value = f"Error uploading file: {e.error}"
# #             self.attached_image_bytes = b""
# #             self.image_display.update()
# #             self.warning_text.update()











# #     # def handle_asset_image(self, event):
# #     #     if not event.files:
# #     #         return
        
# #     #     self.attached_image = []
# #     #     for file in event.files:
# #     #         file_data = {"name": file.name, "data": b""}
# #     #         if file.path:
# #     #             with open(file.path, "rb") as f:
# #     #                 file_data["data"] = f.read()
# #     #         elif hasattr(file, 'read_bytes'):
# #     #             file_data["data"] = file.read_bytes()

# #     #         if len(file_data["data"]) > 50 * 1024 * 1024:  # 50 MB
# #     #             self.error_popup.content = ft.Text(f"File {file.name} exceeds the maximum size of 50 MB.")
# #     #             self.error_popup.open = True
# #     #             self.page.update()
# #     #             continue

# #     #         self.attached_image.append(file_data)
# #     #     self.asset_image_button.text = f"{len(self.attached_image)} image(s) selected."
# #     #     self.page.update()

      

# #     # def handle_bill_image(self, event):
# #     #     if not event.files:
# #     #         return
        
# #     #     self.attached_bill = []
# #     #     for file in event.files:
# #     #         file_data = {"name": file.name, "data": b""}
# #     #         if file.path:
# #     #             with open(file.path, "rb") as f:
# #     #                 file_data["data"] = f.read()
# #     #         elif hasattr(file, 'read_bytes'):
# #     #             file_data["data"] = file.read_bytes()

# #     #         if len(file_data["data"]) > 50 * 1024 * 1024:  # 50 MB
# #     #             self.error_popup.content = ft.Text(f"File {file.name} exceeds the maximum size of 50 MB.")
# #     #             self.error_popup.open = True
# #     #             self.page.update()
# #     #             continue

# #     #         self.attached_bill.append(file_data)
# #     #     self.asset_bill_button.text = f"{len(self.attached_bill)} bill(s) selected."
# #     #     self.page.update()

# #     def open_date_picker(self, event):
# #         self.purchase_date.open = True
# #         self.page.update()

# #     def update_purchase_date(self, event):
# #         if event.control.value:  # Use event.control.value for DatePicker
# #             self.purchase_date_button.text = f"Purchase Date: {event.control.value.strftime('%Y-%m-%d')}"
# #         else:
# #             self.purchase_date_button.text = "Purchase Date"
# #         self.page.update()

# #     def close_dialog(self, event):
# #         """Close the dialog and reset form fields."""
# #         self.dialog.open = False
# #         # Reset form fields
# #         self.asset_model.value = ""
# #         self.asset_serial_number.value = ""
# #         self.asset_company.value = ""
# #         self.asset_location.value = ""
# #         self.attached_image = None
# #         self.attached_bill = []
# #         self.asset_image_button.text = "Select Image"
# #         self.asset_bill_button.text = "Upload Bill"
# #         self.purchase_date_button.text = "Purchase Date"
# #         self.asset_status.value = "Available"

# #         self.close_success_popup(event)  # Close success popup if open
# #         self.page.update()

# #     def close_error_popup(self, event):
# #         self.error_popup.open = False
# #         self.page.update()

# #     def close_success_popup(self, event):
# #         self.success_popup.open = False
# #         self.dialog.open = False  # Close the dialog when success popup is closed
# #         # Reset form fields
# #         self.asset_model.value = ""
# #         self.asset_serial_number.value = ""
# #         self.asset_company.value = ""
# #         self.asset_location.value = ""
# #         self.attached_image = None
# #         self.attached_bill = []
# #         self.asset_image_button.text = "Select Image"
# #         self.asset_bill_button.text = "Upload Bill"
# #         self.purchase_date_button.text = "Purchase Date"
# #         self.asset_status.value = "Available"
# #         self.page.update()
# #         # Reload assets in the parent AssetPage
# #         if self.parent and hasattr(self.parent, 'load_assets'):
# #             self.parent.load_assets()

# #     def save_asset(self, event):
# #         model = self.asset_model.value
# #         serial_number = self.asset_serial_number.value
# #         company = self.asset_company.value
# #         location = self.asset_location.value
# #         status = self.asset_status.value
# #         purchase_date = self.purchase_date_button.text.replace("Purchase Date: ", "")

# #         if not all([model, serial_number, company, location, purchase_date]) or purchase_date == "Purchase Date":
# #             self.error_popup.content = ft.Text("All fields are required.")
# #             self.error_popup.open = True
# #             self.page.update()
# #             return

# #         db_config = {
# #             "host": "200.200.200.23",
# #             "user": "root",
# #             "password": "Pak@123",
# #             "database": "asm_sys"
# #         }

# #         try:
# #             conn = mysql.connector.connect(**db_config)
# #             cursor = conn.cursor()

# #             # Check if asset already exists
# #             cursor.execute("SELECT id FROM assets WHERE serial_number = %s", (serial_number,))
# #             existing_asset = cursor.fetchone()

# #             if existing_asset:
# #                 cursor.execute("""
# #                     UPDATE assets 
# #                     SET model = %s, company = %s, location = %s, purchase_date = %s, status = %s
# #                     WHERE serial_number = %s
# #                 """, (model, company, location, purchase_date, status, serial_number))
# #             else:
# #                 cursor.execute("""
# #                     INSERT INTO assets (model, serial_number, company, location, purchase_date, status)
# #                     VALUES (%s, %s, %s, %s, %s, %s)
# #                 """, (model, serial_number, company, location, purchase_date, status))
# #                 asset_id = cursor.lastrowid

# #                 # Save images
                
# #                 cursor.execute("""
# #                         INSERT INTO asset_images (asset_id, image_name, image_data)
# #                         VALUES (%s, %s, %s)
# #                     """, (asset_id, self.attached_image.name, self.attached_image_bytes))

# #                 # Save bills
# #                 for bill in self.attached_bill:
# #                     cursor.execute("""
# #                         INSERT INTO asset_bills (asset_id, bill_name, bill_data)
# #                         VALUES (%s, %s, %s)
# #                     """, (asset_id, bill['name'], bill['data']))

# #             conn.commit()
# #             self.success_popup.content = ft.Text("Asset saved successfully!")
# #             self.success_popup.open = True
# #             self.page.update()

# #         except Error as e:
# #             self.error_popup.content = ft.Text(f"Error saving asset: {e}")
# #             self.error_popup.open = True
# #             self.page.update()
# #         finally:
# #             if 'cursor' in locals():
# #                 cursor.close()
# #             if 'conn' in locals():
# #                 conn.close()


# # # import os
# # # os.environ["FLET_SECRET_KEY"] = "mysecret123"
# # # import flet as ft
# # # import base64
# # # import mysql.connector
# # # from flet import FilePicker, FilePickerResultEvent, FilePickerUploadEvent



# # # class AssetFormPage:
# # #     def __init__(self, page: ft.Page, parent=None):
# # #         self.page = page
# # #         self.parent = parent  # Store the parent (AssetPage) for reload
        

# # #         self.TEMP_DIR = os.path.join(os.getcwd(), "temp")
# # #         os.makedirs(self.TEMP_DIR, exist_ok=True)

# # #         self.state = self.ImageState()
# # #         # Initialize error and success popups
# # #         self.error_popup = ft.AlertDialog(
# # #             title=ft.Text("Error"),
# # #             content=ft.Text(""),
# # #             actions=[ft.TextButton("OK", on_click=self.close_error_popup)]
# # #         )
# # #         self.success_popup = ft.AlertDialog(
# # #             title=ft.Text("Success"),
# # #             content=ft.Text(""),
# # #             actions=[ft.TextButton("OK", on_click=self.close_success_popup)]
# # #         )

# # #         # Form fields
# # #         self.asset_model = ft.TextField(label="Model", hint_text="Model", icon=ft.Icons.DEVICE_HUB)
# # #         self.asset_serial_number = ft.TextField(label="Serial Number", hint_text="Enter Asset Serial Number", icon=ft.Icons.DEVICE_HUB)
# # #         self.asset_company = ft.TextField(label="Company Name", hint_text="Enter Company Name", icon=ft.Icons.BUSINESS)
# # #         self.asset_location = ft.TextField(label="Location", hint_text="Enter Location", icon=ft.Icons.LOCATION_ON)
# # #         self.asset_image_picker = ft.FilePicker(on_result=self.handle_asset_image_picker_result, on_upload=self.handle_asset_image_upload)
# # #         self.asset_image_button = ft.ElevatedButton("Select Image", icon=ft.Icons.IMAGE, on_click=lambda e: self.asset_image.pick_files(allow_multiple=True))
# # #         self.bill_image_picker = ft.FilePicker(on_result=self.handle_asset_bill_picker_result, on_upload=self.handle_asset_bill_upload)
# # #         self.asset_bill_button = ft.ElevatedButton("Upload Bill", icon=ft.Icons.ATTACH_FILE, on_click=lambda e: self.bill_image.pick_files(allow_multiple=True))
# # #         self.purchase_date_button = ft.ElevatedButton("Purchase Date", icon=ft.Icons.DATE_RANGE, on_click=self.open_date_picker)
# # #         self.purchase_date = ft.DatePicker(on_change=self.update_purchase_date)

# # #         self.asset_status = ft.Dropdown(
# # #             label="Asset Status",
# # #             options=[
# # #                 ft.dropdown.Option("Available"),
# # #                 ft.dropdown.Option("Deployed"),
# # #                 ft.dropdown.Option("Disposed/Sold")
# # #             ]
# # #         )

# # #         # Initialize the dialog
# # #         self.dialog = ft.AlertDialog(
# # #             modal=True,
# # #             bgcolor=ft.Colors.RED_100,
# # #             title=ft.Text("Add/Edit Asset"),
# # #             content=ft.Container(
# # #                 width=400,
# # #                 height=550,
# # #                 content=ft.Column(
# # #                     controls=[
# # #                         self.asset_model,
# # #                         self.asset_serial_number,
# # #                         self.asset_company,
# # #                         self.asset_location,
# # #                         self.asset_image_button,
# # #                         self.asset_bill_button,
# # #                         self.purchase_date_button,
# # #                         self.asset_status
# # #                     ],
# # #                     spacing=10
# # #                 ),
# # #                 padding=20
# # #             ),
# # #             actions=[
# # #                 ft.TextButton("Cancel", on_click=self.close_dialog),
# # #                 ft.TextButton("Save", on_click=self.save_asset)
# # #             ],
# # #             actions_alignment=ft.MainAxisAlignment.END,
# # #         )

# # #         # Add overlay components only once during initialization
# # #         self.page.overlay.extend([self.error_popup, self.success_popup, self.asset_image_picker, self.bill_image_picker, self.purchase_date, self.dialog])



# # #     def open_dialog(self):
# # #         """Open the dialog for adding/editing an asset."""
# # #         self.dialog.open = True
# # #         self.page.update()

# # #     class ImageState:
# # #         def __init__(self):
# # #             self.image_files = None
# # #             self.bill_files = None

# # #             self.image_bytes = b""
# # #             self.bill_bytes = b""


# # #     def handle_asset_image_picker_result(self, e: FilePickerResultEvent):

# # #         self.asset_image_button.text = "Select Image"
# # #         self.state.image_files = None
# # #         self.state.image_bytes = b""

# # #         if e.files:
# # #             self.state.image_files = e.files[0]
# # #             self.asset_image_button.text = self.state.image_files.name

# # #             if self.page.web:

# # #                 try:
# # #                     self.state.image_bytes = self.state.image_files.read_file()




# import os
# os.environ["FLET_SECRET_KEY"] = "mysecret123"
# import flet as ft
# import mysql.connector
# from mysql.connector import Error
# import base64

# class AssetFormPage:
#     def __init__(self, page: ft.Page, parent=None):
#         if page is None:
#             raise ValueError("Page object must be provided to AssetFormPage")
#         self.page = page
#         self.parent = parent  # Store the parent (AssetPage) for reload
#         self.attached_image = None  # Store as FilePickerFile or bytes
#         self.attached_bill = None  # Store as list of dicts {name, data}
#         self.TEMP_DIR = os.path.join(os.getcwd(), "temp")
#         os.makedirs(self.TEMP_DIR, exist_ok=True)
#         print(f"Initialized TEMP_DIR: {self.TEMP_DIR}, writable: {os.access(self.TEMP_DIR, os.W_OK)}")

#         # Initialize error and success popups
#         self.error_popup = ft.AlertDialog(
#             title=ft.Text("Error"),
#             content=ft.Text(""),
#             actions=[ft.TextButton("OK", on_click=self.close_error_popup)]
#         )
#         self.success_popup = ft.AlertDialog(
#             title=ft.Text("Success"),
#             content=ft.Text(""),
#             actions=[ft.TextButton("OK", on_click=self.close_success_popup)]
#         )

#         # Form fields
#         self.asset_model = ft.TextField(label="Model", hint_text="Model", icon=ft.Icons.DEVICE_HUB)
#         self.asset_serial_number = ft.TextField(label="Serial Number", hint_text="Enter Asset Serial Number", icon=ft.Icons.DEVICE_HUB)
#         self.asset_company = ft.TextField(label="Company Name", hint_text="Enter Company Name", icon=ft.Icons.BUSINESS)
#         self.asset_location = ft.TextField(label="Location", hint_text="Enter Location", icon=ft.Icons.LOCATION_ON)
#         self.asset_image = ft.FilePicker(on_result=self.handle_asset_image, on_upload=self.handle_image_upload)
#         self.asset_image_button = ft.ElevatedButton("Select Image", icon=ft.Icons.IMAGE, on_click=lambda e: self.asset_image.pick_files(allow_multiple=False))
#         self.image_display = ft.Image(width=50, height=50, fit="contain")
#         self.warning_text = ft.Text("", color="red")
#         self.bill_image = ft.FilePicker(on_result=self.handle_bill_image, on_upload=self.handle_bill_upload)
#         self.asset_bill_button = ft.ElevatedButton("Upload Bill", icon=ft.Icons.ATTACH_FILE, on_click=lambda e: self.bill_image.pick_files(allow_multiple=True))
#         self.bill_display = ft.Image(width=50, height=50, fit="contain")
#         self.bill_warning_text = ft.Text("", color="red")
#         self.purchase_date_button = ft.ElevatedButton("Purchase Date", icon=ft.Icons.DATE_RANGE, on_click=self.open_date_picker)
#         self.purchase_date = ft.DatePicker(on_change=self.update_purchase_date)

#         self.asset_status = ft.Dropdown(
#             label="Asset Status",
#             border=ft.InputBorder.UNDERLINE,
#             enable_filter=True,
#             editable=True,
#             leading_icon=ft.Icons.SEARCH,
#             options=[
#                 ft.dropdown.Option("Available"),
#                 ft.dropdown.Option("Deployed"),
#                 ft.dropdown.Option("Disposed/Sold")
#             ]
#         )

#         # Initialize the dialog
#         self.dialog = ft.AlertDialog(
#             modal=True,
#             bgcolor=ft.Colors.RED_100,
#             title=ft.Text("Add/Edit Asset"),
#             content=ft.Container(
#                 width=400,
#                 height=600,
#                 content=ft.Column(
#                     controls=[
#                         self.asset_model,
#                         self.asset_serial_number,
#                         self.asset_company,
#                         self.asset_location,
#                         self.asset_image_button,
#                         self.image_display,
#                         self.warning_text,
#                         self.asset_bill_button,
#                         self.bill_display,
#                         self.bill_warning_text,
#                         self.purchase_date_button,
#                         self.asset_status
#                     ],
#                     spacing=10
#                 ),
#                 padding=20
#             ),
#             actions=[
#                 ft.TextButton("Cancel", on_click=self.close_dialog),
#                 ft.TextButton("Save", on_click=self.save_asset)
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )

#         # Add overlay components only once during initialization
#         self.page.overlay.extend([self.error_popup, self.success_popup, self.asset_image, self.bill_image, self.purchase_date, self.dialog])

#     def open_dialog(self):
#         """Open the dialog for adding/editing an asset."""
#         self.dialog.open = True
#         self.page.update()

#     def handle_asset_image(self, e: ft.FilePickerResultEvent):
#         self.attached_image = None
#         self.asset_image_button.text = "Select Image"
#         self.image_display.src_base64 = None
#         self.warning_text.value = ""

#         if e.files:
#             self.attached_image = e.files[0]
#             self.asset_image_button.text = self.attached_image.name
#             if self.page.web:
#                 try:
#                     self.attached_image_bytes = self.attached_image.read_file()
#                     self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
#                     self.warning_text.value = "Image selected successfully."
#                 except AttributeError:
#                     self.warning_text.value = "Web mode requires temporary upload. Initiating upload..."
#                     upload_file = ft.FilePickerUploadFile(name=self.attached_image.name, upload_url=self.page.get_upload_url(self.attached_image.name, 600))
#                     self.asset_image.upload([upload_file])
#                 except Exception as ex:
#                     self.warning_text.value = f"Error reading file: {ex}"
#                     self.attached_image_bytes = b""
#             else:
#                 try:
#                     with open(self.attached_image.path, "rb") as f:
#                         self.attached_image_bytes = f.read()
#                     self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
#                     self.warning_text.value = "Image selected successfully."
#                 except Exception as ex:
#                     self.warning_text.value = f"Error reading file: {ex}"
#                     self.attached_image_bytes = b""

#             self.image_display.update()
#         self.warning_text.update()
#         self.page.update()
#     def handle_bill_image(self, e: ft.FilePickerResultEvent):
#         self.attached_bill = None
#         self.asset_bill_button.text = "Upload Bill"
#         self.bill_display.src_base64 = None
#         self.bill_warning_text.value = ""
#         if e.files:
#             self.attached_bill = e.files[0]
#             self.asset_bill_button.text = self.attached_bill.name
#             if self.page.web:
#                 try:
#                     self.attached_bill_bytes = self.attached_bill.read_file()
#                     self.bill_display.src_base64 = base64.b64encode(self.attached_bill_bytes).decode('utf-8')
#                     self.bill_warning_text.value = "Bill Selected Successfully."
#                 except AttributeError:
#                     self.bill_warning_text.value = "Web mode requires temporary upload. Initiating upload..."
#                     upload_file = ft.FilePickerUploadFile(name=self.attached_bill.name, upload_url=self.page.get_upload_url(self.attached_bill.name, 600))
#                     self.bill_image.upload([upload_file])
#                 except Exception as ex:
#                     self.bill_warning_text.value = f"Error reading file: {ex}"
#                     self.attached_bill_bytes = b""
#             else:
#                 try:
#                     with open(self.attached_bill.path, "rb") as f:
#                         self.attached_bill_bytes = f.read()
#                     self.bill_display.src_base64 = base64.b64encode(self.attached_bill_bytes).decode('utf-8')
#                     self.bill_warning_text.value = "Bill selected successfully."
#                 except Exception as ex:
#                     self.bill_warning_text.value = f"Error reading file: {ex}"
#                     self.attached_bill_bytes = b""
#             self.bill_display.update()
#         self.bill_warning_text.update()
#         self.page.update()
#     def handle_bill_upload(self, e: ft.FilePickerUploadEvent):
#         if e.progress == 1:
#             upload_path = os.path.join(self.TEMP_DIR, e.file_name)
#             if not os.path.exists(upload_path):
#                 print(f"File not found at {upload_path}. Checking default upload dir...")
#                 default_upload_dir = os.path.join(os.getcwd(), "uploads")
#                 upload_path = os.path.join(default_upload_dir, e.file_name)
#                 if not os.path.exists(upload_path):
#                     self.bill_warning_text.value = f"Uploaded file {e.file_name} not found in {self.TEMP_DIR} or {default_upload_dir}"
#                     self.error_popup.open = True
#                     self.page.update()
#                     return
#             try:
#                 with open(upload_path, "rb") as f:
#                     file_data = f.read()
#                 if len(file_data) > 50 * 1024 * 1024:  # 50 MB
#                     self.bill_warning_text.value = f"File {e.file_name} exceeds the maximum size of 50 MB."
#                     self.error_popup.open = True
#                 else:
#                     if self.attached_bill and self.attached_bill.name == e.file_name:
#                         self.attached_bill_bytes = file_data
#                         self.bill_display.src_base64 = base64.b64encode(file_data).decode('utf-8')
#                         self.bill_warning_text.value = "Bill uploaded successfully."
#                         self.asset_bill_button.text = self.attached_bill.name
#                     else:
#                         self.bill_warning_text.value = f"Bill {e.file_name} uploaded successfully."
#                         self.asset_bill_button.text = f"{len(self.attached_bill)} bill(s) selected."
#                 try:
#                     os.remove(upload_path)
#                     print(f"Deleted temporary file: {upload_path}")
#                 except Exception as ex:
#                     print(f"Error deleting temporary file {upload_path}: {ex}")
#             except Exception as ex:
#                 self.bill_warning_text.value = f"Error reading uploaded file {e.file_name}: {ex}"
#                 self.error_popup.open = True
#             self.bill_display.update() if self.attached_bill and self.attached_bill.name == e.file_name else None
#             self.bill_warning_text.update()
#             self.page.update()
#         elif e.error:
#             self.bill_warning_text.value = f"Upload error for {e.file_name}: {e.error}"
#             self.error_popup.open = True
#             self.page.update()



#     # def handle_bill_image(self, e: ft.FilePickerResultEvent):
#     #     self.attached_bill = []
#     #     self.asset_bill_button.text = "Upload Bill"
#     #     self.warning_text.value = ""

#     #     if e.files:
#     #         for file in e.files:
#     #             file_data = {"name": file.name, "data": b""}
#     #             if self.page.web:
#     #                 try:
#     #                     file_data["data"] = file.read_file()
#     #                     if not file_data["data"]:
#     #                         raise ValueError("Empty bill data")
#     #                 except AttributeError:
#     #                     self.warning_text.value = f"Web mode requires temporary upload for {file.name}. Initiating upload..."
#     #                     upload_file = ft.FilePickerUploadFile(name=file.name, upload_url=self.page.get_upload_url(file.name, 600))
#     #                     self.bill_image.upload([upload_file])
#     #                     continue
#     #                 except Exception as ex:
#     #                     self.warning_text.value = f"Error reading {file.name}: {ex}"
#     #                     continue
#     #             else:
#     #                 try:
#     #                     with open(file.path, "rb") as f:
#     #                         file_data["data"] = f.read()
#     #                 except Exception as ex:
#     #                     self.warning_text.value = f"Error reading {file.name}: {ex}"
#     #                     continue

#     #             if len(file_data["data"]) > 50 * 1024 * 1024:  # 50 MB
#     #                 self.warning_text.value = f"File {file.name} exceeds the maximum size of 50 MB."
#     #                 self.error_popup.open = True
#     #                 continue

#     #             self.attached_bill.append(file_data)
#     #         self.asset_bill_button.text = f"{len(self.attached_bill)} bill(s) selected."
#     #     self.warning_text.update()
#     #     self.page.update()

#     def handle_image_upload(self, e: ft.FilePickerUploadEvent):
#         print(f"Upload event: file={e.file_name}, progress={e.progress}, error={e.error}")
#         if e.progress == 1:
#             # Try the expected TEMP_DIR first
#             upload_path = os.path.join(self.TEMP_DIR, e.file_name)
#             if not os.path.exists(upload_path):
#                 print(f"File not found at {upload_path}. Checking default upload dir...")
#                 # Fallback to Flet's default upload dir (if different)
#                 default_upload_dir = os.path.join(os.getcwd(), "uploads")  # Adjust based on Flet behavior
#                 upload_path = os.path.join(default_upload_dir, e.file_name)
#                 if not os.path.exists(upload_path):
#                     self.warning_text.value = f"Uploaded file {e.file_name} not found in {self.TEMP_DIR} or {default_upload_dir}"
#                     self.error_popup.open = True
#                     self.page.update()
#                     return
#             try:
#                 with open(upload_path, "rb") as f:
#                     file_data = f.read()
#                 if len(file_data) > 50 * 1024 * 1024:  # 50 MB
#                     self.warning_text.value = f"File {e.file_name} exceeds the maximum size of 50 MB."
#                     self.error_popup.open = True
#                 else:
#                     if self.attached_image and self.attached_image.name == e.file_name:
#                         self.attached_image_bytes = file_data
#                         self.image_display.src_base64 = base64.b64encode(file_data).decode('utf-8')
#                         self.warning_text.value = "Image uploaded successfully."
#                         self.asset_image_button.text = self.attached_image.name
#                     else:
#                         for bill in self.attached_bill:
#                             if bill["name"] == e.file_name:
#                                 bill["data"] = file_data
#                                 self.warning_text.value = f"Bill {e.file_name} uploaded successfully."
#                                 self.asset_bill_button.text = f"{len(self.attached_bill)} bill(s) selected."
#                                 break
#                 try:
#                     os.remove(upload_path)
#                     print(f"Deleted temporary file: {upload_path}")
#                 except Exception as ex:
#                     print(f"Error deleting temporary file {upload_path}: {ex}")
#             except Exception as ex:
#                 self.warning_text.value = f"Error reading uploaded file {e.file_name}: {ex}"
#                 self.error_popup.open = True
#             self.image_display.update() if self.attached_image and self.attached_image.name == e.file_name else None
#             self.warning_text.update()
#             self.page.update()
#         elif e.error:
#             self.warning_text.value = f"Upload error for {e.file_name}: {e.error}"
#             self.error_popup.open = True
#             self.page.update()

#     def open_date_picker(self, event):
#         self.purchase_date.open = True
#         self.page.update()

#     def update_purchase_date(self, event):
#         if event.control.value:
#             self.purchase_date_button.text = f"Purchase Date: {event.control.value.strftime('%Y-%m-%d')}"
#         else:
#             self.purchase_date_button.text = "Purchase Date"
#         self.page.update()

#     def close_dialog(self, event):
#         """Close the dialog and reset form fields."""
#         self.dialog.open = False
#         self.asset_model.value = ""
#         self.asset_serial_number.value = ""
#         self.asset_company.value = ""
#         self.asset_location.value = ""
#         self.attached_image = None
#         self.attached_bill = None
#         self.asset_image_button.text = "Select Image"
#         self.asset_bill_button.text = "Upload Bill"
#         self.purchase_date_button.text = "Purchase Date"
#         self.asset_status.value = "Available"
#         self.image_display.src_base64 = None
#         self.warning_text.value = ""
#         self.close_success_popup(event)
#         self.page.update()

#     def close_error_popup(self, event):
#         self.error_popup.open = False
#         self.page.update()

#     def close_success_popup(self, event):
#         self.success_popup.open = False
#         self.dialog.open = False
#         self.asset_model.value = ""
#         self.asset_serial_number.value = ""
#         self.asset_company.value = ""
#         self.asset_location.value = ""
#         self.attached_image = None
#         self.attached_bill = None
#         self.asset_image_button.text = "Select Image"
#         self.asset_bill_button.text = "Upload Bill"
#         self.purchase_date_button.text = "Purchase Date"
#         self.asset_status.value = "Available"
#         self.image_display.src_base64 = None
#         self.bill_display.src_base64 = None
#         self.warning_text.value = ""
#         self.bill_warning_text.value = ""
#         if self.parent and hasattr(self.parent, 'load_assets'):
#             self.parent.load_assets()
#         self.page.update()

#     def save_asset(self, event):
#         model = self.asset_model.value
#         serial_number = self.asset_serial_number.value
#         company = self.asset_company.value
#         location = self.asset_location.value
#         status = self.asset_status.value
#         purchase_date = self.purchase_date_button.text.replace("Purchase Date: ", "")

#         if not all([model, serial_number, company, location, purchase_date]) or purchase_date == "Purchase Date":
#             self.error_popup.content = ft.Text("All fields are required.")
#             self.error_popup.open = True
#             self.page.update()
#             return

#         db_config = {
#             "host": "200.200.200.23",
#             "user": "root",
#             "password": "Pak@123",
#             "database": "asm_sys"
#         }

#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor()

#             cursor.execute("SELECT id FROM assets WHERE serial_number = %s", (serial_number,))
#             existing_asset = cursor.fetchone()

#             if existing_asset:
#                 cursor.execute("""
#                     UPDATE assets 
#                     SET model = %s, company = %s, location = %s, purchase_date = %s, status = %s
#                     WHERE serial_number = %s
#                 """, (model, company, location, purchase_date, status, serial_number))
#             else:
#                 cursor.execute("""
#                     INSERT INTO assets (model, serial_number, company, location, purchase_date, status)
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                 """, (model, serial_number, company, location, purchase_date, status))
#                 asset_id = cursor.lastrowid

#                 if self.attached_image and hasattr(self, 'attached_image_bytes'):
#                     cursor.execute("""
#                         INSERT INTO asset_images (asset_id, image_name, image_data)
#                         VALUES (%s, %s, %s)
#                     """, (asset_id, self.attached_image.name, self.attached_image_bytes))

#                 if self.attached_bill and hasattr(self, 'attached_bill_bytes'):
#                     cursor.execute("""
#                         INSERT INTO asset_bills (asset_id, bill_name, bill_data)
#                         VALUES (%s, %s, %s)
#                     """, (asset_id, self.attached_bill.name, self.attached_bill_bytes))

#             conn.commit()
#             self.success_popup.content = ft.Text("Asset saved successfully!")
#             self.success_popup.open = True
#             self.page.update()

#         except Error as e:
#             self.error_popup.content = ft.Text(f"Error saving asset: {e}")
#             self.error_popup.open = True
#             self.page.update()
#         finally:
#             if 'cursor' in locals():
#                 cursor.close()
#             if 'conn' in locals():
#                 conn.close()



import os
os.environ["FLET_SECRET_KEY"] = "mysecret123"
import flet as ft
import mysql.connector
from mysql.connector import Error
import base64

class AssetFormPage:
    def __init__(self, page: ft.Page, parent=None):
        if page is None:
            raise ValueError("Page object must be provided to AssetFormPage")
        self.page = page
        self.parent = parent
        self.attached_images = []  # Store multiple images
        self.attached_bills = []  # Store multiple bills
        self.TEMP_DIR = os.path.join(os.getcwd(), "temp")
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        print(f"Initialized TEMP_DIR: {self.TEMP_DIR}, writable: {os.access(self.TEMP_DIR, os.W_OK)}")

        self.error_popup = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(""), actions=[ft.TextButton("OK", on_click=self.close_error_popup)])
        self.success_popup = ft.AlertDialog(title=ft.Text("Success"), content=ft.Text(""), actions=[ft.TextButton("OK", on_click=self.close_success_popup)])

        self.asset_model = ft.TextField(label="Model", hint_text="Model", icon=ft.Icons.DEVICE_HUB)
        self.asset_serial_number = ft.TextField(label="Serial Number", hint_text="Enter Asset Serial Number", icon=ft.Icons.DEVICE_HUB)
        self.asset_company = ft.TextField(label="Company Name", hint_text="Enter Company Name", icon=ft.Icons.BUSINESS)
        self.asset_location = ft.TextField(label="Location", hint_text="Enter Location", icon=ft.Icons.LOCATION_ON)
        self.asset_image = ft.FilePicker(on_result=self.handle_asset_image, on_upload=self.handle_image_upload)
        self.asset_image_button = ft.ElevatedButton("Select Image", icon=ft.Icons.IMAGE, on_click=lambda e: self.asset_image.pick_files(allow_multiple=True))
        self.image_display = ft.Image(width=50, height=50, fit="contain")
        self.warning_text = ft.Text("", color="red")
        self.bill_image = ft.FilePicker(on_result=self.handle_bill_image, on_upload=self.handle_bill_upload)
        self.asset_bill_button = ft.ElevatedButton("Upload Bill", icon=ft.Icons.ATTACH_FILE, on_click=lambda e: self.bill_image.pick_files(allow_multiple=True))
        self.bill_display = ft.Image(width=50, height=50, fit="contain")
        self.bill_warning_text = ft.Text("", color="red")
        self.purchase_date_button = ft.ElevatedButton("Purchase Date", icon=ft.Icons.DATE_RANGE, on_click=self.open_date_picker)
        self.purchase_date = ft.DatePicker(on_change=self.update_purchase_date)

        self.asset_status = ft.Dropdown(label="Asset Status", border=ft.InputBorder.UNDERLINE, enable_filter=True, editable=True, leading_icon=ft.Icons.SEARCH,
                                       options=[ft.dropdown.Option("Available"), ft.dropdown.Option("Deployed"), ft.dropdown.Option("Disposed/Sold")])

        self.dialog = ft.AlertDialog(modal=True, bgcolor=ft.Colors.RED_100, title=ft.Text("Add/Edit Asset"),
                                    content=ft.Container(width=400, height=600, content=ft.Column(controls=[
                                        self.asset_model, self.asset_serial_number, self.asset_company, self.asset_location,
                                        self.asset_image_button, self.image_display, self.warning_text,
                                        self.asset_bill_button, self.bill_display, self.bill_warning_text,
                                        self.purchase_date_button, self.asset_status
                                    ], spacing=15,scroll=ft.ScrollMode.AUTO), padding=20),
                                    actions=[ft.TextButton("Cancel", on_click=self.close_dialog), ft.TextButton("Save", on_click=self.save_asset)],
                                    actions_alignment=ft.MainAxisAlignment.END)

        self.page.overlay.extend([self.error_popup, self.success_popup, self.asset_image, self.bill_image, self.purchase_date, self.dialog])

    def open_dialog(self):
        self.dialog.open = True
        self.page.update()

    def handle_asset_image(self, e: ft.FilePickerResultEvent):
        self.attached_images = e.files if e.files else []
        self.asset_image_button.text = f"{len(self.attached_images)} image(s) selected."
        self.image_display.src_base64 = None
        self.warning_text.value = ""
        if self.attached_images:
            file = self.attached_images[0]  # Preview the first image
            if self.page.web:
                try:
                    self.attached_image_bytes = file.read_file()
                    self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
                    self.warning_text.value = "Image selected successfully."
                except AttributeError:
                    self.warning_text.value = "Web mode requires temporary upload. Initiating upload..."
                    upload_file = ft.FilePickerUploadFile(name=file.name, upload_url=self.page.get_upload_url(file.name, 600))
                    self.asset_image.upload([upload_file])
                except Exception as ex:
                    self.warning_text.value = f"Error reading file: {ex}"
            else:
                try:
                    with open(file.path, "rb") as f:
                        self.attached_image_bytes = f.read()
                    self.image_display.src_base64 = base64.b64encode(self.attached_image_bytes).decode('utf-8')
                    self.warning_text.value = "Image selected successfully."
                except Exception as ex:
                    self.warning_text.value = f"Error reading file: {ex}"
            self.image_display.update()
        self.warning_text.update()
        self.page.update()

    def handle_bill_image(self, e: ft.FilePickerResultEvent):
        self.attached_bills = e.files if e.files else []
        self.asset_bill_button.text = f"{len(self.attached_bills)} bill(s) selected."
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
                self.warning_text.value = f"Uploaded file {e.file_name} not found"
                self.error_popup.open = True
                self.page.update()
                return
            try:
                with open(upload_path, "rb") as f:
                    file_data = f.read()
                if len(file_data) > 50 * 1024 * 1024:  # 50 MB
                    self.warning_text.value = f"File {e.file_name} exceeds the maximum size of 50 MB."
                    self.error_popup.open = True
                else:
                    for img in self.attached_images:
                        if img.name == e.file_name:
                            self.attached_image_bytes = file_data
                            self.image_display.src_base64 = base64.b64encode(file_data).decode('utf-8')
                            self.warning_text.value = "Image uploaded successfully."
                            break
                os.remove(upload_path)
                print(f"Deleted temporary file: {upload_path}")
            except Exception as ex:
                self.warning_text.value = f"Error reading uploaded file {e.file_name}: {ex}"
                self.error_popup.open = True
            self.image_display.update()
            self.warning_text.update()
            self.page.update()
        elif e.error:
            self.warning_text.value = f"Upload error for {e.file_name}: {e.error}"
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
        self.asset_model.value = ""
        self.asset_serial_number.value = ""
        self.asset_company.value = ""
        self.asset_location.value = ""
        self.attached_images = []
        self.attached_bills = []
        self.asset_image_button.text = "Select Image"
        self.asset_bill_button.text = "Upload Bill"
        self.purchase_date_button.text = "Purchase Date"
        self.asset_status.value = "Available"
        self.image_display.src_base64 = None
        self.bill_display.src_base64 = None
        self.warning_text.value = ""
        self.bill_warning_text.value = ""
        self.close_success_popup(event)
        self.page.update()

    def close_error_popup(self, event):
        self.error_popup.open = False
        self.page.update()

    def close_success_popup(self, event):
        self.success_popup.open = False
        self.dialog.open = False
        self.asset_model.value = ""
        self.asset_serial_number.value = ""
        self.asset_company.value = ""
        self.asset_location.value = ""
        self.attached_images = []
        self.attached_bills = []
        self.asset_image_button.text = "Select Image"
        self.asset_bill_button.text = "Upload Bill"
        self.purchase_date_button.text = "Purchase Date"
        self.asset_status.value = "Available"
        self.image_display.src_base64 = None
        self.bill_display.src_base64 = None
        self.warning_text.value = ""
        self.bill_warning_text.value = ""
        if self.parent and hasattr(self.parent, 'load_assets'):
            self.parent.load_assets()
        self.page.update()

    def save_asset(self, event):
        model = self.asset_model.value
        serial_number = self.asset_serial_number.value
        company = self.asset_company.value
        location = self.asset_location.value
        status = self.asset_status.value
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

            cursor.execute("SELECT id FROM assets WHERE serial_number = %s", (serial_number,))
            existing_asset = cursor.fetchone()

            if existing_asset:
                cursor.execute("""
                    UPDATE assets 
                    SET model = %s, company = %s, location = %s, purchase_date = %s, status = %s
                    WHERE serial_number = %s
                """, (model, company, location, purchase_date, status, serial_number))
            else:
                cursor.execute("""
                    INSERT INTO assets (model, serial_number, company, location, purchase_date, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (model, serial_number, company, location, purchase_date, status))
                asset_id = cursor.lastrowid

            if self.attached_images and hasattr(self, 'attached_image_bytes'):
                for img in self.attached_images:
                    cursor.execute("""
                        INSERT INTO asset_images (asset_id, image_name, image_data)
                        VALUES (%s, %s, %s)
                    """, (asset_id, img.name, self.attached_image_bytes))
            if self.attached_bills and hasattr(self, 'attached_bill_bytes'):
                for bill in self.attached_bills:
                    cursor.execute("""
                        INSERT INTO asset_bills (asset_id, bill_name, bill_data)
                        VALUES (%s, %s, %s)
                    """, (asset_id, bill.name, self.attached_bill_bytes))

            conn.commit()
            self.success_popup.content = ft.Text("Asset saved successfully!")
            self.success_popup.open = True
            self.page.update()

        except Error as e:
            self.error_popup.content = ft.Text(f"Error saving asset: {e}")
            self.error_popup.open = True
            self.page.update()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
