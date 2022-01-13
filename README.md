My username is kk21812.
My name is Yingtong Qi.

To add some use information
In part1, the code should be run in 'main'
In part2, the jupyter file can be run directly.
In part3, the jupyter file can be run directly.




# OnlineBank- Financial technology and data science - Yingtong Qi

## Project features
   * > #### 1. registration and login for different types of accounts
   * > #### 2. Online transfers and deposits
   * > #### 3. Viewing of locally stored transfer records
   * > #### 4. PIN code modification of accounts
   * > #### 5. View account information, check available balance
   * > #### 6. Input check function
   * > #### 7. Exception handling function
   * > #### 8. Freeze/unfreeze accounts
     
## Support
<a href="https://pypi.org/project/PyUniversalKit/"><img src="https://warehouse-camo.ingress.cmh1.psfhosted.org/047074c34350165c9a6a57b844a2390d638c173d/68747470733a2f2f6769746875622e636f6d2f6a696e612d61692f6a696e612f626c6f622f6d61737465722f2e6769746875622f6261646765732f707974686f6e2d62616467652e7376673f7261773d74727565"></a>

## Project structure
   * ### models.py
     * #### Base category `Account`
       ```python
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
                self.times = time.strftime('%Y.%m.%d', time.localtime(time.time()))
            def __str__(self):
                    return self.Username   
       ```
       The base class Account takes four parameters to set the attributes username, PIN, email, address, and in its `__init__()` function, initializes the user with an initial amount of `Balance` to 0 and a state of `State` to True
     * #### Subcategories `SavingsAccount`
       ```python
       # Savings Account
       class SavingsAccount(Account):
           def __init__(self, username, pin, email, address):
               super().__init__(username, pin, email, address)
               self.kind = 'Savings Account'

           @property
           def return_to_storage_list(self):
               return [self.__str__(), self.PIN, self.Address, self.Email, self.Balance, self.State, self.kind, self.times]

       ```
       SavingsAccount inherits from the base class `Account`. The `SavingsAccount` type of account is characterised by a 1% fee when it makes a transfer, and no interest rate on deposits. A property `kind` has been added to delimit the properties. The class method `return_to_storage_list` returns a list containing all the information of the class and will be called when modifying or storing account information.
     * #### Subcategories `CheckingAccount`
       ```python
       # Checking Account
       class CheckingAccount(Account):
            def __init__(self, username, pin, email, address):
               super().__init__(username, pin, email, address)
               self.kind = 'Checking Account'

           @property
           def return_to_storage_list(self):
               return [self.__str__(), self.PIN, self.Address, self.Email, self.Balance, self.State, self.kind, self.times]
       ```
       Also inherits from the base class `Account`. Accounts of type `CheckingAccount` have the following features: no fees are charged when they are transferred and a certain interest rate is applied to the deposit.
   * ### handle.py
     * #### Class`TransactionHistory` 
       ```python
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
       ```
       The `TransactionHistory` class accepts four parameters: the originator of the transfer, the recipient of the transfer, the date of the transfer and the amount of the transfer. The class uses the built-in function `return_to_storage_list` to generate data that can be inserted directly into the file for the main function `main.py` to call
   * ### main.py
     * #### `MainPage`
       It encapsulates all the functions of the initial page and defines the relevant functions. The `MainPage` mainly contains the login section and the registration section.
       * #### Register Account
         ```python
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

            
         ```
         The registration function allows the user to select a different registration type and enter the relevant parameters to complete the registration. The system will first determine if the user name to be registered has already been registered, if not, a new account will be created; otherwise the user will be reminded to re-enter until the user name entered has not been registered by someone else. The registration data will be stored in a local text file.
       * #### Login Account
         ```python
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

         ```
         In the login function, the user logs into the system by using their username and PIN. If the username and password match, the program will switch to another theme page by calling the `success_page_interface` function of `SuccessPage`; if the username and password do not match, the user will be prompted for an incorrect password or username and will jump to the main screen.
       * #### Unfreeze your account
         ```python
            # Unfreeze your account
            # Encapsulated unpacking operator functions (class functions)
            # Specify return value as string type or bool type
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
                        # When the PIN codes are not the same twice
                        print(Fore.RED + 'PIN code error')
                        # Returns False
                        return False
                    else:
                        # Write the new PIN code to the original data Raw_data, and then re-write the original data Raw_data to the file
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

         ```
         The user can unblock the account by entering the account number and PIN code. When the entered account number and PIN code match, the system will unblock the account; otherwise, an error will be reported and the user will be returned to the main screen. It is important to note that when an account is frozen, the system will prevent the user from logging in.
     * #### `SuccessPage`
       This corresponds to the page that the user will be redirected to after a successful login. In the previous page, if the user has entered their username and password correctly, the `success_page_interface` function within `SuccessPage` will be called.
       The `success_page_interface` function will be called and the information of the currently logged in user will be extracted and stored as an attribute by the `__init__` function, which facilitates various data interactions on this page.
       This page provides seven business options, and the user can select the business by selecting serial numbers 1-6
       * ##### Check the balance
         ```python
         # Call self.balance directly, i.e. the balance of the current user
         print('Your balance is ' + Fore.GREEN + '{0}£'.format(self.balance))
         print('\n')
         ```
         The service gets the current account balance directly by calling the value of the property `balance
       * ##### Online transfer
         ```python
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
         ```
         The online transfer operation enables the transfer of amounts between different accounts. Before the transfer is made, the system confirms the legitimacy of the person to whom the transfer is made and asks the current user to enter a PIN code to verify its authenticity.
         It is then determined whether the current balance can cover the amount of the transfer. Finally, depending on the type of account, an additional 1% service fee will be deducted from the savings account. After the transaction has been completed, regardless of
         A record of the transfer will be generated and saved to a local file, regardless of whether it is successful or not.
       * ##### View account information
         ```python
            # There are different types of descriptions for different types of accounts
            print('Your account type is{0}'.format(self.kind))
            if self.kind == 'Savings Account':
                print(Fore.LIGHTBLUE_EX + 'According to the rules, you will be charged the appropria'
                      'te service fee for each transaction, and there is no interest rate.')
            if self.kind == 'Checking Account':
                print(Fore.LIGHTBLUE_EX + 'You will not be charged a service fee for your transactions and will enjoy a 3% annualized interest rate')
                print(Fore.LIGHTBLUE_EX + 'Your account opening date is: {0}, the system will calculate your earnings based on this. '.format(self.times))
            print('\n')
         ```
         View account information and the system will inform you of the current benefits and account details depending on the account type.
       * #### View transaction history
         ```python
            all_list_His = self.__get_TransactionHistory
            # Get all transfer records and store them in a list
            # Format [[transferee, transfer recipient, transfer amount, transfer time, transfer status],... [...]]
            alls_charts_data = [[lists[0], lists[1], lists[2], lists[3], lists[4]] for keys, lists in
                                all_list_His.items()]
            # Table top
             table = PrettyTable(
                ['Transfer Initiator', 'Receiver', 'Transfer Amount', 'Transfer Time', 'Transfer Status'],
                encoding=sys.stdout.encoding)
            # Printable forms
            for i in alls_charts_data:
                table.add_row([i[0], i[1], i[2], i[3], i[4]])
            print(table)
            print('\n')
         ```
         Viewing the transfer history will retrieve the stored records stored locally and inform the user visually in a table format. The format of the transfer record is
         
         |  Transfer originator  |  Transfer Recipient  |  Transfer time  |  Transfer Amount  |  Transfer Status  |
         |  --------  |  --------  |  ------   |  ------  |  -------  |
         |    data    |    data    |   data   |   data  |   data   |
         In addition, a third party library `PrettyTable` is used for the presentation of data, which can be entered into neat data tables.
       
       * #### Online Deposit
         ```python
                try:
                    Raw_data = self.__get_client_data
                    # Ask the user to enter an integer
                    money = self.__balace_check_input(input('Please enter the deposit amount >>'))
                    # Use as above
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
         ```
         The online deposit service allows the user to deposit the amount entered.
       
       * #### Change PIN code
         ```python
                try:
                    usr_password = input('Please enter a new PIN >>')
                    # Change the requirement that the new PIN entered by the user must not be equal to the current user's PIN
                    if usr_password == self.pin:
                        print(Fore.RED + 'The new PIN cannot be the same as the current PIN')
                    else:
                        # Raw data
                        # Change the PIN code
                        Raw_data = self.__get_client_data
                        target_list = Raw_data['{0}'.format(self.cur_username)]
                        target_list[1] = usr_password
                        # Update raw data
                        Raw_data['{0}'.format(self.cur_username)] = target_list
                        # Write to file
                        self.__save_client_data(client_data=Raw_data)
                        print(Fore.GREEN + 'Password changed successfully')
                except Exception as e:
                    print(Fore.RED + 'Password change failed.\nDetailed reasons：{0}'.format(str(e)))

         ```
         Users are allowed to change their PIN online and the change will take effect instantly, the next time they log in they will need to use the new password.
       * #### Cancellation of accounts 
         ```python
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
         ```
         will clear the user's login status and return to the initial page `MainPage`.
       * #### Freeze this account
         ```python
         print('You have securely cancelled your account. \n')
         MainPage().start()
         break
         ```
         The system will freeze the current account and clear the current login information to return to the initial page. When the account is frozen, the system will ban the user. If you need to unfreeze your account please go to the initial page.
