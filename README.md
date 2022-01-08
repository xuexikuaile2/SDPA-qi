# OnlineBank


## Project function
   * > #### 1. Registration and login of different types of accounts
   * > #### 2. Online transfer and deposit
   * > #### 3. View transfer records stored locally
   * > #### 4. Modify the PIN code of the account
   * > #### 5. View account information and check available balance
   * > #### 6. Input check function
   * > #### 7. Exception handling function
   * > #### 8. Freeze/Unfreeze Account
     
## support
<img src = "https://warehouse-camo.ingress.cmh1.psfhosted.org/047074c34350165c9a6a57b844a2390d638c173d/68747470733a2f2f6769746875622e636f6d2f6a696e612d61692f6a696e612f626c6f622f6d61737465722f2e6769746875622f6261646765732f707974686f6e2d62616467652e7376673f7261773d74727565">

## Project structure
   * ### models.py
     * #### Base class `Account`
       Receive four parameters to set the attribute user name, PIN code, email, and address. In its `__init__()` function, initialize the user's initial balance `Balance` to 0 and state `State` to True
     * #### Subclass `SavingsAccount`
       It inherits from the base class `Account`. The characteristics of the `SavingsAccount` type account are: when it is transferring money, it needs to charge a 1% handling fee, and there is no interest rate on the deposit.
     * #### Subclass `CheckingAccount`
       Also inherited from the base class `Account`. The characteristics of the `CheckingAccount` type of account are: when it is transferring money, there is no need to charge a handling fee, and there is a certain interest rate for deposits.
   * ### handle.py
     * #### `TransactionHistory` class
       Four parameters are accepted: transfer initiator, transfer recipient, transfer date and transfer amount. This class uses the built-in function `return_to_storage_list` to generate data that can be directly inserted into the file, which is convenient for the main function `main.py` to call
   * ### main.py
     * #### `MainPage`
       Encapsulates all the functions of the initial page and defines related functions. `MainPage` mainly includes the login part and the registration part.
       * [README.md](https://github.com/xuexikuaile2/SDPA-qi/files/7833231/README.md)
#### Register Account
         Allow users to choose different registration types and enter relevant parameters to complete the registration. The registered data will be stored in a local text file.
       * #### Login Account
         The user logs in to the system by using his username and PIN code, and the program will switch to another theme page by calling the `success_page_interface` function of `SuccessPage`.
       * #### Unfreeze your account
         The user can release the freeze by entering the account number and PIN code. It is worth noting that when the account is frozen, the system will prohibit the user to log in.
     * #### `SuccessPage`
       It corresponds to the page that the user jumps to after successfully logging in. On the previous page, if the user correctly enters the user name and password, it will call the "SuccessPage"
       The `success_page_interface` function extracts the information of the currently logged in user and stores it as an attribute through the `__init__` function, which facilitates various data interactions on this page.
       This page provides 6 types of business options, users can select the serial number 1-6 for business
       * ##### Check the balance
         The business directly obtains the current account balance directly by calling the value of the attribute `balance`
       * ##### Online transfer
         The online transfer business realizes the transfer of amounts between different accounts. Before the transfer, the system will confirm the legitimacy of the transfer object and require the current user to enter the PIN code to verify its authenticity.
         After that, it will be judged whether the current balance can bear the transfer amount. Finally, according to the difference between different types of accounts, a 1% service fee will be deducted for savings accounts. After completing the transaction, regardless of
         Whether it succeeds or not, the transfer record will be generated and stored in a local file.
       * ##### View account information
         Check the account information, the system will inform the user of the current discounts and account details according to the account type
       * #### View transaction history
         Viewing the transfer records will retrieve the local storage records and inform users intuitively in the form of a table. The format of the transfer record is
         
         | Transfer initiator | Transfer recipient | Transfer time | Transfer amount | Transfer status |
         | -------- | -------- | ------ | ------ | ------- |
         | data | data | data | data | data |
       
       * #### Online Deposit
         The online deposit service allows users to deposit the amount entered.
       
       * #### Change PIN code
         Allow users to change their PIN code online, this modification will take effect immediately, and you need to log in with the new password the next time you log in.
       * #### Cancellation of accounts
         Will clear the user login status and return to the initial page `MainPage`
       * #### Freeze this account
         The system will freeze the current account, clear the current login information and return to the initial page. When the account is frozen, the system will ban the user. If you need to defrost, please go to the initial page
