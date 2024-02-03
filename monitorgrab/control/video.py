import asyncio
import base64
import platform
import mss
import numpy

import cv2
import flet as ft


class VideoControl(ft.UserControl):
    def __init__(self, seconds, queue):
        super().__init__()
        self.seconds = seconds
        self.queue = queue
        self.streming = True
        self.cam_index = 0
        self.sct = mss.mss()
        self.monitor_number = 2


    async def did_mount_async(self):
        self.running = True
        asyncio.create_task(self.update_timer())

    async def will_unmount_async(self):
        self.running = False
        self.cap.release()

    async def update_timer(self):
        while self.running:
            if self.streming: #and self.cap.isOpened():
                self.mon = self.sct.monitors[self.monitor_number]
                self.monitor = {
                "top": self.mon["top"],  # 100px from the top
                "left": self.mon["left"],  # 100px from the left
                "width": self.mon["width"],
                "height": self.mon["height"],
                "mon": self.monitor_number,
                }
                raw = self.sct.grab(self.monitor)
                buffer = cv2.imencode('.jpg', numpy.array(raw))[1].tobytes()
                self.image_string = base64.b64encode(buffer).decode("utf-8")
                self.img.src_base64 = self.image_string
                await self.update_async()
            await asyncio.sleep(0.01)

    async def send_message_click(self, e):
        await self.queue.put(0)

    async def start_click(self, e):
        self.streming = True
        await self.queue.put(0)

    async def stop_click(self, e):
        self.streming = False
        await self.queue.put(-1)

    def build(self):
                
        self.img = ft.Image(src=False,fit=ft.ImageFit.CONTAIN)
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
