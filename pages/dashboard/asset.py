import os
os.environ["FLET_SECRET_KEY"] = "mysecret123"
import flet as ft
import mysql.connector
from mysql.connector import Error
import base64
from components.assetformpage import AssetFormPage
from components.assetformmanage import AssetFormManage

class AssetPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self.page.title = "Asset Management"
        self.page.window_title = "Asset Management"

        self.expand = True
        self.asset_add = []

        # Initialize dialogs with self as parent
        self.add_asset_dialog = AssetFormPage(page, self)
        self.manage_asset_dialog = AssetFormManage(page, self)

        self.add_asset_button = ft.ElevatedButton(
            text="Add Asset",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.BLUE_300,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.add_asset_dialog.open_dialog()
        )

        # Initialize tabs before loading assets
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[],  # Start with empty tabs; will be populated by load_assets
            expand=True
        )

        # Load initial assets
        self.load_assets()

        self.content = ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.Colors.WHITE),
                ft.Row(
                    controls=[
                        ft.Text("Asset Management", size=24, weight=ft.FontWeight.BOLD, color="#263238"),
                        self.add_asset_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                self.tabs,
            ],
            expand=True,
            spacing=10
        )

        # Defer page update to ensure all controls are initialized
        self.page.add(self)
        self.page.update()

    def load_assets(self):
        """Reload asset data from the database and update the UI."""
        self.asset_add = []
        db_config = {
            "host": "200.200.200.23",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM assets")
            assets = cursor.fetchall()

            for asset in assets:
                cursor.execute("SELECT image_data FROM asset_images WHERE asset_id = %s", (asset['id'],))
                image_result = cursor.fetchone()
                if image_result and image_result['image_data']:
                    asset['image_base64'] = base64.b64encode(image_result['image_data']).decode('utf-8')
                else:
                    asset['image_base64'] = None
                self.asset_add.append(asset)

        except Error as e:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error fetching assets: {e}"),
                duration=4000
            )
            self.page.snack_bar.open = True
            self.page.update()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

        # Update tabs after loading assets
        self.tabs.tabs = self.create_tabs()
        self.page.update()

    def create_tabs(self):
        """Create tabs based on asset status."""
        available_assets = [a for a in self.asset_add if a['status'].lower() == 'available']
        deployed_assets = [a for a in self.asset_add if a['status'].lower() == 'deployed']
        disposed_sold_assets = [a for a in self.asset_add if a['status'].lower() in ['dispose', 'sold']]

        available_row = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_asset_card(asset, "Available"),
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    padding=ft.padding.all(10),
                )
                for asset in available_assets
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            run_spacing=10,
        )

        deployed_row = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_asset_card(asset, "Deployed"),
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    padding=ft.padding.all(10),
                )
                for asset in deployed_assets
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            run_spacing=10,
        )

        disposed_sold_row = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_asset_card(asset, "Disposed/Sold"),
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    padding=ft.padding.all(10),
                )
                for asset in disposed_sold_assets
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            run_spacing=10,
        )

        return [
            ft.Tab(
                text="Available",
                icon=ft.Icons.PIE_CHART,
                content=ft.Column(
                    controls=[
                        available_row if available_assets else
                        ft.Text("No available assets found.", size=20, color=ft.Colors.RED_300)
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            ),
            ft.Tab(
                text="Deployed",
                icon=ft.Icons.DEVICE_HUB,
                content=ft.Column(
                    controls=[
                        deployed_row if deployed_assets else
                        ft.Text("No deployed assets found.", size=20, color=ft.Colors.RED_300)
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            ),
            ft.Tab(
                text="Disposed/Sold",
                icon=ft.Icons.DELETE,
                content=ft.Column(
                    controls=[
                        disposed_sold_row if disposed_sold_assets else
                        ft.Text("No disposed or sold assets found.", size=20, color=ft.Colors.RED_300)
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            )
        ]

    def show_asset_detail(self, asset):
        """Display asset details in an AlertDialog."""
        image_content = (
            ft.Image(
                src_base64=asset.get('image_base64'),
                width=200,
                height=200,
                fit=ft.ImageFit.CONTAIN,
            ) if asset.get('image_base64') else
            ft.Container(
                content=ft.Text("No image available", size=16, color=ft.Colors.GREY_400),
                width=200,
                height=200,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.GREY_100,
            )
        )

        dialog_content = ft.Column(
            controls=[
                image_content,
                ft.Text(f"Model: {asset['model']}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Serial Number: {asset['serial_number']}", size=14),
                ft.Text(f"Company: {asset['company']}", size=14),
                ft.Text(f"Location: {asset['location']}", size=14),
                ft.Text(f"Status: {asset['status']}", size=14),
                ft.Text(f"Deployed Type: {asset.get('deployed_type', 'N/A')}", size=14),
                ft.Text(f"Deployed User: {asset.get('deployed_user_id', 'N/A')}", size=14),
                ft.Text(f"Deployed Department: {asset.get('deployed_department_id', 'N/A')}", size=14),
                ft.Text(f"Deployed On: {asset.get('deployed_on', 'N/A')}", size=14),
                ft.Text(f"Disposed Type: {asset.get('disposed_type', 'N/A')}", size=14),
                ft.Text(f"Disposed Reason: {asset.get('disposed_reason', 'N/A')}", size=14),
                ft.Text(f"Sold To: {asset.get('sold_to', 'N/A')}", size=14),
                ft.Text(f"Sold Price: {asset.get('sold_price', 'N/A')}", size=14),
                ft.Text(f"Disposed On: {asset.get('disposed_on', 'N/A')}", size=14),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        dialog = ft.AlertDialog(
            title=ft.Text(f"Details for {asset['model']} ({asset['serial_number']})", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=dialog_content,
                padding=10,
                width=300,
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: self.close_asset_detail_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def create_asset_card(self, asset, card_type):
        status_Colors = {
            'available': ft.Colors.LIGHT_GREEN_ACCENT_400,
            'deployed': ft.Colors.YELLOW_ACCENT_400,
            'dispose': ft.Colors.RED_400,
            'sold': ft.Colors.RED_400
        }
        status_color = status_Colors.get(asset['status'].lower(), ft.Colors.GREY_400)

        card_height = 400
        image_height = card_height / 3

        image_content = (
            ft.Image(
                src_base64=asset.get('image_base64'),
                width=270,
                height=image_height,
                fit=ft.ImageFit.COVER,
            ) if asset.get('image_base64') else
            ft.Container(
                content=ft.Icon(
                    ft.Icons.IMAGE_NOT_SUPPORTED,
                    size=50,
                    color=ft.Colors.GREY_400
                ),
                width=270,
                height=image_height,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.GREY_100,
            )
        )

        additional_content = []
        if card_type.lower() == 'available':
            additional_content = [
                ft.Text(f"Serial: {asset['serial_number']}", size=14, color="#263238"),
                ft.Text(f"Company: {asset['company']}", size=14, color="#263238"),
                ft.Text(f"Location: {asset['location']}", size=14, color="#263238"),
            ]
        elif card_type.lower() == 'deployed':
            additional_content = [
                ft.Text(f"Serial: {asset['serial_number']}", size=14, color="#263238"),
                ft.Text(f"Company: {asset['company']}", size=14, color="#263238"),
                ft.Text(f"Deployed To: {asset.get('deployed_user_id', 'N/A') if asset.get('deployed_type') == 'User' else asset.get('deployed_department_id', 'N/A')}", size=14, color="#263238"),
                ft.Text(f"Deployed On: {asset.get('deployed_on', 'N/A')}", size=14, color="#263238"),
            ]
        elif card_type.lower() == 'disposed/sold':
            if asset['status'].lower() == 'dispose':
                additional_content = [
                    ft.Text(f"Serial: {asset['serial_number']}", size=14, color="#263238"),
                    ft.Text(f"Disposed Reason: {asset.get('disposed_reason', 'N/A')}", size=14, color="#263238"),
                    ft.Text(f"Disposed On: {asset.get('disposed_on', 'N/A')}", size=14, color="#263238"),
                ]
            elif asset['status'].lower() == 'sold':
                additional_content = [
                    ft.Text(f"Serial: {asset['serial_number']}", size=14, color="#263238"),
                    ft.Text(f"Sold To: {asset.get('sold_to', 'N/A')}", size=14, color="#263238"),
                    ft.Text(f"Sold Price: {asset.get('sold_price', 'N/A')}", size=14, color="#263238"),
                    ft.Text(f"Disposed On: {asset.get('disposed_on', 'N/A')}", size=14, color="#263238"),
                ]

        card_content = [
            ft.Row(
                controls=[
                    ft.Text(
                        f"Model: {asset['model']}",
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        color="#263238"
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
                                ft.Text(asset["status"], color=ft.Colors.BLACK)
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
                width=100,
                on_click=lambda e, sn=asset['serial_number']: self.manage_asset_dialog.open(sn)
            )
        ]

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=card_content,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=15,
                bgcolor="#E3F2FD",
                border_radius=12,
                ink=True,
                on_click=lambda e: self.show_asset_detail(asset),
                width=300,
                height=card_height
            ),
            elevation=5
        )

    def close_asset_detail_dialog(self):
        """Close the asset detail dialog."""
        self.page.dialog.open = False
        self.page.update()