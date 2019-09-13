import random
import logging

import requests

from dateutil.tz import tzoffset
from datetime import datetime

from .base import WeatherAPI

logger = logging.getLogger(__name__)


class FakeWeatherAPI(WeatherAPI):
    """This class is fake api and returns random values"""

    def __init__(self, *args, **kwargs):
        """Fake weather API class"""
        super(FakeWeatherAPI, self).__init__(*args, **kwargs)

    @property
    def location(self):
        location_ = {"lat": random.randint(-90, 90), "lon": random.randint(-180, 180)}
        return location_

    @property
    def title(self):
        return "Fake place"

    @property
    def timestamp(self):
        return datetime.now(tzoffset("", 0)).isoformat()

    @property
    def temperature(self):
        return random.randint(-40, 40)

    @property
    def humidity(self):
        return random.randint(0, 100)

    @property
    def pressure(self):
        return random.randint(700, 800)

    def update_weather(self):
        update_result = "Success"
        self.last_updated = datetime.utcnow()

        return update_result
