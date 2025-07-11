



import flet as ft
from components.cards import MainCardsPage as MainCards
from components.chart import chart_page as ChartPage
from components.history_table import history_table as HistoryTable

class Home(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True

        # Set a light background with subtle gradient overlay
        self.page.bgcolor = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.Colors.with_opacity(0.1, ft.Colors.AMBER_50), ft.Colors.with_opacity(0.1, ft.Colors.TEAL_50)],
            tile_mode=ft.GradientTileMode.MIRROR
        )
        page.window.title = "Asset Management System"
        # page.window.width = 1500  # Set a reasonable default width
        # page.window.height = 900  # Set a reasonable default height

        # Buttons with enhanced styling and scale animation
        def create_button(text, icon, route, color, overlay_color):
            button_content = ft.ElevatedButton(
                text=text,
                color=ft.Colors.WHITE,
                icon=ft.Icon(name=icon),
                on_click=lambda e: page.go(route),
                style=ft.ButtonStyle(
                    bgcolor=color,
                    overlay_color=overlay_color,
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
                elevation=6,
                width=250,
                height=80,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(text, size=16, weight=ft.FontWeight.BOLD),
                            ft.Icon(name=icon, size=22),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=10,
                ),
            )

            def animate_hover(e):
                if e.data == "true":
                    container.scale = 1.1
                else:
                    container.scale = 1.0
                container.update()

            container = ft.Container(
                content=button_content,
                scale=1.0,
                animate_scale=ft.Animation(duration=200, curve=ft.AnimationCurve.EASE_IN_OUT)
            )
            container.on_hover = animate_hover
            return container

        jobcard_button = create_button("Job Card", "WORK", "/jobcard", ft.Colors.BLUE_600, ft.Colors.BLUE_GREY_300)
        asset_button = create_button("Asset", "COMPUTER", "/asset", ft.Colors.YELLOW_ACCENT_700, ft.Colors.CYAN_900)
        component_button = create_button("Component", "PIE_CHART", "/component", ft.Colors.TEAL_ACCENT_700, ft.Colors.TEAL_ACCENT)
        device_button = create_button("SaleForce Device", "DEVICE_HUB", "/device", ft.Colors.GREEN_ACCENT_700, ft.Colors.LIGHT_GREEN_400)
        consumeable_button = create_button("Consumable", "INVENTORY", "/consumeable", ft.Colors.RED_ACCENT, ft.Colors.TEAL_ACCENT_400)

        # Styled header
        # header = ft.Container(
        #     content=ft.Row(
        #         [
        #             ft.Text(
        #                 "Asset Management Dashboard",
        #                 size=28,
        #                 weight=ft.FontWeight.BOLD,
        #                 color=ft.Colors.TEAL_ACCENT_100,
        #             ),
        #         ],
        #         alignment=ft.MainAxisAlignment.CENTER,
        #     ),
        #     padding=20,
        #     bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.AMBER_100),
        #     border_radius=10,
        #     shadow=ft.BoxShadow(
        #         spread_radius=2,
        #         blur_radius=15,
        #         color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
        #         offset=ft.Offset(0, 4),
        #     ),
        # )

        # Main content with enhanced styling
        main_content = ft.Column(
            controls=[
                # header,
                ft.Container(
                    content=ft.Row(
                        controls=[
                            jobcard_button,
                            asset_button,
                            component_button,
                            device_button,
                            consumeable_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                        spacing=20,
                    ),
                    padding=15,
                    margin=ft.margin.only(top=10),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.CYAN_50),
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.2, ft.Colors.CYAN_200),
                        offset=ft.Offset(0, 3),
                    ),
                ),
                ft.Container(
                    content=MainCards(page),
                    padding=15,
                    margin=ft.margin.only(top=15),
                    bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.AMBER_100),
                    border=ft.border.all(1, ft.Colors.TEAL_300),
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                        offset=ft.Offset(0, 5),
                    ),
                ),
                ft.Container(
                    content=ChartPage(page),
                    width=1400,
                    height=700,
                    padding=15,
                    margin=ft.margin.only(top=15),
                    bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.TEAL_100),
                    border=ft.border.all(1, ft.Colors.TEAL_300),
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                        offset=ft.Offset(0, 5),
                    ),
                    expand=False,
                ),
                ft.Container(
                    content=HistoryTable(page),
                    padding=15,
                    margin=ft.margin.only(top=15),
                    bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.CYAN_100),
                    border=ft.border.all(1, ft.Colors.TEAL_300),
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                        offset=ft.Offset(0, 5),
                    ),
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        # Enhanced outer container with light gradient
        self.content = ft.Container(
            content=ft.Column(
                controls=[main_content],
                expand=True,
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            border_radius=15,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.with_opacity(0.1, ft.Colors.AMBER_100), ft.Colors.with_opacity(0.1, ft.Colors.TEAL_100)]
            ),
            expand=True,
        )

