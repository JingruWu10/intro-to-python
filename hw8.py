class bankaccount(object):
    def __init__(self,name,account_number,initial_amount):
        self.balance=initial_amount
        self.name=name
        self.no=account_number

    def withdraw(self,amount):
        if self.balance-amount<0:
            print("Sorry, you do not have enough money in the acount")
        else:
            self.balance-=amount

    def deposit(self,amount):
        self.balance+= amount

    def dump(self):
        print("{},{},balance:{}".format(self.name,self.no,self.balance))

