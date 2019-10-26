from dataclasses import dataclass
from datetime import datetime
import copy
from google.api_core import protobuf_helpers


@dataclass
class Conversion:
    """Conversion implements Common Ad conversion.
    """
    id: str = ""
    click_id: str = ""
    action: str = ""
    amount: float = 0.0
    unit: str = ""
    currency: str = "USD"
    uniq_id_per_action: str = ""
    actioned_at: datetime = datetime.now()

    def to_google_click_conversion(self, c: object) -> object:
        """Convert to Google Ads click conversion object based on passed.
        Safe opearation, return new object.
        Based on https://developers.google.com/google-ads/api/reference/rpc/google.ads.googleads.v2.services#google.ads.googleads.v2.services.ClickConversion
        Date format is "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. “2019-01-01 12:32:45-08:00”.
        """
        newConversion = copy.deepcopy(c)
        newConversion.gclid.value = self.click_id
        newConversion.conversion_action.value = self.action
        tz = "{0:%z}".format(self.actioned_at)
        tz_sep = tz[:3] + ':' + tz[3:]
        newConversion.conversion_date_time.value = "{0:%Y-%m-%d %H:%M:%S}{1}".format(
            self.actioned_at, tz_sep)
        newConversion.conversion_value.value = self.amount
        newConversion.currency_code.value = self.currency
        newConversion.order_id.value = self.uniq_id_per_action
        return newConversion
