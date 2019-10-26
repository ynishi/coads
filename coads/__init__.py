import google.ads.google_ads.client
from google.api_core import protobuf_helpers
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from coads.config import configs
from coads import handler


def create_app(env_name):
    """Create and configure Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(configs[env_name])
    api = Api(app)

    ga_client = (google.ads.google_ads.client.GoogleAdsClient
                 .load_from_storage())

    handler.defaultConversion = ga_client.get_type(
        'ClickConversion', version='v2')

    api.add_resource(handler.Conversion,
                     '/v1/customers/<string:customer_id>/conversion')

    return api


if __name__ == '__main__':
    app.run(debug=True)
