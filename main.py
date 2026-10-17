import json
import random
import string
from pathlib import Path

from django.conf.locale import tr
from matplotlib import use


class Bank:
    database='data.json'
    data=[]

    try:
        if Path(database).exists():
            with open(database,'r') as fs:
                data=json.loads(fs.read())
        else:
            print('no such file found')
    except Exception as err:
        print(f'An exception occurred: {err}')

    @staticmethod    
    def __update():
        with open(Bank.database,'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountGenerate(cls):
        alpha=random.choices(string.ascii_letters,k=3)
        num=random.choices(string.digits,k=3)
        spechar=random.choices("!@#$%^&*",k=1)
        id=alpha + num + spechar
        random.shuffle(id)
        return "".join(id)

    def depositMoney(self):
        accountNumber=input("tell your account number:-")
        pinNumber=int(input("tell your pin:-"))

        userdata=[i for i in Bank.data if i['account number']==accountNumber and i['pin']==pinNumber]

        if userdata == []:
            print("no such account found")
        else:
            print(userdata)
            amount= int(input("tell ypur amount;-"))
            if amount > 20000 and amount < 0:
                print ("you can not deposit more than 20000 and less than 0")
            else:
                userdata[0]['balance']+=amount
                print("your amount is successfully deposited ")
                Bank.__update()
    minimum_amount=100
    def withdrawMoney(self):
        accountNumber = input("tell your account number:-")
        pinNumber = int(input("tell your pin number:-"))

        userdata=[i for i in Bank.data if i['account number']==accountNumber and i['pin']==pinNumber]

        if userdata ==[]:
            print("no such account found")
        else:
            print(userdata)
            amount =int(input("tell your amount what you want to withdraw:-"))
            if userdata[0]['balance'] < amount:
                print("you have not sufficient balance in your account")
                
            else:
                if userdata[0]['balance']- amount<Bank.minimum_amount:
                    print("you have to keep minimum balance of 100 in your account and please try again")
                else:
                    userdata[0]['balance']-=amount
                    print ("your amount is successfully withdraw")
                    Bank.__update()   
                    
    def showDetails(self):
        accountNumber = input("tell your account number:-")
        pinNumber = int(input("tell your pin number:-"))

        userdata=[i for i in Bank.data if i['account number']==accountNumber and i['pin']==pinNumber]

        if userdata ==[]:
            print("no such account found")
        else:
            print(userdata)
            for i in userdata[0]:
                print(f'{i}:{userdata[0][i]}')

    def updateDetails(self):
        accountNumber=input('tell your account number:-') 
        try:
            pinNumber= int(input("tell ypur pin Number:-"))
        except ValueError:
            print("pin must be inter")

        userdata=[i for i in Bank.data if i['account number']==accountNumber and i['pin']==pinNumber]
        print("you can not update your account age and balance")
       
        if userdata==[]:
            print("no such account found")
        else:
            newData={
                        "name":input("tell your new name or skip:-"),
                        "email":input("tell your new email or skip:-"),
                        "pin":input("tell your new pin or skip:-")
                    }
            
            print(userdata)
            
            if newData['name']=="":
                newData['name']=userdata[0]['name']
            if newData['email']=="":
                newData['email']=userdata[0]['email']
            if newData['pin']=="":
                newData['pin']=userdata[0]['pin']

            if type(newData['pin']) == str:
                newData['pin']=int(newData['pin'])
                                          
            for i in newData:
                if newData[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i]=newData[i]
                    Bank.__update()
            print("your details are updated successfully")
            

    def deleteAccount(self):
        accountNumber=input("tell your account number:-")
        try:
            pinNumber=int(input("tell your pin number:-"))
        except ValueError:
            print("Pin must be a number")
            return

        userdata=[i for i in Bank.data if i['account number']==accountNumber and i['pin']==pinNumber]

        if userdata==[]:
            print('no such account found')
        else:
            userwill=input("are you sure you want to delete your account (yes/no):-")
            if userwill.lower() !='yes':
                print("you can acccess other features of your account")
            else:
                print(userdata[0])
                index=Bank.data.index(userdata[0])
                Bank.data.pop(index)
                Bank.__update()
                print("your account is deleted successfully")
                


    def createAccount(self):
        info={
            "name":input("tell your name:-"),
            "age":int(input("teel your age :-")),
            "email":input("tell your email:-"),
            "pin":int(input("tell your pin:-")),
            "account number":Bank.__accountGenerate(),
            "balance":0
        }

        if info['age'] < 18 or len(str(info['pin'])) !=4:

            print("you are not eligible for creating account")
        else:

            print("your account is created successfully")

            for i in info:

                print(f'{i}:{info[i]}')

            print("please note down your account number")
            Bank.data.append(info)
            Bank.__update()

user=Bank()
print("Press 1 for creating account")
print("press 2 for deposit money")
print("press 3 for withdrawing money")
print("press 4 for showing details")
print("press 5 for updating details")
print("press 6 for deleting account")

check= int(input("tell your response:-"))

if check==1:
    user.createAccount()

if check==2:
    user.depositMoney()

if check==3:
    user.withdrawMoney()

if check==4:
    user.showDetails()

if check==5:
    user.updateDetails()

if check==6:
    user.deleteAccount()