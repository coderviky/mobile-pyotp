from typing import Any, Union, Optional
import time
import datetime
import calendar
import hashlib

from .otp import OTP
from .utils import strings_equal


class TOTP(OTP):
    """
    Handler for time-based OTP counters.
    """

    def __init__(self, secret: str, digits: int = 6, digest: Any = hashlib.sha1, name: Optional[str] = None,
                 issuer: Optional[str] = None, interval: int = 30) -> None:
        """
        :param secret: secret in base32 format
        :param interval: the time interval in seconds for OTP. This defaults to 30.
        :param digits: number of integers in the OTP. Some apps expect this to be 6 digits, others support more.
        :param digest: digest function to use in the HMAC (expected to be sha1)
        :param name: account name
        :param issuer: issuer
        """
        self.interval = interval
        super().__init__(secret=secret, digits=digits,
                         digest=digest, name=name, issuer=issuer)

    def now(self, mobile_number: str) -> str:
        """
        Generate the current time OTP for perticular mobile number

        :param mobile_number: mobile number string without country code
        :returns: OTP value
        """
        number = int(mobile_number)
        return self.generate_otp(self.timecode(datetime.datetime.now()) + (number * self.interval))

    def verify(self, otp: str, mobile_number: str, for_time: Optional[datetime.datetime] = None, valid_window: int = 0) -> bool:
        """
        Verifies the OTP passed in against the current time OTP.

        :param otp: the OTP to check against
        :param mobile_number: the mobile number to check against
        :param for_time: Time to check OTP at (defaults to now)
        :param valid_window: extends the validity to this many counter ticks before and after the current one
        :returns: True if verification succeeded, False otherwise
        """
        number = int(mobile_number)
        if for_time is None:
            for_time = datetime.datetime.now()

        if valid_window:
            for i in range(-valid_window, valid_window + 1):
                if strings_equal(str(otp), str(self.at(for_time, i))):
                    return True
            return False

        # return utils.strings_equal(str(otp), str(self.at(for_time)))
        return strings_equal(str(otp), str(self.generate_otp(self.timecode(for_time) + (number * self.interval))))

    def timecode(self, for_time: datetime.datetime) -> int:
        """
        Accepts either a timezone naive (`for_time.tzinfo is None`) or
        a timezone aware datetime as argument and returns the
        corresponding counter value (timecode).

        """
        if for_time.tzinfo:
            return int(calendar.timegm(for_time.utctimetuple()) / self.interval)
        else:
            return int(time.mktime(for_time.timetuple()) / self.interval)

    def at(self, for_time: Union[int, datetime.datetime], counter_offset: int = 0) -> str:
        """
        Accepts either a Unix timestamp integer or a datetime object.
        To get the time until the next timecode change (seconds until the current OTP expires), use this instead::
            totp = pyotp.TOTP(...)
            time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
        :param for_time: the time to generate an OTP for
        :param counter_offset: the amount of ticks to add to the time counter
        :returns: OTP value
        """
        if not isinstance(for_time, datetime.datetime):
            for_time = datetime.datetime.fromtimestamp(int(for_time))
        return self.generate_otp(self.timecode(for_time) + counter_offset)
