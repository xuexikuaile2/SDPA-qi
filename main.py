# This is the Main function entry

# You may need to download the third-party libraries prettytable and colorama, otherwise the program will report an error
# Your python version needs to be python 3.7+

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
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
    """
    :param input_values: Receive user input
    :param message: A prompt for the user to re-enter if the user's input does not match the specification
    :param MaxIntConditions: Maximum integer
    :param MinIntConditions: Minimum Integer
    :return: Returns an integer

    Function workflow: The function receives user input and goes through various judgments to determine if the user input is correct. If it is not correct, the function will prompt the user to keep entering until the user enters correctly.
    Type of error: When the user input is empty, or not an integer, or does not meet the specified integer, the function will determine that the user input is incorrect and will prompt the user to re-enter.
    For example: the initial page calls this function in the following format
                check_last_user_input = check_input(input_values=input('>>'), MaxIntConditions=4)
    This means that the current user's input is passed into the function and the user's input is judged to be valid if it is in the range of 0 to 4 (not 0, but 4), corresponding to the initial page The four operations of the initial page.
    """
    while True:
        # When the input is empty
        # if not input_values i.e. if input_values ! = True, i.e. if input_values is empty
        # A variable with no value or an empty list can be represented as False
        if not input_values:
            print(Fore.RED + 'Your input is empty, please re-enter.')
            # {0} is the booth character
            # Example: a = "Hello everyone, my name is {0}, I'm {1} years old".format("小明", "18")
            # The above example is equivalent to: "Hello everyone, my name is Xiao Ming and I am 18 years old"
            input_values = input('{0}'.format(message))
        else:
            try:
                # Determine if the input value is in range when it can be converted to an integer
                if int(input_values) < MinIntConditions or int(input_values) > MaxIntConditions:
                    print(Fore.RED + 'Make sure your input is between 1 and 3.')
                    input_values = input('{0}'.format(message))
                else:
                    # Return the value if it meets the requirements
                    return int(input_values)
            except Exception as e:
                print(Fore.RED + 'Please make sure your input is correct.\nerror:{0}'.format(str(e)))
                input_values = input('{0}'.format(message))


