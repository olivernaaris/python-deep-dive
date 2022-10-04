import itertools
import numbers
from datetime import timedelta
from datetime import datetime
from collections import namedtuple

Confirmation = namedtuple('Confirmation', 'account_number, transaction_code, transaction_id, time_utc, time')


class TimeZone:
    def __init__(self, name, offset_hours, offset_minutes):
        if name is None or len(str(name).strip()) == 0:
            raise ValueError('Timezone name cannot be empty.')

        self._name = str(name).strip()
        # technically we should check that offset is a
        if not isinstance(offset_hours, numbers.Integral):
            raise ValueError('Hour offset must be an integer.')

        if not isinstance(offset_minutes, numbers.Integral):
            raise ValueError('Minutes offset must be an integer.')

        if offset_minutes < -59 or offset_minutes > 59:
            raise ValueError('Minutes offset must between -59 and 59 (inclusive).')

        # for time delta sign of minutes will be set to sign of hours
        offset = timedelta(hours=offset_hours, minutes=offset_minutes)

        # offsets are technically bounded between -12:00 and 14:00
        # see: https://en.wikipedia.org/wiki/List_of_UTC_time_offsets
        if offset < timedelta(hours=-12, minutes=0) or offset > timedelta(hours=14, minutes=0):
            raise ValueError('Offset must be between -12:00 and +14:00.')

        self._offset_hours = offset_hours
        self._offset_minutes = offset_minutes
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return (isinstance(other, TimeZone) and
                self.name == other.name and
                self._offset_hours == other._offset_hours and
                self._offset_minutes == other._offset_minutes)

    def __repr__(self):
        return (f"TimeZone(name='{self.name}', "
                f"offset_hours={self._offset_hours}, "
                f"offset_minutes={self._offset_minutes})")


class Account:
    transaction_counter = itertools.count(100)
    _interest_rate = 0.5  # percentage

    _transaction_codes = {
        'deposit': 'D',
        'withdraw': 'W',
        'interest': 'I',
        'rejected': 'X'
    }

    def __init__(self, account_number, first_name, last_name,
                 timezone=None, initial_balance=0):
        # in practice we probably would want to add checks to make sure these values are valid / non-empty
        self._account_number = account_number
        self.first_name = first_name
        self.last_name = last_name

        if timezone is None:
            timezone = TimeZone('UTC', 0, 0)
        self.timezone = timezone

        self._balance = float(initial_balance)

    @property
    def balance(self):
        return self._balance

    @property
    def account_number(self):
        return self._account_number

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self.validate_and_set_name('_first_name', value, 'First Name')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self.validate_and_set_name('_last_name', value, 'Last Name')

    # also going to create a full_name computed property, for ease of use
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        if not isinstance(value, TimeZone):
            raise ValueError('Time Zone must be a valid TimeZone object.')
        self._timezone = value

    @classmethod
    def get_interest_rate(cls):
        return cls._interest_rate

    @classmethod
    def set_interest_rate(cls, value):
        if not isinstance(value, numbers.Real):
            raise ValueError('Interest rate must be a real number.')
        if value < 0:
            raise ValueError('Interest rate cannot be negative.')
        cls._interest_rate = value

    def validate_and_set_name(self, property_name, value, field_title):
        if value is None or len(str(value).strip()) == 0:
            raise ValueError(f'{field_title} cannot be empty.')
        setattr(self, property_name, value)

    def generate_confirmation_code(self, transaction_code):
        # main difficulty here is to generate the current time in UTC using this formatting:
        # YYYYMMDDHHMMSS
        dt_str = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f'{transaction_code}-{self.account_number}-{dt_str}-{next(Account.transaction_counter)}'

    @staticmethod
    def parse_confirmation_code(confirmation_code, preferred_time_zone=None):
        # dummy-A100-20190325224918-101
        parts = confirmation_code.split('-')
        if len(parts) != 4:
            # really simplistic validation here - would need something better
            raise ValueError('Invalid confirmation code')

        # unpack into separate variables
        transaction_code, account_number, raw_dt_utc, transaction_id = parts

        # need to convert raw_dt_utc into a proper datetime object
        try:
            dt_utc = datetime.strptime(raw_dt_utc, '%Y%m%d%H%M%S')
        except ValueError as ex:
            # again, probably need better error handling here
            raise ValueError('Invalid transaction datetime') from ex

        if preferred_time_zone is None:
            preferred_time_zone = TimeZone('UTC', 0, 0)

        if not isinstance(preferred_time_zone, TimeZone):
            raise ValueError('Invalid TimeZone specified.')

        dt_preferred = dt_utc + preferred_time_zone.offset
        dt_preferred_str = f"{dt_preferred.strftime('%Y-%m-%d %H:%M:%S')} ({preferred_time_zone.name})"

        return Confirmation(account_number, transaction_code, transaction_id, dt_utc.isoformat(), dt_preferred_str)

    def make_transaction(self):
        return self.generate_confirmation_code('dummy')


try:
    a = Account('12345', 'John', '')
except ValueError as ex:
    print(ex)

a1 = Account('12345', 'Alex', 'Martelli', initial_balance=100)
a2 = Account('12345', 'John', 'Cleese', initial_balance=200)
print(a1.first_name, a1.last_name, a1.full_name, a1.timezone.name, a1.balance)
print(a2.first_name, a2.last_name, a2.full_name, a2.timezone.name, a2.balance)

a1 = Account('A100', 'John', 'Cleese', initial_balance=100)
a2 = Account('B100', 'Alex', 'Martelli', initial_balance=200)
a = Account('A100', 'John', 'Cleese', initial_balance=100)
conf_code = a.make_transaction()
print(conf_code)
print(Account.parse_confirmation_code(conf_code))
print(Account.parse_confirmation_code(conf_code, TimeZone('MST', -7, 0)))
try:
    Account.parse_confirmation_code('X-A100-asdasd-123')
except ValueError as ex:
    print(ex)