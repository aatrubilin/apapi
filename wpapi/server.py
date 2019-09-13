import os
import logging

from app import app
from weather_services import OpenWeatherMapAPI, FakeWeatherAPI

DEBUG = os.environ.get("FLASK_ENV", "production") == "dev"

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="[%(levelname)-5s] <%(name)-10s> %(lineno)-4s - %(message)s'",
)

if __name__ == "__main__":
    token = os.environ.get("WEATHER_API_TOKEN", None)

    novosibirsk = OpenWeatherMapAPI(lat=55.03, lon=82.92, token=token, timeout_sec=2)
    app.register_api(novosibirsk, url_prefix=None)

    moscow = OpenWeatherMapAPI(lat=55.75, lon=37.6, token=token, timeout_sec=2)
    app.register_api(novosibirsk, url_prefix="/msk")

    fake = FakeWeatherAPI()
    app.register_api(fake, "/fake")

    app.run()