class MainPage:
    # Initialization functions
    def __init__(self):
        pass

    # Calculate the proceeds of a checking account
    # Rough calculations
    @staticmethod
    def checking_input(days, nowMoney):
        # Total money earned at 3% p.a. based on current account balance
        OneYearInput = 0.03 * nowMoney
        # Apportioned to daily
        OneDay = OneYearInput / 365
        # Time points multiplied by daily earnings to give current earnings
        return nowMoney + OneDay * days

    #  Call this function to update the balance of all checking accounts before the start of each program
    def init_Account(self):
        news_dict = {}
        Raw_data = self.__get_client_data
        for keys, values in Raw_data.items():
            initTime = datetime.datetime.strptime(values[7], "%Y.%m.%d")
            nows = datetime.datetime.strptime(time.strftime('%Y.%m.%d', time.localtime(time.time())), "%Y.%m.%d")
            Duration = (nows - initTime).days
            values[4] = self.checking_input(days=Duration, nowMoney=values[4])
            news_dict[keys] = values
        self.__save_client_data(client_data=news_dict)

    # Entry functions for default pages
    def start(self):
        self.init_Account()
        self.main_page_interface()

    # Get the user data, read all the stored data from Client.txt
    # The storage format is: { 'user1':[user1 name, user1 PIN, user1 address, user1 email, user1 balance, user1 status, user1 type], { 'user1':[user1 name, user1 PIN, user1 address, user1 address, user1 email, user1 balance, user1 status, user1 type
    # 'user2':[user2 name, user2 PIN, user2 address, user2 email, user2 balance, user2 status, user2 type].
    # ...
    # }
    # What json.loads does is to convert the text content into a dictionary object that can be called directly
    @property
    def __get_client_data(self) -> json:
        with open('./Storage/Client.txt', 'r') as f:
            data = json.loads(f.read())
            return data

    # This has the advantage of not destroying its original properties and structure
    @staticmethod
    def __save_client_data(client_data):
        # w is the read/write method, in which each time a file is written with this method, the original content is not retained, i.e. the latest written content overwrites the original content.
        with open('./Storage/Client.txt', 'w') as w:
            w.write(json.dumps(client_data))

    # Home Page Interface
    # This is the main function that first prints the welcome message and then prints out all the businesses on the initial page for the user to choose from
    def main_page_interface(self):
        while True:
            print('-' * 20 + ' Welcome to OnlineBank ' + '-' * 20)
            print(' ' * 15 + 'Please select the business you need' + ' ' * 15)
            print('\n')
            print(' ' * 22 + '1. Register Account' + ' ' * 22)
            print(' ' * 22 + '2. Login Account' + ' ' * 22)
            print(' ' * 22 + '3. Unfreeze your account' + ' ' * 22)
            print(' ' * 22 + '4. Exit' + ' ' * 22)
            print('\n')
            # The check_input method is called to check user input. The user will be asked to keep typing until the correct value is entered.
            check_last_user_input = check_input(input_values=input('>>'), MaxIntConditions=4)
            # Corresponding registered business
            if check_last_user_input == 1:
                self.registration()
            elif check_last_user_input == 2:
                # self.login() is the program that allows the user to log in. If the user is successfully logged in, it will return True, otherwise it will return no value (i.e. False)
                login_flag = self.login()
                # If login is successful
                if login_flag:
                    # Stop the current application and call SuccessPage(cur_username=login_flag).success_page_interface()
                    # Switch to the success page
                    SuccessPage(cur_username=login_flag).success_page_interface()
                    break
                else:
                    pass
            # Corresponding unblocked account operations
            elif check_last_user_input == 3:
                # Call self.unfreeze() method, if the user authentication is successful, self.unfreeze() will return True, otherwise
                # will return False
                unfreeze = self.unfreeze()
                if unfreeze:
                    print(Fore.GREEN + 'Your account status is normal')
                    print('\n')
                else:
                    pass
            # Corresponding to exit program operations, the system will terminate all currently running programs.
            elif check_last_user_input == 4:
                sys.exit()
            else:
                continue

    # Unfreeze your account
    # Encapsulated unseal operation function (class function)
    # Specify the return value as a string or bool type
    def unfreeze(self) -> Union[str, bool]:
        # Requires the user to enter a username and checks the user input by calling the __registration_check_input method. The user will always be prompted for input when the user input does not meet the requirements.
        check_last_username = self.__registration_check_input(input_values=input('Please enter your username >>'),
                                                              message='Please enter your username >>')
        # As above
        check_last_pin = self.__registration_check_input(input_values=input('Please enter the PIN code >>'),
                                                         message='Please enter the PIN code >>')
        # Raw data
        # Raw data obtained from Client.txt (transformed into a dictionary)
        Raw_data = self.__get_client_data
        # Determine if the user name has been registered
        # Extract the names of all the users
        # Store in the format of: {
        # 'user1':[user1 name, user1 PIN, user1 address, user1 email, user1 balance, user1 status, user1 type], # 'user1':[user1 name, user1 PIN, user1 address, user1 email, user1 balance, user1 type
        # 'user2':[user2 name, user2 PIN, user2 address, user2 email, user2 balance, user2 status, user2 type], # 'user2':[user2 name, user2 PIN, user2 address, user2 email, user2 balance, user2 status, user2 type], #
        # ...
        # }
        # Use .items() to separate the keys of the dictionary for easy manipulation
        # This writeup is a list expression
        clients_list_name = [key for key, value in Raw_data.items()]
        # Verify that the username is legitimate
        # If the user name entered is in the list of all registered users
        if check_last_username in clients_list_name:
            # It is known that
            # Raw_data[username] = list of user information
            # and the format of the user information list is: [user name, user PIN, user address, user email, user balance, user status, user type]
            # Raw_data[username][1] means get user's PIN
            # So Raw_data['{0}'.format(check_last_username)][1] means to get the PIN of the user who entered the username.
            true_pin = Raw_data['{0}'.format(check_last_username)][1]
            # Compare the difference between the real PIN and the PIN entered by the user.
            if true_pin != check_last_pin:
                # When the PIN is not the same twice
                print(Fore.RED + 'PIN code error')
                # Returns False
                return False
            else:
                # Write the new PIN code to the original data Raw_data, then re-write the original Raw_data to the file
                # Since the latest written data will overwrite the previous data, the current Raw_data is the latest user data
                target_list = Raw_data['{0}'.format(check_last_username)]
                target_list[5] = True
                # Call . __save_client_data(client_data=Raw_data) to write data
                self.__save_client_data(client_data=Raw_data)
                print(Fore.GREEN + 'Unfrozen successfully! Now you can log in to your account.')
                # Return username name
                return check_last_username

        else:
            # This is the user name entered by the user that is not in the text file
            print(Fore.RED + 'This user does not exist')
            return False

    # Login function
    # Encapsulated user login operations
    def login(self) -> Union[str, bool]:
        # Function as above
        check_last_username = self.__registration_check_input(input_values=input('Please enter your username >>'),
                                                              message='Please enter your username >>')
        # Function as above
        check_last_pin = self.__registration_check_input(input_values=input('Please enter the PIN code >>'),
                                                         message='Please enter the PIN code >>')
        # Raw user data
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
                # Password verification successful
                # Get a list of detailed user data
                userStates = Raw_data['{0}'.format(check_last_username)][5]
                # If the user's kind attribute is False, the account has been frozen and is not allowed to log in to the account
                if userStates:
                    print(Fore.GREEN + 'Login successful!')
                    return check_last_username
                else:
                    print(Fore.RED + 'Your account has been frozen.')

        else:
            print(Fore.RED + 'This user does not exist')
            return False

    # Registration function
    # Encapsulate user registration operations
    def registration(self):
        # Let the user choose which account type
        print('1. Savings Account')
        print('2. Checking Account')
        # As above, check input
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
        # Check that the username currently being registered has not already been registered by someone else
        clients_list_name = [key for key, value in Raw_data.items()]
        # The username is already occupied by someone else
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
    # Check input function for registration function
    # Requires that user input cannot be empty or have special characters, otherwise it will keep prompting the user for input
    # Other functions are the same as check_input
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


