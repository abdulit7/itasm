
# import flet as ft
# import mysql.connector
# from mysql.connector import Error

# def login_page(page: ft.Page):
#     page.title = "Asset Management System - Login"
#     page.window_title = "Asset Management System - Login"

#     # Session management
#     page.session.set("user", None)

#     # Form fields
#     emp_id_field = ft.TextField(
#         label="EMP ID",
#         hint_text="Enter your EMP ID",
#         border_color=ft.Colors.BLUE_200,
#         icon=ft.Icons.PERSON,
#         width=300,
#     )
#     password_field = ft.TextField(
#         label="Password",
#         hint_text="Enter your password",
#         border_color=ft.Colors.BLUE_200,
#         icon=ft.Icons.LOCK,
#         password=True,
#         width=300,
#     )

#     def login(e):
#         emp_id = emp_id_field.value.strip()
#         password = password_field.value.strip()

#         if not emp_id or not password:
#             page.snack_bar = ft.SnackBar(ft.Text("Please fill in all fields."), duration=4000)
#             page.snack_bar.open = True
#             page.update()
#             return

#         connection = None
#         try:
#             connection = mysql.connector.connect(
#                 host="200.200.201.100",
#                 user="root",
#                 password="Pak@123",
#                 database="asm_sys",
#                 auth_plugin='mysql_native_password'
#             )
#             cursor = connection.cursor(dictionary=True)
#             cursor.execute(
#                 "SELECT emp_id, password, can_login FROM users WHERE emp_id = %s AND password = %s",
#                 (emp_id, password)
#             )
#             user = cursor.fetchone()

#             if user and user["can_login"] == 1:
#                 cursor.execute(
#                     "SELECT name FROM users WHERE emp_id = %s",
#                     (emp_id,)
#                 )
#                 name = cursor.fetchone()["name"]
#                 page.session.set("user", {"emp_id": user["emp_id"], "can_login": user["can_login"], "name": name})
#                 print("Session user set:", page.session.get("user"))  # Debug print
#                 page.snack_bar = ft.SnackBar(ft.Text(f"Login successful as {name}"), duration=4000)
#                 page.snack_bar.open = True
#                 page.go("/dashboard")
#             elif user and user["can_login"] == 0:
#                 page.snack_bar = ft.SnackBar(ft.Text("Login disabled for this user."), duration=4000)
#                 page.snack_bar.open = True
#             else:
#                 page.snack_bar = ft.SnackBar(ft.Text("Invalid EMP ID or password."), duration=4000)
#                 page.snack_bar.open = True
#         except Error as e:
#             page.snack_bar = ft.SnackBar(ft.Text(f"Database error: {e}"), duration=4000)
#             page.snack_bar.open = True
#             print(f"Database error: {e}")  # Debug print
#         finally:
#             if connection and connection.is_connected():
#                 cursor.close()
#                 connection.close()
#         page.update()

#     # Layout
#     login_form = ft.Column(
#         controls=[
#             ft.Text("Login", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
#             ft.Container(height=20),
#             emp_id_field,
#             ft.Container(height=10),
#             password_field,
#             ft.Container(height=20),
#             ft.ElevatedButton(
#                 text="Login",
#                 bgcolor=ft.Colors.BLUE_400,
#                 color=ft.Colors.WHITE,
#                 on_click=login,
#                 width=300,
#             ),
#         ],
#         alignment=ft.MainAxisAlignment.CENTER,
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#     )

#     return ft.Container(
#         content=login_form,
#         alignment=ft.alignment.center,
#         expand=True,
#         bgcolor=ft.Colors.WHITE,
#     )


import flet as ft
import mysql.connector
from mysql.connector import Error

def login_page(page: ft.Page):
    page.title = "Asset Management System - Login"
    page.window_title = "Asset Management System - Login"

    # Session management
    page.session.set("user", None)

    # Form fields with enhanced styling
    emp_id_field = ft.TextField(
        label="EMP ID",
        hint_text="Enter your EMP ID",
        border_color="blue",
        icon="person",
        width=300,
        text_size=14,
        filled=True,
        fill_color="white",
        border_radius=8,
        content_padding=ft.padding.all(10),
    )
    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        border_color="blue",
        icon="lock",
        password=True,
        width=300,
        text_size=14,
        filled=True,
        fill_color="white",
        border_radius=8,
        content_padding=ft.padding.all(10),
    )

    def login(e):
        emp_id = emp_id_field.value.strip()
        password = password_field.value.strip()

        if not emp_id or not password:
            page.snack_bar = ft.SnackBar(ft.Text("Please fill in all fields."), duration=4000)
            page.snack_bar.open = True
            page.update()
            return

        connection = None
        try:
            connection = mysql.connector.connect(
                host="200.200.201.100",
                user="root",
                password="Pak@123",
                database="asm_sys",
                auth_plugin='mysql_native_password'
            )
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT emp_id, password, can_login FROM users WHERE emp_id = %s AND password = %s",
                (emp_id, password)
            )
            user = cursor.fetchone()

            if user and user["can_login"] == 1:
                cursor.execute(
                    "SELECT name FROM users WHERE emp_id = %s",
                    (emp_id,)
                )
                name = cursor.fetchone()["name"]
                page.session.set("user", {"emp_id": user["emp_id"], "can_login": user["can_login"], "name": name})
                print("Session user set:", page.session.get("user"))  # Debug print
                page.snack_bar = ft.SnackBar(ft.Text(f"Login successful as {name}"), duration=4000)
                page.snack_bar.open = True
                page.go("/dashboard")
            elif user and user["can_login"] == 0:
                page.snack_bar = ft.SnackBar(ft.Text("Login disabled for this user."), duration=4000)
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Invalid EMP ID or password."), duration=4000)
                page.snack_bar.open = True
        except Error as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Database error: {e}"), duration=4000)
            page.snack_bar.open = True
            print(f"Database error: {e}")  # Debug print
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
        page.update()

    # Logo-like title with department name
    logo_text = ft.Row(
        [
            ft.Icon(name="computer", color="blue", size=40),
            ft.Text(
                "Gujranwala Food Industries IT Department",
                size=24,
                weight=ft.FontWeight.BOLD,
                color="blue",
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Login form with card
    login_form = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    logo_text,
                    ft.Container(height=50),  # Increased spacing for logo
                    ft.Text("Login", size=20, weight=ft.FontWeight.BOLD, color="blue", font_family="Athelas"),
                    ft.Container(height=25),
                    emp_id_field,
                    ft.Container(height=20),
                    password_field,
                    ft.Container(height=25),
                    ft.ElevatedButton(
                        text="Login",
                        bgcolor="blue",
                        color="white",
                        on_click=login,
                        width=300,
                        elevation=6,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,  # Increased column spacing
            ),
            padding=ft.padding.all(25),  # Increased padding
            bgcolor="white",  # Solid white background for card
            width=1000,
            height=800,  # Increased height for less congestion
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=10,
                color="blue",
                offset=ft.Offset(0, 4),
            ),
        ),
    )

    # Page layout with full background
    return ft.Container(
        content=login_form,
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="lightcyan",  # Full window background color
    )