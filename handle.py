"""
Other models related to business processing
"""
import time

class TransactionHistory:
    def __init__(self, initiators, receiver, amount, state):
        self.Initiators = initiators
        self.Receiver = receiver
        self.Amount = amount
        self.State = state
        self.times = time.strftime('%Y.%m.%d', time.localtime(time.time()))

    @property
    def return_to_storage_list(self):
        return [self.Initiators, self.Receiver, self.Amount, self.times, self.State]
