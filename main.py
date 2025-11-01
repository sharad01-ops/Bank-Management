import streamlit as st
import json
import random
import string
from pathlib import Path


# ------------------- Backend Logic -------------------
class Bank:
    database = 'data.json'

    def __init__(self):
        if Path(self.database).exists():
            with open(self.database, 'r') as fs:
                try:
                    self.data = json.load(fs)
                except json.JSONDecodeError:
                    self.data = []
        else:
            self.data = []
            

    def __update(self):
        with open(self.database, 'w') as fs:
            json.dump(self.data, fs, indent=2)

    def __generate_account(self):
        acc = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return acc

    def create_account(self, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return "You must be 18+ and have a 4-digit PIN."
        acc_no = self.__generate_account()
        data = {"name": name, "age": age, "email": email, "PIN": pin, "accountNo": acc_no, "balance": 0}
        self.data.append(data)
        self.__update()
        return f"Account created successfully! Your account number is {acc_no}"

    def deposit(self, acc_no, pin, amount):
        for user in self.data:
            if user['accountNo'] == acc_no and user['PIN'] == pin:
                if amount <= 0:
                    return "Amount must be positive."
                user['balance'] += amount
                self.__update()
                return f"Deposited ₹{amount}. New balance: ₹{user['balance']}"
        return "Invalid account number or PIN."

    def withdraw(self, acc_no, pin, amount):
        for user in self.data:
            if user['accountNo'] == acc_no and user['PIN'] == pin:
                if amount <= 0:
                    return "Amount must be positive."
                if user['balance'] < amount:
                    return "Insufficient balance."
                user['balance'] -= amount
                self.__update()
                return f"Withdrawn ₹{amount}. New balance: ₹{user['balance']}"
        return "Invalid account number or PIN."

    def show_details(self, acc_no, pin):
        for user in self.data:
            if user['accountNo'] == acc_no and user['PIN'] == pin:
                return user
        return None

    def update_details(self, acc_no, pin, new_name, new_email, new_pin):
        for user in self.data:
            if user['accountNo'] == acc_no and user['PIN'] == pin:
                if new_name:
                    user['name'] = new_name
                if new_email:
                    user['email'] = new_email
                if new_pin:
                    user['PIN'] = new_pin
                self.__update()
                return "Details updated successfully."
        return "Invalid account number or PIN."

    def delete_account(self, acc_no, pin):
        for user in self.data:
            if user['accountNo'] == acc_no and user['PIN'] == pin:
                self.data.remove(user)
                self.__update()
                return "Account deleted successfully."
        return "Invalid account number or PIN."


# ------------------- Streamlit UI -------------------
bank = Bank()
st.set_page_config(page_title="Python Bank", layout="centered")

st.title("🏦 Python Bank System")

menu = [
    "Create Account",
    "Deposit Money",
    "Withdraw Money",
    "Show Details",
    "Update Details",
    "Delete Account"
]
choice = st.sidebar.selectbox("Select an Action", menu)


# --- Create Account ---
if choice == "Create Account":
    st.header("Create New Account")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    email = st.text_input("Email")
    pin = st.text_input("4-Digit PIN", type="password")

    if st.button("Create Account"):
        if not (name and age and email and pin):
            st.warning("Please fill in all fields.")
        else:
            try:
                pin_int = int(pin)
                msg = bank.create_account(name, age, email, pin_int)
                st.success(msg)
            except ValueError:
                st.error("PIN must be numeric.")


# --- Deposit Money ---
elif choice == "Deposit Money":
    st.header("Deposit Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        try:
            pin_int = int(pin)
            msg = bank.deposit(acc_no, pin_int, amount)
            st.info(msg)
        except ValueError:
            st.error("PIN must be numeric.")


# --- Withdraw Money ---
elif choice == "Withdraw Money":
    st.header("Withdraw Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        try:
            pin_int = int(pin)
            msg = bank.withdraw(acc_no, pin_int, amount)
            st.info(msg)
        except ValueError:
            st.error("PIN must be numeric.")


# --- Show Details ---
elif choice == "Show Details":
    st.header("View Account Details")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        try:
            pin_int = int(pin)
            details = bank.show_details(acc_no, pin_int)
            if details:
                st.subheader("Account Information")
                st.json(details)
            else:
                st.error("Invalid account number or PIN.")
        except ValueError:
            st.error("PIN must be numeric.")


# --- Update Details ---
elif choice == "Update Details":
    st.header("Update Account Details")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    new_name = st.text_input("New Name (leave blank to keep current)")
    new_email = st.text_input("New Email (leave blank to keep current)")
    new_pin = st.text_input("New 4-Digit PIN (leave blank to keep current)", type="password")

    if st.button("Update"):
        try:
            pin_int = int(pin)
            new_pin_int = int(new_pin) if new_pin else None
            msg = bank.update_details(acc_no, pin_int, new_name, new_email, new_pin_int)
            st.info(msg)
        except ValueError:
            st.error("PIN must be numeric.")


# --- Delete Account ---
elif choice == "Delete Account":
    st.header("Delete Account")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    confirm = st.checkbox("I confirm I want to delete my account")

    if st.button("Delete"):
        if confirm:
            try:
                pin_int = int(pin)
                msg = bank.delete_account(acc_no, pin_int)
                st.error(msg)
            except ValueError:
                st.error("PIN must be numeric.")
        else:
            st.warning("Please confirm before deleting.")
