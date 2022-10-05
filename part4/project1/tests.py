import unittest
from main import TimeZone, Account
from datetime import timedelta, datetime


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account_number = 'A100'
        self.first_name = 'FIRST'
        self.last_name = 'LAST'
        self.tz = TimeZone('TZ', 1, 30)
        self.balance = 100.0

    def create_account(self):
        return Account(self.account_number, self.first_name, self.last_name, self.tz, self.balance)

    def test_create_timezone(self):
        tz = TimeZone('ABC', -1, -30)
        self.assertEqual('ABC', tz.name)
        self.assertEqual(timedelta(hours=-1, minutes=-30), tz.offset)

    def test_timezone_equal(self):
        tz1 = TimeZone('ABC', -1, -30)
        tz2 = TimeZone('ABC', -1, -30)
        self.assertEqual(tz1, tz2)

    def test_timezones_not_equal(self):
        tz = TimeZone('ABC', -1, -30)
        test_timezones = (
            TimeZone('DEF', -1, -30),
            TimeZone('ABC', -1, 0),
            TimeZone('ABC', 1, -30)
        )
        for test_tz in test_timezones:
            self.assertNotEqual(tz, test_tz)

    def test_create_account(self):
        a = self.create_account()
        self.assertEqual(self.account_number, a.account_number)
        self.assertEqual(self.first_name, a.first_name)
        self.assertEqual(self.last_name, a.last_name)
        self.assertEqual(self.first_name + ' ' + self.last_name, a.full_name)
        self.assertEqual(self.tz, a.timezone)
        self.assertEqual(self.balance, a.balance)

    def test_create_account_blank_first_name(self):
        with self.assertRaises(ValueError):
            a = Account(self.account_number, '', self.last_name)

    def test_create_negative_balance(self):
        with self.assertRaises(ValueError):
            a = Account(self.account_number, self.first_name, self.last_name, initial_balance=-100.00)

    def test_account_withdraw_ok(self):
        a = Account(self.account_number, self.first_name, self.last_name, initial_balance=self.balance)
        conf_code = a.withdraw(20)
        self.assertEqual(80, a.balance)
        self.assertIn('W-', conf_code)

    def test_account_withdraw_overdraw(self):
        a = self.create_account()
        conf_code = a.withdraw(200)
        self.assertIn('X-', conf_code)
        self.assertEqual(self.balance, a.balance)


run_tests(TestAccount)
