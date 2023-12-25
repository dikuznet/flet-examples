import asyncio

import flet as ft


class Countup(ft.UserControl):
    def __init__(self, seconds: int, queue: asyncio.Queue[int]) -> None:
        super().__init__()
        self.seconds = seconds
        self.queue = queue
        self.stop = True

    async def did_mount_async(self) -> None:
        self.running = True
        asyncio.create_task(self.update_timer())

    async def will_unmount_async(self) -> None:
        self.running = False

    async def update_timer(self) -> None:
        while self.running:
            try:
                item = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                item = None
            if item is not None:
                self.stop = True if item == -1 else False
                self.seconds = int(item)

            if not self.stop:
                self.seconds += 1
                mins, secs = divmod(self.seconds, 60)
                self.countup.value = "{:02d}:{:02d} sec".format(mins, secs)
                await self.update_async()
            await asyncio.sleep(1)

    def build(self) -> ft.Control:
        self.countup = ft.Text()
        return self.countup
