

import flet as ft
import mysql.connector
from datetime import datetime

class HistoryTable(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.history_data = []
        self.category_map = {}
        
        # Fetch category data for mapping
        self.fetch_categories()
        
        # Fetch history data
        self.fetch_history()
        
        # Create the DataTable
        self.data_table = ft.DataTable(
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            heading_row_color=ft.Colors.BLUE_50,
            heading_row_height=50,
            data_row_color={"hovered": ft.Colors.GREY_100},
            columns=[
                ft.DataColumn(
                    ft.Text("Action", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    tooltip="Type of action performed"
                ),
                ft.DataColumn(
                    ft.Text("Asset Name", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    tooltip="Name of the asset"
                ),
                ft.DataColumn(
                    ft.Text("Category", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    tooltip="Category of the asset"
                ),
                ft.DataColumn(
                    ft.Text("User/Department", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    tooltip="User or Department the asset was deployed to"
                ),
                ft.DataColumn(
                    ft.Text("Date", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    tooltip="Date of the action"
                ),
                ft.DataColumn(
                    ft.Text("Details", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    tooltip="Additional details about the action"
                ),
            ],
            rows=[],
        )
        
        # Populate the table with history data
        self.populate_table()
        
        # Wrap the DataTable in a scrollable container with styling
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Asset History",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK87,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        content=self.data_table,
                        expand=True,
                        border_radius=10,
                        bgcolor=ft.Colors.WHITE,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                        ),
                        padding=10,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_50, ft.Colors.WHITE],
            ),
            border_radius=15,
            padding=10,
            margin=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            ),
            expand=True,
        )

    def fetch_categories(self):
        """Fetch and cache category data."""
        connection = self._get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name FROM category")
                self.category_map = {row[0]: row[1] for row in cursor.fetchall()}
                print(f"Cached categories: {self.category_map}")
            except mysql.connector.Error as err:
                print(f"Error fetching categories: {err}")
                self.show_snackbar(f"Error fetching categories: {err}", ft.Colors.RED_700)
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Database connection closed")

    def _get_db_connection(self):
        """Establish and return a database connection."""
        try:
            connection = mysql.connector.connect(
                host="200.200.201.100",
                user="root",
                password="Pak@123",
                database="asm_sys",  # Corrected to asm_sys
                auth_plugin='mysql_native_password'
            )
            print("Database connection successful")
            return connection
        except mysql.connector.Error as error:
            print(f"Database connection failed: {error}")
            self.show_snackbar(f"Database error: {error}", ft.Colors.RED_700)
            return None

    def fetch_history(self):
        """Fetch history data from asset_history table."""
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor(dictionary=True)

            # Fetch history from asset_history table
            cursor.execute(
                """
                SELECT table_type, entity_id, data_json, action, action_timestamp 
                FROM asset_history
                ORDER BY action_timestamp DESC
                """
            )
            for row in cursor.fetchall():
                data = row["data_json"]
                action = row["action"]
                timestamp = row["action_timestamp"]

                # Extract relevant details based on table_type
                if row["table_type"] == "assets":
                    asset_name = data.get("model", "Unknown Asset")
                    category_id = None  # Assets don't directly link to category_id; adjust if needed
                    user_department = data.get("deployed_user_id") or data.get("deployed_department_id", "N/A")
                    details = data.get("status", "No details")
                else:
                    asset_name = "Unknown"
                    category_id = None
                    user_department = "N/A"
                    details = "Not applicable"

                self.history_data.append({
                    "action": action,
                    "asset_name": asset_name,
                    "category_id": category_id,
                    "user_department": str(user_department) if user_department else "N/A",
                    "date": timestamp,
                    "details": details
                })

        except mysql.connector.Error as err:
            print(f"Error fetching history: {err}")
            self.show_snackbar(f"Error fetching history: {err}", ft.Colors.RED_700)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def populate_table(self):
        """Populate the DataTable with history data."""
        for entry in self.history_data:
            category_name = self.category_map.get(entry["category_id"], "Unknown")
            date_str = entry["date"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(entry["date"], datetime) else str(entry["date"])
            
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                entry["action"],
                                size=14,
                                color={
                                    "Added": ft.Colors.GREEN_700,
                                    "Updated": ft.Colors.BLUE_700,
                                    "Deleted": ft.Colors.RED_700,
                                }.get(entry["action"], ft.Colors.GREY_700),
                                weight=ft.FontWeight.BOLD,
                            )
                        ),
                        ft.DataCell(ft.Text(entry["asset_name"], size=14, color=ft.Colors.BLACK87)),
                        ft.DataCell(ft.Text(category_name, size=14, color=ft.Colors.BLACK87)),
                        ft.DataCell(ft.Text(entry["user_department"], size=14, color=ft.Colors.BLACK87)),
                        ft.DataCell(ft.Text(date_str, size=14, color=ft.Colors.BLACK87)),
                        ft.DataCell(ft.Text(entry["details"], size=14, color=ft.Colors.GREY_800)),
                    ]
                )
            )

    def show_snackbar(self, message, color):
        """Show a snackbar with the given message and color."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
            duration=3000,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def build(self):
        return self.content

def history_table(page):
    return HistoryTable(page)