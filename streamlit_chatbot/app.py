import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Finance Tracker", layout="centered")

st.title("💰 TTTT Money Tracker")

# Store expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# User input
st.subheader("Your Bank Account Survivor")

with st.form("expense_form", clear_on_submit = True):
  category = st.selectbox(
    "Category",
    ["Food", "Transport", "Shopping", "Entertainment", "Study Supplies", "Other"]
)

  amount_input = st.text_input(
        "Enter Amount",
)
  submit = st.form_submit_button("Add Expenses")

if submit:
   try:
       amount = float(amount_input)
       
       expense_data = {
         "Category": category,
         "Amount": amount
       }
       st.session_state.expenses.append(expense_data)
       st.success("Expense Added!")

       st.session_state.amount_input = ""

   except ValueError:
       st.error("Please enter a valid number.")

    

# Show data
if st.session_state.expenses:

    df = pd.DataFrame(st.session_state.expenses)

    st.subheader("📋 Expense List")
    st.dataframe(df)

    # Total monthly expense
    total_expense = df["Amount"].sum()

    st.subheader("🗓️ Monthly Summary")
    st.write(f"Total Expenses This Month: RM {total_expense:.2f}")

    # Category totals
    category_summary = df.groupby("Category")["Amount"].sum()

    st.subheader("📊 Expenses by Category")

# Define colors for each category
    color_map = {
      "Food": "skyblue",
      "Transport": "lightyellow",
      "Entertainment": "lightgreen",
      "Shopping": "plum",
      "Study Supplies": "pink",
      "Others": "lightgrey"
    }

# Match colors to categories
    colors = [
      color_map.get(category, "gray")
      for category in category_summary.index
    ]

# Create figure
    fig, ax = plt.subplots()

# Create bar chart
    ax.bar(
      category_summary.index,
      category_summary.values,
      color=colors
    )

# Labels
    ax.set_title("Expenses by Category")
    ax.set_ylabel("Amount (RM)")
    ax.set_xlabel("Category")

    st.pyplot(fig)

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