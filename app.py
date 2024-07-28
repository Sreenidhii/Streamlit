import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Type'])

if 'savings_goals' not in st.session_state:
    st.session_state.savings_goals = pd.DataFrame(columns=['Goal', 'Amount', 'Progress'])

# App title
st.title('Personal Finance Tracker')

# Transaction entry form
with st.expander("Add New Transaction"):
    with st.form("transaction_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Transportation", "Entertainment", "Other"])
        amount = st.number_input("Amount", min_value=0.0)
        transaction_type = st.radio("Type", ["Expense", "Income"])
        submitted = st.form_submit_button("Add Transaction")

        if submitted:
            new_entry = pd.DataFrame([[date, category, amount, transaction_type]], columns=['Date', 'Category', 'Amount', 'Type'])
            st.session_state.transactions = pd.concat([st.session_state.transactions, new_entry], ignore_index=True)
            st.success("Transaction added!")

# Savings goal entry form
with st.expander("Add Savings Goal"):
    with st.form("savings_goal_form"):
        goal_name = st.text_input("Goal Name")
        goal_amount = st.number_input("Goal Amount", min_value=0.0)
        progress = st.number_input("Current Progress", min_value=0.0)
        goal_submitted = st.form_submit_button("Add Savings Goal")

        if goal_submitted and goal_name:
            new_goal = pd.DataFrame([[goal_name, goal_amount, progress]], columns=['Goal', 'Amount', 'Progress'])
            st.session_state.savings_goals = pd.concat([st.session_state.savings_goals, new_goal], ignore_index=True)
            st.success("Savings goal added!")

# Convert Date column to datetime format
st.session_state.transactions['Date'] = pd.to_datetime(st.session_state.transactions['Date'], errors='coerce')

# Display transactions
st.subheader('Transaction Data')
st.dataframe(st.session_state.transactions)

# Display savings goals
st.subheader('Savings Goals')
st.dataframe(st.session_state.savings_goals)

# Plot expense vs income
st.subheader('Expense vs Income')
fig, ax = plt.subplots()

# Ensure Amount column is numeric
st.session_state.transactions['Amount'] = pd.to_numeric(st.session_state.transactions['Amount'], errors='coerce')

# Filter data
expense_data = st.session_state.transactions[st.session_state.transactions['Type'] == 'Expense']
income_data = st.session_state.transactions[st.session_state.transactions['Type'] == 'Income']

# Check if data is not empty
if not expense_data.empty:
    expense_data.groupby('Date')['Amount'].sum().plot(kind='line', label='Expenses', ax=ax)
else:
    st.write("No expense data to plot.")

if not income_data.empty:
    income_data.groupby('Date')['Amount'].sum().plot(kind='line', label='Income', ax=ax)
else:
    st.write("No income data to plot.")

ax.set_title('Expenses vs Income Over Time')
ax.set_ylabel('Amount')
ax.legend()
st.pyplot(fig)

# Plot expenses by category
st.subheader('Expenses by Category')
fig, ax = plt.subplots()

# Check if expense data is not empty
if not expense_data.empty:
    expense_data.groupby('Category')['Amount'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Expenses by Category')
else:
    st.write("No expense data to plot.")

st.pyplot(fig)

# Plot savings progress
st.subheader('Savings Goals Progress')
fig, ax = plt.subplots()

# Check if savings goals data is not empty
if not st.session_state.savings_goals.empty:
    st.session_state.savings_goals.set_index('Goal')['Progress'].plot(kind='bar', ax=ax)
    ax.set_title('Savings Goals Progress')
    ax.set_ylabel('Amount')
else:
    st.write("No savings goals data to plot.")

st.pyplot(fig)
