import streamlit as st
import random
import string
import json
from pathlib import Path

DATABASE = "data.json"

# ---------- Load Data ----------
def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            return json.load(f)
    return []

# ---------- Save Data ----------
def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Generate Account ----------
def generate_account():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

data = load_data()

st.set_page_config(page_title="BGI Bank", page_icon="🏦")

st.title("🏦 Bharat Growth & Investment Bank (BGI)")
st.write("Secure Digital Banking System")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Create Account", "Login", "Forgot PIN"]
)

# ================= CREATE ACCOUNT =================

if menu == "Create Account":

    st.subheader("Create New Account")

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1)
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN", type="password")

    if st.button("Create Account"):

        if age < 18:
            st.error("Age must be 18+")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be 4 digits")
        else:

            acc = generate_account()

            user = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "account_no": acc,
                "balance": 0
            }

            data.append(user)
            save_data(data)

            st.success("Account Created Successfully!")
            st.write("Your Account Number:", acc)
            st.balloons()

# ================= LOGIN =================

elif menu == "Login":

    st.subheader("Login to Your Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Login"):

        user = None

        for u in data:
            if u["account_no"] == acc and u["pin"] == int(pin):
                user = u
                break

        if user:

            st.success("Login Successful")

            option = st.selectbox(
                "Dashboard",
                ["Deposit", "Withdraw", "View Details"]
            )

            # Deposit
            if option == "Deposit":

                amt = st.number_input("Amount", min_value=1)

                if st.button("Deposit Money"):
                    user["balance"] += amt
                    save_data(data)

                    st.success("Deposit Successful")
                    st.balloons()

            # Withdraw
            elif option == "Withdraw":

                amt = st.number_input("Amount", min_value=1)

                if st.button("Withdraw Money"):

                    if amt > user["balance"]:
                        st.error("Insufficient Balance")
                    else:
                        user["balance"] -= amt
                        save_data(data)

                        st.success("Withdrawal Successful")

            # Details
            elif option == "View Details":

                st.write("Name:", user["name"])
                st.write("Age:", user["age"])
                st.write("Email:", user["email"])
                st.write("Account No:", user["account_no"])
                st.write("Balance:", user["balance"])

        else:
            st.error("Invalid Credentials")

# ================= FORGOT PIN =================

elif menu == "Forgot PIN":

    st.subheader("Reset PIN")

    acc = st.text_input("Account Number")
    email = st.text_input("Registered Email")
    new_pin = st.text_input("New 4 Digit PIN", type="password")

    if st.button("Reset PIN"):

        for u in data:

            if u["account_no"] == acc and u["email"] == email:

                u["pin"] = int(new_pin)
                save_data(data)

                st.success("PIN Reset Successful")
                st.balloons()
                break
        else:
            st.error("Invalid Account Number or Email")         