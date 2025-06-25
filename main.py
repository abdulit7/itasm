import os
os.environ["FLET_SECRET_KEY"] = "mysecret123"
import flet as ft
from pages.dashboard.home import Home
from pages.dashboard.user_department import UsersAndDepartmentsPage
from pages.dashboard.asset import AssetPage
from pages.dashboard.component import Component
from pages.dashboard.saleforce2 import SaleForce2
from pages.dashboard.category import Category
from pages.dashboard.history import HistoryPage
from pages.dashboard.department import Department
from pages.dashboard.consumables import Consumables
from pages.dashboard.printers import PrintersPage
from pages.dashboard.jobcard import JobCardPage
from pages.dashboard.login import login_page
from nav.sidebar import TopBar

def main(page: ft.Page):
    # Validate page parameter
    if page is None:
        print("Error: Page is None. This function must be called by Flet runtime.")
        return

    print("Starting app...")
    try:
        page.title = "Asset Management System"
        page.expand = True
        page.scroll = "adaptive"
        page.padding = 0
        page.bgcolor = ft.Colors.BLUE_GREY_50
        top_bar_ref = ft.Ref[ft.Container]()

        def get_content_padding():
            window_width = page.window.width if page.window.width > 0 else 800
            return (ft.padding.symmetric(horizontal=20, vertical=15) if window_width > 1024 
                    else ft.padding.symmetric(horizontal=15, vertical=10) if window_width > 600 
                    else ft.padding.symmetric(horizontal=10, vertical=5))

        content_area = ft.Container(
            expand=True,
            padding=get_content_padding(),
            content=ft.Text("Loading...", size=20),
        )

        def change_route(route):
            """Handle route changes and update the page content."""
            print(f"Changing route to: {route}")
            routes = {
                "/dashboard": lambda p: Home(p),
                "/user": lambda p: UsersAndDepartmentsPage(p),
                "/asset": lambda p: AssetPage(p),
                "/component": lambda p: Component(p),
                "/saleforce": lambda p: SaleForce2(p),
                "/history": lambda p: HistoryPage(p),
                "/category": lambda p: Category(p),
                "/department": lambda p: Department(p),
                "/consumable": lambda p: Consumables(p),
                "/printers": lambda p: PrintersPage(p),
                "/jobcard": lambda p: JobCardPage(p),
                "/login": lambda p: login_page(p),
                "/profile": lambda p: ft.Text("Profile Page", size=20),
                "/settings": lambda p: ft.Text("Settings Page", size=20),
                "/notifications": lambda p: ft.Text("Notifications Page", size=20),
                "/logout": lambda p: ft.Text("Logged Out - Redirecting...", size=20, on_create=lambda e: p.go("/login")),
            }

            try:
                content = routes.get(page.route, lambda p: ft.Text("Page not found", size=20, color=ft.Colors.RED_600))(page)
                print(f"Content for {page.route}: {content}")
                if isinstance(content, ft.Control):
                    content_area.content = ft.Column([content], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
                else:
                    content_area.content = ft.Column([ft.Text("Invalid content", size=20, color=ft.Colors.RED_600)], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
                if top_bar_ref.current:
                    top_bar_ref.current.content = TopBar(page, top_bar_ref=top_bar_ref)
                    top_bar_ref.current.update()
                page.update()
            except Exception as e:
                print(f"Error loading route {page.route}: {e}")
                content_area.content = ft.Column([ft.Text(f"Error: {str(e)}", size=20, color=ft.Colors.RED_600)], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
                page.update()

        def view_pop(view):
            """Handle back navigation."""
            if len(page.views) > 1:
                page.views.pop()
                page.go(page.views[-1].route)
            else:
                print("No more views to pop!")
                page.go("/login")

        def on_resize(e):
            """Adjust padding on window resize."""
            content_area.padding = get_content_padding()
            print(f"Resized: Content padding={content_area.padding}")
            page.update()

        # Initialize main layout
        main_column = ft.Column(
            controls=[
                ft.Container(ref=top_bar_ref, content=TopBar(page, top_bar_ref=top_bar_ref)),
                content_area,
            ],
            expand=True,
            spacing=0,
        )
        initial_view = ft.View(
            "/",
            controls=[main_column],
            padding=0,
            bgcolor=ft.Colors.WHITE,
        )
        page.views.append(initial_view)

        # Attach event handlers
        page.on_resize = on_resize
        page.on_route_change = change_route
        page.on_view_pop = view_pop
        page.go("/login")

    except Exception as e:
        print(f"Critical error in main: {e}")
        page.add(ft.Text(f"Critical Error: {e}", color=ft.Colors.RED_600))
        page.update()

    # Ensure temp directory exists
temp_dir = os.path.join(os.getcwd(), "temp")
os.makedirs(temp_dir, exist_ok=True)

# Run the app (Flet will call main with a page object)
ft.app(
    target=main,
    assets_dir="assets",
    upload_dir=temp_dir,
    view=ft.AppView.WEB_BROWSER,
    route_url_strategy="hash",
    port=8080,
)
# import os
# os.environ["FLET_SECRET_KEY"] = "mysecret123"
# import flet as ft
# from pages.dashboard.home import Home
# from pages.dashboard.user_department import UsersAndDepartmentsPage
# from pages.dashboard.asset import AssetPage
# from pages.dashboard.component import Component
# from pages.dashboard.saleforce2 import SaleForce2
# from pages.dashboard.category import Category
# from pages.dashboard.history import HistoryPage
# from pages.dashboard.department import Department
# from pages.dashboard.consumables import Consumables
# from pages.dashboard.printers import PrintersPage
# from pages.dashboard.jobcard import JobCardPage
# from pages.dashboard.login import login_page
# from nav.sidebar import TopBar

# def main(page: ft.Page):
#     page.title = "Asset Management System"
#     page.expand = True
#     page.scroll = "adaptive"
#     page.padding = 0
#     page.bgcolor = ft.Colors.BLUE_GREY_50
#     top_bar_ref = ft.Ref[ft.Container]()

#     def get_content_padding():
#         window_width = page.window.width if page.window.width > 0 else 800
#         return ft.padding.symmetric(horizontal=20, vertical=15) if window_width > 1024 else ft.padding.symmetric(horizontal=15, vertical=10) if window_width > 600 else ft.padding.symmetric(horizontal=10, vertical=5)

#     content_area = ft.Container(
#         expand=True,
#         padding=get_content_padding(),
#         content=ft.Text("Loading...", size=20),
#     )

#     def change_route(route):
#         print(f"Changing route to: {route}")
#         routes = {
#             "/dashboard": lambda p: Home(p),
#             "/user": lambda p: UsersAndDepartmentsPage(p),
#             "/asset": lambda p: AssetPage(p),
#             "/component": lambda p: Component(p),
#             "/saleforce": lambda p: SaleForce2(p),
#             "/history": lambda p: HistoryPage(p),
#             "/category": lambda p: Category(p),
#             "/department": lambda p: Department(p),
#             "/consumable": lambda p: Consumables(p),
#             "/printers": lambda p: PrintersPage(p),
#             "/jobcard": lambda p: JobCardPage(p),
#             "/login": lambda p: login_page(p),
#             "/profile": lambda p: ft.Text("Profile Page", size=20),
#             "/settings": lambda p: ft.Text("Settings Page", size=20),
#             "/notifications": lambda p: ft.Text("Notifications Page", size=20),
#             "/logout": lambda p: ft.Text("Logged Out - Redirecting...", size=20, on_create=lambda e: p.go("/login")),
#         }

#         try:
#             content = routes.get(page.route, lambda p: ft.Text("Page not found", size=20, color=ft.Colors.RED_600))(page)
#             print(f"Content for {page.route}: {content}")
#             if isinstance(content, ft.Control):
#                 content_area.content = ft.Column([content], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
#             else:
#                 content_area.content = ft.Column([ft.Text("Invalid content", size=20, color=ft.Colors.RED_600)], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
#             if top_bar_ref.current:
#                 top_bar_ref.current.content = TopBar(page, top_bar_ref=top_bar_ref)
#                 top_bar_ref.current.update()
#             page.update()
#         except Exception as e:
#             print(f"Error loading route {page.route}: {e}")
#             content_area.content = ft.Column([ft.Text(f"Error: {str(e)}", size=20, color=ft.Colors.RED_600)], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
#             page.update()

#     def view_pop(view):
#         if len(page.views) > 1:
#             page.views.pop()
#             page.go(page.views[-1].route)
#         else:
#             print("No more views to pop!")
#             page.go("/login")

#     def on_resize(e):
#         content_area.padding = get_content_padding()
#         print(f"Resized: Content padding={content_area.padding}")
#         page.update()

#     main_column = ft.Column(
#         controls=[
#             ft.Container(ref=top_bar_ref, content=TopBar(page, top_bar_ref=top_bar_ref)),
#             content_area,
#         ],
#         expand=True,
#         spacing=0,
#     )
#     initial_view = ft.View(
#         "/",
#         controls=[main_column],
#         padding=0,
#         bgcolor=ft.Colors.WHITE,
#     )
#     page.views.append(initial_view)

#     page.on_resize = on_resize
#     page.on_route_change = change_route
#     page.on_view_pop = view_pop
#     page.go("/login")

# temp_dir = os.path.join(os.getcwd(), "temp")
# os.makedirs(temp_dir, exist_ok=True)
# ft.app(
#     target=main,
#     assets_dir="assets",
#     upload_dir=temp_dir,
#     view=ft.AppView.WEB_BROWSER,
#     route_url_strategy="hash",
#     port=8080,
# )

# import os
# os.environ["FLET_SECRET_KEY"] = "mysecret123"
# import flet as ft
# from pages.dashboard.home import Home
# from pages.dashboard.user_department import UsersAndDepartmentsPage
# from pages.dashboard.asset import AssetPage
# from pages.dashboard.component import Component
# from pages.dashboard.saleforce2 import SaleForce2
# from pages.dashboard.category import Category
# from pages.dashboard.history import HistoryPage
# from pages.dashboard.department import Department
# from pages.dashboard.consumables import Consumables
# from pages.dashboard.printers import PrintersPage
# from pages.dashboard.jobcard import JobCardPage
# from pages.dashboard.login import login_page
# from nav.sidebar import TopBar

# def main(page: ft.Page):
#     page.title = "Asset Management System"
#     page.expand = True
#     page.scroll = "adaptive"
#     page.padding = 0
#     page.bgcolor = ft.Colors.BLUE_GREY_50
#     appbar_text_ref = ft.Ref[ft.Text]()

#     # Determine content area padding based on screen size
#     def get_content_padding():
#         window_width = page.window.width if page.window.width > 0 else 800
#         if window_width <= 600:  # Mobile
#             return ft.padding.symmetric(horizontal=10, vertical=5)
#         elif window_width <= 1024:  # Tablet
#             return ft.padding.symmetric(horizontal=15, vertical=10)
#         else:  # Desktop
#             return ft.padding.symmetric(horizontal=20, vertical=15)

#     # Create a Ref for the TopBar to enable updates
#     top_bar_ref = ft.Ref[ft.Container]()
#     content_area = ft.Container(
#         expand=True,
#         padding=get_content_padding(),
#         content=ft.Text("Loading...", size=20),
#     )

#     def change_route(route):
#         print(f"Changing route to: {route}")

#         routes = {
#             "/dashboard": lambda p: Home(p),
#             "/user": lambda p: UsersAndDepartmentsPage(p),
#             "/asset": lambda p: AssetPage(p),
#             "/component": lambda p: Component(p),
#             "/saleforce": lambda p: SaleForce2(p),
#             "/history": lambda p: HistoryPage(p),
#             "/category": lambda p: Category(p),
#             "/department": lambda p: Department(p),
#             "/consumable": lambda p: Consumables(p),
#             "/printers": lambda p: PrintersPage(p),
#             "/jobcard": lambda p: JobCardPage(p),
#             "/login": lambda p: login_page(p),
#             "/profile": lambda p: ft.Text("Profile Page", size=20),
#             "/settings": lambda p: ft.Text("Settings Page", size=20),
#             "/notifications": lambda p: ft.Text("Notifications Page", size=20),
#             "/logout": lambda p: ft.Text("Logged Out - Redirecting...", size=20, on_create=lambda e: p.go("/login")),
#         }

#         try:
#             content = routes.get(page.route, lambda p: ft.Text("Page not found", size=20, color=ft.Colors.RED_600))(page)
#             print(f"Content for {page.route}: {content}")  # Debug the content
#             if content is None:
#                 content = ft.Text(f"Error: No content for {page.route}", size=20, color=ft.Colors.RED_600)
#             content_area.content = content
#             if top_bar_ref.current:
#                 top_bar_ref.current.content = TopBar(page, top_bar_ref=top_bar_ref)
#                 top_bar_ref.current.update()
#             page.update()
#         except Exception as e:
#             print(f"Error loading route {page.route}: {e}")
#             content_area.content = ft.Text(f"Error: {str(e)}", size=20, color=ft.Colors.RED_600)
#             page.update()

#     def view_pop(view):
#         if len(page.views) > 1:
#             page.views.pop()
#             page.go(page.views[-1].route)
#         else:
#             print("No more views to pop!")
#             page.go("/login")

#     # Update layout on window resize
#     def on_resize(e):
#         content_area.padding = get_content_padding()
#         print(f"Resized: Content padding={content_area.padding}")
#         page.update()

#     # Set initial layout with persistent TopBar
#     main_column = ft.Column(
#         controls=[
#             ft.Container(ref=top_bar_ref, content=TopBar(page, top_bar_ref=top_bar_ref)),
#             content_area,
#         ],
#         expand=True,
#         spacing=0,
#     )
#     initial_view = ft.View(
#         "/",
#         controls=[main_column],
#         padding=0,
#         bgcolor=ft.Colors.WHITE,
#     )
#     page.views.append(initial_view)

#     # Attach event handlers and initial navigation
#     page.on_resize = on_resize
#     page.on_route_change = change_route
#     page.on_view_pop = view_pop
#     page.update()
#     page.go("/asset")

# # Run in web browser mode with upload_dir set to match AssetFormPage's TEMP_DIR
# temp_dir = os.path.join(os.getcwd(), "temp")
# os.makedirs(temp_dir, exist_ok=True)
# ft.app(
#     target=main,
#     assets_dir="assets",
#     upload_dir=temp_dir,
#     view=ft.AppView.WEB_BROWSER,
#     route_url_strategy="hash",
#     port=8080,
# )


# import os
# os.environ["FLET_SECRET_KEY"] = "mysecret123"
# import flet as ft
# from pages.dashboard.home import Home
# from pages.dashboard.users import Users
# from pages.dashboard.asset import AssetPage
# from pages.dashboard.component import Component
# from pages.dashboard.saleforce2 import SaleForce2
# from pages.dashboard.category import Category
# from pages.dashboard.history import HistoryPage
# from pages.dashboard.department import Department
# from pages.dashboard.consumables import Consumables
# from pages.dashboard.user_department import UsersAndDepartmentsPage
# from pages.dashboard.printers import PrintersPage
# from pages.dashboard.jobcard import JobCardPage
# from pages.dashboard.login import login_page
# from nav.sidebar import TopBar

# def main(page: ft.Page):
#     page.title = "Asset Management System"
#     page.expand = True
#     page.scroll = "adaptive"
#     page.padding = 0
#     page.bgcolor = ft.Colors.BLUE_GREY_50
#     appbar_text_ref = ft.Ref[ft.Text]()

#     # Determine content area padding based on screen size
#     def get_content_padding():
#         window_width = page.window.width if page.window.width > 0 else 800
#         if window_width <= 600:  # Mobile
#             return ft.padding.symmetric(horizontal=10, vertical=5)
#         elif window_width <= 1024:  # Tablet
#             return ft.padding.symmetric(horizontal=15, vertical=10)
#         else:  # Desktop
#             return ft.padding.symmetric(horizontal=20, vertical=15)

#     # Create a fixed TopBar and scrollable content area
#     top_bar = TopBar(page)
#     content_area = ft.Container(
#         expand=True,
#         padding=get_content_padding(),  # Initial padding
#     )

#     def change_route(route):
#         print(f"Changing route to: {route}")

#         routes = {
#             "/dashboard": lambda p: Home(p),
#             "/user": lambda p: UsersAndDepartmentsPage(p),  # Corrected with lambda
#             "/asset": lambda p: AssetPage(p),
#             "/component": lambda p: Component(p),
#             "/saleforce": lambda p: SaleForce2(p),
#             "/history": lambda p: HistoryPage(p),
#             "/category": lambda p: Category(p),
#             "/department": lambda p: Department(p),
#             "/consumable": lambda p: Consumables(p),
#             "/printers": lambda p: PrintersPage(p),
#             "/jobcard": lambda p: JobCardPage(p),
#             "/login": lambda p: login_page(p),  # Use the login_page function
#             "/profile": lambda p: ft.Text("Profile Page", size=20),
#             "/settings": lambda p: ft.Text("Settings Page", size=20),
#             "/notifications": lambda p: ft.Text("Notifications Page", size=20),
#             "/logout": lambda p: ft.Text("Logged Out - Redirecting...", size=20, on_create=lambda e: p.go("/login")),
#         }

#         if page.route in routes:
#             content = routes[page.route](page)
#             content_area.content = ft.Column(
#                 controls=[content],
#                 expand=True,
#                 scroll=ft.ScrollMode.AUTO,
#                 spacing=0,
#             )
#         else:
#             content_area.content = ft.Column(
#                 controls=[
#                     ft.Text("Page not found", size=20, color=ft.Colors.RED_600),
#                 ],
#                 expand=True,
#                 scroll=ft.ScrollMode.AUTO,
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 spacing=0,
#             )
#         page.update()

#     def view_pop(view):
#         if len(page.views) > 1:
#             page.views.pop()
#             page.go(page.views[-1].route)
#         else:
#             print("No more views to pop!")
#             page.go("/login")

#     # Update layout on window resize
#     def on_resize(e):
#         content_area.padding = get_content_padding()
#         print(f"Resized: Content padding={content_area.padding}")
#         page.update()

#     # Set initial layout
#     page.views.append(
#         ft.View(
#             "/",
#             controls=[
#                 ft.Column(
#                     controls=[
#                         top_bar,  # Fixed TopBar
#                         content_area,  # Scrollable content area
#                     ],
#                     expand=True,
#                     spacing=0,
#                 ),
#             ],
#             padding=0,
#             bgcolor=ft.Colors.WHITE,
#         )
#     )

#     # Attach resize handler
#     page.on_resize = on_resize
#     page.on_route_change = change_route
#     page.on_view_pop = view_pop
#     page.go("/asset")  # Changed initial route to /dashboard

# # Run in web browser mode with upload_dir set to match AssetFormPage's TEMP_DIR
# temp_dir = os.path.join(os.getcwd(), "temp")
# os.makedirs(temp_dir, exist_ok=True)
# ft.app(
#     target=main,
#     assets_dir="assets",
#     upload_dir=temp_dir,  # Changed to match AssetFormPage's TEMP_DIR
#     view=ft.AppView.WEB_BROWSER,
#     route_url_strategy="hash",
#     port=8080,  # Uncommented and set to 8080 (or use os.getenv("PORT", "8080"))
#     # host="200.200.200.23",  # Uncomment if needed for specific hosting
# )


# import os
# os.environ["FLET_SECRET_KEY"] = "mysecret123"
# import flet as ft
# from pages.dashboard.home import Home
# from pages.dashboard.users import Users
# from pages.dashboard.asset import AssetPage
# from pages.dashboard.component import Component
# from pages.dashboard.saleforce2 import SaleForce2
# from pages.dashboard.category import Category
# from pages.dashboard.history import HistoryPage
# from pages.dashboard.department import Department
# from pages.dashboard.consumables import Consumables
# from pages.dashboard.user_department import UsersAndDepartmentsPage
# from pages.dashboard.printers import PrintersPage
# from pages.dashboard.jobcard import JobCardPage

# from nav.sidebar import TopBar

# def main(page: ft.Page):
#     page.title = "Asset Management System"
#     page.expand = True
#     page.scroll = "adaptive"
#     page.padding = 0
#     page.bgcolor = ft.Colors.BLUE_GREY_50
#     appbar_text_ref = ft.Ref[ft.Text]()

#     # Determine content area padding based on screen size
#     def get_content_padding():
#         window_width = page.window.width if page.window.width > 0 else 800
#         if window_width <= 600:  # Mobile
#             return ft.padding.symmetric(horizontal=10, vertical=5)
#         elif window_width <= 1024:  # Tablet
#             return ft.padding.symmetric(horizontal=15, vertical=10)
#         else:  # Desktop
#             return ft.padding.symmetric(horizontal=20, vertical=15)

#     # Create a fixed TopBar and scrollable content area
#     top_bar = TopBar(page)
#     content_area = ft.Container(
#         expand=True,
#         padding=get_content_padding(),  # Initial padding
#     )

#     def change_route(route):
#         print(f"Changing route to: {route}")

#         routes = {
#             "/dashboard": lambda p: Home(p),
#             "/user": lambda p: UsersAndDepartmentsPage(p),  # Corrected with lambda
#             "/asset": lambda p: AssetPage(p),
#             "/component": lambda p: Component(p),
#             "/saleforce": lambda p: SaleForce2(p),
#             "/history": lambda p: HistoryPage(p),
#             "/category": lambda p: Category(p),
#             "/department": lambda p: Department(p),
#             "/consumable": lambda p: Consumables(p),
#             "/printers": lambda p: PrintersPage(p),
#             "/jobcard": lambda p: JobCardPage(p),
#             "/login": lambda p: ft.Container(
#                 content=ft.Column([
#                     ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
#                     ft.TextField(label="Username", width=300),
#                     ft.TextField(label="Password", width=300, password=True),
#                     ft.ElevatedButton("Login", width=300, on_click=lambda e: p.go("/dashboard")),
#                 ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
#                 bgcolor=ft.Colors.BLUE_GREY_50,
#                 expand=True,
#             ),
#             "/profile": lambda p: ft.Text("Profile Page", size=20),
#             "/settings": lambda p: ft.Text("Settings Page", size=20),
#             "/notifications": lambda p: ft.Text("Notifications Page", size=20),
#             "/logout": lambda p: ft.Text("Logged Out - Redirecting...", size=20, on_create=lambda e: p.go("/login")),
#         }

#         if page.route in routes:
#             content = routes[page.route](page)
#             content_area.content = ft.Column(
#                 controls=[content],
#                 expand=True,
#                 scroll=ft.ScrollMode.AUTO,
#                 spacing=0,
#             )
#         else:
#             content_area.content = ft.Column(
#                 controls=[
#                     ft.Text("Page not found", size=20, color=ft.Colors.RED_600),
#                 ],
#                 expand=True,
#                 scroll=ft.ScrollMode.AUTO,
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 spacing=0,
#             )
#         page.update()

#     def view_pop(view):
#         if len(page.views) > 1:
#             page.views.pop()
#             page.go(page.views[-1].route)
#         else:
#             print("No more views to pop!")
#             page.go("/login")

#     # Update layout on window resize
#     def on_resize(e):
#         content_area.padding = get_content_padding()
#         print(f"Resized: Content padding={content_area.padding}")
#         page.update()

#     # Set initial layout
#     page.views.append(
#         ft.View(
#             "/",
#             controls=[
#                 ft.Column(
#                     controls=[
#                         top_bar,  # Fixed TopBar
#                         content_area,  # Scrollable content area
#                     ],
#                     expand=True,
#                     spacing=0,
#                 ),
#             ],
#             padding=0,
#             bgcolor=ft.Colors.WHITE,
#         )
#     )

#     # Attach resize handler
#     page.on_resize = on_resize
#     page.on_route_change = change_route
#     page.on_view_pop = view_pop
#     page.go("/dashboard")  # Changed initial route to /dashboard

# #Run in web browser mode with upload_dir set
# port = int(os.getenv("PORT", "8080"))
# ft.app(
#     target=main,
#     assets_dir="assets",
#     upload_dir="assets/images",  # Enable upload storage
#     view=ft.AppView.WEB_BROWSER,
#     route_url_strategy="hash",
#     # port=port,
#     # host="200.200.200.23",


# port = int(os.getenv("PORT", "8080"))
# ft.app(
#     target=main,
#     assets_dir="assets",
#     upload_dir="assets/images",  # Ensure uploads go to assets/images/                   # For Docker 22/04/2025
#     view=ft.WEB_BROWSER,  # Explicitly set to web mode for Docker
#     port=port,
#     host="0.0.0.0",
#     route_url_strategy="hash",
# )


# import os
# os.environ["FLET_SECRET_KEY"] = "mysecret123"
# import flet as ft
# from pages.dashboard.home import Home
# from pages.dashboard.users import Users
# #from components.userform import UserForm
# from pages.dashboard.asset import AssetPage
# #from components.assetform import AssetFormPage
# from pages.dashboard.component import Component
# from pages.dashboard.saleforce2 import SaleForce2
# from pages.dashboard.category import Category
# from pages.dashboard.history import HistoryPage
# #from components.assetdialog import AssetDialog
# from pages.dashboard.department import Department
# from nav.sidebar import TopBar  # Import the updated TopBar without sidebar toggle
# #from components.componentform import create_component_form
# #from pages.dashboard.consumable import consumables_page
# from pages.dashboard.consumables import Consumables
# from pages.dashboard.user_department import create_users_and_departments_page
# from pages.dashboard.printers import PrintersPage
# from pages.dashboard.jobcard import JobCardPage
# import os

# def main(page: ft.Page):
#     page.title = "Asset Management System"
#     page.expand = True
#     page.scroll = "adaptive"
#     page.padding = 0
#     page.bgcolor = ft.Colors.BLUE_GREY_50
#     appbar_text_ref = ft.Ref[ft.Text]()

#     # Determine content area padding based on screen size
#     def get_content_padding():
#         window_width = page.window.width if page.window.width > 0 else 800
#         if window_width <= 600:  # Mobile
#             return ft.padding.symmetric(horizontal=10, vertical=5)
#         elif window_width <= 1024:  # Tablet
#             return ft.padding.symmetric(horizontal=15, vertical=10)
#         else:  # Desktop
#             return ft.padding.symmetric(horizontal=20, vertical=15)

#     # Create a fixed TopBar and scrollable content area
#     top_bar = TopBar(page)
#     content_area = ft.Container(
#         expand=True,
#         padding=get_content_padding(),  # Initial padding
#     )

#     def change_route(route):
#         print(f"Changing route to: {route}")

#         routes = {
#             "/dashboard": Home,
#             "/user": create_users_and_departments_page(p),  # Use the function to create the page
#             #"/userform": UserForm,
#             "/asset": AssetPage,
#             #"/assetform": AssetFormPage,
#             "/component": Component,
#             "/saleforce": SaleForce2,
#             "/history": HistoryPage,
#             "/category": Category,
#             #"/componentform": create_component_form,
#             "/department": Department,
#             #"/assetformdialog": AssetDialog,
#             "/consumable": Consumables,
#             "/printers": PrintersPage,
#             "/jobcard": JobCardPage,
#             "/login": lambda page: ft.Container(
#                 content=ft.Column([
#                     ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
#                     ft.TextField(label="Username", width=300),
#                     ft.TextField(label="Password", width=300, password=True),
#                     ft.ElevatedButton("Login", width=300, on_click=lambda e: page.go("/dashboard")),
#                 ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
#                 bgcolor=ft.Colors.BLUE_GREY_50,
#                 expand=True,
#             ),
#             "/profile": lambda page: ft.Text("Profile Page", size=20),
#             "/settings": lambda page: ft.Text("Settings Page", size=20),
#             "/notifications": lambda page: ft.Text("Notifications Page", size=20),
#             "/logout": lambda page: ft.Text("Logged Out - Redirecting...", size=20, on_create=lambda e: page.go("/login")),
#         }

#         if page.route in routes:
#             content = routes[page.route](page)
#             content_area.content = ft.Column(
#                 controls=[content],
#                 expand=True,
#                 scroll=ft.ScrollMode.AUTO,
#                 spacing=0,
#             )
#         else:
#             content_area.content = ft.Column(
#                 controls=[
#                     ft.Text("Page not found", size=20, color=ft.Colors.RED_600),
#                 ],
#                 expand=True,
#                 scroll=ft.ScrollMode.AUTO,
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 spacing=0,
#             )
#         page.update()

#     def view_pop(view):
#         if len(page.views) > 1:
#             page.views.pop()
#             page.go(page.views[-1].route)
#         else:
#             print("No more views to pop!")
#             page.go("/login")

#     # Update layout on window resize
#     def on_resize(e):
#         content_area.padding = get_content_padding()
#         print(f"Resized: Content padding={content_area.padding}")
#         page.update()

#     # Set initial layout
#     page.views.append(
#         ft.View(
#             "/",
#             controls=[
#                 ft.Column(
#                     controls=[
#                         top_bar,  # Fixed TopBar
#                         content_area,  # Scrollable content area
#                     ],
#                     expand=True,
#                     spacing=0,
#                 ),
#             ],
#             padding=0,
#             bgcolor=ft.Colors.WHITE,
#         )
#     )

#     # Attach resize handler
#     page.on_resize = on_resize
#     page.on_route_change = change_route
#     page.on_view_pop = view_pop
#     page.go("/jobcard")

# #Run in web browser mode with upload_dir set
# # ft.app(
# #     target=main,
# #     assets_dir="assets",
# #     upload_dir="assets/images",  # Enable upload storage
# #     view=ft.AppView.WEB_BROWSER,
# #     route_url_strategy="hash",
# # )

# port = int(os.getenv("PORT", "8080"))
# ft.app(
#     target=main,
#     assets_dir="assets",
#     upload_dir="assets/images",  # Enable upload storage
#     view=ft.AppView.WEB_BROWSER,
#     route_url_strategy="hash",
#     port=port,
#     host="200.200.200.23",
# )
# port = int(os.getenv("PORT", "8080"))
# ft.app(
#     target=main,
#     assets_dir="assets",
#     upload_dir="assets/images",
#     view=ft.WEB_BROWSER,
#     port=port,
#     host="0.0.0.0",
#     route_url_strategy="hash",
#     upload_max_size=50 * 1024 * 1024,  # 50MB limit
# )




# import flet as ft
# from pages.dashboard.home import Home
# from pages.dashboard.users import Users
# from components.userform import UserForm
# from pages.dashboard.asset2 import AssetPagee
# from components.assetform import AssetFormPage
# from pages.dashboard.components import Components
# from pages.dashboard.saleforce import SaleForcePage
# from pages.dashboard.category import Category
# from components.assetdialog import AssetDialog
# from pages.dashboard.department import Department

# def main(page: ft.Page):
#     page.title = "Asset Management System"
#     page.expand = True
#     page.scroll = "adaptive"

#     # Function to handle route changes
#     def change_route(route):
#         """Handles navigation between different pages."""
#         page.views.clear()  # Ensure only one active view at a time

#         routes = {
#             "/dashboard": Home,
#             "/user": Users,
#             "/userform": UserForm,
#             "/asset": AssetPagee,
#             "/assetform": AssetFormPage,
#             "/component": Components,
#             "/saleforce": SaleForcePage,
#             "/category": Category,
#             "/department": Department,
#             "/assetformdialog": AssetDialog,
#         }

#         if page.route in routes:
#             page.views.append(ft.View(page.route, controls=[routes[page.route](page)]))
#         else:
#             page.views.append(ft.View("/", controls=[ft.Text("Page not found")]))
        
#         page.update()

#     def view_pop(view):
#         """Handles back navigation."""
#         if len(page.views) > 1:
#             page.views.pop()
#             page.go(page.views[-1].route)  # Ensure it redirects to the last valid route
#         else:
#             print("No more views to pop!")

#     # Assign event handlers
#     page.on_route_change = change_route
#     page.on_view_pop = view_pop

#     # Start the app at the dashboard page
#     page.go("/dashboard")

# #ft.app(target=main, assets_dir="assets", view=None, port=8080, host="0.0.0.0")      # for docker

# ft.app(target=main, assets_dir="assets",)   # for local
# #ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)   # for local browser
# #ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER, port=8080)   # for local browser with port

# #ft.app(target=main, view=ft.WEB_BROWSER)   # for github

