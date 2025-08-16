from fastapi import FastAPI
from uvicorn import run
from config.env import PORT, DEBUG
from routes.clients import clients_route
from routes.login import login_route
from routes.favorites import favorites_route
import logging

logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s [%(name)s] [%(levelname)s] - %(message)s",)


app = FastAPI(debug=DEBUG)
app.include_router(clients_route)
app.include_router(login_route)
app.include_router(favorites_route)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=PORT)