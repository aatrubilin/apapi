import logging

from flask import Flask, Blueprint, jsonify

from .errors import page_not_found

logger = logging.getLogger(__name__)


class MyFlask(Flask):
    @staticmethod
    def _get_bp_name(api_name, url_prefix):
        bp_postfix = ""
        if url_prefix:
            bp_postfix = url_prefix.replace("/", "_")

        return "{class_name}{postfix}".format(class_name=api_name, postfix=bp_postfix)

    def register_api(self, api, url_prefix=None):
        bp_name = self._get_bp_name(api.__class__.__name__, url_prefix)
        bp = Blueprint(bp_name, __name__)

        @bp.route("/weather/current/", methods=["GET"])
        def weather_current():

            return jsonify(api.current)

        logger.info("Register blueprint with name: %s", bp_name)
        self.register_blueprint(bp, url_prefix=url_prefix)


app = MyFlask(__name__)
app.register_error_handler(404, page_not_found)
