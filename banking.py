# Write your code here

import random
import sqlite3

class bank():
    
    def __init__(self):
        # init a dict to store as {'card number' : pin }
        #self.card_and_pin = dict()
        #self.card_and_balance = dict()
        # a handle/ cursor connectd to data base
        self.db_connect = sqlite3.connect("card.s3db")
        self.db_cur = self.db_connect.cursor()
        #self.db_cur.execute('CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
        #self.db_connect.commit()
        # record the number of the records now
        self.record_num =  len(self.db_cur.execute("SELECT * FROM card").fetchall())
    def bank_interface(self):
        #bank_interface deal the users' request 
        while True:
            # the option system provied
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')
            command = input()

            if command == '1':
                self.creat_account()
            elif command == "2":
                exit_flag = self.log_in
                # if user directly exit
                if exit_flag:
                    print('Bye!')
                    break
            elif command == "0":
                print('Bye!')
                break

    def creat_account(self):
        #In our banking system, the IIN must be 400000.
        IIN = '400000'
        account_num = self.get_account_number()
        #check unique
        while self.db_cur.execute(f'SELECT * FROM card WHERE number = {IIN + account_num}').fetchone():
            #get a number again if not unique
            account_num = self.get_account_number()
        # add IIn to head
        account_num = IIN + account_num
        #genetate a pin number
        pin_num = str(random.randint(0, 9999))
        if len(pin_num) < 4:
            pin_num = ('0'*(4-len(pin_num))) + pin_num

        # add card number & pin to dictionary
        #self.card_and_pin[account_num] = pin_num
        #self.card_and_balance[account_num] = 0
        # add the record to database
        self.record_num = self.record_num +1
        self.db_cur.execute(f'INSERT INTO card (id, number, pin) VALUES ({self.record_num},"{account_num}","{pin_num}")')
        self.db_connect.commit()
        print('Your card has been created')
        print("Your card number:")
        print(account_num)
        print('Your card PIN:')
        print(pin_num)

    def get_account_number(self):
        #t a unique and have a length of 16 digits for account number.
        account_num = str(random.randint(0,(1E9)-1))
        # if it is not enough 9 digitals, padding it to 16
        if len(account_num) < 9:
            account_num = ('0'*(9-len(account_num))) + account_num
        # get a sum check number
        luhn_num = self.get_check_digital(account_num)
        account_num = account_num + luhn_num
        # return generated number
        return account_num

    def get_check_digital(self,account_num):
        # pad the IIN number for sum check
        s = 0
        account_num = '400000' + account_num
        for i in range(len(account_num)):
            # if it is a odd digital (i is even), double it
            if i%2 == 0:
                n = int(account_num[i]) * 2
            else:
                n = int(account_num[i])
            # if n > 9, sunstract by 9
            if n > 9:
                n = n-9
            # sum it
            s = s + n
        # get a luhn number
        total = (int(s/10) +1) * 10
        luhn_num = total - s
        # in case luhn num is just 10
        if luhn_num%10 == 0 :
            luhn_num = 0
        return str(luhn_num)

    @property
    def log_in(self):
        # 
        print('Enter your card number:')
        card_num = input()
        print('Enter your PIN:')
        pin_num = input()
        # try to select the card records
        # loged in if num and password are right
        selecter = self.db_cur.execute(f'SELECT * FROM card WHERE number = {card_num}').fetchone()
        if selecter and (selecter[2] == pin_num):
            exit_flag = self.loged_in(card_num)
            return exit_flag
        else:
            print('Wrong card number or PIN!')
            return

    def loged_in(self,card_num):
        print('You have successfully logged in!')
        #loop in loged interface
        while True:
            # read balance at begining of the loop
            balance = self.db_cur.execute(f'SELECT * FROM card WHERE number = {card_num}').fetchone()[-1]
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')

            command = input()
            if command == "1":
                print(f'Balance: {balance}')
            if command == "2":
                self.add_income(card_num, balance)
            if command == "3":
                self.do_transfer(card_num, balance)
            if command == "4":
                self.db_cur.execute(f'DELETE FROM card WHERE number = {card_num}')
                self.db_connect.commit()
                print('The account has been closed!')
                return None
            if command == "5":
                print('You have successfully logged out!')
                return None
            if command == '0':
                # return exit flag
                return True

    def add_income(self, card_num, balance):
        print("Enter income:")
        # add to database
        income = input()
        new_balance = str(balance + int(income))
        print(f'new balance after add is {new_balance}')
        self.db_cur.execute(f'UPDATE card SET balance = {new_balance} WHERE number = {card_num}')
        self.db_connect.commit()
        print('Income was added!')
        return

    def do_transfer(self, my_card_num, balance):
        print('Enter card number:')
        target_card = input()
        if target_card == my_card_num:
            print('You can''t transfer money to the same account!')
            return

        if (not self.luhn_test(target_card)):
            print('Probably you made a mistake in the card number. Please try again')
            return
        # read target record
        target_record = self.db_cur.execute(f'SELECT * FROM card WHERE number = {target_card}').fetchone()
        if target_record:
            target_balance = target_record[-1]
            print("Enter how much money you want to transfer:")
            transfer_amount = int(input())
            if transfer_amount < balance:
                balance = balance - transfer_amount
                target_balance = target_balance + transfer_amount
                # write the data base
                self.db_cur.execute(f'UPDATE card SET balance = {balance} WHERE number = {my_card_num}')
                self.db_cur.execute(f'UPDATE card SET balance = {target_balance} WHERE number = {target_card}')
                self.db_connect.commit()
                print("Success!")
                return
            else:
                print("Not enough money!")
                return
        else:
            print('Such a card does not exist.')
            return

    def luhn_test(self, card_number):
        total = 0
        for i in range(len(card_number) - 1 ):
            if i%2 == 0:
                num = int(card_number[i]) *2
            else:
                num = int(card_number[i])
            if num > 9:
                num = num -9
            total = total + num
        total = total + int(card_number[-1])
        #print(f'luna sum is {total}')
        if total%10 == 0:
            return True
        else:
            return False
# call part
if __name__ == "__main__":
    my_bank = bank()
    my_bank.bank_interface()

