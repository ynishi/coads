from unittest import TestCase, mock
from datetime import datetime
from dateutil import tz
import google.ads.google_ads.client
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import coads
from coads.config import configs
from coads.handler import Conversion
from coads import handler


class TestHandler(TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(configs["test"])
        self.api = Api(self.app)
        ga_client = (google.ads.google_ads.client.GoogleAdsClient
                     .load_from_storage())

        handler.defaultConversion = ga_client.get_type(
            'ClickConversion', version='v2')
        self.api.add_resource(handler.Conversion,
                              '/v1/customers/<string:customer_id>/conversion')

    def test_get(self):
        mock_conversion = mock.Mock()
        reqpath = "/v1/customers/123/conversion?click_id=c1&action_name=an&actioned_at=20191001010203&amount=1.0&currency=JPY&action_type=A"
        response = self.app.test_client().get(reqpath)
