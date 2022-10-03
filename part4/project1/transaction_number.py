import itertools


class Account:
    transaction_counter = itertools.count(100)

    def make_transaction(self):
        new_trans_id = next(Account.transaction_counter)
        return new_trans_id


a1 = Account()
a2 = Account()

print(a1.make_transaction())
print(a2.make_transaction())
print(a1.make_transaction())
