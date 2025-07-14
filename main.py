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

# Preload view factories to avoid repeated imports or initialization
VIEW_FACTORIES = {
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
        page.bgcolor = ft.Colors.RED
        top_bar_ref = ft.Ref[ft.Container]()

        def get_content_padding():
            window_width = page.window.width if page.window.width > 0 else 800
            return (ft.padding.symmetric(horizontal=20, vertical=15) if window_width > 1024 
                    else ft.padding.symmetric(horizontal=15, vertical=10) if window_width > 600 
                    else ft.padding.symmetric(horizontal=10, vertical=5))

        # Initialize content area with a placeholder
        content_area = ft.Container(
            expand=True,
            padding=get_content_padding(),
            content=ft.Text("Loading...", size=20),
            ref=ft.Ref[ft.Container](),  # Add ref for content updates
        )

        # Preload initial content (e.g., login page)
        current_content = VIEW_FACTORIES.get("/login", lambda p: ft.Text("Page not found", size=20, color=ft.Colors.RED_600))(page)
        if isinstance(current_content, ft.Control):
            content_area.content = ft.Column([current_content], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)

        def change_route(e: ft.RouteChangeEvent):
            """Handle route changes efficiently."""
            route = e.route  # Extract the route string from the RouteChangeEvent
            print(f"Changing route to: {route}")
            if not route or route not in VIEW_FACTORIES:
                route = "/login"  # Default to login if route is invalid

            # Check authentication
            user = page.session.get("user")
            print(f"Authentication status for route {route}: {user is not None}")
            if route != "/login" and user is None:  # Protect all routes except /login
                page.go("/login")
                return

            # Update content
            new_content = VIEW_FACTORIES[route](page)
            if isinstance(new_content, ft.Control):
                content_area.content = ft.Column([new_content], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
            else:
                content_area.content = ft.Column([ft.Text("Invalid content", size=20, color=ft.Colors.RED_600)], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)

            # Update top bar and page in one call
            if top_bar_ref.current:
                top_bar_ref.current.content = TopBar(page, top_bar_ref=top_bar_ref)
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
        page.go("/jobcard")  # Initial route

    except Exception as e:
        print(f"Critical error in main: {e}")
        if page is not None:
            page.add(ft.Text(f"Critical Error: {e}", color=ft.Colors.RED_600))
            page.update()

    # Ensure temp directory exists
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)

# Run the app
temp_dir = os.path.join(os.getcwd(), "temp")
os.makedirs(temp_dir, exist_ok=True)
ft.app(
    target=main,
    assets_dir="assets",
    upload_dir=temp_dir,
    view=None,
    route_url_strategy="hash",
    port=8080,
    host="0.0.0.0",
)
