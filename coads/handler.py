from datetime import datetime
from dateutil import tz

from flask_restful import Resource, reqparse


from coads import conversion, repository


tokenRepository = repository.TokenRepository()

clientFactory = repository.ClientFactory()

conversionS3Repository = repository.ConversionS3Repository()

defaultConversion = None


class Conversion(Resource):
    """Conversion is a handler. Recieve Conversion and put them to Google.
    """
    config = None

    def get(self, customer_id):

        parser = reqparse.RequestParser()
        parser.add_argument('click_id', type=str, required=True)
        parser.add_argument('action_name', type=str, required=True)
        parser.add_argument('actioned_at', type=str, required=True)
        parser.add_argument('amount', type=float, required=True)
        parser.add_argument('currency', type=str, required=True)
        parser.add_argument('action_type', type=str, required=True)

        args = parser.parse_args()

        # auth and get user
        try:
            token = tokenRepository.get_token(customer_id)
            authed_client = clientFactory.get_client(token)
        except Exception as e:
            # log
            print(e)
            return "Auth Failed"
        if authed_client is None:
            return "Auth Failed"

        actioned_at_date = datetime.strptime(args.actioned_at, '%Y%m%d%H%M%S')
        actioned_at_date.replace(tzinfo=tz.gettz('Asia/Tokyo'))
        gconversion = conversion.Conversion(
            click_id=args.click_id,
            action=args.action_name,
            amount=args.amount,
            currency=args.currency,
            actioned_at=actioned_at_date,
        ).to_google_click_conversion(defaultConversion)

        conversion_upload_service = authed_client.get_service(
            'ConversionUploadService', version='v2')
        try:
            response = conversion_upload_service.upload_click_conversions(
                customer_id,
                [gconversion],
                partial_failure=True,
                validate_only=False)
        except Exception as e:
            print(e)
            return "Internal Error"

        try:
            conversionS3Repository.put_dict(
                self.config['bucketname'], args.click_id, args.click_id)
        except Exception as e:
            print(e)
            return "Internal Error"

        return "OK"
