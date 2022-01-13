My username is kk21812.
My name is Yingtong Qi.

To add some use information
In part1, the code should be run in 'main'
In part2, the jupyter file can be run directly.
In part3, the jupyter file can be run directly. And you can cilck the website in the last line of running results for more charts.


THe following context of part3 is all in the part3 jupyter file. 

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


# Part3 -- DataAnalytics


## Project functions
   * > #### 1. Obtain the corresponding historical data according to the stock code
   * > #### 2. Store the acquired stock data
   * > #### 3. Read, analyse and clean stock data
   * > #### 4. Counting differences about stock data

## Data preparation and acquisition
   * ### Sina Finance Stock Data API Interface
     #### We use the Sina Finance Stock Data API to obtain stock data. This is shown below
      ```python
      # Access to basic stock information
      url = 'http://hq.sinajs.cn/list=sh601006'
      ```
     #### A GET request to this API using the `Python` third-party library `requests` gives the following feedback data.
     ```text
     var hq_str_sh601006="XXX, 27.55, 27.25, 26.91, 27.55, 26.20, 26.91, 26.92,22114263, 589824680, 4695, 26.91, 57590, 26.90, 14700, 26.89, 14300,26.88, 15100, 26.87, 3100, 26.92, 8900, 26.93, 14230, 26.94, 25150, 26.95, 15220, 26.96, 2008-01-11, 15:05:32";
     ```
     #### This string consists of a number of pieces of data stitched together, with the different meanings separated by commas. Using Python's built-in library `split` to split the string, you can get the list
     ```python
     var = ['XXX', '27.55', '27.25', '26.91', '27.55', '26.20', '26.91', '26.92', '22114263', '589824680', '4695', '26.91', '57590', '26.90', '14700', '26.89', '14300', '26.88', '15100', '26.87', '3100', '26.92', '8900', '26.93', '14230', '26.94', '25150', '26.95', '15220', '26.96', '2008-01-11', '15:05:32']
     ```
     #### This list has the following meaning from the first element in order to the last element. (The beginning is the index value)
     * #### 0: "Daqin Railway", the name of the stock.
     * #### 1: "27.55″, today's opening price.
     * #### 2: "27.25″, yesterday's closing price.
     * #### 3: "26.91″, current price.
     * #### 4: "27.55″, today's high price.
     * #### 5: "26.20″, today's low; * #### 5: "26.20″, today's low.
     * #### 6: "26.91″, the bid price, i.e. "buy one" offer.
     * #### 7: "26.92″, the bid price, i.e. "sell one" offer.
     * #### 8: "22114263″, the number of shares traded, which is usually divided by one hundred when used as the basic unit of stock trading is one hundred shares.
     * #### 9: "589824680″, the amount of the transaction, in "yuan", which is usually divided by 10,000, as "ten thousand" is the unit of the transaction amount for the sake of clarity.
     * #### 10: "4695″, "buy one" request for 4695 shares, i.e. 47 lots.
     * #### 11: "26.91″, a "buy one" quote.
     * #### 12: "57590″, "Buy 2"
     * #### 13: "26.90″, "Buy Two"
     * #### 14: "14700″, "Buy 3"
     * #### 15: "26.89″, "Buy Three"
     * #### 16: "14300″, "Buy 4"
     * #### 17: "26.88″, "buy four"
     * #### 18: "15,100″, "Buy Five"
     * #### 19: "26.87″, "Buy Five"
     * #### 20: "3100″, "Sell One" for 3100 shares, i.e. 31 lots.
     * #### 21: "26.92″, "Sell One" quote
     * #### (22, 23), (24, 25), (26, 27), (28, 29) for "Sell 2" to "Sell 4" respectively
     * #### 30: "2008-01-11", date.
     * #### 31: "15:05:32″, time.
     #### In addition, there is an API for getting historical stock data as follows
       ```python
       url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php' \
              '/CN_MarketData.getKLineData?symbol={0}&scale={1}&ma={2}&datalen=' \
              '{3}'.format(self.code, self.scale, self.ma, self.datalen)
       ``''
     #### shows that in the composition of the URL of this API, `code` represents the stock code, `scale` represents the time interval (in minutes), `ma` is the average value (can be 5, 10, 15, 20, 25), and `datalen` is the number of data fetched at one time.
     #### is also accessed using the `requests` library, which gives json data with a structure similar to the following
     ```json
     [{"day": "2022-01-10 15:00:00", "open": "24.680", "high": "25.140", "low": "24.380", "close": "25.140", "volume": "3965150", "ma_price20": 21.105, "ma_volume20":3964285}]
     ```''
     #### shows that the API will return a list which holds `datalen` data. Each entry is a json dictionary containing the following main fields
     * #### day: time
     * #### open: the opening price
     * #### high: the highest share price for the time period
     * #### low: the lowest share price at that time
     * #### close: the closing price
     * #### volume: volume
     * #### ma_price20: average price
     * #### ma_volume20: average number of shares traded
     #### It is worth noting that the volume is in hundreds of shares.

   * ### Data fetching, and saving
     #### In order to fetch the stock data as quickly as possible, reduce API response time, and facilitate plotting, we specify that we fetch 500 pieces of data per stock, with an interval of 60 and an average value of 5.
     #### To make crawling and storing data efficient, we have encapsulated a data collection class `Stock`. The initialisation function of this class accepts an incoming value `code`, the stock code, as follows.
     ```python
     class Stock:
         def __init__(self, code, scale=5, ma=5, datalen=5):
             self.code = code
             # Intervals (minutes)
             self.scale = scale
             self.ma = ma
             # of individuals
             self.datalen = datalen
             self.bass_message_list = False
     ```
     #### The default values for `scale`, `ma` and `datalen` are 5, 5 and 5 respectively, so if you need to change these parameters you can do so directly. The main method for obtaining API data in this class is `get_storage_list`, as shown in the figure below.
     ```python
        def get_storage_list(self) -> [[]]:
            all_list_data = []
            url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php' \
                '/CN_MarketData.getKLineData?symbol={0}&scale={1}&ma={2}&datalen=' \
                '{3}'.format(self.code, self.scale, self.ma, self.datalen)
            res = requests.get(url=url).json()
            for each_data in res:
                all_list_data.append(
                    [
                        # Time
                        each_data['day'],
                        # Opening price
                        each_data['open'],
                        # Highest price
                        each_data['high'],
                        # Lowest price
                        each_data['low'],
                        # Closing price
                        each_data['close'],
                        # Volume (in hundreds of shares)
                        each_data['volume']
                    ]
                )
            return all_list_data
     ```
     #### In the session to get the data, we only get 6 key fields, i.e. time, open, high, low, close and volume. Once the data is obtained, the method `storage_csv` is called to store it as a `csv` file. This is shown below.
     ```python
     @property
     def storage_csv(self):
         try:
             csv_obj = CSVkit.write(PATH='{0}.csv'.format(self.code),
                                   header=["Time", "Open", "High", "Low", "Close", "Volume"],
                                   rows=self.get_storage_list())
             return csv_obj
         except Exception as e:
             return str(e)
     ```
     #### To use it, pass the stock code into the `Stock` class, it will crawl the data according to the default settings and then store the fetched file in a csv file in the current folder with the name of the stock. The file format is
      | Stock Code | Open | High | Low | Close | Volume |
      | -------- | -------- | ------ | ------ | ------- | ------- |
      | data | data | data | data | data | data | data | data
      | ...    | ...    | ...   ... | data | data | data | data | data | ...  ... | ...   | ...   |...
## Data preparation and cleaning
   * ### Reading data from an already stored `csv` file
     #### We have defined a function to fetch `csv` data as follows.
     ```python
     import csv 
     # Read CSV functions
     def CSVread(PATH, Reading_method='r'):
         with open(PATH, Reading_method) as this_file_read:
         csv_reader = csv.reader(this_file_read)
         _content_List_ = []
         for i in csv_reader:
             _content_List_.append(i)
         return _content_List_
     ```
     #### This function accepts an incoming value `PATH` which is the file address of the file to be read, and `Reading_method` which is the reading method, defaulting here to `r`, i.e. read-only mode. The function uses Python's own `csv` library to read, storing each line of the file in a list, and then storing each line list to a total list to return for subsequent iterations of the data.
   * ### Define class `CSVobjects` to initially clean the data
     #### Its role is to read the contents of the target csv file and has multiple functions for extracting information from the target csv file, as follows.
      ```python
      class CSVobjects:
          def __init__(self, _content: list):
          self._content = _content
      ```
      #### The initialization function accepts a `_content` field. This field is a list of the contents of the target function, i.e. the `CSVread` function that needs to be called as described above. The initialisation function copies it to the class variable `_content` to facilitate subsequent calls to class functions within the class.
      The #### main function `specifyROW` is used to return a list of data in the appropriate range based on the user's input, as follows
      ```python
       def specifyROW(self, **kwargs) -> str or list:
           """
          :param kwargs: start_num:int,end_num:int,equal:bool
          :return: List

          * When equal is true, data in the range `[start_num,end_num]` will be returned

          * When equal is False, data in the range `[start_num,end_num)` will be returned
          """
          if "start_num" not in kwargs:
               kwargs.setdefault("start_num", 0)
          if "end_num" not in kwargs:
               kwargs.setdefault("end_num", len(self._content))
          if "equal" not in kwargs:
               kwargs.setdefault("equal", False)

          start_num = int(kwargs["start_num"])
          end_num = int(kwargs["end_num"])

          if start_num >= end_num:
               return "start_num '%s' must smaller than '%s" % (start_num, end_num)
          elif start_num < 0 or end_num < 0:
               return "input must bigger than 0 or it is 0."
          else:
               return_list:[] = []
               for i in self.__get_iterator(start_num,end_num,kwargs["equal"]):
                    return_list.append(self._content[i])
               return return_list
     ```
     #### This class of functions can receive multiple input values, the input value `start_num` represents the start index position, for example, when `start_num` is 0, it will return the first line of the csv file, that is, the location of the file header; `end_num` for the end index position, if not passed in these two parameters, the program will default to the full list of data returned; ` equal` indicates whether the end index position is desirable, if `True` is considered desirable, then the returned data list contains the data list of the line where the end index position is located.
     #### This function calls a private function of the class `__get_iterator` to scan the entire list of data item by item according to the condition and then return the target list of data. This is shown below.
     ```python
     @staticmethod
     def __get_iterator(start_value: int, end_value: int, equal: bool):
          if equal == True:
               while start_value <= end_value:
                    yield start_value
                    start_value += 1
          else:
               while start_value < end_value:
                    yield start_value
                    start_value += 1
     ```
     #### The class decorator `@staticmethod` transforms `__get_iterator` into a static method (in line with the PEP8 specification), which essentially generates an iterator that keeps returning the data that matches the condition to the list based on the condition. This has the advantage of not taking up too much memory and saving time.
     #### In addition, the `CSVobjects` class has the method `header` to return the file header of the current csv file, as follows.
     ```python
     @property
     def header(self):
          return self._content[:1][0]
     ```
     #### This part is more important for further data pre-processing later on
     * ### Using the `pandas` library to clean, manage data
     #### pandas is a powerful toolset for analysing structured data; it is based on the use of Numpy (which provides high performance matrix operations); it is used for data mining and data analysis, and also provides data cleansing capabilities. This project uses its built-in `DateFrame` module to manage the data
     #### According to the requirements of the project, we need to check if there are any gaps in the target data and get a list of the data in the target csv file arranged in columns. To do this we define a function `return_DF_list` that does.
     ```python
     def return_DF_list(code):
          var_path = './Storage/{0}.csv'.format(code)
          CSVobj = CSVobjects(_content=CSVread(PATH=var_path))
          all_content = CSVobj.specifyROW()[1:]
          header = CSVobj.header
          index = CSVobj.index
          DF = pd.DataFrame(data=all_content, columns=header, index=index)
          # Get the number of rows
          All_Rows = DF.shape[0]
          # Get the number of columns
          All_Columns = DF.shape[1]
          # Get the statistics
          # print(DF.describe())
          # Determine if any values are empty
          ALL_list = []
          for columns in header:
               the_loop = []
               for rows in range(1, All_Rows + 1):
                    time.sleep(0.001)
                    cur_value = DF.loc[rows, '{0}'.format(columns)]
                    the_loop.append(cur_value)
                    print('\r', "< {0} > The system is checking the value of column label {1}".format(var_path, columns) + "and row label {0}".format(rows), end='', flush=True)
                    if not cur_value:
                         print('The value of column label {0}, row label {1} is empty. '.format(columns, rows))
                    else:
                         pass
               ALL_list.append(the_loop)
          return ALL_list
     ```
     #### As shown in the code above, the function accepts a parameter `code`, which is the stock code, the function will automatically stitch into the corresponding file path and use `CSVobjects` to initially collate the data, then construct `pd.DataFrame` after obtaining the initial list of data and the file header. Once loaded, it will iterate over the row labels (i.e. the file header) and then iterate over the row labels twice under them, using the `DF.loc` function to locate the elements in the current table and determine if they are empty. If it is empty the program will print the empty value and stop running. The program will then progressively read and determine the value of each table and store the data for each column by row label.
     The #### `return_DF_list` function will eventually return a list of the data in the csv file grouped by row labels. Subsequent analysis of the data is based on this data.
## Analysis of the data and questioning
   * ### Using the web interface to display K-line charts
     #### This project uses Python's built-in `Socket` library to implement a simple HTTP server to display HTML pages. It is shown below.
     ```python
        sock = socket.socket()
        port = 8000
        while True:
            try:
                sock.bind(("127.0.0.1", port))
                sock.listen(5)
                print('Go to http://{0}:{1} to view the report'.format('127.0.0.1', port))
                break
            except:
                port += 1
                continue
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1000000000)
            print("You Get: ", data)  # 打印请求内容

            try:
                conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
                conn.send(b'%s' % bytes(r_d, encoding="utf8"))
            except:
                continue

            conn.close()
     ```
     #### As described above, the program first creates a new socket using `socket.socket()`, then binds the local port `8000` and listens on this port. It then uses `While True` to constantly prepare to receive requests from users. If a user request is received, the HTML file of the display interface is returned to the user.
     #### r_d is the content of the HTML file of the display interface, which needs to be converted to Byte type before it can be sent to the user
     #### The front-end page uses the `Echarts` framework to display the data. ECharts, an open source visualisation library implemented in JavaScript, runs smoothly on PC and mobile devices and is compatible with most current browsers (IE8/9/10/11, Chrome, Firefox, Safari, etc.), the underlying Relies on the lightweight vector graphics library ZRender to provide intuitive, interactive and highly customisable data visualisation charts.
     #### `ECharts` provides the usual line, bar, scatter, pie and K-line charts, box charts for statistics, maps, heat maps and line charts for geographic data visualisation, relationship and sunburst charts for relational data visualisation, parallel coordinates for multidimensional data visualisation, funnel charts for BI, dashboards and support for mixing and matching between charts.
     #### `Echarts` is introduced as follows.
     ```html
     <!DOCTYPE html>
          <html>
          <head>
          <meta charset="utf-8" />
          <!-- 引入刚刚下载的 ECharts 文件 -->
          <script src="echarts.js"></script>
          </head>
        </html>
     ```
     #### We configure the charts using one of the professional k-line chart configuration items. This chart is highly interactive, responsive and has a professional looking interface. The configuration items are shown below
     ```javascript
     var myChart = echarts.init(document.getElementById('mainnew'));
     const upColor = '#ec0000';
     const upBorderColor = '#8A0000';
     const downColor = '#00da3c';
     const downBorderColor = '#008F28';
     // Each item: open，close，lowest，highest
     const data0 = splitData(
     Your Data List
     );
     function splitData(rawData) {
     const categoryData = [];
     const values = [];
     for (var i = 0; i < rawData.length; i++) {
     categoryData.push(rawData[i].splice(0, 1)[0]);
     values.push(rawData[i]);
     }
     return {
     categoryData: categoryData,
     values: values
     };
     }
     function calculateMA(dayCount) {
     var result = [];
     for (var i = 0, len = data0.values.length; i < len; i++) {
     if (i < dayCount) {
          result.push('-');
          continue;
       }
     var sum = 0;
     for (var j = 0; j < dayCount; j++) {
          sum += +data0.values[i - j][1];
     }
     result.push(sum / dayCount);
     }
     return result;
     }
     ```
     #### As shown above, simply replace `Your Data List` with a list of data retrieved from within the program. The list data format is
     ```python
     [[time, open, high, low, close, volume], [... , ...] , ...]
     ```
     #### Code needs to be written to clean the stock data to be analysed. As shown below.
     ```python
     # Self-selected stocks, manually enter the stock code
     ALL_list = return_DF_list(code='sz002217')
     # SSE index
     ALL_list_sh = return_DF_list(code='sh000001')
     # The k-line chart for this period (WEB display)
     k = []
     # all_times = [i for i in ALL_list[0]]
     for i in range(0, len(ALL_list[0])):
          k.append(
               [
               ALL_list[0][i],
               float(ALL_list[1][i]),
               float(ALL_list[2][i]),
               float(ALL_list[3][i]),
               float(ALL_list[4][i]),
               float(ALL_list[5][i])
               ]
          )
     with open('Templates/show.html', 'r') as f:
            r_d = f.read().replace('@data', str(k))
     ```
     #### As shown above, the user customizes the input of two stock codes (which must be stored in csv beforehand), gets the corresponding data list through the `return_DF_list` function, and then iterates over it, taking out each piece of data and putting it into the total list; then opens the file where the front-end is located through `open`, replaces the obtained data into it, and finally sends the replaced data then open the file in which the front-end is located by `open` and replace it with the data obtained.
     ! [Image text](Storage/PIC/K line chart report.png)

   * ### Use the web interface to show the difference between the broad market and the currently selected stock for different indicators
     #### The specific front-end configuration method is similar to the above. The data acquisition method needs to be written by yourself, as shown below.
     ```python
     
     def draw_sh_this(input_list_stock, sh_stock_list, type='open'):
          global flag_num
          publicTime = []
          public_all = []
          public_sh = []
          for eachTIMES in input_list_stock[0]:
               if eachTIMES in sh_stock_list[0]:
                    publicTime.append(eachTIMES)
          for i in range(0, len(input_list_stock[0])):
               if input_list_stock[0][i] in publicTime:
                    public_all.append(
                         [
                              input_list_stock[0][i],
                              input_list_stock[1][i],
                              input_list_stock[2][i],
                              input_list_stock[3][i],
                              input_list_stock[4][i],
                              input_list_stock[5][i],
                         ]
                    )
          for j in range(0, len(sh_stock_list[0])):
               if sh_stock_list[0][j] in publicTime:
                    public_sh.append(
                    [
                              sh_stock_list[0][j],
                              sh_stock_list[1][j],
                              sh_stock_list[2][j],
                              sh_stock_list[3][j],
                              sh_stock_list[4][j],
                              sh_stock_list[5][j],
                    ]
                    )
          if type == 'open':
               flag_num = 1
          elif type == 'high':
               flag_num = 2
          elif type == 'low':
               flag_num = 3
          elif type == 'close':
               flag_num = 4
          elif type == 'volume':
               flag_num = 5
          x_label_sh = [float(i[flag_num]) for i in public_sh]
          x_label = [float(i[flag_num]) for i in public_all]
          times_sh = [i[0] for i in public_sh]
          return str(x_label_sh), str(x_label), str(times_sh), type
     ```
     #### As shown above, the function takes three fields, the first `input_list_stock` accepts a list of data for the selected stock; the second parameter `sh_stock_list` is a list of data for the broad market and `type` is the name of the indicator to be extracted, optionally open, close, high, low and volme.
     #### iterates over each of the two lists, extracting the target parameters (depending on the value of type) and the respective time lists and returning them. Subsequent code will embed this in the HTML page and eventually render the chart. This is shown below
     #### ![Image text](DataAnalytics/Storage/PIC/echarts.png)
     

   * ### Question 1: Correlation analysis of stock averages and equity numbers
     #### The first step is for the user to select the stock codes to be analysed (data must be obtained well in advance and stored in a csv file), as shown in the figure.
     ```python
     class Setting(object):
          def __init__(self):
          # Custom rules need to be added to this again
          self.all_return = []

          @staticmethod
          def add(func):
               def target_adding():
                    target_static = {}
                    for eachscode in func():
                         target_static['{0}'.format(eachscode)] = './Storage/{0}.csv'.format(eachscode)
                    return target_static
               return target_adding()

          @property
        def return_all_static(self) -> dict:
                @self.add
                def _():
                    static_lists = [
                        'sz002217',
                        'sz000620',
                        'sz002613',
                        'sz002317',
                        'sz300398',
                        'sh600476'
                    ]
                    return static_lists
                return _
     ```
     #### As shown above, we have written a `Setting` class that gets the user's selection, which defines a main function `return_all_static`. Within this function, an unnamed function `_` is decorated with the `add` decorator, which returns a list of stocks, which are the stock codes to be compared. The decorator transforms the list of stocks within this function into a dictionary in the format of
     ```text
     "stock code" : "corresponding data file storage address"
     ```
     #### The advantage of this is that the user only needs to delete the list of stocks within the nameless function, after which the data cleaning program can determine which stocks need to be cleaned for the program, facilitating the management of the stock data visualisation by the user.
     #### The second step is to write the data visualisation code to extract the relevant stock data and perform the data extraction based on the stock code selected by the user, as follows.
     ```python
     def boxplot(input_dict):
          labels = []
          alldata = []
          for code, paths in input_dict.items():
               labels.append(code)
               cur_all_average = []
               list_cur = return_DF_list(code=code)
               for j in range(0, len(list_cur[0])):
                    cur_all_average.append(
                              (float(list_cur[2][j]) + float(list_cur[3][j])) / 2,
                    )
               alldata.append(cur_all_average)

          plt.boxplot(alldata, labels=labels)
        plt.show()
     ```
     #### As shown above, the function `boxplot` accepts an `input_dict` parameter in the format of a dictionary. The dictionary is all the ticker symbols that need to be displayed visually. The program iterates through the dictionary by disassembling the dictionary key-value pairs, putting all the keys of the dictionary, i.e. the ticker symbols, into the `label` list; at the same time, according to the value, i.e. the path of the file corresponding to the ticker data, the `return_DF_list` method is used to obtain a list of all the data in that file (sorted by column label). It is now known that the ones in the second and third positions correspond to the lowest and highest prices of the stock. These two variables are taken out of the iterator and averaged to obtain a list of the means of all the data bars for the stock, which is then stored in the list `cur_all_average`. Finally a box plot is drawn using plt. The results of the run are shown below.
     #### ! [Image text](box.jpg)
     #### As can be seen from the graph, sz002317 has the highest overall mean and the entire box is at the highest and the box is the longest in width, indicating the highest variance and the lowest stability. This means that sz300398 has the highest returnable range, but also the highest risk due to the high and variable share price. sz002217 and sz000620 have about the same stability in comparison, both being at a lower level with a smoother share price, but are more suitable for risk averse investment players as sz000620 has a lower share price and the lowest overall and mean values.
   * ### Question 2: Correlation analysis of stock averages and number of share capital
     #### The data cleaning process is shown below.
     ```python
    
     # Average price: Self-selecting function
     averge_self_stock = [(float(i[2]) + float(i[3]))/2 for i in public_all] 。
     # Average price: Large property
     averge_sh_stock = [(float(i[2]) + float(i[3])) / 2 for i in public_sh] ?
     # Scatterplot
     plt.scatter(averge_self_stock, averge_sh_stock, color='red', label='TEST')
     plt.legend()  # Show legend
     plt.show()
     return str(x_label_sh), str(x_label), str(times_sh), type
     ```
     #### A stock code is selected and a list of its data is obtained using `return_DF_list` and this analysis is also performed on the broader stock market. It is then necessary to find the intersection of the stock in time that overlaps with the broader market data in time, and gradually remove the common parts by iterative methods until the cleaning is finally completed. The final front-end rendering is shown below
     #### ![Image text](plot.jpg)
     #### From the graph, we can see that the share price of sz002217 and the price of the general market are positively correlated, from the lower left corner of the image to the upper right is the correlation tendency of the image. The higher the price of the broader market, the higher the share price becomes; when the broader market moves badly, the share price also falls off.
   * ### Question 3: Relationship between trading volume and share price (mean) of a stock
     #### It can be seen that it is only necessary to obtain the time series as well as the share price as follows
     ```python
     def q3(code):
          the_stock_list = return_DF_list(code=code)
          # Trading volume for this period
          v = [float(i) / 39030660 for i in the_stock_list[5]]
          print('\n')
          print(v)
          times = the_stock_list[0]
          aver_price = []
          for i in range(0, len(the_stock_list[0])):
               aver_price.append((float(the_stock_list[2][i]) + float(the_stock_list[3][i])) / 2)
          print(aver_price)
          plt.plot(times, aver_price, color='green', label='aver_price')
          plt.bar(times, v, color='red', label='Volume')
          plt.savefig('q3.jpg')
          plt.legend()
          plt.yticks([])  # Removing the y-axis

          plt.xticks([])  # Removing the x-axis
          plt.show()
     ```
     As shown above, the function `q3` takes one argument `code`. The function `return_DF_list` is called to obtain a list of data for that stock. The data list is iterated through, and since the lowest and highest prices are in the third and fourth columns of the list, this logic is used to extract the lowest and highest prices and average them out into the list. The same can be done for the time list and the volume list. Using plt for plotting, with stock code `sz00060` as an example, the chart is shown below.
     #### ![Image text](q3.png)
     #### The waveform on the chart shows that volume and price are positively correlated, with the stock price on a downward trend when volume is at a low point, and a higher slope when volume surges.

   

   
     
   
     
