import csv

import itertools

from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from pprint import pprint
"""
We are using datetime to provide a proper treatment for invalid dates.
Assuming we are on a financial setting, proper data-types and proper 
data-formatting is a must
Also, using datetime we are able to do date_diffs

I know, we could've replaced the dashes in the date column and make it 
an integer,but I think this is more elegant
"""


def transaction_test(transactionTest, transactionProofTest,
                     transactionValidation, transactionValidationProof):
    test_dates = [-1, 0, 1]
    for transaction in transactionTest:
        # Search for the value using the keys of dictionary
        if transaction[-1] == 'MISSING':
            try:
                for date_diff in test_dates:
                    foundKey = None
                    date_final = datetime.strptime(
                        transaction[0], '%Y-%m-%d') - timedelta(days=date_diff)
                    # A very long checker, but the idea here is that the data in the dict will fit into the row
                    foundKeyValidation = transactionValidationProof[
                        date_final][transaction[1]][transaction[3]][
                            transaction[2]]
                    foundKeyTest = transactionProofTest[date_final][
                        transaction[1]][transaction[3]][transaction[2]]
                    if foundKeyTest and foundKeyValidation and transaction[
                            -1] != 'FOUND':
                        # Since it's possible to have more than one line and each repeated line can only match another one
                        foundKeyTest = foundKeyTest.pop(0)
                        foundKeyValidation = foundKeyValidation.pop(0)
                        transactionTest[foundKeyTest][-1] = 'FOUND'
                        transactionValidation[foundKeyValidation][-1] = 'FOUND'
            except Exception as e:
                break
    return transactionTest, transactionValidation


class TransactionDict(dict):

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


def data_formatting(transactions):
    transactionProof = TransactionDict()
    for idx, transaction in enumerate(transactions):
        transaction.append('MISSING')
        datetime_val = datetime.strptime(transaction[0], '%Y-%m-%d')
        transactionProof[datetime_val][transaction[1]][transaction[3]][
            transaction[2]] = list(
                list(transactionProof[datetime_val][transaction[1]][
                    transaction[3]][transaction[2]])) + [idx]
    return transactionProof


def reconcile_accounts(transaction1, transaction2):
    transaction2_ = data_formatting(transaction2)
    transaction1_ = data_formatting(transaction1)
    # We only need to use the array of smallest value, such as:
    if len(transaction1) > len(transaction2):
        transaction1, transaction2 = transaction_test(transaction1,
                                                      transaction1_,
                                                      transaction2,
                                                      transaction2_)
    else:
        transaction2, transaction1 = transaction_test(transaction2,
                                                      transaction2_,
                                                      transaction1,
                                                      transaction1_)

    return transaction1, transaction2


transactions1 = list(csv.reader(Path('transactions1.csv').open()))
transactions2 = list(csv.reader(Path('transactions2.csv').open()))
out1, out2 = reconcile_accounts(transactions1, transactions2)
pprint(out1)
pprint(out2)