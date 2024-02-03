import asyncio
import sys

import flet as ft
from control.counter import Countup
from control.video import VideoControl


async def main(page: ft.Page):
    page.title = "Video capture example"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    queue: asyncio.Queue[int] = asyncio.Queue()
    await page.add_async(
        ft.Column(scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            controls=
            [
                VideoControl(0, queue),
                Countup(0, queue),
                # ft.Text("Video capture example: ", size=10, weight="bold"),
            ]
        )
    )


if __name__ == "__main__":
    if "webview" in sys.argv:
        print("Run in WEB BROWSER")
        ft.app(target=main, view=ft.WEB_BROWSER)
    else:
        print("Run desktop app")
        ft.app(target=main)
