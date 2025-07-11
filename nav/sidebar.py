


import flet as ft

def TopBar(page: ft.Page, height=55, bg_color="#4682B4", top_bar_ref=None):
    """
    Creates a top bar matching the Snipe-IT design with logo, search bar, user profile, and a menu bar.
    
    Args:
        page (ft.Page): The Flet page instance.
        height (int): Height of the top bar (default: 80 to accommodate the menu bar).
        bg_color (str): Background color (default: #4682B4, matching the screenshot).
        top_bar_ref (ft.Ref): Reference to update the top bar.
    """
    def handle_logout(e):
        print("Logging out")
        page.session.set("user", None)
        page.close_dialog()
        page.go("/login")
        if top_bar_ref:
            top_bar_ref.current.update()

    # Logo (placeholder)
    logo = ft.Text("Asset Management", color=ft.Colors.WHITE, size=20)

    # Search bar
    # search_bar = ft.Container(
    #     content=ft.TextField(
    #         hint_text="Lookup by Asset Tag",
    #         width=200,
    #         height=35,
    #         bgcolor=ft.Colors.WHITE,
    #         border=ft.border.all(1, ft.Colors.GREY_300),
    #         border_radius=5,
    #         prefix_icon=ft.Icons.SEARCH,
    #         text_size=14,
    #         content_padding=ft.padding.symmetric(vertical=0, horizontal=10),
    #         visible=True,
    #     ),
    #     width=200,
    # )

    # Icons and user profile
    user = page.session.get("user")
    user_name = user.get("name", "Guest") if user else "Guest"
    is_admin = user.get("can_login", 0) == 1 if user else False
    user_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(
                text=user_name,
                on_click=lambda e: page.go("/profile") if user else None,
                disabled=not user,
            ),
            ft.PopupMenuItem(
                text="Create New",
                on_click=lambda e: page.go("/assetform") if user and is_admin else None,
                disabled=not user or not is_admin,
            ),
            ft.PopupMenuItem(
                text="Messages (57)",
                on_click=lambda e: page.go("/messages") if user else None,
                disabled=not user,
            ),
            ft.PopupMenuItem(
                text="Logout",
                on_click=handle_logout,
                disabled=not user,
            ),
        ],
        content=ft.Row([
            ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=24),
            ft.Text(user_name, color=ft.Colors.WHITE, size=14),
            ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.WHITE, size=18),
        ], spacing=5),
        tooltip="User Menu",
    )

    # Menu bar with submenu buttons
    menubar = ft.MenuBar(
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            bgcolor="#4682B4",
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.ALIAS,
                ft.ControlState.DEFAULT: ft.MouseCursor.BASIC,
            },
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Menu", color=ft.Colors.WHITE),
                leading=ft.Icon(ft.Icons.MENU, color=ft.Colors.WHITE),
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                ),
                tooltip="Menu",
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Dashboard"),
                        leading=ft.Icon(ft.Icons.DASHBOARD),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/dashboard") if user else None,
                        disabled=not user,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("JobCard"),
                        leading=ft.Icon(ft.Icons.CALL_ROUNDED),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/jobcard") if user else None,
                        disabled=not user,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Assets"),
                        leading=ft.Icon(ft.Icons.REPORT),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/asset") if user else None,
                        disabled=not user,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Components"),
                        leading=ft.Icon(ft.Icons.INVENTORY),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/component") if user else None,
                        disabled=not user,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Printers"),
                        leading=ft.Icon(ft.Icons.INVENTORY),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/printers") if user else None,
                        disabled=not user,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Users"),
                        leading=ft.Icon(ft.Icons.PEOPLE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/user") if user and is_admin else None,
                        disabled=not user or not is_admin,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Category"),
                        leading=ft.Icon(ft.Icons.LABEL),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/category") if user and is_admin else None,
                        disabled=not user or not is_admin,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Consumable"),
                        leading=ft.Icon(ft.Icons.LABEL),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/consumable") if user and is_admin else None,
                        disabled=not user or not is_admin,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Sale Force"),
                        leading=ft.Icon(ft.Icons.BUSINESS),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/saleforce") if user and is_admin else None,
                        disabled=not user or not is_admin,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Departments"),
                        leading=ft.Icon(ft.Icons.HDR_OFF_SELECT_OUTLINED),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/department") if user and is_admin else None,
                        disabled=not user or not is_admin,
                    ),
                ],
            ),
        ],
    )

    # settingbar = ft.MenuBar(
    #     style=ft.MenuStyle(
    #         alignment=ft.alignment.top_left,
    #         bgcolor=ft.Colors.GREEN,
    #         mouse_cursor={
    #             ft.ControlState.HOVERED: ft.MouseCursor.ALIAS,
    #             ft.ControlState.DEFAULT: ft.MouseCursor.BASIC,
    #         },
    #     ),
    #     controls=[
    #         ft.SubmenuButton(
    #             content=ft.Text("Setting"),
    #             controls=[
    #                 ft.MenuItemButton(
    #                     content=ft.Text("Profile"),
    #                     leading=ft.Icon(ft.Icons.PERSON),
    #                     style=ft.ButtonStyle(
    #                         bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
    #                     ),
    #                     on_click=lambda e: page.go("/profile") if user else None,
    #                     disabled=not user,
    #                 ),
    #                 ft.MenuItemButton(
    #                     content=ft.Text("Settings"),
    #                     leading=ft.Icon(ft.Icons.SETTINGS),
    #                     style=ft.ButtonStyle(
    #                         bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
    #                     ),
    #                     on_click=lambda e: page.go("/settings") if user else None,
    #                     disabled=not user,
    #                 ),
    #                 ft.MenuItemButton(
    #                     content=ft.Text("Notifications"),
    #                     leading=ft.Icon(ft.Icons.NOTIFICATIONS),
    #                     style=ft.ButtonStyle(
    #                         bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
    #                     ),
    #                     on_click=lambda e: page.go("/notifications") if user else None,
    #                     disabled=not user,
    #                 ),
    #             ],
    #         ),
    #     ],
    # )

    # Layout with the menu bar below the top bar elements
    return ft.Container(
        bgcolor=bg_color,
        padding=ft.padding.symmetric(vertical=10, horizontal=15),
        height=height,
        shadow=ft.BoxShadow(
            blur_radius=10,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        ),
        content=ft.Column([
            ft.Row([
                menubar,
                #settingbar,
                ft.Container(expand=True),  # Spacer
                #search_bar,
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ADD,
                        icon_color=ft.Colors.WHITE,
                        icon_size=24,
                        tooltip="Create New",
                        on_click=lambda e: page.go("/user") if user and is_admin else None,
                        style=ft.ButtonStyle(
                            bgcolor={"hovered": "#5A9BD5"},
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        disabled=not user or not is_admin,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.MESSAGE,
                        icon_color=ft.Colors.WHITE,
                        icon_size=24,
                        tooltip="Messages (57)",
                        on_click=lambda e: page.go("/messages") if user else None,
                        style=ft.ButtonStyle(
                            bgcolor={"hovered": "#5A9BD5"},
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        disabled=not user,
                    ),
                    user_menu,
                ], spacing=10),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], spacing=5),
    )
