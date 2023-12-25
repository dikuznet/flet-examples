import asyncio
import base64
import platform

import cv2
import flet as ft


class VideoControl(ft.UserControl):
    def __init__(self, seconds: int, queue: asyncio.Queue[int]) -> None:
        super().__init__()
        self.seconds = seconds
        self.queue = queue
        self.streming = False

    async def did_mount_async(self) -> None:
        self.running = True
        asyncio.create_task(self.update_timer())

    async def will_unmount_async(self) -> None:
        self.running = False
        self.cap.release()

    async def update_timer(self) -> None:
        while self.running:
            if self.streming and self.cap.isOpened():
                success, frame = self.cap.read()
                ret, buffer = cv2.imencode(".jpg", frame)
                self.image_string = base64.b64encode(buffer).decode("utf-8")
                self.img.src_base64 = self.image_string
                await self.update_async()
            await asyncio.sleep(0.01)

    async def send_message_click(self, _) -> None:
        await self.queue.put(0)

    async def start_click(self, _) -> None:
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        self.streming = True
        await self.queue.put(0)

    async def stop_click(self, _) -> None:
        self.streming = False
        await self.queue.put(-1)

    def build(self) -> ft.Control:
        if self.cap.isOpened():
            success, frame = self.cap.read()
            ret, buffer = cv2.imencode(".jpg", frame)
            self.image_string = base64.b64encode(buffer).decode("utf-8")
            self.img = ft.Image(src_base64=self.image_string)
        else:
            self.img = ft.Image(src=False)

        return ft.Column(
            [
                self.img,
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.PLAY_CIRCLE,
                            tooltip="Start stream",
                            on_click=self.start_click,
                        ),
                        ft.IconButton(
                            icon=ft.icons.STOP_CIRCLE_SHARP,
                            tooltip="Stop stream",
                            on_click=self.stop_click,
                        ),
                    ]
                ),
            ]
        )
