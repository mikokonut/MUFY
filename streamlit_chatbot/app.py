import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finance Tracker", layout="centered")

st.title("💰 TTTT Money Tracker")

# Store expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# User input
st.subheader("Bank Account Survivor")

category = st.selectbox(
    "Category",
    ["Food", "Transport", "Shopping", "Entertainment", "Study Supplies", "Other"]
)

amount_input = st.text_input(
        "Enter Amount",
)
if amount_input:
   try:
       amount = float(amount_input)
       expense_data = {
          "Category": category,
          "Amount": amount
       }

       st.session_state.expenses.append(expense_data)

       st.success("Expense Added!")
   except ValueError:
       st.error("Please enter a valid number.")

# Show data
if st.session_state.expenses:

    df = pd.DataFrame(st.session_state.expenses)

    st.subheader("📋 Expense List")
    st.dataframe(df)

    # Total monthly expense
    total_expense = df["Amount"].sum()

    st.subheader("📅 Monthly Summary")
    st.write(f"Total Expenses This Month: RM {total_expense:.2f}")

    # Category totals
    category_summary = df.groupby("Category")["Amount"].sum()

    st.subheader("📊 Expenses by Category")
    st.bar_chart(category_summary)

    # Spending suggestion
    highest_category = category_summary.idxmax()
    highest_amount = category_summary.max()

    st.subheader("💡 Spending Suggestion")

    st.warning(
        f"You spent the most on '{highest_category}' "
        f"(RM {highest_amount:.2f}). "
        f"Consider reducing spending in this category."
    )

else:
    st.info("No expenses added yet.")