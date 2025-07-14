import flet as ft
import mysql.connector

from components.userform import UserDialog
from components.departmentform import DepartDialog

class UsersAndDepartmentsPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "Asset Management System - Users & Departments"
        self.page.window_title = "Asset Management System - Users & Departments"
        self.expand = True
        self.users_list = []
        self.departments_list = []

        # Dialogs
        self.user_dialog = UserDialog(page, self)
        self.department_dialog = DepartDialog(page, self)

        # Add Button
        self.add_button = ft.ElevatedButton(
            icon=ft.Icons.ADD,
            text="Add User/Department",
            bgcolor=ft.Colors.PURPLE_400,
            color=ft.Colors.WHITE,
            width=200,
            height=50,
            on_click=self.show_add_selection
        )

        # Loading Indicator
        self.loading_indicator = ft.ProgressRing(visible=False)

        # Tables
        self.admin_table = ft.DataTable(
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            heading_row_color=ft.Colors.INDIGO_100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={ft.ControlState.HOVERED: ft.Colors.LIGHT_BLUE_50},
            data_row_min_height=50,
            data_text_style=ft.TextStyle(
                color=ft.Colors.GREY_800,
                size=14,
            ),
            show_checkbox_column=False,
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("EMP ID", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Branch", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Department", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Can Login", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Image", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
            rows=[],
        )

        self.user_table = ft.DataTable(
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            heading_row_color=ft.Colors.INDIGO_100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={ft.ControlState.HOVERED: ft.Colors.LIGHT_BLUE_50},
            data_row_min_height=50,
            data_text_style=ft.TextStyle(
                color=ft.Colors.GREY_800,
                size=14,
            ),
            show_checkbox_column=False,
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("EMP ID", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Branch", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Department", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Can Login", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Image", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
            rows=[],
        )

        self.department_table = ft.DataTable(
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            heading_row_color=ft.Colors.INDIGO_100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={ft.ControlState.HOVERED: ft.Colors.LIGHT_BLUE_50},
            data_row_min_height=50,
            data_text_style=ft.TextStyle(
                color=ft.Colors.GREY_800,
                size=14,
            ),
            show_checkbox_column=False,
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Description", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Users", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )

        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Users",
                    icon=ft.Icons.GROUP,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Admin Users", size=20, weight=ft.FontWeight.W_600),
                                    ft.Text("Regular Users", size=20, weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(content=self.admin_table, expand=True),
                                    ft.Container(content=self.user_table, expand=True),
                                ],
                                spacing=10,
                                expand=True
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Departments",
                    icon=ft.Icons.BUSINESS,
                    content=ft.Column(
                        controls=[
                            ft.Text("Departments", size=20, weight=ft.FontWeight.W_600),
                            self.department_table,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
            ]
        )

        # Page Layout
        self.content = ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.Colors.WHITE),
                ft.Row(
                    controls=[
                        self.add_button,
                        self.loading_indicator,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
                self.tabs,
            ],
            expand=True,
            spacing=10,
        )

        self.page.add(self)
        self.load_users()
        self.load_departments()

    def _get_db_connection(self):
        """Establish and return a database connection."""
        try:
            connection = mysql.connector.connect(
                host="200.200.201.100",
                user="root",
                password="Pak@123",
                database="asm_sys",
                auth_plugin='mysql_native_password'
            )
            print("Database connection successful")
            return connection
        except mysql.connector.Error as error:
            print(f"Database connection failed: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))
            return None

    def load_users(self):
        """Fetches and displays user data."""
        self.loading_indicator.visible = True
        self.page.update()

        connection = self._get_db_connection()
        if not connection:
            self.loading_indicator.visible = False
            self.page.update()
            return

        try:
            cur = connection.cursor()
            cur.execute("""
                SELECT u.id, u.name, u.emp_id, u.branch, d.name as dept_name, u.can_login, u.image_path
                FROM users u
                LEFT JOIN department d ON u.department_id = d.id
                WHERE u.can_login = 1
            """)
            admins = cur.fetchall()

            cur.execute("""
                SELECT u.id, u.name, u.emp_id, u.branch, d.name as dept_name, u.can_login, u.image_path
                FROM users u
                LEFT JOIN department d ON u.department_id = d.id
                WHERE u.can_login = 0
            """)
            users = cur.fetchall()

            self.admin_table.rows.clear()
            self.user_table.rows.clear()

            for admin_user in admins:
                user_id, name, emp_id, branch, dept_name, can_login, image_path = admin_user
                self.admin_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(name or "N/A")),
                            ft.DataCell(ft.Text(emp_id or "N/A")),
                            ft.DataCell(ft.Text(branch or "N/A")),
                            ft.DataCell(ft.Text(dept_name or "N/A")),
                            ft.DataCell(ft.Text("Yes" if can_login else "No")),
                            ft.DataCell(ft.Text(image_path or "N/A")),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Edit",
                                            bgcolor=ft.Colors.LIGHT_GREEN_500,
                                            color=ft.Colors.WHITE,
                                            on_click=lambda e, user_id=user_id: self.edit_user(user_id)
                                        ),
                                        ft.ElevatedButton(
                                            "Delete",
                                            bgcolor=ft.Colors.RED_500,
                                            color=ft.Colors.WHITE,
                                            on_click=lambda e, user_id=user_id: self.delete_user(user_id)
                                        ),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                )
                            ),
                        ]
                    )
                )

            for user in users:
                user_id, name, emp_id, branch, dept_name, can_login, image_path = user
                self.user_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(name or "N/A")),
                            ft.DataCell(ft.Text(emp_id or "N/A")),
                            ft.DataCell(ft.Text(branch or "N/A")),
                            ft.DataCell(ft.Text(dept_name or "N/A")),
                            ft.DataCell(ft.Text("Yes" if can_login else "No")),
                            ft.DataCell(ft.Text(image_path or "N/A")),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Edit",
                                            bgcolor=ft.Colors.LIGHT_GREEN_500,
                                            color=ft.Colors.WHITE,
                                            on_click=lambda e, user_id=user_id: self.edit_user(user_id)
                                        ),
                                        ft.ElevatedButton(
                                            "Delete",
                                            bgcolor=ft.Colors.RED_500,
                                            color=ft.Colors.WHITE,
                                            on_click=lambda e, user_id=user_id: self.delete_user(user_id)
                                        ),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                )
                            ),
                        ]
                    )
                )

        except mysql.connector.Error as error:
            print(f"Error fetching users: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching users: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")
            self.loading_indicator.visible = False
            self.page.update()

    def load_departments(self):
        """Fetches and displays department data."""
        self.loading_indicator.visible = True
        self.page.update()

        connection = self._get_db_connection()
        if not connection:
            self.loading_indicator.visible = False
            self.page.update()
            return

        try:
            cur = connection.cursor()
            cur.execute("""
                SELECT department.id, department.name, department.description, COUNT(users.id) as user_count
                FROM department
                LEFT JOIN users ON department.id = users.department_id
                GROUP BY department.id
            """)
            departments = cur.fetchall()
            self.department_table.rows.clear()

            for department in departments:
                dept_id, name, description, user_count = department
                self.department_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(name or "N/A")),
                            ft.DataCell(ft.Text(description or "N/A")),
                            ft.DataCell(
                                ft.TextButton(
                                    str(user_count),
                                    on_click=lambda e, count=user_count: self.show_users(count)
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Edit",
                                            bgcolor=ft.Colors.LIGHT_GREEN_500,
                                            color=ft.Colors.WHITE,
                                            on_click=lambda e, id=dept_id: self.edit_department(id)
                                        ),
                                        ft.ElevatedButton(
                                            "Delete",
                                            bgcolor=ft.Colors.RED_500,
                                            color=ft.Colors.WHITE,
                                            on_click=lambda e, id=dept_id: self.delete_department(id)
                                        ),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                )
                            ),
                        ]
                    )
                )

        except mysql.connector.Error as error:
            print(f"Failed to load departments: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error loading departments: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")
            self.loading_indicator.visible = False
            self.page.update()

    def show_add_selection(self, e):
        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add New"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            "Add User",
                            icon=ft.Icons.PERSON,
                            bgcolor=ft.Colors.BLUE_400,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: self.user_dialog.open()
                        ),
                        ft.ElevatedButton(
                            "Add Department",
                            icon=ft.Icons.BUSINESS,
                            bgcolor=ft.Colors.YELLOW_600,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: self.department_dialog.open()
                        ),
                    ],
                    spacing=20,
                ),
                width= 300,
                height=200,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog.open = True
        self.page.overlay.append(self.page.dialog)
        self.page.update()

    def edit_user(self, user_id: int):
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("SELECT name, emp_id, password, branch, department_id, can_login, image_path FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                name, emp_id, password, branch, department_id, can_login, image_path = user_data
                self.user_dialog.open(
                    name=name,
                    emp_id=emp_id,
                    password=password,
                    branch=branch,
                    department_id=department_id,
                    can_login=bool(can_login),
                    image_path=image_path,
                    user_id=user_id
                )
            else:
                self.page.open(ft.SnackBar(ft.Text(f"User ID {user_id} not found."), duration=4000))
        except mysql.connector.Error as error:
            print(f"Error fetching user: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching user: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def delete_user(self, user_id: int):
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
            print(f"Deleted user ID: {user_id}")
            self.page.open(ft.SnackBar(ft.Text("User deleted successfully."), duration=3000))
            self.load_users()
        except mysql.connector.Error as error:
            print(f"Error deleting user: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error deleting user: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def show_users(self, user_count: int):
        if user_count > 0:
            self.tabs.selected_index = 0
            self.page.update()

    def edit_department(self, dept_id: int):
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("SELECT name, description FROM department WHERE id = %s", (dept_id,))
            department = cur.fetchone()
            if department:
                name, description = department
                self.department_dialog.open(name, description, dept_id)
            else:
                self.page.open(ft.SnackBar(ft.Text(f"Department ID {dept_id} not found."), duration=4000))
        except mysql.connector.Error as error:
            print(f"Failed to fetch department: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching department: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def delete_department(self, dept_id: int):
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("DELETE FROM department WHERE id = %s", (dept_id,))
            connection.commit()
            print(f"Deleted department ID: {dept_id}")
            self.page.open(ft.SnackBar(ft.Text("Department deleted successfully."), duration=3000))
            self.load_departments()
        except mysql.connector.Error as error:
            print(f"Failed to delete department: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error deleting department: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()

# def create_users_and_departments_page(page: ft.Page) -> UsersAndDepartmentsPage:
#     return UsersAndDepartmentsPage(page)