import flet as ft
import mysql.connector
from mysql.connector import Error
import base64
from components.componentdialog import ComponentDialog
from components.compoenentmanage import ComponentManage  # Fixed typo

class Component(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "Components"
        self.expand = True
        self.components_add = []

        # Initialize dialogs
        self.add_component_dialog = ComponentDialog(self.page, parent=self)
        self.manage_component_dialog = ComponentManage(self.page, parent=self)  # Added parent=self

        # Database configuration
        db_config = {
            "host": "200.200.200.23",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }

        # Fetch components
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM components")
            components = cursor.fetchall()

            for component in components:
                cursor.execute("SELECT image_data FROM component_images WHERE component_id = %s", (component['id'],))
                image_result = cursor.fetchone()
                if image_result and image_result['image_data']:
                    image_base64 = base64.b64encode(image_result['image_data']).decode('utf-8')
                    component['image_base64'] = image_base64
                else:
                    component['image_base64'] = None
                self.components_add.append(component)

        except Error as e:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error fetching components: {e}"),
                duration=4000
            )
            self.page.snack_bar.open = True
            self.page.update()
            self.components_add = []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

        # Add Component Button
        self.add_component = ft.ElevatedButton(
            "Add Component",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.BLUE_300,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.add_component_dialog.open_dialog()
        )

        self.component_detail = ft.AlertDialog(
            modal=True,
            title=ft.Text("Component Details"),
            content=ft.Text("Details of the component will be displayed here."),
            actions=[
                ft.TextButton("Close", on_click=lambda e: self.close_component_detail(e))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.BLUE_100,
        )
        self.page.overlay.append(self.component_detail)

        # Create component lists for each tab
        available_components = [c for c in self.components_add if c['status'].lower() == 'available']
        deployed_components = [c for c in self.components_add if c['status'].lower() == 'deployed']
        disposed_components = [c for c in self.components_add if c['status'].lower() == 'disposed']

        # Create ResponsiveRows for each tab
        available_row = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_component_card(component, 'available'),
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    padding=ft.padding.all(10),
                )
                for component in available_components
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            run_spacing=10,
        )

        deployed_row = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_component_card(component, 'deployed'),
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    padding=ft.padding.all(10),
                )
                for component in deployed_components
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            run_spacing=10,
        )

        disposed_row = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_component_card(component, 'disposed'),
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    padding=ft.padding.all(10),
                )
                for component in disposed_components
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            run_spacing=10,
        )

        # Tabs with dynamic content
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Available",
                    icon=ft.Icons.PIE_CHART,
                    content=ft.Column(
                        controls=[
                            available_row if available_components else
                            ft.Text("No available components found.", size=20, color=ft.Colors.RED_300)
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
                            deployed_row if deployed_components else
                            ft.Text("No deployed components found.", size=20, color=ft.Colors.RED_300)
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
                            disposed_row if disposed_components else
                            ft.Text("No disposed components found.", size=20, color=ft.Colors.RED_300)
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    )
                )
            ],
            expand=True
        )

        # Page Layout
        self.content = ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.Colors.WHITE),
                ft.Row(
                    controls=[
                        ft.Text("Device Management", size=24, weight=ft.FontWeight.BOLD, color="#263238"),
                        self.add_component
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                self.tabs,
            ],
            expand=True,
            spacing=10
        )

    def load_components(self):
        """Refresh components from the database."""
        self.components_add = []
        try:
            conn = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="asm_sys"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM components")
            components = cursor.fetchall()

            for component in components:
                cursor.execute("SELECT image_data FROM component_images WHERE component_id = %s", (component['id'],))
                image_result = cursor.fetchone()
                if image_result and image_result['image_data']:
                    image_base64 = base64.b64encode(image_result['image_data']).decode('utf-8')
                    component['image_base64'] = image_base64
                else:
                    component['image_base64'] = None
                self.components_add.append(component)

            # Update tabs
            available_components = [c for c in self.components_add if c['status'].lower() == 'available']
            deployed_components = [c for c in self.components_add if c['status'].lower() == 'deployed']
            disposed_components = [c for c in self.components_add if c['status'].lower() == 'disposed']

            self.tabs.tabs[0].content.controls[0] = ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=self.create_component_card(component, 'available'),
                        col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                        padding=ft.padding.all(10),
                    )
                    for component in available_components
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
                run_spacing=10,
            ) if available_components else ft.Text("No available components found.", size=20, color=ft.Colors.RED_300)

            self.tabs.tabs[1].content.controls[0] = ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=self.create_component_card(component, 'deployed'),
                        col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                        padding=ft.padding.all(10),
                    )
                    for component in deployed_components
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
                run_spacing=10,
            ) if deployed_components else ft.Text("No deployed components found.", size=20, color=ft.Colors.RED_300)

            self.tabs.tabs[2].content.controls[0] = ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=self.create_component_card(component, 'disposed'),
                        col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                        padding=ft.padding.all(10),
                    )
                    for component in disposed_components
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
                run_spacing=10,
            ) if disposed_components else ft.Text("No disposed components found.", size=20, color=ft.Colors.RED_300)

            self.page.update()
        except Error as e:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error refreshing components: {e}"),
                duration=4000
            )
            self.page.snack_bar.open = True
            self.page.update()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def create_component_card(self, component, card_type):
        """Create a card for a component based on its type (available, deployed, disposed)."""
        status_Colors = {
            'available': ft.Colors.LIGHT_GREEN_ACCENT_400,
            'deployed': ft.Colors.YELLOW_ACCENT_400,
            'disposed': ft.Colors.RED_400
        }
        status_color = status_Colors.get(component['status'].lower(), ft.Colors.GREY_400)

        card_height = 400
        image_height = card_height / 3

        image_content = (
            ft.Image(
                src_base64=component['image_base64'],
                width=270,
                height=image_height,
                fit=ft.ImageFit.COVER,
            ) if component.get('image_base64') else
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
        if card_type == 'available':
            additional_content = [
                ft.Text(f"Serial: {component['serial_number']}", size=14, color="#263238"),
                ft.Text(f"Company: {component['company']}", size=14, color="#263238"),
                ft.Text(f"Location: {component['location']}", size=14, color="#263238"),
            ]
        elif card_type == 'deployed':
            additional_content = [
                ft.Text(f"Serial: {component['serial_number']}", size=14, color="#263238"),
                ft.Text(f"Company: {component['company']}", size=14, color="#263238"),
                ft.Text(f"Location: {component['location']}", size=14, color="#263238"),
                ft.Text(f"Deployed On: {component.get('deployed_on', 'N/A')}", size=14, color="#263238"),
            ]
        elif card_type == 'disposed':
            additional_content = [
                ft.Text(f"Serial: {component['serial_number']}", size=14, color="#263238"),
                ft.Text(f"Disposed Reason: {component.get('disposed_reason', 'N/A')}", size=14, color="#263238"),
                ft.Text(f"Disposed On: {component.get('disposed_on', 'N/A')}", size=14, color="#263238"),
            ]

        card_content = [
            ft.Row(
                controls=[
                    ft.Text(
                        f"Model: {component['model']}",
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
                                ft.Text(component["status"], color=ft.Colors.BLACK)
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
                on_click=lambda e, sn=component['serial_number']: self.manage_component_dialog.open_dialog(sn)  # Fixed: open → open_dialog
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
                on_click=lambda e: self.show_component_detail(component, image_content),
                width=300,
                height=card_height
            ),
            elevation=5
        )

    def show_component_detail(self, component, image_content):
        self.component_detail.title = ft.Text(f"Details for {component['model']} ({component['serial_number']})")
        self.component_detail.content = ft.Column(
            controls=[
                ft.Text(f"Model: {component['model']}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Serial Number: {component['serial_number']}"),
                ft.Text(f"Company: {component['company']}"),
                ft.Text(f"Location: {component['location']}"),
                ft.Text(f"Status: {component['status']}"),
                image_content
            ]
        )
        self.component_detail.open = True
        self.page.update()

    def close_component_detail(self, e):
        """Closes the component detail dialog."""
        self.component_detail.open = False
        self.page.update()