def home_page(page):
    home = Home(page)
    page.add(home)
    page.update()
    return home



# import flet as ft
# from components.cards import MainCardsPage as MainCards
# from components.chart import chart_page as ChartPage
# from components.history_table import history_table as HistoryTable
# import flet_lottie as fl

# class Home(ft.Container):
#     def __init__(self, page: ft.Page):
#         super().__init__()
#         self.page = page
#         self.expand = True

#         # Set a light background with subtle gradient overlay
#         self.page.bgcolor = ft.LinearGradient(
#             begin=ft.alignment.top_left,
#             end=ft.alignment.bottom_right,
#             colors=[ft.Colors.with_opacity(0.1, ft.Colors.AMBER_50), ft.Colors.with_opacity(0.1, ft.Colors.TEAL_50)],
#             tile_mode=ft.GradientTileMode.MIRROR
#         )
#         page.window.title = "Asset Management System"
#         page.window.width = 1500  # Set a reasonable default width
#         page.window.height = 900  # Set a reasonable default height

#         # Buttons with enhanced styling and scale animation
#         def create_button(text, icon, route, color, overlay_color):
#             button_content = ft.ElevatedButton(
#                 text=text,
#                 color=ft.Colors.WHITE,
#                 icon=ft.Icon(name=icon),
#                 on_click=lambda e: page.go(route),
#                 style=ft.ButtonStyle(
#                     bgcolor=color,
#                     overlay_color=overlay_color,
#                     shape=ft.RoundedRectangleBorder(radius=20),
#                 ),
#                 elevation=6,
#                 width=250,
#                 height=80,
#                 content=ft.Container(
#                     content=ft.Column(
#                         [
#                             ft.Text(text, size=16, weight=ft.FontWeight.BOLD),
#                             ft.Icon(name=icon, size=22),
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                     ),
#                     padding=10,
#                 ),
#             )

#             def animate_hover(e):
#                 if e.data == "true":
#                     container.scale = 1.1
#                 else:
#                     container.scale = 1.0
#                 container.update()

#             container = ft.Container(
#                 content=button_content,
#                 scale=1.0,
#                 animate_scale=ft.Animation(duration=200, curve=ft.AnimationCurve.EASE_IN_OUT)
#             )
#             container.on_hover = animate_hover
#             return container

#         jobcard_button = create_button("Job Card", "WORK", "/jobcard", ft.Colors.DEEP_ORANGE_200, ft.Colors.DEEP_ORANGE_300)
#         asset_button = create_button("Asset", "COMPUTER", "/asset", ft.Colors.AMBER_300, ft.Colors.AMBER_400)
#         component_button = create_button("Component", "PIE_CHART", "/component", ft.Colors.ORANGE_300, ft.Colors.ORANGE_400)
#         device_button = create_button("SaleForce Device", "DEVICE_HUB", "/device", ft.Colors.LIGHT_GREEN_300, ft.Colors.LIGHT_GREEN_400)
#         consumeable_button = create_button("Consumable", "INVENTORY", "/consumeable", ft.Colors.TEAL_300, ft.Colors.TEAL_400)

