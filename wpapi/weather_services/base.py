from abc import ABC, abstractmethod


class WeatherError(Exception):
    """Basic weather exception"""

    pass


class WeatherAPI(ABC):
    def __init__(self, *args, **kwargs):
        if args:
            raise TypeError("WeatherAPI takes no positional arguments")
        self.last_updated = None

    @property
    @abstractmethod
    def location(self):
        """Returns Dict with `lon` and `lat`"""
        pass

    @property
    @abstractmethod
    def title(self):
        """Returns city name"""
        pass

    @property
    @abstractmethod
    def timestamp(self):
        """Returns city name"""
        pass

    @property
    @abstractmethod
    def temperature(self):
        """Returns temperature, °C"""
        pass

    @property
    @abstractmethod
    def humidity(self):
        """Returns humidity, %"""
        pass

    @property
    @abstractmethod
    def pressure(self):
        """Returns atmospheric pressure, atm"""
        pass

    @property
    def current(self):
        """Updating and returns dict with current weather state"""
        self.update_weather()
        current = {
            "location": self.location,
            "title": self.title,
            "timestamp": self.timestamp,
            "temperature": {"C": self.temperature},
            "humidity": {"percent": self.humidity},
            "pressure": {"atm": self.pressure},
        }
        return current

    @abstractmethod
    def update_weather(self):
        """Method updating current data"""
        pass