# All functions and methods of the encapsulated login success page
class SuccessPage:
    def __init__(self, cur_username):
        # On the previous page, if the user logs in successfully, their details are passed in
        # Facilitates the interaction of user input with the current user's data'
        # Equivalent to remembering all information about the currently logged in user and indicating that the current user is logged in
        self.cur_username = cur_username
        details = self.__get_message
        self.pin = details[1]
        self.email = details[3]
        self.address = details[2]
        self.balance = details[4]
        self.state = details[5]
        self.kind = details[6]
        self.times = details[7]

    @property
    # Get all the user information
    def __get_message(self):
        with open('./Storage/Client.txt', 'r') as f:
            data = json.loads(f.read())
            return data['{0}'.format(self.cur_username)]

    # Page for success login
    # Main page interface
    # Print all operations
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
            print(' ' * 32 + '7. Freeze this account')
            print(' ' * 32 + '8. Cancellation of accounts')
            check_last_user_input = check_input(input_values=input('>>'), MaxIntConditions=8)
            # Check input
            # Print balance information
            if check_last_user_input == 1:
                # Call self.balance directly, i.e. the current user's balance
                print('Your balance is ' + Fore.GREEN + '{0}£'.format(self.balance))
                print('\n')
            # Transfer operations
            elif check_last_user_input == 2:
                receiver = input("Please enter the other party's account >>")
                # Check user input, no illegal characters or null characters
                money = self.__balace_check_input(input('Please enter the transfer amount >>'))
                # Verify recipient legitimacy
                # Get the original user data
                Raw_data = self.__get_client_data
                # Determine if the user name has been registered
                # Get all user names
                clients_list_name = [key for key, value in Raw_data.items()]
                # Determine if the user to be transferred is enrolled
                # If enrolled
                if receiver in clients_list_name:
                    # Require PIN code to verify identity
                    check_pin = input('Please enter the PIN code to verify your identity >>')
                    # If verification is successful
                    if check_pin == self.pin:
                        # Distinguished Accounts
                        # Operate separately according to different types of accounts
                        if self.kind == 'Savings Account':
                            # Determine if the current balance can support the transfer
                            # Savings Account charges an additional 1% service fee
                            if 1.01 * money > self.balance:
                                print(Fore.RED + 'Transfer failed, your balance is insufficient')
                            # Transfer restrictions, no more than 1000 in a single transfer
                            if 1.01 * money > 1000:
                                print(Fore.RED + 'Maximum transfer amount cannot exceed 1000')
                            else:
                                try:

                                    # Get the respective data
                                    # Get a detailed list of data for the current user and the user who transferred the money
                                    target_list = Raw_data['{0}'.format(self.cur_username)]
                                    receiver_list = Raw_data['{0}'.format(receiver)]
                                    # Amount change
                                    # Change the details table for the current user, 4 for their amount
                                    target_list[4] = self.balance - 1.01 * money
                                    # Change the details table of the transfer user, with 4 representing their amount
                                    receiver_list[4] = receiver_list[4] + 1.01 * money
                                    # Current user amount change
                                    self.balance = target_list[4]
                                    # Update original user data
                                    Raw_data['{0}'.format(self.cur_username)] = target_list
                                    Raw_data['{0}'.format(receiver)] = receiver_list
                                    # Store original user data to file
                                    self.__save_client_data(client_data=Raw_data)
                                    # Keeping transfer records
                                    # Store the transfer record
                                    # The current transfer was successful, so state='Successful transfer'
                                    History_obj = TransactionHistory(initiators=self.cur_username, receiver=receiver,
                                                                     amount=1.01 * money, state='Successful transfer')
                                    # Get all the transfer record data
                                    # Format: {
                                    # 'transfer time':[transfer originator, transfer recipient, transfer amount, transfer time, transfer status],
                                    # ...
                                    # }
                                    all_list_His = self.__get_TransactionHistory
                                    # Get time
                                    now = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
                                    all_list_His['{0}'.format(now)] = History_obj.return_to_storage_list
                                    # Storage transfer history
                                    self.__save_TransactionHistory(savingOBJ=all_list_His)
                                    print(
                                        Fore.LIGHTBLUE_EX + 'The transfer was successful, but since you have a savings account, a 1% fee will be charged for this transfer')
                                    print('Your balance:' + Fore.GREEN + '{0} £'.format(self.balance))
                                    print('\n')
                                except Exception as e:
                                    print('Transfer failed. \n Detailed reason: {0}'.format(str(e)))
                        # The following operations are the same as above
                        # The main difference is that there is no service charge for the transfer
                        elif self.kind == 'Checking Account':
                            if money > self.balance:
                                print(Fore.RED + 'Transfer failed, your balance is insufficient')
                            if money > 1000:
                                print(Fore.RED + 'Maximum transfer amount cannot exceed 1000')
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
                                    print(
                                        'The transfer is successful, and since you have a checking account, no fees will be charged for this transfer')
                                    print('Your balance:' + Fore.GREEN + '{0} £'.format(self.balance))
                                    print('\n')
                                except Exception as e:
                                    # Failed transfers
                                    # Keeping transfer records
                                    # Keeping transfer records with a status of False
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
            # Print account details
            elif check_last_user_input == 3:
                # There will be different types of descriptions for different types of accounts
                print('Your account type is{0}'.format(self.kind))
                if self.kind == 'Savings Account':
                    print(Fore.LIGHTBLUE_EX + 'According to the rules, you will be charged the appropria'
                          'te service fee for each transaction, and there is no interest rate.')
                if self.kind == 'Checking Account':
                    print(Fore.LIGHTBLUE_EX + 'You will not be charged a service fee for your transactions and will enjoy a 3% annualized interest rate')
                    print(Fore.LIGHTBLUE_EX + 'Your account opening date is: {0}, the system will calculate your earnings based on this. '.format(self.times))
                print('\n')
            # View Transfer Data
            elif check_last_user_input == 4:
                all_list_His = self.__get_TransactionHistory
                # Get all transfer records and store them in a list
                # Format [[transferee, transfer recipient, transfer amount, transfer time, transfer status],... [...]]
                alls_charts_data = [[lists[0], lists[1], lists[2], lists[3], lists[4]] for keys, lists in
                                    all_list_His.items()]
                # Table header
                table = PrettyTable(
                    ['Transfer Initiator', 'Receiver', 'Transfer Amount', 'Transfer Time', 'Transfer Status'],
                    encoding=sys.stdout.encoding)
                # Print the table
                for i in alls_charts_data:
                    table.add_row([i[0], i[1], i[2], i[3], i[4]])
                print(table)
                print('\n')
            # Online deposit
            elif check_last_user_input == 5:
                try:
                    Raw_data = self.__get_client_data
                    # Ask the user to enter an integer
                    money = self.__balace_check_input(input('Please enter the deposit amount >>'))
                    # Used as above
                    target_list = Raw_data['{0}'.format(self.cur_username)]
                    # Change amount (to be stored)
                    target_list[4] = self.balance + money
                    # Update the amount for the current user
                    self.balance = self.balance + money
                    Raw_data['{0}'.format(self.cur_username)] = target_list
                    # Write to file storage
                    self.__save_client_data(client_data=Raw_data)
                    print('The deposit was successful. Your balance：' + Fore.GREEN + ' {0} £'.format(self.balance))
                except Exception as e:
                    print('Deposit failed. \n Reason for error: {0}'.format(str(e)))
                print('\n')
            # Change the PIN code
            elif check_last_user_input == 6:
                try:
                    usr_password = input('Please enter a new PIN >>')
                    # Change to require the new PIN entered by the user not to be equal to the current user's PIN
                    if usr_password == self.pin:
                        print(Fore.RED + 'The new PIN cannot be the same as the current PIN')
                    else:
                        # Raw data
                        # Change the PIN code
                        Raw_data = self.__get_client_data
                        target_list = Raw_data['{0}'.format(self.cur_username)]
                        target_list[1] = usr_password
                        # Update the original data
                        Raw_data['{0}'.format(self.cur_username)] = target_list
                        # Write to file
                        self.__save_client_data(client_data=Raw_data)
                        print(Fore.GREEN + 'Password changed successfully')
                except Exception as e:
                    print(Fore.RED + 'Password change failed.\nDetailed reasons：{0}'.format(str(e)))
            # Freezing of accounts
            elif check_last_user_input == 7:
                # Raw data
                Raw_data = self.__get_client_data
                # Get a list of current user details
                target_list = Raw_data['{0}'.format(self.cur_username)]
                # Update status to False
                target_list[5] = False
                self.__save_client_data(client_data=Raw_data)
                # Clear the login information and return to the initial screen
                print(Fore.GREEN + 'The account is frozen successfully and you will be returned to the initial screen.')
                print('\n')
                MainPage().start()
                break
            elif check_last_user_input == 8:
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
