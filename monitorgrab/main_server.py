import flet_fastapi
from main_page import main


app = flet_fastapi.FastAPI()
app.mount("/", flet_fastapi.app(main))
