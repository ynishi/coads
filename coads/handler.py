from datetime import datetime
from dateutil import tz
import boto3
from flask_restful import Resource, reqparse
from google.api_core import protobuf_helpers
import google.ads.google_ads.client

from coads import conversion


class TokenRepository:
    def get_token(self, id):
        return {
            'developer_token': '',
            'client_id': id,
            'client_secret': '',
            'refresh_token': 'xx'
        }


tokenRepository = TokenRepository()

defaultConversion = None


class Conversion(Resource):
    """Conversion is a handler. Recieve Conversion and put them to Google.
    """
    dc = None

    def get(self, customer_id):

        parser = reqparse.RequestParser()
        parser.add_argument('click_id', type=str, required=True)
        parser.add_argument('action_name', type=str, required=True)
        parser.add_argument('actioned_at', type=str, required=True)
        parser.add_argument('amount', type=float, required=True)
        parser.add_argument('currency', type=str, required=True)
        parser.add_argument('action_type', type=str, required=True)

        args = parser.parse_args()

        actioned_at_date = datetime.strptime(args.actioned_at, '%Y%m%d%H%M%S')
        actioned_at_date.replace(tzinfo=tz.gettz('Asia/Tokyo'))
        gconversion = conversion.Conversion(
            click_id=args.click_id,
            action=args.action_name,
            amount=args.amount,
            currency=args.currency,
            actioned_at=actioned_at_date,
        ).to_google_click_conversion(defaultConversion)

        token = tokenRepository.get_token(customer_id)
        authed_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_dict(token))

        conversion_upload_service = authed_client.get_service(
            'ConversionUploadService', version='v2')
        response = conversion_upload_service.upload_click_conversions(
            customer_id,
            [gconversion],
            partial_failure=True,
            validate_only=False)

        s3 = boto3.client('s3')
        bucket = self.s3.put_object(
            config.bucketname, args.click_id, args.click_id)

        return "OK"
