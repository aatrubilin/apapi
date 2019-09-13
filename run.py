import os
import argparse

from wpapi.server import app
import wpapi.weather_services as services


parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--service",
    type=str,
    required=True,
    choices=["OpenWeatherMapAPI", "FakeWeatherAPI"],
    help="Working weather api.",
)
parser.add_argument(
    "-lat",
    "--latitude",
    type=float,
    metavar="55.03",
    default=55.03,
    help="City geo location, latitude",
)
parser.add_argument(
    "-lon",
    "--longitude",
    type=float,
    metavar="82.92",
    default=82.92,
    help="City geo location, longitude",
)
parser.add_argument(
    "-t",
    "--timeout",
    type=int,
    metavar="10",
    default=10,
    help="Min seconds between requests to API. Default 10",
)

args = parser.parse_args()

token = os.environ.get("WEATHER_API_TOKEN", None)

api = getattr(services, args.service)(
    lat=args.latitude, lon=args.longitude, token=token, timeout_sec=args.timeout
)
app.register_api(api, url_prefix=None)
app.run()
