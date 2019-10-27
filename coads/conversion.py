from dataclasses import dataclass
from datetime import datetime
import pytz
import copy


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
    actioned_at: datetime = datetime.now(pytz.utc)
    actioned_tz: str = "UTC"

    def __post_init__(self):
        # init private __actioned_ptz
        self.__actioned_ptz: datetime.tzinfo = None
        if self.actioned_at.tzinfo is None:
            self.__actioned_ptz = pytz.timezone(
                self.actioned_tz)
        else:
            self.__actioned_ptz = self.actioned_at.tzinfo
        # init private __actioned_at_utc
        self.__actioned_at_utc: datetime = to_utc(
            self.actioned_at, self.actioned_tz)

    def to_google_click_conversion(self, c: object) -> object:
        """Convert to Google Ads click conversion object based on passed.
        Safe opearation, return new object.
        Based on https://developers.google.com/google-ads/api/reference/rpc/google.ads.googleads.v2.services#google.ads.googleads.v2.services.ClickConversion
        """
        newConversion = copy.deepcopy(c)
        newConversion.gclid.value = self.click_id
        newConversion.conversion_action.value = self.action
        actioned_tzed = self.__actioned_at_utc.astimezone(self.__actioned_ptz)
        newConversion.conversion_date_time.value = f'{actioned_tzed}'
        newConversion.conversion_value.value = self.amount
        newConversion.currency_code.value = self.currency
        newConversion.order_id.value = self.uniq_id_per_action
        return newConversion


def to_utc(d: datetime, timezone: str) -> datetime:
    """
    helper to convert from datetime(naive or aware) with timezone name to utc datetime.
    throws error when failed to utc
    :param d: from datetime
    :param timezone: timezone name like "US/Eastern"
    :return: datetime converted to utc
    """
    tz_obj = pytz.timezone(timezone)
    if d.tzinfo is None:
        d_aware_tz = tz_obj.localize(d, is_dst=None)
    else:
        d_aware_tz = d
    return d_aware_tz.astimezone(pytz.utc)
