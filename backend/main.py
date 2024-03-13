import os

# Main dependencies
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from config import get_app_settings

from cassandra.cqlengine.management import sync_table
from repositories import BasePrices, DiscountPrices


from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


directory = 'D:/projects/HAKATON_5/app/build/static'
#directory = '/root/purplehack/build/static'

path = 'D:/projects/HAKATON_5/app/build/'
#path = '/root/purplehack/build/'
def get_application() -> FastAPI:
    settings = get_app_settings()
    application = FastAPI(**settings.fastapi_kwargs)


    application.mount("/static", StaticFiles(directory=directory), name="static")

    application.add_event_handler(
        "startup",
        on_startup,
    )

    application.add_event_handler(
        "shutdown",
        on_shutdown,
    )

    application.include_router(api_router)

    return application


# Process startup events
def on_startup():
    pass


# Process startup events
def on_shutdown():
    pass


app = get_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    sync_table(BasePrices)
    sync_table(DiscountPrices)
# Маршрут для обслуживания index.html
@app.get("/")
async def serve_index(request: Request):
    file_path = os.path.join(path, "index.html")
    return FileResponse(file_path)
