
import flet as ft
import mysql.connector
from mysql.connector import Error

class MainCards(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True

        # Improved color scheme
        self.card_colors = [
            {"card": "#E3F2FD", "icon": "#42A5F5"},  # Blue theme
            {"card": "#F3E5F5", "icon": "#AB47BC"},  # Purple theme
            {"card": "#E8F5E9", "icon": "#66BB6A"},  # Green theme
            {"card": "#FFF3E0", "icon": "#FFA726"},  # Orange theme
            {"card": "#FCE4EC", "icon": "#EC407A"},  # Pink theme
            {"card": "#E0F7FA", "icon": "#26A69A"}   # Cyan theme
        ]

        # Fetch data from database
        self.card_data = self.fetch_card_data()

        self.content = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_card(item["icon"], item["title"], item["subtitle"], colors["card"], colors["icon"]),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10)
                ) 
                for item, colors in zip(self.card_data, self.card_colors)
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )

    def fetch_card_data(self):
        db_config = {
            "host": "200.200.200.23",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }
        card_data = []
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Fetch total available assets
            cursor.execute("SELECT COUNT(*) as count FROM assets WHERE status = 'Available'")
            assets_count = cursor.fetchone()[0]
            
            # Fetch total available components
            cursor.execute("SELECT COUNT(*) as count FROM components WHERE status = 'Available'")
            components_count = cursor.fetchone()[0]
            
            # Fetch total available consumables
            cursor.execute("SELECT COUNT(*) as count FROM consumables WHERE status = 'Available'")
            consumables_count = cursor.fetchone()[0]
            
            # Fetch total users
            cursor.execute("SELECT COUNT(*) as count FROM users")
            users_count = cursor.fetchone()[0]
            
            # Fetch total departments
            cursor.execute("SELECT COUNT(*) as count FROM department")
            departments_count = cursor.fetchone()[0]
            
            # Fetch total categories
            cursor.execute("SELECT COUNT(*) as count FROM category")
            categories_count = cursor.fetchone()[0]

            card_data = [
                {"icon": ft.Icons.COMPUTER, "title": "Available Assets", "subtitle": str(assets_count) or "0"},
                {"icon": ft.Icons.BUILD, "title": "Available Components", "subtitle": str(components_count) or "0"},
                {"icon": ft.Icons.SHOPPING_BAG, "title": "Available Consumables", "subtitle": str(consumables_count) or "0"},
                {"icon": ft.Icons.PERSON, "title": "Total Users", "subtitle": str(users_count) or "0"},
                {"icon": ft.Icons.DASHBOARD, "title": "Total Departments", "subtitle": str(departments_count) or "0"},
                {"icon": ft.Icons.CATEGORY, "title": "Total Categories", "subtitle": str(categories_count) or "0"}
            ]

        except Error as e:
            print(f"Error fetching card data: {e}")
            card_data = [
                {"icon": ft.Icons.COMPUTER, "title": "Available Assets", "subtitle": "0"},
                {"icon": ft.Icons.BUILD, "title": "Available Components", "subtitle": "0"},
                {"icon": ft.Icons.SHOPPING_BAG, "title": "Available Consumables", "subtitle": "0"},
                {"icon": ft.Icons.PERSON, "title": "Total Users", "subtitle": "0"},
                {"icon": ft.Icons.DASHBOARD, "title": "Total Departments", "subtitle": "0"},
                {"icon": ft.Icons.CATEGORY, "title": "Total Categories", "subtitle": "0"}
            ]
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
        return card_data

    def create_card(self, icon, title, subtitle, card_bgcolor, icon_bgcolor):
        # Circular icon container
        icon_container = ft.Container(
            content=ft.Icon(icon, color="#FFFFFF", size=40),
            bgcolor=icon_bgcolor,
            width=60,
            height=60,
            alignment=ft.alignment.center,
            border_radius=30,
            padding=5
        )

        # Card content with centered layout
        card_content = ft.Column(
            controls=[
                icon_container,
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color="#424242", text_align=ft.TextAlign.CENTER),
                ft.Text(subtitle, size=28, weight=ft.FontWeight.BOLD, color=icon_bgcolor, text_align=ft.TextAlign.CENTER)
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        return ft.Card(
            content=ft.Container(
                content=card_content,
                padding=15,
                bgcolor=card_bgcolor,
                border_radius=12,
                ink=True
            ),
            elevation=8,
            
        )

def MainCardsPage(page):
    return MainCards(page)