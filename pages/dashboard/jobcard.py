
import os
os.environ["FLET_SECRET_KEY"] = "mysecret123"
import flet as ft
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json

class JobCardPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "Job Card Management"
        self.page.window_title = "Job Card Management"
        self.expand = True
        self.padding = ft.padding.all(20)
        self.job_cards = []
        self.departments = []
        self.deployed_assets = []
        self.deployed_consumables = []
        self.deployed_components = []
        self.deployed_devices = []

        self.add_job_card_button = ft.ElevatedButton(
            text="Create Job Card",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            elevation=4,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                overlay_color=ft.Colors.TEAL_700
            ),
            width=160,
            height=50,
            on_click=self.open_job_card_dialog
        )

        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[],
            expand=True
        )

        self.load_departments()
        self.load_job_cards()
        self.load_deployed_entities()

        self.content = ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Row(
                    controls=[
                        ft.Text("Job Card Management", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        self.add_job_card_button
                    ],
                ),
                self.tabs
            ],
            expand=True,
            spacing=10
        )

    def load_departments(self):
        db_config = {
            "host": "200.200.201.100",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name FROM department")
            self.departments = cursor.fetchall()
        except Error as e:
            self.show_snack_bar(f"Error fetching departments: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def load_deployed_entities(self):
        db_config = {
            "host": "200.200.201.100",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Load deployed assets
            cursor.execute("SELECT id, serial_number, model FROM assets WHERE status = 'Deployed'")
            self.deployed_assets = cursor.fetchall()

            # Load deployed consumables
            cursor.execute("""
                SELECT c.id, c.cartridge_no, p.model AS printer_model
                FROM consumables c
                LEFT JOIN printers p ON c.deployed_to = p.id
                WHERE c.status = 'Deployed'
            """)
            self.deployed_consumables = cursor.fetchall()

            # Load deployed components
            cursor.execute("SELECT id, serial_number, model FROM components WHERE status = 'Deployed'")
            self.deployed_components = cursor.fetchall()

            # Load deployed devices
            cursor.execute("SELECT id, serial_number, model FROM devices WHERE status = 'Deployed'")
            self.deployed_devices = cursor.fetchall()

        except Error as e:
            self.show_snack_bar(f"Error fetching deployed entities: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def load_job_cards(self):
        self.job_cards = []
        db_config = {
            "host": "200.200.201.100",
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
                SELECT jc.id, jc.job_number, jc.title, jc.description, jc.status, jc.created_date, jc.started_date,
                       jc.completed_date, jc.entity_type, jc.entity_id, jc.closure_details, d.name AS department
                FROM job_cards jc
                LEFT JOIN department d ON jc.department_id = d.id
            """)
            self.job_cards = cursor.fetchall()
            for jc in self.job_cards:
                if jc['entity_type'] and jc['entity_id']:
                    jc['entity_info'] = self.get_entity_info(jc['entity_type'], jc['entity_id'])
                else:
                    jc['entity_info'] = "No entity assigned"
        except Error as e:
            self.show_snack_bar(f"Error fetching job cards: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        self.tabs.tabs = self.create_tabs()
        self.page.update()

    def get_entity_info(self, entity_type, entity_id):
        db_config = {
            "host": "200.200.201.100",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            if entity_type == "Asset":
                cursor.execute("SELECT serial_number, model FROM assets WHERE id = %s", (entity_id,))
                result = cursor.fetchone()
                return f"Asset: {result['serial_number']} ({result['model']})" if result else "Unknown Asset"
            elif entity_type == "Consumable":
                cursor.execute("""
                    SELECT c.cartridge_no, p.model AS printer_model
                    FROM consumables c
                    LEFT JOIN printers p ON c.deployed_to = p.id
                    WHERE c.id = %s
                """, (entity_id,))
                result = cursor.fetchone()
                return f"Consumable: {result['cartridge_no']} (Printer: {result['printer_model']})" if result else "Unknown Consumable"
            elif entity_type == "Component":
                cursor.execute("SELECT serial_number, model FROM components WHERE id = %s", (entity_id,))
                result = cursor.fetchone()
                return f"Component: {result['serial_number']} ({result['model']})" if result else "Unknown Component"
            elif entity_type == "Device":
                cursor.execute("SELECT serial_number, model FROM devices WHERE id = %s", (entity_id,))
                result = cursor.fetchone()
                return f"Device: {result['serial_number']} ({result['model']})" if result else "Unknown Device"
            return "Unknown Entity"
        except Error:
            return "Error fetching entity info"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def create_tabs(self):
        open_cards = [jc for jc in self.job_cards if jc['status'].lower() == 'open']
        started_cards = [jc for jc in self.job_cards if jc['status'].lower() == 'started']
        completed_cards = [jc for jc in self.job_cards if jc['status'].lower() == 'completed']

        return [
            ft.Tab(
                text="Open",
                icon=ft.Icons.HOURGLASS_TOP,
                content=self._build_tab_content(open_cards, "No open job cards found.")
            ),
            ft.Tab(
                text="Started",
                icon=ft.Icons.PLAY_CIRCLE,
                content=self._build_tab_content(started_cards, "No started job cards found.")
            ),
            ft.Tab(
                text="Completed",
                icon=ft.Icons.CHECK_CIRCLE,
                content=self._build_tab_content(completed_cards, "No completed job cards found.")
            )
        ]

    def _build_tab_content(self, cards, no_cards_message):
        if not cards:
            return ft.Column(
                controls=[ft.Text(no_cards_message, size=20, color=ft.Colors.RED_300)],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )
        return ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=self.create_job_card_card(jc),
                            col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                            padding=ft.padding.all(10)
                        )
                        for jc in cards
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                    run_spacing=10
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

    def create_job_card_card(self, job_card):
        created_date = job_card.get('created_date', 'N/A').strftime('%Y-%m-%d %H:%M:%S') if job_card.get('created_date') else 'N/A'
        started_date = job_card.get('started_date', 'N/A').strftime('%Y-%m-%d %H:%M:%S') if job_card.get('started_date') else 'N/A'
        completed_date = job_card.get('completed_date', 'N/A').strftime('%Y-%m-%d %H:%M:%S') if job_card.get('completed_date') else 'N/A'

        card_content = ft.Column(
            controls=[
                ft.Text(job_card['job_number'], weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLUE_900),
                ft.Text(job_card['title'], size=14, color=ft.Colors.BLACK),
                ft.Text(job_card['description'], size=12, color=ft.Colors.GREY_700),
                ft.Text(f"Department: {job_card.get('department', 'N/A')}", size=12, color=ft.Colors.GREY_700),
                ft.Text(f"Entity: {job_card.get('entity_info', 'N/A')}", size=12, color=ft.Colors.GREY_700),
                ft.Text(f"Created: {created_date}", size=12, color=ft.Colors.GREY_700),
                ft.Text(f"Started: {started_date}", size=12, color=ft.Colors.GREY_700),
                ft.Text(f"Completed: {completed_date}", size=12, color=ft.Colors.GREY_700),
                ft.Text(f"Status: {job_card['status']}", size=12, color=ft.Colors.GREEN_700 if job_card['status'].lower() == 'open' else ft.Colors.YELLOW_700 if job_card['status'].lower() == 'started' else ft.Colors.GREY_600),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Start",
                            icon=ft.Icons.PLAY_ARROW,
                            bgcolor=ft.Colors.YELLOW_300,
                            color=ft.Colors.WHITE,
                            on_click=lambda e, jc=job_card: self.start_job_card(jc),
                            disabled=job_card['status'].lower() != 'open'
                        ),
                        ft.ElevatedButton(
                            text="Complete",
                            icon=ft.Icons.CHECK,
                            bgcolor=ft.Colors.GREEN_300,
                            color=ft.Colors.WHITE,
                            on_click=lambda e, jc=job_card: self.open_complete_dialog(jc),
                            disabled=job_card['status'].lower() in ['completed', 'open']
                        ),
                        ft.ElevatedButton(
                            text="View Details",
                            icon=ft.Icons.VISIBILITY,
                            bgcolor=ft.Colors.BLUE_300,
                            color=ft.Colors.WHITE,
                            on_click=lambda e, jc=job_card: self.show_job_card_detail(jc)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    spacing=10
                )
            ],
            spacing=5
        )

        return ft.Card(
            content=ft.Container(
                content=card_content,
                padding=15,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=12,
                ink=True,
                on_click=lambda e, jc=job_card: self.show_job_card_detail(jc)
            ),
            elevation=5
        )

    def show_job_card_detail(self, job_card):
        created_date = job_card.get('created_date', 'N/A').strftime('%Y-%m-%d %H:%M:%S') if job_card.get('created_date') else 'N/A'
        started_date = job_card.get('started_date', 'N/A').strftime('%Y-%m-%d %H:%M:%S') if job_card.get('started_date') else 'N/A'
        completed_date = job_card.get('completed_date', 'N/A').strftime('%Y-%m-%d %H:%M:%S') if job_card.get('completed_date') else 'N/A'

        dialog_content = ft.Column(
            controls=[
                ft.Text(f"Job Number: {job_card['job_number']}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PINK_600),
                ft.Text(f"Title: {job_card['title']}", size=14, color=ft.Colors.ORANGE_600),
                ft.Text(f"Description: {job_card['description']}", size=14, color=ft.Colors.PURPLE_600),
                ft.Text(f"Department: {job_card.get('department', 'N/A')}", size=14, color=ft.Colors.TEAL_600),
                ft.Text(f"Entity: {job_card.get('entity_info', 'N/A')}", size=14, color=ft.Colors.AMBER_600),
                ft.Text(f"Closure Details: {job_card.get('closure_details', 'N/A')}", size=14, color=ft.Colors.DEEP_ORANGE_600),
                ft.Text(f"Created: {created_date}", size=14, color=ft.Colors.LIGHT_GREEN_600),
                ft.Text(f"Started: {started_date}", size=14, color=ft.Colors.CYAN_600),
                ft.Text(f"Completed: {completed_date}", size=14, color=ft.Colors.INDIGO_600),
                ft.Text(f"Status: {job_card['status']}", size=14, color=ft.Colors.DEEP_PURPLE_600)
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Job Card Details (ID: {job_card['id']})", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700, font_family="Roboto"),
            content=ft.Container(
                content=dialog_content,
                width=400,
                height=600,
                padding=ft.padding.all(20),
                bgcolor=ft.Colors.YELLOW_50,
                border_radius=ft.border_radius.all(15)
            ),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=self.close_dialog,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.PINK_500,
                        color=ft.Colors.WHITE,
                        elevation=4,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        overlay_color=ft.Colors.PINK_700
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.ORANGE_300, ft.Colors.YELLOW_100]
            ),
            content_padding=ft.padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=15),
            barrier_color=ft.Colors.BLACK54
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.overlay.append(dialog)
        self.page.update()

    def close_dialog(self, e):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def open_job_card_dialog(self, e=None):
        self.job_title = ft.TextField(label="Job Title", hint_text="Enter job title", border_color=ft.Colors.PURPLE_200, color=ft.Colors.PURPLE_900)
        self.job_description = ft.TextField(label="Description", hint_text="Enter job description", multiline=True, border_color=ft.Colors.PURPLE_200, color=ft.Colors.PURPLE_900)
        self.department_dropdown = ft.Dropdown(
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            menu_height=200,
            label="Department",
            options=[ft.dropdown.Option(key=str(d['id']), text=d['name']) for d in self.departments],
            value=str(self.departments[0]['id']) if self.departments else None,
            border_color=ft.Colors.PURPLE_200,
            color=ft.Colors.PURPLE_900
        )

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Create Job Card", color=ft.Colors.PURPLE_800, size=20, weight=ft.FontWeight.BOLD, font_family="Roboto"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.job_title,
                        self.job_description,
                        self.department_dropdown
                    ],
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO
                ),
                width=400,
                height=600,
                padding=ft.padding.all(20),
                bgcolor=ft.Colors.LIGHT_BLUE_50,
                border_radius=ft.border_radius.all(15)
            ),
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=self.close_dialog,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_500,
                        color=ft.Colors.WHITE,
                        elevation=4,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        overlay_color=ft.Colors.RED_700
                    )
                ),
                ft.TextButton(
                    "Save",
                    on_click=self.save_job_card,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        elevation=4,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        overlay_color=ft.Colors.GREEN_900
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.PURPLE_200, ft.Colors.LIGHT_BLUE_100]
            ),
            content_padding=ft.padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=15),
            barrier_color=ft.Colors.BLACK54
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.overlay.append(self.dialog)
        self.page.update()

    def save_job_card(self, e):
        title = self.job_title.value.strip()
        description = self.job_description.value.strip()
        department_id = self.department_dropdown.value

        if not all([title, description, department_id]):
            self.show_snack_bar("Title, description, and department are required.", ft.Colors.RED_800)
            return

        db_config = {
            "host": "200.200.201.100",
            "user": "root",
            "password": "Pak@123",
            "database": "asm_sys"
        }
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as count FROM job_cards WHERE created_date LIKE %s", (f"{datetime.now().strftime('%Y-%m-%d')}%",))
            count_data = cursor.fetchone()
            count = count_data['count'] + 1
            job_number = f"JC-{datetime.now().strftime('%Y%m%d')}-{count:04d}"

            cursor.execute("""
                INSERT INTO job_cards (job_number, title, description, status, created_date, department_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (job_number, title, description, "Open", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), department_id))

            conn.commit()
            self.show_snack_bar("Job card created successfully!", ft.Colors.GREEN_800)
            self.load_job_cards()
            self.close_dialog(None)
        except Error as e:
            self.show_snack_bar(f"Error saving job card: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def start_job_card(self, job_card):
        db_config = {
            "host": "200.200.201.100",
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
                UPDATE job_cards 
                SET status = 'Started', started_date = %s
                WHERE id = %s
            """, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), job_card['id']))
            conn.commit()
            self.show_snack_bar("Job card started successfully!", ft.Colors.GREEN_800)
            self.load_job_cards()
        except Error as e:
            self.show_snack_bar(f"Error starting job card: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def open_complete_dialog(self, job_card):
        self.complete_details = ft.TextField(
            label="Completion Details",
            hint_text="Enter what was done, parts used",
            multiline=True,
            border_color=ft.Colors.DEEP_ORANGE_200,
            color=ft.Colors.DEEP_ORANGE_900
        )
        self.entity_type_dropdown = ft.Dropdown(
            label="Entity Type",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[
                ft.dropdown.Option("Asset"),
                ft.dropdown.Option("Consumable"),
                ft.dropdown.Option("Component"),
                ft.dropdown.Option("Device")
            ],
            value=None,
            on_change=self.update_entity_dropdown,
            border_color=ft.Colors.DEEP_ORANGE_200,
            color=ft.Colors.DEEP_ORANGE_900
        )
        self.entity_dropdown = ft.Dropdown(
            label="Select Deployed Entity",
            border=ft.InputBorder.UNDERLINE,
            enable_filter=True,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[],
            value=None,
            border_color=ft.Colors.DEEP_ORANGE_200,
            color=ft.Colors.DEEP_ORANGE_900
        )

        self.load_deployed_entities()

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Complete Job Card", color=ft.Colors.DEEP_ORANGE_800, size=20, weight=ft.FontWeight.BOLD, font_family="Roboto"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"Job Number: {job_card['job_number']}", color=ft.Colors.DEEP_ORANGE_600),
                        ft.Text(f"Title: {job_card['title']}", color=ft.Colors.AMBER_600),
                        self.complete_details,
                        self.entity_type_dropdown,
                        self.entity_dropdown
                    ],
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO
                ),
                width=400,
                height=600,
                padding=ft.padding.all(20),
                bgcolor=ft.Colors.ORANGE_50,
                border_radius=ft.border_radius.all(15)
            ),
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=self.close_dialog,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_500,
                        color=ft.Colors.WHITE,
                        elevation=4,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        overlay_color=ft.Colors.BLUE_700
                    )
                ),
                ft.TextButton(
                    "Save",
                    on_click=lambda e: self.complete_job_card(job_card),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.TEAL_700,
                        color=ft.Colors.WHITE,
                        elevation=4,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        overlay_color=ft.Colors.TEAL_900
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.AMBER_300, ft.Colors.ORANGE_100]
            ),
            content_padding=ft.padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=15),
            barrier_color=ft.Colors.BLACK54
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.overlay.append(self.dialog)
        self.page.update()

    def update_entity_dropdown(self, e):
        entity_type = self.entity_type_dropdown.value
        self.entity_dropdown.options = []
        self.entity_dropdown.value = None

        if entity_type == "Asset":
            self.entity_dropdown.options = [
                ft.dropdown.Option(key=str(asset['id']), text=f"{asset['serial_number']} ({asset['model']})")
                for asset in self.deployed_assets
            ]
        elif entity_type == "Consumable":
            self.entity_dropdown.options = [
                ft.dropdown.Option(key=str(consumable['id']), text=f"{consumable['cartridge_no']} (Printer: {consumable['printer_model']})")
                for consumable in self.deployed_consumables
            ]
        elif entity_type == "Component":
            self.entity_dropdown.options = [
                ft.dropdown.Option(key=str(component['id']), text=f"{component['serial_number']} ({component['model']})")
                for component in self.deployed_components
            ]
        elif entity_type == "Device":
            self.entity_dropdown.options = [
                ft.dropdown.Option(key=str(device['id']), text=f"{device['serial_number']} ({device['model']})")
                for device in self.deployed_devices
            ]

        self.page.update()

    def complete_job_card(self, job_card):
        details = self.complete_details.value.strip()
        entity_type = self.entity_type_dropdown.value
        entity_id = self.entity_dropdown.value

        if not details:
            self.show_snack_bar("Completion details are required.", ft.Colors.RED_800)
            return

        db_config = {
            "host": "200.200.201.100",
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
                UPDATE job_cards 
                SET status = 'Completed', completed_date = %s, closure_details = %s, entity_type = %s, entity_id = %s
                WHERE id = %s
            """, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), details, entity_type, entity_id if entity_id else None, job_card['id']))

            # Log to asset_history
            cursor.execute("""
                INSERT INTO asset_history (table_type, entity_id, data_json, action)
                VALUES (%s, %s, %s, %s)
            """, (
                'job_cards',
                job_card['id'],
                json.dumps({
                    'job_number': job_card['job_number'],
                    'title': job_card['title'],
                    'status': 'Completed',
                    'entity_type': entity_type,
                    'entity_id': entity_id,
                    'closure_details': details
                }),
                'Updated'
            ))

            conn.commit()
            self.show_snack_bar("Job card completed successfully!", ft.Colors.GREEN_800)
            self.load_job_cards()
            self.close_dialog(None)
        except Error as e:
            self.show_snack_bar(f"Error completing job card: {e}", ft.Colors.RED_800)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_snack_bar(self, message, color=ft.Colors.BLACK):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            duration=4000
        )
        self.page.snack_bar.open = True
        self.page.update()