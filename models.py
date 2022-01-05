"""
Defining Account Classes
"""

# Account Class
# Base Class
class Account:
    def __init__(self, username, pin, email, address):
        self.Username = username
        self.PIN = pin
        self.Email = email
        self.Address = address
        # Account Status
        self.State = True
        # Account Balance
        self.Balance = 0

    def __str__(self):
        return self.Username

# Savings Account
class SavingsAccount(Account):
    def __init__(self, username, pin, email, address):
        super().__init__(username, pin, email, address)
        self.kind = 'Savings Account'

    @property
    def return_to_storage_list(self):
        return [self.__str__(), self.PIN, self.Address, self.Email, self.Balance, self.State, self.kind]

# Checking Account
class CheckingAccount(Account):
    def __init__(self, username, pin, email, address):
        super().__init__(username, pin, email, address)
        self.kind = 'Checking Account'

    @property
    def return_to_storage_list(self):
        return [self.__str__(), self.PIN, self.Address, self.Email, self.Balance, self.State, self.kind]
