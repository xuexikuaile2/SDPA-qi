"""
Main function entry
"""

import json
import sys
import time
from typing import Union
from colorama import init, Fore
from prettytable import PrettyTable
from OnlineBank.models import SavingsAccount, CheckingAccount
from OnlineBank.handle import TransactionHistory

init(autoreset=True)

def check_input(input_values: str, message='>>', MaxIntConditions=3, MinIntConditions=0) -> int:
    while True:
        if not input_values:
            print(Fore.RED + 'Your input is empty, please re-enter.')
            input_values = input('{0}'.format(message))
        else:
            try:
                if int(input_values) < MinIntConditions or int(input_values) > MaxIntConditions:
                    print(Fore.RED + 'Make sure your input is between 1 and 3.')
                    input_values = input('{0}'.format(message))
                else:
                    return int(input_values)
            except Exception as e:
                print(Fore.RED + 'Please make sure your input is correct.\nerror:{0}'.format(str(e)))
                input_values = input('{0}'.format(message))


class MainPage:
    def __init__(self):
        pass

    def start(self):
        self.main_page_interface()

    @property
    def __get_client_data(self) -> json:
        with open('./Storage/Client.txt', 'r') as f:
            data = json.loads(f.read())
            return data

    @staticmethod
    def __save_client_data(client_data):
        with open('./Storage/Client.txt', 'w') as w:
            w.write(json.dumps(client_data))

    # Home Page Interface
    def main_page_interface(self):
        while True:
            print('-' * 20 + ' Welcome to OnlineBank ' + '-' * 20)
            print(' ' * 15 + 'Please select the business you need' + ' ' * 15)
            print('\n')
            print(' ' * 22 + '1. Register Account' + ' ' * 22)
            print(' ' * 22 + '2. Login Account' + ' ' * 22)
            print(' ' * 22 + '3. Exit' + ' ' * 22)
            print('\n')
            check_last_user_input = check_input(input_values=input('>>'))
            if check_last_user_input == 1:
                self.registration()
            elif check_last_user_input == 2:
                login_flag = self.login()
                if login_flag:
                    SuccessPage(cur_username=login_flag).success_page_interface()
                    break
                else:
                    pass
            elif check_last_user_input == 3:
                sys.exit()
            else:
                continue

    # Login function
    def login(self) -> Union[str, bool]:
        check_last_username = self.__registration_check_input(input_values=input('Please enter your username >>'),
                                                              message='Please enter your username >>')
        check_last_pin = self.__registration_check_input(input_values=input('Please enter the PIN code >>'),
                                                         message='Please enter the PIN code >>')
        # Raw data
        Raw_data = self.__get_client_data
        # Determine if the user name has been registered
        clients_list_name = [key for key, value in Raw_data.items()]
        # Verify that the username is legitimate
        if check_last_username in clients_list_name:
            true_pin = Raw_data['{0}'.format(check_last_username)][1]
            if true_pin != check_last_pin:
                print(Fore.RED + 'PIN code error')
                return False
            else:
                print(Fore.GREEN + 'Login successful!')
                return check_last_username
        else:
            print(Fore.RED + 'This user does not exist')
            return False

    # Registration function
    def registration(self):
        print('1. Savings Account')
        print('2. Checking Account')
        kind = check_input(input_values=input('Please select the type of account you want to create >>'),
                           MaxIntConditions=2,
                           message='Please select the type of account you want to create >>')
        check_last_username = self.__registration_check_input(input_values=input('Please enter your username >>'),
                                                              message='Please enter your username >>')
        check_last_pin = self.__registration_check_input(input_values=input('Please enter the PIN code >>'),
                                                         message='Please enter your username >>')
        email = input('Please enter your email >>')
        address = input('Please enter your address >>')
        if kind == 1:
            new_ac = SavingsAccount(username=check_last_username, pin=check_last_pin, email=email, address=address)
        else:
            new_ac = CheckingAccount(username=check_last_username, pin=check_last_pin, email=email, address=address)
        # Raw_data
        Raw_data = self.__get_client_data
        # Determine if the user name has been registered
        clients_list_name = [key for key, value in Raw_data.items()]
        if check_last_username in clients_list_name:
            print(Fore.RED + 'This username already exists')
        else:
            try:
                # Storage data
                added_list = new_ac.return_to_storage_list
                Raw_data['{0}'.format(check_last_username)] = added_list
                self.__save_client_data(client_data=Raw_data)
                print(Fore.GREEN + 'Register successfully')
            except Exception as e:
                print(Fore.RED + str(e))
        print('\n')

    @staticmethod
    def __registration_check_input(input_values: str, message='>>'):
        while True:
            if not input_values:
                print(Fore.RED + 'Your input is empty, please re-enter.')
                input_values = input('{0}'.format(message))
            elif input_values in ['\\', '/']:
                print(Fore.RED + 'Your input has special characters, please check.')
                input_values = input('{0}'.format(message))
            else:
                return input_values

 # Page for success login
    def success_page_interface(self):
        while True:
            print('-' * 30 + ' Welcome to OnlineBank ' + '-' * 30)
            print(' ' * 6 + Fore.GREEN + 'You have successfully logged in'
                                         ', you can select the following services' + ' ' * 1)
            print('\n')
            print(' ' * 32 + '1. Check the balance' + ' ' * 32)
            print(' ' * 32 + '2. Online transfer')
            print(' ' * 32 + '3. View account information')
            print(' ' * 32 + '4. View transaction history')
            print(' ' * 32 + '5. Online Deposit')
            print(' ' * 32 + '6. Change PIN code')
            print(' ' * 32 + '7. Cancellation of accounts')
            check_last_user_input = check_input(input_values=input('>>'), MaxIntConditions=7)
            if check_last_user_input == 1:
                print('Your balance is ' + Fore.GREEN + '{0}£'.format(self.balance))
                print('\n')
            elif check_last_user_input == 2:
                receiver = input("Please enter the other party's account >>")
                money = self.__balace_check_input(input('Please enter the transfer amount >>'))
                # Verify recipient legitimacy
                Raw_data = self.__get_client_data
                # Determine if the user name has been registered
                clients_list_name = [key for key, value in Raw_data.items()]
                if receiver in clients_list_name:
                    check_pin = input('Please enter the PIN code to verify your identity >>')
                    if check_pin == self.pin:
                        # Distinguished Accounts
                        if self.kind == 'Savings Account':
                            if 1.01 * money > self.balance:
                                print(Fore.RED + 'Transfer failed, your balance is insufficient')
                            else:
                                try:
                                    # Get the respective data
                                    target_list = Raw_data['{0}'.format(self.cur_username)]
                                    receiver_list = Raw_data['{0}'.format(receiver)]
                                    target_list[4] = self.balance - 1.01 * money
                                    receiver_list[4] = receiver_list[4] + 1.01 * money
                                    self.balance = target_list[4]
                                    Raw_data['{0}'.format(self.cur_username)] = target_list
                                    Raw_data['{0}'.format(receiver)] = receiver_list
                                    self.__save_client_data(client_data=Raw_data)
                                    # Keeping transfer records
                                    History_obj = TransactionHistory(initiators=self.cur_username, receiver=receiver,
                                                                     amount=1.01*money, state='Successful transfer')
                                    all_list_His = self.__get_TransactionHistory
                                    now = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
                                    all_list_His['{0}'.format(now)] = History_obj.return_to_storage_list
                                    self.__save_TransactionHistory(savingOBJ=all_list_His)
                                    print('The transfer was successful, but since you have a savings account, a 1% fee will be charged for this transfer')
                                    print('Your balance:' + Fore.GREEN + '{0} £'.format(self.balance))
                                    print('\n')
                                except Exception as e:
                                    print('Transfer failed. \n Detailed reason: {0}'.format(str(e)))
                        elif self.kind == 'Checking Account':
                            if money > self.balance:
                                print(Fore.RED + 'Transfer failed, your balance is insufficient')
                            else:
                                try:
                                    # Get the respective data
                                    target_list = Raw_data['{0}'.format(self.cur_username)]
                                    receiver_list = Raw_data['{0}'.format(receiver)]
                                    target_list[4] = self.balance - money
                                    receiver_list[4] = receiver_list[4] + money
                                    self.balance = target_list[4]
                                    Raw_data['{0}'.format(self.cur_username)] = target_list
                                    Raw_data['{0}'.format(receiver)] = receiver_list
                                    self.__save_client_data(client_data=Raw_data)
                                    # Keeping transfer records
                                    History_obj = TransactionHistory(initiators=self.cur_username, receiver=receiver,
                                                                     amount=money, state='Successful transfer')
                                    all_list_His = self.__get_TransactionHistory
                                    now = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
                                    all_list_His['{0}'.format(now)] = History_obj.return_to_storage_list
                                    self.__save_TransactionHistory(savingOBJ=all_list_His)
                                    print('The transfer is successful, and since you have a checking account, no fees will be charged for this transfer')
                                    print('Your balance:' + Fore.GREEN + '{0} £'.format(self.balance))
                                    print('\n')
                                except Exception as e:
                                    # Keeping transfer records
                                    History_obj = TransactionHistory(initiators=self.cur_username, receiver=receiver,
                                                                     amount=money, state='Transfer failed')
                                    all_list_His = self.__get_TransactionHistory
                                    now = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
                                    all_list_His['{0}'.format(now)] = History_obj.return_to_storage_list
                                    print('Transfer failed. \n detailed reason：{0}'.format(str(e)))
                    else:
                        print(Fore.RED + 'PIN code error')
                else:
                    print(Fore.RED + 'No user found: {0}'.format(receiver))
            elif check_last_user_input == 3:
                print('Your account type is{0}'.format(self.kind))
                if self.kind == 'Savings Account':
                    print('According to the rules, you will be charged the appropria'
                          'te service fee for each transaction, and there is no interest rate.')
                if self.kind == 'Checking Account':
                    print('You are not charged a service fee for your transactions and enjoy interest rates.')
                print('\n')
            # View Transfer Data
            elif check_last_user_input == 4:
                all_list_His = self.__get_TransactionHistory
                alls_charts_data = [[lists[0], lists[1], lists[2], lists[3], lists[4]] for keys, lists in all_list_His.items()]
                table = PrettyTable(['Transfer Initiator', 'Receiver', 'Transfer Amount', 'Transfer Time', 'Transfer Status'], encoding=sys.stdout.encoding)
                for i in alls_charts_data:
                    table.add_row([i[0], i[1], i[2], i[3], i[4]])
                print(table)
                print('\n')
            elif check_last_user_input == 5:
                try:
                    Raw_data = self.__get_client_data
                    money = self.__balace_check_input(input('Please enter the deposit amount >>'))
                    target_list = Raw_data['{0}'.format(self.cur_username)]
                    target_list[4] = self.balance + money
                    self.balance = self.balance + money
                    Raw_data['{0}'.format(self.cur_username)] = target_list
                    self.__save_client_data(client_data=Raw_data)
                    print('The deposit was successful. Your balance：' + Fore.GREEN + ' {0} £'.format(self.balance))
                except Exception as e:
                    print('Deposit failed. \n Reason for error: {0}'.format(str(e)))
                print('\n')

            elif check_last_user_input == 6:
                try:
                    usr_password = input('Please enter a new PIN >>')
                    if usr_password == self.pin:
                        print(Fore.RED + 'The new PIN cannot be the same as the current PIN')
                    else:
                        # Raw data
                        Raw_data = self.__get_client_data
                        target_list = Raw_data['{0}'.format(self.cur_username)]
                        target_list[1] = usr_password
                        Raw_data['{0}'.format(self.cur_username)] = target_list
                        self.__save_client_data(client_data=Raw_data)
                        print(Fore.GREEN + 'Password changed successfully')
                except Exception as e:
                    print(Fore.RED + 'Password change failed.\nDetailed reasons：{0}'.format(str(e)))
            elif check_last_user_input == 7:
                print('You have securely cancelled your account. \n')
                MainPage().start()
                break

    # Access to transfer records
    def __save_TransactionHistory(self, savingOBJ):
        with open('./Storage/TransactionHistory.txt', 'w') as w:
            w.write(json.dumps(savingOBJ))

    # Read transfer records
    @property
    def __get_TransactionHistory(self):
        with open('./Storage/TransactionHistory.txt', 'r') as f:
            data = json.loads(f.read())
            return data

    @staticmethod
    def __balace_check_input(input_values: str):
        while True:
            if not input_values:
                print(Fore.RED + 'Your input is empty, please re-enter.')
                input_values = input('Please enter the transfer amount >>')
            else:
                try:
                    if int(input_values) < 0:
                        print(Fore.RED + 'Please enter a number greater than 0')
                        input_values = input('Please enter the transfer amount >>')
                    else:
                        return int(input_values)
                except Exception as e:
                    print(Fore.RED + 'Please make sure your input is correct.\nerror:{0}'.format(str(e)))
                    input_values = input('Please enter the transfer amount >>')

    @property
    def __get_client_data(self) -> json:
        with open('./Storage/Client.txt', 'r') as f:
            data = json.loads(f.read())
            return data

    @staticmethod
    def __save_client_data(client_data):
        with open('./Storage/Client.txt', 'w') as w:
            w.write(json.dumps(client_data))


if __name__ == '__main__':
    MainPage().start()
