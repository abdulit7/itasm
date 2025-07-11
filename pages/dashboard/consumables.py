import flet as ft
import mysql.connector
from mysql.connector import Error
import base64
from datetime import datetime

class Consumables(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "Consumables Management"
        self.page.window_title = "Consumables Management"
        self.expand = True
        self.padding = ft.padding.all(20)
        self.consumables_list = []

        # Initialize snackbar and dialog
        self.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)
        self.dialog = ft.AlertDialog(
            modal=True,
            
            title=ft.Text(""),
            content=ft.Column(controls=[], spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            content_padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.overlay.extend([self.snack_bar, self.dialog])

        # Initialize form fields for deploy/consume dialogs
        self.qty_field = ft.TextField(
            label="Quantity to Deploy",
            keyboard_type=ft.KeyboardType.NUMBER,
            value="1",
            border_color=ft.Colors.BLUE_200
        )
        self.printer_dropdown = ft.Dropdown(
            label="Select Printer",
            border_color=ft.Colors.BLUE_200
        )
        self.description_field = ft.TextField(
            label="Description",
            multiline=True,
            hint_text="Enter reason or description for consumption",
            border_color=ft.Colors.RED_200
        )

        # Initialize UI
        self.add_button = ft.ElevatedButton(
            "Add Consumable",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.TEAL_600,
            color=ft.Colors.WHITE,
            elevation=4,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                overlay_color=ft.Colors.TEAL_700
            ),
            width=160,
            height=50,
            on_click=self.show_add_form
        )
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[],
            expand=True
        )

        self.refresh_page()

    def refresh_page(self):
        """Reload data and rebuild page content."""
        self.load_consumables()
        self.tabs.tabs = self.build_tabs()
        self.content = ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Row(
                    controls=[
                        ft.Text("Consumables", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        self.add_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                self.tabs
            ],
            expand=True,
            spacing=10
        )
        self.page.update()

    def load_consumables(self):
        self.consumables_list = []
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT cs.*, p.model AS printer_model, c.printer_model AS model
                FROM consumables cs
                LEFT JOIN printers p ON cs.deployed_to = p.id
                LEFT JOIN cartridges c ON cs.cartridge_id = c.id
            """)
            for consumable in cursor.fetchall():
                cursor.execute("SELECT image_data FROM consumable_images WHERE consumable_id = %s LIMIT 1", (consumable['id'],))
                image_data = cursor.fetchone()
                consumable['image_base64'] = base64.b64encode(image_data['image_data']).decode('utf-8') if image_data and image_data['image_data'] else None
                self.consumables_list.append(consumable)
        except Error as e:
            self.show_snack_bar(f"Error fetching consumables: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def build_tabs(self):
        available = [c for c in self.consumables_list if c['status'] == 'Available']
        deployed = [c for c in self.consumables_list if c['status'] == 'Deployed']
        consumed = [c for c in self.consumables_list if c['status'] == 'Consumed']
        return [
            ft.Tab(
                text="Available",
                icon=ft.Icons.PIE_CHART,
                content=self._build_tab_content(available, "No available consumables found.")
            ),
            ft.Tab(
                text="Deployed",
                icon=ft.Icons.DEVICE_HUB,
                content=self._build_tab_content(deployed, "No deployed consumables found.")
            ),
            ft.Tab(
                text="Consumed",
                icon=ft.Icons.DELETE,
                content=self._build_tab_content(consumed, "No consumed consumables found.")
            )
        ]

    def _build_tab_content(self, items, no_items_message):
        if not items:
            return ft.Column(
                controls=[ft.Text(no_items_message, size=20, color=ft.Colors.RED_300)],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )
        return ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=self.create_card(c, c['status'].lower()),
                            col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                            padding=ft.padding.all(10)
                        ) for c in items
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                    run_spacing=10
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

    def create_card(self, consumable, card_type):
        status_Colors = {
            'available': ft.Colors.LIGHT_GREEN_ACCENT_400,
            'deployed': ft.Colors.YELLOW_ACCENT_400,
            'consumed': ft.Colors.RED_400
        }
        card_height = 400
        image_height = card_height / 3
        image_content = (
            ft.Image(
                src_base64=consumable.get('image_base64'),
                width=270,
                height=image_height,
                fit=ft.ImageFit.COVER
            ) if consumable.get('image_base64') else
            ft.Container(
                content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=50, color=ft.Colors.GREY_400),
                width=270,
                height=image_height,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.GREY_100
            )
        )
        additional_content = []
        if card_type == "available":
            additional_content = [
                ft.Text(f"Company: {consumable['company']}", size=14),
                ft.Text(f"Location: {consumable['location']}", size=14),
                ft.Text(f"Available Quantity: {consumable['available_quantity']}", size=14),
                ft.ElevatedButton(
                    "Deploy",
                    icon=ft.Icons.SEND,
                    bgcolor=ft.Colors.BLUE_300,
                    color=ft.Colors.WHITE,
                    on_click=lambda e, c=consumable: self.show_deploy_dialog(c)
                )
            ]
        elif card_type == "deployed":
            additional_content = [
                ft.Text(f"Company: {consumable['company']}", size=14),
                ft.Text(f"Deployed To: {self.get_printer_serial(consumable['deployed_to']) or 'N/A'}", size=14),
                ft.Text(f"Deployment Date: {consumable['deployed_on'] or 'N/A'}", size=14),
                ft.ElevatedButton(
                    "Consumed",
                    icon=ft.Icons.DELETE,
                    bgcolor=ft.Colors.RED_300,
                    color=ft.Colors.WHITE,
                    on_click=lambda e, c=consumable: self.show_consume_dialog(c)
                )
            ]
        elif card_type == "consumed":
            additional_content = [
                ft.Text(f"Company: {consumable['company']}", size=14),
                ft.Text(f"Consumed By: {consumable['consumed_by'] or 'N/A'}", size=14),
                ft.Text(f"Consumption Date: {consumable['consumption_date'] or 'N/A'}", size=14),
                ft.Text(f"Description: {consumable['description'] or 'N/A'}", size=14)
            ]
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(f"Model: {consumable['model']}", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLUE_900),
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Container(width=15, height=15, bgcolor=status_Colors.get(consumable['status'].lower(), ft.Colors.GREY_400), border_radius=10),
                                            ft.Text(consumable["status"], color=ft.Colors.BLACK)
                                        ],
                                        spacing=5,
                                        alignment=ft.MainAxisAlignment.END
                                    ),
                                    alignment=ft.alignment.center_right
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        image_content,
                        *additional_content
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=15,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=12,
                ink=True,
                width=300,
                height=card_height
            ),
            elevation=5
        )

    def show_add_form(self, e):
        from components.consumeformpage import ConsumableForm
        try:
            self.form = ConsumableForm(self.page, on_save_callback=self.refresh_page)
            self.page.dialog = self.form.dialog
            self.form.dialog.open = True
            self.page.update()
        except Exception as ex:
            self.show_snack_bar(f"Error opening add form: {ex}", ft.Colors.RED_800)

    def show_deploy_dialog(self, consumable):
        self.populate_printers()
        self.dialog.title = ft.Text("Deploy Consumable", color=ft.Colors.BLUE_800)
        self.dialog.content.controls = [
            ft.Text(f"Cartridge No: {consumable['cartridge_no']}"),
            ft.Text(f"Available Quantity: {consumable['available_quantity']}"),
            self.qty_field,
            self.printer_dropdown
        ]
        self.dialog.actions = [
            ft.TextButton("Cancel", on_click=self.close_dialog),
            ft.TextButton("Deploy", on_click=lambda e: self.deploy_consumable(consumable))
        ]
        self.qty_field.value = "1"
        self.printer_dropdown.value = None
        self.dialog.open = True
        self.page.update()

    def show_consume_dialog(self, consumable):
        self.dialog.title = ft.Text("Mark Consumable as Consumed", color=ft.Colors.RED_800)
        self.dialog.content.controls = [
            ft.Text(f"Cartridge No: {consumable['cartridge_no']}"),
            ft.Text(f"Quantity: {consumable['available_quantity']}"),
            self.description_field
        ]
        self.dialog.actions = [
            ft.TextButton("Cancel", on_click=self.close_dialog),
            ft.TextButton("Save", on_click=lambda e: self.consume_consumable(consumable))
        ]
        self.description_field.value = ""
        self.dialog.open = True
        self.page.update()

    def consume_consumable(self, consumable):
        description = self.description_field.value.strip()
        if not description:
            self.show_snack_bar("Please enter a description.", ft.Colors.RED_800)
            return
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT model FROM printers WHERE id = %s", (consumable['deployed_to'],))
            printer = cursor.fetchone()
            printer_model = printer['model'] if printer else None
            if not printer_model:
                self.show_snack_bar("No printer found for this consumable.", ft.Colors.RED_800)
                return
            cursor.execute("""
                UPDATE consumables 
                SET status = 'Consumed', consumed_by = %s, consumption_date = %s, description = %s
                WHERE id = %s AND status = 'Deployed'
            """, (printer_model, datetime.now().strftime('%Y-%m-%d'), description, consumable['id']))
            if cursor.rowcount > 0:
                conn.commit()
                self.show_snack_bar("Consumable marked as consumed successfully!", ft.Colors.GREEN_800)
                self.close_dialog(None)
                self.refresh_page()
            else:
                self.show_snack_bar("Consumable is not in Deployed status.", ft.Colors.RED_800)
        except Error as e:
            self.show_snack_bar(f"Error marking consumable as consumed: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def deploy_consumable(self, consumable):
        try:
            deploy_qty = int(self.qty_field.value)
        except ValueError:
            self.show_snack_bar("Please enter a valid number for quantity.", ft.Colors.RED_800)
            return
        if deploy_qty <= 0 or deploy_qty > consumable['available_quantity']:
            self.show_snack_bar(f"Quantity must be between 1 and {consumable['available_quantity']}.", ft.Colors.RED_800)
            return
        printer_id = self.printer_dropdown.value
        if not printer_id:
            self.show_snack_bar("Please select a printer.", ft.Colors.RED_800)
            return
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                UPDATE consumables 
                SET available_quantity = available_quantity - %s
                WHERE id = %s AND available_quantity >= %s
            """, (deploy_qty, consumable['id'], deploy_qty))
            if cursor.rowcount == 0:
                self.show_snack_bar("Insufficient quantity available to deploy.", ft.Colors.RED_800)
                conn.rollback()
                return
            cursor.execute("""
                INSERT INTO consumables 
                (cartridge_no, company, location, purchase_date, available_quantity, status, cartridge_id, deployed_to, deployed_on)
                VALUES (%s, %s, %s, %s, %s, 'Deployed', %s, %s, %s)
            """, (
                consumable['cartridge_no'],
                consumable['company'],
                consumable['location'],
                consumable['purchase_date'],
                deploy_qty,
                consumable['cartridge_id'],
                printer_id,
                datetime.now().strftime('%Y-%m-%d')
            ))
            cursor.execute("SELECT image_name, image_data FROM consumable_images WHERE consumable_id = %s LIMIT 1", (consumable['id'],))
            image_data = cursor.fetchone()
            if image_data:
                cursor.execute("""
                    INSERT INTO consumable_images (consumable_id, image_name, image_data)
                    VALUES (LAST_INSERT_ID(), %s, %s)
                """, (image_data['image_name'], image_data['image_data']))
            cursor.execute("UPDATE printers SET cartridge_no = %s WHERE id = %s", (consumable['cartridge_no'], printer_id))
            conn.commit()
            self.show_snack_bar(f"Deployed {deploy_qty} consumable(s) successfully!", ft.Colors.GREEN_800)
            self.close_dialog(None)
            self.refresh_page()
        except Error as e:
            self.show_snack_bar(f"Error deploying consumable: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def populate_printers(self):
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, model, location FROM printers")
            printers = cursor.fetchall()
            self.printer_dropdown.options = [
                ft.dropdown.Option(key=str(p['id']), text=f"{p['model']} ({p['location']})") for p in printers
            ]
            self.page.update()
        except Error as e:
            self.show_snack_bar(f"Error fetching printers: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_printer_serial(self, printer_id):
        if not printer_id:
            return None
        db_config = {"host": "200.200.200.23", "user": "root", "password": "Pak@123", "database": "asm_sys"}
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT model FROM printers WHERE id = %s", (printer_id,))
            result = cursor.fetchone()
            return result['model'] if result else None
        except Error:
            return None
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
        self.qty_field.value = "1"
        self.printer_dropdown.value = None
        self.description_field.value = ""
        self.page.update()

    def show_snack_bar(self, message, color=ft.Colors.BLACK):
        self.snack_bar.content.value = message
        self.snack_bar.bgcolor = color
        self.snack_bar.open = True
        self.page.update()