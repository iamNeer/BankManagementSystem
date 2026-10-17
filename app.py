import streamlit as st
from bank import Bank

st.set_page_config(
    page_title="My Banking System",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 My Banking System")
st.caption("Bank Account Management System")

user = Bank()

check = st.sidebar.selectbox(
    "Select an option",
    [
        "Dashboard",
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Details",
        "Update Details",
        "Delete Account"
    ]
)

if check == "Dashboard":
    col1, col2 = st.columns(2)

    col1.metric("Total Accounts", len(Bank.data))

    total_balance = sum(
        i['balance'] for i in Bank.data
    )

    col2.metric("Total Balance", f"Rs. {total_balance}")

    st.info("Select an option from the sidebar.")

elif check == "Create Account":
    st.subheader("Create Account")

    with st.form("create"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        email = st.text_input("Email")
        pin = st.text_input("4-digit PIN", type="password", max_chars=4)

        submit = st.form_submit_button("Create Account")

    if submit:
        success, result = user.createAccount(name, age, email, pin)

        if success:
            st.success("Account created successfully!")
            st.write("Name:", result["name"])
            st.write("Email:", result["email"])
            st.warning(f"Account Number: {result['account number']}")
        else:
            st.error(result)

elif check in ["Deposit Money", "Withdraw Money"]:
    st.subheader(check)

    with st.form("transaction"):
        accountNumber = st.text_input("Account Number")
        pinNumber = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount (Rs.)", min_value=0, step=100)

        submit = st.form_submit_button(check)

    if submit:
        if check == "Deposit Money":
            success, result = user.depositMoney(
                accountNumber, pinNumber, amount
            )
        else:
            success, result = user.withdrawMoney(
                accountNumber, pinNumber, amount
            )

        if success:
            st.success("Transaction successful")
            st.metric("Updated Balance", f"Rs. {result}")
        else:
            st.error(result)

elif check == "Show Details":
    st.subheader("Account Details")

    with st.form("details"):
        accountNumber = st.text_input("Account Number")
        pinNumber = st.text_input("PIN", type="password", max_chars=4)

        submit = st.form_submit_button("Show Details")

    if submit:
        details = user.showDetails(accountNumber, pinNumber)

        if details is None:
            st.error("No such account found")
        else:
            for key, value in details.items():
                st.write(f"**{key.title()}:** {value}")

elif check == "Update Details":
    st.subheader("Update Details")

    with st.form("update"):
        accountNumber = st.text_input("Account Number")
        pinNumber = st.text_input("Current PIN", type="password", max_chars=4)
        newName = st.text_input("New name (leave blank to skip)")
        newEmail = st.text_input("New email (leave blank to skip)")
        newPin = st.text_input("New PIN (leave blank to skip)", type="password", max_chars=4)

        submit = st.form_submit_button("Update Details")

    if submit:
        success, result = user.updateDetails(
            accountNumber, pinNumber, newName, newEmail, newPin
        )

        if success:
            st.success(result)
        else:
            st.error(result)

elif check == "Delete Account":
    st.subheader("Delete Account")

    with st.form("delete"):
        accountNumber = st.text_input("Account Number")
        pinNumber = st.text_input("PIN", type="password", max_chars=4)
        confirm = st.checkbox("I confirm account deletion")

        submit = st.form_submit_button("Delete Account")

    if submit:
        if not confirm:
            st.warning("Please confirm account deletion")
        else:
            success, result = user.deleteAccount(
                accountNumber, pinNumber
            )

            if success:
                st.success(result)
            else:
                st.error(result)