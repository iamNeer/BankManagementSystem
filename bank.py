# bank.py

import json
import random
import string
from pathlib import Path


class Bank:
    database = 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database, 'r') as fs:
                data = json.loads(fs.read())
        else:
            with open(database, 'w') as fs:
                json.dump([], fs)
    except Exception as err:
        print(f'An exception occurred: {err}')

    @staticmethod
    def __update():
        with open(Bank.database, 'w') as fs:
            fs.write(json.dumps(Bank.data, indent=4))

    @classmethod
    def __accountGenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spechar = random.choices("!@#$%^&*", k=1)

        id = alpha + num + spechar
        random.shuffle(id)

        return "".join(id)

    def createAccount(self, name, age, email, pin):
        if not name.strip():
            return False, "Name cannot be empty"

        if age < 18:
            return False, "You must be at least 18 years old"

        if not pin.isdigit() or len(pin) != 4:
            return False, "PIN must contain exactly 4 digits"

        info = {
            "name": name.strip(),
            "age": age,
            "email": email.strip(),
            "pin": pin,
            "account number": Bank.__accountGenerate(),
            "balance": 0
        }

        Bank.data.append(info)
        Bank.__update()

        return True, info

    def depositMoney(self, accountNumber, pinNumber, amount):
        userdata = [
            i for i in Bank.data
            if i['account number'] == accountNumber
            and i['pin'] == pinNumber
        ]

        if not userdata:
            return False, "No such account found"

        if amount <= 0 or amount > 20000:
            return False, "Deposit must be between Rs. 1 and Rs. 20,000"

        userdata[0]['balance'] += amount
        Bank.__update()

        return True, userdata[0]['balance']

    minimum_amount = 100

    def withdrawMoney(self, accountNumber, pinNumber, amount):
        userdata = [
            i for i in Bank.data
            if i['account number'] == accountNumber
            and i['pin'] == pinNumber
        ]

        if not userdata:
            return False, "No such account found"

        if amount <= 0:
            return False, "Amount must be greater than zero"

        if userdata[0]['balance'] < amount:
            return False, "Insufficient balance"

        if userdata[0]['balance'] - amount < Bank.minimum_amount:  #condition is true ,so the operation "withdraw money ids failed so, return false" 
            return False, "You must maintain a minimum balance of Rs. 100"

        userdata[0]['balance'] -= amount
        Bank.__update()

        return True, userdata[0]['balance']

    def showDetails(self, accountNumber, pinNumber):
        userdata = [
            i for i in Bank.data
            if i['account number'] == accountNumber
            and i['pin'] == pinNumber
        ]

        if not userdata:
            return None

        return {
            key: value
            for key, value in userdata[0].items()
            if key != 'pin'
        }

    def updateDetails(
        self, accountNumber, pinNumber,
        newName="", newEmail="", newPin=""
    ):
        userdata = [
            i for i in Bank.data
            if i['account number'] == accountNumber
            and i['pin'] == pinNumber
        ]

        if not userdata:
            return False, "No such account found"

        if newPin and (
            not newPin.isdigit() or len(newPin) != 4
        ):
            return False, "PIN must contain exactly 4 digits"

        if newName:
            userdata[0]['name'] = newName.strip()

        if newEmail:
            userdata[0]['email'] = newEmail.strip()

        if newPin:
            userdata[0]['pin'] = newPin

        Bank.__update()

        return True, "Your details are updated successfully"

    def deleteAccount(self, accountNumber, pinNumber):
        userdata = [
            i for i in Bank.data
            if i['account number'] == accountNumber
            and i['pin'] == pinNumber
        ]

        if not userdata:
            return False, "No such account found"

        if userdata[0]['balance'] != Bank.minimum_amount:
            return False, "Balance must be 100 before deleting"

        Bank.data.remove(userdata[0])
        Bank.__update()

        return True, "Your account is deleted successfully"