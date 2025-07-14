


import flet as ft
import mysql.connector

class ChartPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Chart styling constants
        normal_radius = 150
        hover_radius = 170
        normal_title_style = ft.TextStyle(
            size=16,  # Normal text size
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        hover_title_style = ft.TextStyle(
            size=20,  # Hover text size
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
        )
        normal_badge_size = 60

        def badge(icon, size):
            return ft.Container(
                content=ft.Icon(icon, size=size * 0.6),
                width=size,
                height=size,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=size / 2,
                bgcolor=ft.Colors.WHITE,
                alignment=ft.alignment.center,
            )

        def fetch_chart_data():
            try:
                connection = mysql.connector.connect(
                    host="200.200.201.100",
                    user="root",
                    password="Pak@123",
                    database="asm_sys"
                )
                cursor = connection.cursor()

                cursor.execute("SELECT status, COUNT(*) as count FROM job_cards GROUP BY status")
                job_data = {row[0]: row[1] for row in cursor.fetchall()}
                job_open = job_data.get("Open", 0)
                job_started = job_data.get("Started", 0)
                job_closed = job_data.get("Completed", 0)

                cursor.execute("SELECT status, COUNT(*) as count FROM assets GROUP BY status")
                asset_data = {row[0]: row[1] for row in cursor.fetchall()}
                asset_available = asset_data.get("Available", 0)
                asset_deployed = sum(1 for status in asset_data if "deployed" in status.lower()) or 0
                asset_disposed = asset_data.get("Disposed", 0)

                cursor.execute("SELECT status, COUNT(*) as count FROM consumables GROUP BY status")
                consumable_data = {row[0]: row[1] for row in cursor.fetchall()}
                consumable_available = consumable_data.get("Available", 0)
                consumable_deployed = consumable_data.get("Deployed", 0)
                consumable_consumed = consumable_data.get("Consumed", 0)

                data = {
                    "job": {"Open": job_open, "Started": job_started, "Closed": job_closed},
                    "asset": {"Available": asset_available, "Deployed": asset_deployed, "Disposed": asset_disposed},
                    "consumable": {"Available": consumable_available, "Deployed": consumable_deployed, "Consumed": consumable_consumed},
                }
                print(f"Chart data fetched: {data}")  # Debug output
                return data

            except mysql.connector.Error as err:
                print(f"Error fetching chart data: {err}")
                return {
                    "job": {"Open": 30, "Started": 20, "Closed": 50},
                    "asset": {"Available": 40, "Deployed": 30, "Disposed": 30},
                    "consumable": {"Available": 25, "Deployed": 35, "Consumed": 40},
                }
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'connection' in locals():
                    connection.close()

        # Fetch data
        chart_data = fetch_chart_data()

        # Job Cards Chart
        def on_job_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(job_chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            job_chart.update()

        job_chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    chart_data["job"]["Open"],
                    title=f"Open: {chart_data['job']['Open']}",
                    title_style=normal_title_style,
                    color=ft.Colors.BLUE,
                    radius=normal_radius,
                    badge=badge(ft.Icons.HOURGLASS_EMPTY, normal_badge_size),
                    badge_position=0.98,
                ) if chart_data["job"]["Open"] > 0 else None,
                ft.PieChartSection(
                    chart_data["job"]["Started"],
                    title=f"Started: {chart_data['job']['Started']}",
                    title_style=normal_title_style,
                    color=ft.Colors.YELLOW,
                    radius=normal_radius,
                    badge=badge(ft.Icons.PLAY_ARROW, normal_badge_size),
                    badge_position=0.98,
                ) if chart_data["job"]["Started"] > 0 else None,
                ft.PieChartSection(
                    chart_data["job"]["Closed"],
                    title=f"Closed: {chart_data['job']['Closed']}",
                    title_style=normal_title_style,
                    color=ft.Colors.GREEN,
                    radius=normal_radius,
                    badge=badge(ft.Icons.CHECK_CIRCLE, normal_badge_size),
                    badge_position=0.98,
                ) if chart_data["job"]["Closed"] > 0 else None,
            ],
            sections_space=5,
            center_space_radius=40,
            on_chart_event=on_job_chart_event,
            expand=True,
        )
        job_chart.sections = [s for s in job_chart.sections if s is not None]  # Filter out None

        # Asset Chart
        def on_asset_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(asset_chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            asset_chart.update()

        asset_chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    chart_data["asset"]["Available"],
                    title=f"Available: {chart_data['asset']['Available']}",
                    title_style=normal_title_style,
                    color=ft.Colors.BLUE,
                    radius=normal_radius,
                    badge=badge(ft.Icons.CHECK, normal_badge_size),
                    badge_position=0.98,
                ) if chart_data["asset"]["Available"] > 0 else None,
                ft.PieChartSection(
                    chart_data["asset"]["Deployed"],
                    title=f"Deployed: {chart_data['asset']['Deployed']}",
                    title_style=normal_title_style,
                    color=ft.Colors.YELLOW,
                    radius=normal_radius,
                    badge=badge(ft.Icons.SEND, normal_badge_size),
                    badge_position=0.98,
                ) if chart_data["asset"]["Deployed"] > 0 else None,
                ft.PieChartSection(
                    chart_data["asset"]["Disposed"],
                    title=f"Disposed: {chart_data['asset']['Disposed']}",
                    title_style=normal_title_style,
                    color=ft.Colors.RED,
                    radius=normal_radius,
                    badge=badge(ft.Icons.DELETE, normal_badge_size),
                    badge_position=0.98,
                ) if chart_data["asset"]["Disposed"] > 0 else None,
            ],
            sections_space=5,
            center_space_radius=40,
            on_chart_event=on_asset_chart_event,
            expand=True,
        )
        asset_chart.sections = [s for s in asset_chart.sections if s is not None]  # Filter out None

        # Consumable Chart
        def on_consumable_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(consumable_chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            consumable_chart.update()

        consumable_chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    chart_data["consumable"]["Available"],
                    title=f"Available: {chart_data['consumable']['Available']}",
                    title_style=normal_title_style,
                    color=ft.Colors.BLUE,
                    radius=normal_radius,
                    badge=badge(ft.Icons.INVENTORY, normal_badge_size),
                    badge_position=0.98,
                ) if chart_data["consumable"]["Available"] > 0 else None,
                ft.PieChartSection(
                    chart_data["consumable"]["Deployed"],
                    title=f"Deployed: {chart_data['consumable']['Deployed']}",
                    title_style=normal_title_style,
                    color=ft.Colors.YELLOW,
                    radius=normal_radius,
                    badge=badge(ft.Icons.SEND, normal_badge_size),
                    badge_position=0.98,
                ) if chart_data["consumable"]["Deployed"] > 0 else None,
                ft.PieChartSection(
                    chart_data["consumable"]["Consumed"],
                    title=f"Consumed: {chart_data['consumable']['Consumed']}",
                    title_style=normal_title_style,
                    color=ft.Colors.RED,
                    radius=normal_radius,
                    badge=badge(ft.Icons.REMOVE_CIRCLE, normal_badge_size),
                    badge_position=0.98,
                ) if chart_data["consumable"]["Consumed"] > 0 else None,
            ],
            sections_space=5,
            center_space_radius=40,
            on_chart_event=on_consumable_chart_event,
            expand=True,
        )
        consumable_chart.sections = [s for s in consumable_chart.sections if s is not None]  # Filter out None

        # Wrap charts in a Row for side-by-side display
        self.content = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Job Cards Status",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK87,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            job_chart,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                        offset=ft.Offset(0, 5),
                    ),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Asset Status",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK87,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            asset_chart,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                        offset=ft.Offset(0, 5),
                    ),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Consumables Status",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK87,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            consumable_chart,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                        offset=ft.Offset(0, 5),
                    ),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
        print("ChartPage initialized with content")  # Debug output

def chart_page(page):
    return ChartPage(page)