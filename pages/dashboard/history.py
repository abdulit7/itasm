import flet as ft
import mysql.connector
from mysql.connector import Error
import json

class HistoryPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self.page.title = "History Management"
        self.page.window_title = "History Management"

        self.expand = True

        self.db_config = {
            "host": "200.200.200.23",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }

        # Fetch history data
        self.history_data = self.fetch_history()

        # Create the DataTable
        self.history_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Table Type")),
                ft.DataColumn(ft.Text("Entity ID")),
                ft.DataColumn(ft.Text("Action")),
                ft.DataColumn(ft.Text("Action Timestamp")),
                ft.DataColumn(ft.Text("Details")),
            ],
            rows=self.create_table_rows(),
            heading_row_color=ft.Colors.BLUE_100,
            data_row_max_height=50,
            column_spacing=20,
            expand=True
        )

        # Main content
        self.content = ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.Colors.WHITE),
                ft.Text("History Management", size=24, weight=ft.FontWeight.BOLD, color="#263238"),
                ft.Container(
                    content=self.history_table,
                    expand=True,
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8
                )
            ],
            expand=True,
            spacing=10
        )

        self.page.add(self)

    def fetch_history(self):
        """Fetch all history records from the asset_history table."""
        history_data = []
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM asset_history ORDER BY action_timestamp DESC")
            history_data = cursor.fetchall()

        except Error as e:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error fetching history: {e}"),
                duration=4000
            )
            self.page.snack_bar.open = True
            self.page.update()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
        return history_data

    def create_table_rows(self):
        """Create rows for the DataTable based on fetched history data."""
        rows = []
        for entry in self.history_data:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(entry['table_type'].capitalize())),
                        ft.DataCell(ft.Text(str(entry['entity_id']))),
                        ft.DataCell(ft.Text(entry['action'])),
                        ft.DataCell(ft.Text(str(entry['action_timestamp']))),
                        ft.DataCell(
                            ft.ElevatedButton(
                                text="View Details",
                                bgcolor=ft.Colors.BLUE_300,
                                color=ft.Colors.WHITE,
                                on_click=lambda e, data=entry['data_json'], entry=entry: self.show_details(data, entry)
                            )
                        ),
                    ]
                )
            )
        return rows

    def show_details(self, data_json, entry):
        """Display the data_json content as an overlay."""
        print(f"show_details called for history_id: {entry['history_id']}")  # Debug log
        try:
            # Parse the JSON data
            data = json.loads(data_json)
            # Create a formatted display of the JSON content
            details_content = []
            for key, value in data.items():
                if value is not None:  # Skip None values for cleaner display
                    details_content.append(
                        ft.Text(f"{key.replace('_', ' ').title()}: {value}", size=14)
                    )

            # Create a Card to display the details
            overlay_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"History Details (ID: {entry['history_id']})",
                                        size=20,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.CLOSE,
                                        on_click=lambda e: self.close_overlay(overlay_card)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Column(
                                controls=details_content,
                                scroll=ft.ScrollMode.AUTO,
                                spacing=5
                            )
                        ],
                        spacing=10
                    ),
                    padding=20,
                    width=400,
                    height=500,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10
                ),
                elevation=10
            )

            # Create a centered overlay with a semi-transparent background
            overlay = ft.Stack(
                controls=[
                    ft.Container(
                        bgcolor=ft.Colors.BLACK54,
                        expand=True,
                        on_click=lambda e: self.close_overlay(overlay_card)
                    ),
                    ft.Container(
                        content=overlay_card,
                        alignment=ft.alignment.center
                    )
                ],
                expand=True
            )

            # Append to page.overlay
            self.page.overlay.append(overlay)
            self.page.update()

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")  # Debug log
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error parsing history details: {e}"),
                duration=4000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            print(f"Unexpected Error: {e}")  # Debug log
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Unexpected error: {e}"),
                duration=4000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def close_overlay(self, overlay_card):
        """Remove the overlay from the page."""
        print("Closing overlay")  # Debug log
        self.page.overlay.remove(overlay_card.parent)  # Remove the Stack containing the Card
        self.page.update()