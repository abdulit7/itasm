import flet as ft
import mysql.connector
from mysql.connector import Error
import base64
import json
from datetime import datetime
from components.saleforceform import SaleForceDialog
from components.managesaleforce import ManageSaleDialog

class SaleForce2(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "Device Management"
        self.expand = True
        self.padding = ft.padding.all(20)
        self.devices = []
        self.saleforce_dialog = SaleForceDialog(page)
        self.manage_sale_dialog = ManageSaleDialog(page)

        self.add_device_button = ft.ElevatedButton(
            text="Add Device",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.BLUE_300,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.saleforce_dialog.open()
        )

        self.show_device_detail = ft.AlertDialog(
            modal=True,
            title=ft.Text("Device Details", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
            content=ft.Container(
                content=ft.Text("Device details will be displayed here."),
                padding=20,
                width=300
            ),
            actions=[
                ft.TextButton("Close", on_click=self.close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        )

        self.page.overlay.append(self.show_device_detail)

        # Initialize tabs before load_devices
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[],
            expand=True
        )

        self.content = ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Row(
                    controls=[
                        ft.Text("Device Management", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        self.add_device_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                self.tabs
            ],
            expand=True,
            spacing=10
        )

        # Load devices after tabs initialization
        self.load_devices()

    def load_devices(self):
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
            cursor.execute("""
                SELECT d.*, di.image_name, di.image_data
                FROM devices d
                LEFT JOIN device_images di ON d.id = di.device_id
            """)
            devices = cursor.fetchall()
            self.devices = []
            device_dict = {}
            for device in devices:
                if device['id'] not in device_dict:
                    device_dict[device['id']] = {
                        'id': device['id'],
                        'model': device['model'],
                        'serial_number': device['serial_number'],
                        'company': device['company'],
                        'location': device['location'],
                        'purchase_date': device['purchase_date'],
                        'status': device['status'],
                        'distributor_name': device['distributor_name'],
                        'distributor_location': device['distributor_location'],
                        'device_tag': device['device_tag'],
                        'disposed_reason': device['disposed_reason'],
                        'deployed_on': device['deployed_on'],
                        'image_base64': None
                    }
                if device['image_data']:
                    device_dict[device['id']]['image_base64'] = base64.b64encode(device['image_data']).decode('utf-8')
            self.devices = list(device_dict.values())
            self.update_tabs()
        except Error as e:
            self.show_snack_bar(f"Error fetching devices: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_tabs(self):
        available_devices = [d for d in self.devices if d['status'].lower() == 'available']
        deployed_devices = [d for d in self.devices if d['status'].lower() == 'deployed']
        disposed_devices = [d for d in self.devices if d['status'].lower() == 'disposed']

        self.tabs.tabs = [
            ft.Tab(
                text="Available",
                icon=ft.Icons.DEVICE_HUB,
                content=ft.Column(
                    controls=[
                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(
                                    content=self.create_device_card(device, "available"),
                                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                                    padding=ft.padding.all(10)
                                )
                                for device in available_devices
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10,
                            run_spacing=10
                        ) if available_devices else ft.Text("No Available Devices", size=16, color=ft.Colors.RED_300)
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            ),
            ft.Tab(
                text="Deployed",
                icon=ft.Icons.DEVICE_UNKNOWN,
                content=ft.Column(
                    controls=[
                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(
                                    content=self.create_device_card(device, "deployed"),
                                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                                    padding=ft.padding.all(10)
                                )
                                for device in deployed_devices
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10,
                            run_spacing=10
                        ) if deployed_devices else ft.Text("No Deployed Devices", size=16, color=ft.Colors.RED_300)
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            ),
            ft.Tab(
                text="Disposed",
                icon=ft.Icons.DELETE,
                content=ft.Column(
                    controls=[
                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(
                                    content=self.create_device_card(device, "disposed"),
                                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                                    padding=ft.padding.all(10)
                                )
                                for device in disposed_devices
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10,
                            run_spacing=10
                        ) if disposed_devices else ft.Text("No Disposed Devices", size=16, color=ft.Colors.RED_300)
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            )
        ]
        self.page.update()

    def create_device_card(self, device, card_type):
        status_Colors = {
            "available": ft.Colors.GREEN_300,
            "deployed": ft.Colors.YELLOW_300,
            "disposed": ft.Colors.RED_300
        }
        status_color = status_Colors.get(device['status'].lower(), ft.Colors.GREY_400)

        card_height = 400
        image_height = card_height / 2

        image_content = (
            ft.Image(
                src_base64=device['image_base64'],
                width=270,
                height=image_height,
                fit=ft.ImageFit.COVER
            ) if device.get('image_base64') else
            ft.Container(
                content=ft.Icon(
                    ft.Icons.IMAGE_NOT_SUPPORTED,
                    size=50,
                    color=ft.Colors.GREY_400
                ),
                width=270,
                height=image_height,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.GREY_100
            )
        )

        additional_content = []
        if card_type == "available":
            additional_content = [
                ft.Text(f"Serial: {device['serial_number']}", size=14, color=ft.Colors.BLACK),
                ft.Text(f"Company: {device['company']}", size=14, color=ft.Colors.BLACK),
                ft.Text(f"Location: {device['location']}", size=14, color=ft.Colors.BLACK)
            ]
        elif card_type == "deployed":
            additional_content = [
                ft.Text(f"Device Tag: {device['device_tag'] or 'N/A'}", size=14, color=ft.Colors.BLACK),
                ft.Text(f"Serial: {device['serial_number']}", size=14, color=ft.Colors.BLACK),
                ft.Text(f"Distributor: {device['distributor_name'] or 'N/A'}", size=14, color=ft.Colors.BLACK),
                ft.Text(f"Location: {device['distributor_location'] or 'N/A'}", size=14, color=ft.Colors.BLACK)
            ]
        elif card_type == "disposed":
            additional_content = [
                ft.Text(f"Serial: {device['serial_number']}", size=14, color=ft.Colors.BLACK),
                ft.Text(f"Reason: {device['disposed_reason'] or 'N/A'}", size=14, color=ft.Colors.BLACK),
                ft.Text(f"Company: {device['company']}", size=14, color=ft.Colors.BLACK),
                ft.Text(f"Location: {device['location']}", size=14, color=ft.Colors.BLACK)
            ]

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"Model: {device['model']}",
                                    weight=ft.FontWeight.BOLD,
                                    size=16,
                                    color=ft.Colors.BLACK
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Container(
                                                width=15,
                                                height=15,
                                                bgcolor=status_color,
                                                border_radius=10
                                            ),
                                            ft.Text(device["status"], color=ft.Colors.BLACK)
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
                        *additional_content,
                        ft.ElevatedButton(
                            text="Manage",
                            icon=ft.Icons.PENDING_ACTIONS,
                            bgcolor=ft.Colors.BLUE_300,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: self.manage_sale_dialog.open(device['serial_number'])
                        )
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=15,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=12,
                ink=True,
                on_click=lambda e: self.show_detail_dialog(device, image_content),
                width=300,
                height=card_height
            ),
            elevation=5
        )

    def show_detail_dialog(self, device, image_content):
        self.show_device_detail.content = ft.Container(
            content=ft.Column(
                controls=[
                    image_content,
                    ft.Text(f"Model: {device['model']}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    ft.Text(f"Serial Number: {device['serial_number']}", size=16, color=ft.Colors.BLACK),
                    ft.Text(f"Company: {device['company']}", size=16, color=ft.Colors.BLACK),
                    ft.Text(f"Location: {device['location']}", size=16, color=ft.Colors.BLACK),
                    ft.Text(f"Status: {device['status']}", size=16, color=ft.Colors.BLACK),
                    ft.Text(f"Device Tag: {device['device_tag'] or 'N/A'}", size=16, color=ft.Colors.BLACK),
                    ft.Text(f"Distributor: {device['distributor_name'] or 'N/A'}", size=16, color=ft.Colors.BLACK),
                    ft.Text(f"Distributor Location: {device['distributor_location'] or 'N/A'}", size=16, color=ft.Colors.BLACK),
                    ft.Text(f"Deployed On: {device['deployed_on'] or 'N/A'}", size=16, color=ft.Colors.BLACK)
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=20,
            width=300
        )
        self.show_device_detail.open = True
        self.page.update()

    def close_dialog(self, e):
        self.show_device_detail.open = False
        self.page.update()

    def show_snack_bar(self, message, color=ft.Colors.BLACK):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            duration=4000
        )
        self.page.snack_bar.open = True
        self.page.update()