from classes import bankaccount
a1 = bankaccount('Jane Wu', '19371554951', 20000)
a2 = bankaccount('Jeffrey Wong',  '19371564761', 20000)
a1.deposit(1000)
a1.withdraw(4000)
a2.withdraw(10500)
a1.withdraw(3500)
print ("a1's balance:", a1.balance)
print("a2's balance:",a2.balance)
a1.dump()
a2.dump()

