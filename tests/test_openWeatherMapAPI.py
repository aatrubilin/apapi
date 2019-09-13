import os
import time
import logging
import threading

import pytest

from weather_services import OpenWeatherMapAPI

logging.basicConfig(
    level=logging.WARNING,
    format="[%(levelname)-5s] <%(name)-10s> %(lineno)-4s - %(message)s'",
)

logger = logging.getLogger(__name__)

token = os.environ.get("WEATHER_API_TOKEN")
if not token:
    raise RuntimeError("WEATHER_API_TOKEN env variable not found")

LATITUDE = 55
LONGITUDE = 83
TIMEOUT_SEC = 2


class TestOpenWeatherMapAPI:
    def setup(self):
        self.api = OpenWeatherMapAPI(
            lat=LATITUDE, lon=LONGITUDE, token=token, timeout_sec=TIMEOUT_SEC
        )
        self.last_updated = self.api.last_updated
        self.current = {
            "location": self.api.location,
            "title": self.api.title,
            "timestamp": self.api.timestamp,
            "temperature": {"C": self.api.temperature},
            "humidity": {"percent": self.api.humidity},
            "pressure": {"atm": self.api.pressure},
        }

    def test_location(self):
        assert self.api.location is not None
        assert isinstance(self.api.location, dict) is True
        assert self.api.location["lat"] == LATITUDE
        assert self.api.location["lon"] == LONGITUDE

    def test_title(self):
        assert self.api.title == "Novosibirsk"

    def test_temperature(self):
        assert self.api.temperature is not None
        assert isinstance(self.api.temperature, (int, float)) is True
        logger.info("temperature: %r", self.api.temperature)

    def test_humidity(self):
        assert self.api.humidity is not None
        assert isinstance(self.api.humidity, (int, float)) is True
        logger.info("humidity: %r", self.api.humidity)

    def test_pressure(self):
        assert self.api.pressure is not None
        assert isinstance(self.api.pressure, (int, float)) is True
        logger.info("pressure: %r", self.api.pressure)

    def test_current(self):
        assert self.current == self.api.current

    def test_update_weather(self):
        assert self.last_updated is not None
        self.api.update_weather()
        assert self.last_updated == self.api.last_updated

        time.sleep(TIMEOUT_SEC)
        self.api.update_weather()
        assert self.last_updated != self.api.last_updated

    def test_multiple_requests(self):
        n = 2000
        last_updated = self.api.last_updated
        last_updated_list = []

        def check_update():
            del last_updated_list[:]

            threads = []
            for _ in range(n):
                thread = threading.Thread(
                    target=lambda: (
                        self.api.current,
                        last_updated_list.append(self.api.last_updated),
                    )
                )
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        check_update()
        assert all([dt == last_updated for dt in last_updated_list])

        time.sleep(TIMEOUT_SEC - 2)
        check_update()
        assert all([dt == last_updated for dt in last_updated_list])

        time.sleep(2)
        check_update()
        assert all([dt != last_updated for dt in last_updated_list])