#         # Styled header with custom Lottie animation
#         header = ft.Container(
#             content=ft.Row(
#                 [
#                     fl.Lottie(
#                     src="gujranwala_food_industries.json",  # Replace with your file path
#                     animate=True,
#                     repeat=True,
#                     reverse=False,
#                     width=200,
#                     height=50,
#                 )
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#             ),
#             padding=20,
#             bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.AMBER_100),
#             border_radius=10,
#             shadow=ft.BoxShadow(
#                 spread_radius=2,
#                 blur_radius=15,
#                 color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
#                 offset=ft.Offset(0, 4),
#             ),
#         )

#         # Main content with enhanced styling
#         main_content = ft.Column(
#             controls=[
#                 header,
#                 ft.Container(
#                     content=ft.Row(
#                         controls=[
#                             jobcard_button,
#                             asset_button,
#                             component_button,
#                             device_button,
#                             consumeable_button,
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         wrap=True,
#                         spacing=20,
#                     ),
#                     padding=15,
#                     margin=ft.margin.only(top=10),
#                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.AMBER_50),
#                     border_radius=12,
#                     shadow=ft.BoxShadow(
#                         spread_radius=1,
#                         blur_radius=10,
#                         color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
#                         offset=ft.Offset(0, 3),
#                     ),
#                 ),
#                 ft.Container(
#                     content=MainCards(page),
#                     padding=15,
#                     margin=ft.margin.only(top=15),
#                     bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.AMBER_100),
#                     border=ft.border.all(1, ft.Colors.TEAL_300),
#                     border_radius=12,
#                     shadow=ft.BoxShadow(
#                         spread_radius=2,
#                         blur_radius=15,
#                         color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
#                         offset=ft.Offset(0, 5),
#                     ),
#                 ),
#                 ft.Container(
#                     content=ChartPage(page),
#                     width=1400,
#                     height=700,
#                     padding=15,
#                     margin=ft.margin.only(top=15),
#                     bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.TEAL_100),
#                     border=ft.border.all(1, ft.Colors.TEAL_300),
#                     border_radius=12,
#                     shadow=ft.BoxShadow(
#                         spread_radius=2,
#                         blur_radius=15,
#                         color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
#                         offset=ft.Offset(0, 5),
#                     ),
#                     expand=False,
#                 ),
#                 ft.Container(
#                     content=HistoryTable(page),
#                     padding=15,
#                     margin=ft.margin.only(top=15),
#                     bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.CYAN_100),
#                     border=ft.border.all(1, ft.Colors.TEAL_300),
#                     border_radius=12,
#                     shadow=ft.BoxShadow(
#                         spread_radius=2,
#                         blur_radius=15,
#                         color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
#                         offset=ft.Offset(0, 5),
#                     ),
#                 ),
#             ],
#             spacing=20,
#             alignment=ft.MainAxisAlignment.START,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             expand=True,
#         )

#         # Enhanced outer container with light gradient
#         self.content = ft.Container(
#             content=ft.Column(
#                 controls=[main_content],
#                 expand=True,
#                 spacing=20,
#                 alignment=ft.MainAxisAlignment.CENTER,
#             ),
#             padding=20,
#             border_radius=15,
#             gradient=ft.LinearGradient(
#                 begin=ft.alignment.top_left,
#                 end=ft.alignment.bottom_right,
#                 colors=[ft.Colors.with_opacity(0.1, ft.Colors.AMBER_100), ft.Colors.with_opacity(0.1, ft.Colors.TEAL_100)]
#             ),
#             expand=True,
#         )

# def home_page(page):
#     home = Home(page)
#     page.add(home)
#     page.update()
#     return home