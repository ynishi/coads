from unittest import TestCase, mock
from datetime import datetime
from dateutil import tz
import google.ads.google_ads.client
from coads.conversion import Conversion


class TestConversion(TestCase):

    def test_to_google(self):
        mock_conversion = mock.Mock()
        conversion = Conversion(
            click_id="id1",
            action="action1",
            amount=1.0,
            currency="JPY",
            actioned_at=datetime.strptime(
                '2019/01/02 03:04:05', '%Y/%m/%d %H:%M:%S').replace(tzinfo=tz.gettz('Asia/Tokyo')),
            uniq_id_per_action="id1Act1"
        ).to_google_click_conversion(mock_conversion)
        self.assertNotEqual(mock_conversion.gclid.value, 'id1')
        self.assertEqual(conversion.gclid.value, 'id1')
        self.assertEqual(conversion.conversion_action.value, 'action1')
        self.assertEqual(conversion.conversion_value.value, 1.0)
        self.assertEqual(conversion.conversion_date_time.value,
                         '2019-01-02 03:04:05+09:00')
        self.assertEqual(conversion.currency_code.value, 'JPY')
        self.assertEqual(conversion.order_id.value, 'id1Act1')
