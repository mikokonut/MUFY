import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="Finance Tracker",
    layout="centered"
)

st.title("💰 TTTT Money Tracker")

# -----------------------------------
# Session State
# -----------------------------------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "allowance" not in st.session_state:
    st.session_state.allowance = 0.0

if "saving_goal" not in st.session_state:
    st.session_state.saving_goal = 0.0

# -----------------------------------
# Monthly Allowance
# -----------------------------------
st.subheader("🏦 Financial Life Support")

allowance = st.number_input(
    "Enter Your Monthly Allowance (RM)",
    min_value=0.0,
    step=10.0,
    value=st.session_state.allowance
)

st.session_state.allowance = allowance

# -----------------------------------
# Saving Goal
# -----------------------------------
st.subheader("🎯 Cha-ching Quest")

saving_goal = st.number_input(
    "Enter Your Saving Goal (RM)",
    min_value=0.0,
    step=10.0,
    value=st.session_state.saving_goal
)

st.session_state.saving_goal = saving_goal

# -----------------------------------
# Expense Form
# -----------------------------------
st.subheader("💵Your Bank Account Survivor")

with st.form("expense_form", clear_on_submit=True):

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Study Supplies",
            "Other"
        ]
    )

    amount_input = st.text_input("Enter Amount")

    submit = st.form_submit_button("Add Expense")

# -----------------------------------
# Add Expense
# -----------------------------------
if submit:

    try:
        amount = float(amount_input)

        if amount <= 0:
            st.error("❌ Amount must be greater than 0.")

        else:

            expense_data = {
                "Category": category,
                "Amount": amount
            }

            st.session_state.expenses.append(expense_data)

            st.success("✅ Expense Added!")

    except ValueError:
        st.error("❌ Please enter a valid number.")

# -----------------------------------
# Display Data
# -----------------------------------
if st.session_state.expenses:

    # Create DataFrame
    df = pd.DataFrame(st.session_state.expenses)

    st.subheader("📋 Expense List")

    # Display Expenses
    for i, expense in enumerate(st.session_state.expenses):

        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.write(expense["Category"])

        with col2:
            st.write(f"RM {expense['Amount']:.2f}")

        with col3:

            if st.button("🗑️", key=f"delete_{i}"):

                st.session_state.expenses.pop(i)
                st.rerun()

    # -----------------------------------
    # Calculations
    # -----------------------------------
    total_expense = df["Amount"].sum()

    # Savings deducted first
    available_budget = allowance - saving_goal

    # Remaining balance after expenses
    remaining_balance = available_budget - total_expense

    # -----------------------------------
    # Low Budget Reminder
    # -----------------------------------
    warning_limit = available_budget * 0.10

    if remaining_balance <= warning_limit and remaining_balance > 0:

        st.warning(
            f"⚠️ Warning: You only have "
            f"RM {remaining_balance:.2f} left "
            f"which is below 10% of your budget!"
        )

    # -----------------------------------
    # Monthly Summary
    # -----------------------------------
    st.subheader("🗓️ Monthly Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Allowance",
        f"RM {allowance:.2f}"
    )

    col2.metric(
        "Saving Goal",
        f"RM {saving_goal:.2f}"
    )

    col3.metric(
        "Expenses",
        f"RM {total_expense:.2f}"
    )

    col4.metric(
        "Balance",
        f"RM {remaining_balance:.2f}"
    )

    # -----------------------------------
    # Budget Progress
    # -----------------------------------
    if available_budget > 0:

        progress = min(total_expense / available_budget, 1.0)

        st.subheader("📉 Budget Usage")

        st.progress(progress)

        st.write(
            f"{progress * 100:.1f}% of your usable budget used"
        )

    # -----------------------------------
    # Saving Goal Status
    # -----------------------------------
    st.subheader("💎 Savings Status")

    if saving_goal > 0:

        st.success(
            f"RM {saving_goal:.2f} has been reserved for savings."
        )

        if remaining_balance >= 0:

            st.info(
                f"You still have RM {remaining_balance:.2f} "
                f"available to spend this month."
            )

        else:

            st.error(
                f"You exceeded your spending budget by "
                f"RM {abs(remaining_balance):.2f}."
            )

    # -----------------------------------
    # Category Summary
    # -----------------------------------
    category_summary = df.groupby("Category")["Amount"].sum()

    st.subheader("📊 Expenses by Category")

    # Color Map
    color_map = {
        "Food": "skyblue",
        "Transport": "lightyellow",
        "Entertainment": "lightgreen",
        "Shopping": "plum",
        "Study Supplies": "pink",
        "Other": "lightgrey"
    }

    colors = [
        color_map.get(category, "gray")
        for category in category_summary.index
    ]

    # -----------------------------------
    # Bar Chart
    # -----------------------------------
    fig, ax = plt.subplots()

    ax.bar(
        category_summary.index,
        category_summary.values,
        color=colors
    )

    ax.set_title("Expenses by Category")
    ax.set_ylabel("Amount (RM)")
    ax.set_xlabel("Category")

    # Straight category names
    plt.xticks(rotation=0)

    st.pyplot(fig)

    # -----------------------------------
    # Spending Suggestion
    # -----------------------------------
    highest_category = category_summary.idxmax()

    highest_amount = category_summary.max()

    st.subheader("💡 Spending Suggestion")

    st.warning(
        f"You spent the most on '{highest_category}' "
        f"(RM {highest_amount:.2f}). "
        f"Consider reducing spending in this category."
    )

    # -----------------------------------
    # Overspending Warning
    # -----------------------------------
    if remaining_balance < 0:

        st.error(
            "⚠️ You have exceeded your available spending budget!"
        )

else:
    st.info("No expenses added yet.")