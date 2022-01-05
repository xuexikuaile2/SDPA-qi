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

