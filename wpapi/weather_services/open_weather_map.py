import os
import logging

import requests
from dateutil.tz import tzoffset
from datetime import datetime

from .base import WeatherAPI, WeatherError

logger = logging.getLogger(__name__)


class OpenWeatherMapError(WeatherError):
    """Exception for OpenWeatherMapAPI exceptions"""

    pass


class OpenWeatherMapAPI(WeatherAPI):
    _API_URL = "https://api.openweathermap.org/data/2.5/weather"
    _REQUEST_TIMEOUT = 2

    def __init__(self, *args, **kwargs):
        """OpenWeatherMap API class

        See Also:
            https://openweathermap.org/current

        Args:
            lat (int | float): City geo location, latitude
            lon (int | float): City geo location, longitude
            token (str): OpenWeatherMap API key
            timeout_sec (int, optional): Min seconds between requests to API.
                By current free price we can call api no more then 60 times
                per minute. You change this parameter to set min time between
                calls to api. Don't set it less then 1 sec on free price.
        """
        super(OpenWeatherMapAPI, self).__init__(*args, **kwargs)

        token = kwargs.get("token") or os.environ.get("WEATHER_API_TOKEN", None)
        if token is None:
            raise TypeError(
                "{} require environment variable 'WEATHER_API_TOKEN'\n"
                "More info: https://openweathermap.org/appid".format(
                    self.__class__.__name__
                )
            )

        lat = kwargs.get("lat")
        if lat is None:
            raise TypeError("Latitude is not specified")
        if lat < -90 or lat > 90:
            raise TypeError("Latitude must be in range [-90, 90])")

        lon = kwargs.get("lon")
        if lon is None:
            raise TypeError("Longitude is not specified")
        if lon < -180 or lon > 180:
            raise TypeError("Longitude must be in range [-180, 180])")

        timeout_sec = kwargs.get("timeout_sec", 10)

        logger.info(
            "%s(%r, %r, <WEATHER_API_TOKEN>, %r)",
            self.__class__.__name__,
            lon,
            lat,
            timeout_sec,
        )
        self.timeout_sec = timeout_sec
        self.data = {}

        self._params = {"lat": lat, "lon": lon, "appid": token}
        self._check_url()

    def _check_url(self):
        """Try to get weather data

        Raises:
            OpenWeatherMapError: if api returns error code
        """
        response = requests.get(
            self._API_URL, params=self._params, timeout=self._REQUEST_TIMEOUT
        )
        if response.status_code == 200:
            self.data = response.json()
            self.last_updated = datetime.utcnow()
        else:
            raise OpenWeatherMapError("Response error: {}".format(response.text))

    @property
    def location(self):
        return self.data.get("coord")

    @property
    def title(self):
        return self.data.get("name")

    @property
    def timestamp(self):
        """Returns city name"""
        dt = self.data.get("dt")
        if dt is not None:
            tz = tzoffset("", self.data.get("timezone", 0))
            dt = datetime.fromtimestamp(dt, tz).isoformat()
        return dt

    @property
    def temperature(self):
        temp = self.data.get("main", {}).get("temp")
        if temp is not None:
            temp -= 273.15
        return temp

    @property
    def humidity(self):
        return self.data.get("main", {}).get("humidity")

    @property
    def pressure(self):
        press = self.data.get("main", {}).get("pressure")
        if press is not None:
            press /= 1.33322
        return round(press)

    def update_weather(self):
        """Request weather from api, and update local data

        Returns:
            str: "Success" if update was success. "Error: {message}" otherwise.
        """
        update_result = "Success"
        sec_from_last_update = (datetime.utcnow() - self.last_updated).total_seconds()
        if sec_from_last_update > self.timeout_sec:
            self.last_updated = datetime.utcnow()
            logger.info("%s update requested", self.__class__.__name__)
            try:
                response = requests.get(self._API_URL, params=self._params)
            except requests.exceptions.RequestException:
                update_result = "Error: RequestException"
                logger.error("Update weather request failed", exc_info=True)
            else:
                if response.status_code == 200:
                    data = response.json()
                    if data.get("cod", 503) == 200:
                        self.data = data
                        logger.info("%s updated", self.__class__.__name__)
                    else:
                        message = data.get(
                            "message", "Unknown error: {data}".format(data=data)
                        )
                        update_result = "Error: {msg}".format(msg=message)
                        logger.error(message)
                else:
                    update_result = "Error: ResponseException: {code} - {message}".format(
                        code=response.status_code, message=response.text
                    )
                    logger.error(
                        "Request error code: {%r} - {%r}",
                        response.status_code,
                        response.text,
                    )
        else:
            logger.debug(
                "Too mach requests to update (%r/%r sec have passed)",
                sec_from_last_update,
                self.timeout_sec,
            )
            update_result = "Error: Too mach requests to update ({cur}/req sec have passed)".format(
                cur=sec_from_last_update, req=self.timeout_sec
            )

        return update_result
