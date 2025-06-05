import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils import load_css, check_authentication, format_currency, get_country_info

# Page configuration
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# Load custom CSS
load_css()

# Check authentication
check_authentication()

if st.session_state.get("logged_in", False):
    with st.sidebar:
        st.header("Navigation")
        if st.button("Dashboard"):
            st.switch_page("streamlit_app.py")
        if st.button("Expense Tracker"):
            st.switch_page("pages/Expense_Tracker.py")
        if st.button("Expense Calculator"):
            st.switch_page("pages/Expense_Calculator.py")
        if st.button("Visa Planner"):
            st.switch_page("pages/Visa_Planner.py")
        if st.button("Community"):
            st.switch_page("pages/Community.py")
        if st.button("Job Board"):
            st.switch_page("pages/Job_Board.py")

country_info = get_country_info()
currency_symbol = country_info[st.session_state.selected_country]['symbol']

# Initialize expense data in session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = [
        {"date": "2024-01-01", "category": "Rent", "amount": 800.00, "description": "Monthly rent payment"},
        {"date": "2024-01-02", "category": "Food", "amount": 45.50, "description": "Groceries"},
        {"date": "2024-01-03", "category": "Travel", "amount": 25.00, "description": "Bus pass"},
        {"date": "2024-01-04", "category": "Utilities", "amount": 120.00, "description": "Electricity and water"},
        {"date": "2024-01-05", "category": "Food", "amount": 12.50, "description": "Lunch"},
    ]

if 'budget' not in st.session_state:
    st.session_state.budget = {
        "Rent": 800,
        "Food": 300,
        "Travel": 100,
        "Utilities": 150,
        "Entertainment": 100,
        "Other": 50
    }

def main():
    st.markdown("""
    <div class="breadcrumb">
        <span>🎓 StudyAbroad Platform</span> > <span>Expense Tracker</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Back to dashboard button
    if st.button("← Back to Dashboard", key="back_to_dashboard"):
        st.switch_page("streamlit_app.py")
    
    st.title("💰 Expense Tracker")
    st.markdown("Track your daily expenses and monitor your budget")
    
    # Welcome message with progress
    if 'expenses' in st.session_state and len(st.session_state.expenses) > 0:
        total_expenses = len(st.session_state.expenses)
        st.success(f"Great job! You've tracked {total_expenses} expenses so far. Keep it up!")
    else:
        st.info("Welcome to your expense tracker! Start by adding your first expense below.")
    
    # Budget overview cards
    st.subheader("Budget Overview")
    
    # Calculate totals
    df_expenses = pd.DataFrame(st.session_state.expenses)
    if not df_expenses.empty:
        df_expenses['date'] = pd.to_datetime(df_expenses['date'])
        current_month_expenses = df_expenses[df_expenses['date'].dt.month == datetime.now().month]
        spent_by_category = current_month_expenses.groupby('category')['amount'].sum().to_dict()
    else:
        spent_by_category = {}
    
    total_budget = sum(st.session_state.budget.values())
    total_spent = sum(spent_by_category.values())
    remaining = total_budget - total_spent
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Total Budget</h3>
                <div class="metric-value">{format_currency(total_budget)}</div>
                <div class="metric-change neutral">Monthly allocation</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Total Spent</h3>
                <div class="metric-value">{format_currency(total_spent)}</div>
                <div class="metric-change {'positive' if total_spent <= total_budget * 0.8 else 'negative'}">
                    {(total_spent/total_budget)*100:.1f}% of budget
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Remaining</h3>
                <div class="metric-value">{format_currency(remaining)}</div>
                <div class="metric-change {'positive' if remaining > 0 else 'negative'}">
                    {'Under budget' if remaining > 0 else 'Over budget'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Two columns layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Add expense form
        st.subheader("Add New Expense")
        
        with st.form("expense_form"):
            date = st.date_input("Date", datetime.now())
            category = st.selectbox("Category", list(st.session_state.budget.keys()))
            amount = st.number_input(f"Amount ({currency_symbol})", min_value=0.01, step=0.01)
            description = st.text_input("Description")
            
            if st.form_submit_button("Add Expense", use_container_width=True):
                new_expense = {
                    "date": date.strftime("%Y-%m-%d"),
                    "category": category,
                    "amount": float(amount),
                    "description": description
                }
                st.session_state.expenses.append(new_expense)
                st.success("Expense added successfully!")
                st.rerun()
    
    with col2:
        # Budget management
        st.subheader("Manage Budget")
        
        with st.form("budget_form"):
            st.markdown("Update your monthly budget allocations:")
            
            new_budget = {}
            for category, current_amount in st.session_state.budget.items():
                new_budget[category] = st.number_input(
                    f"{category} ({currency_symbol})",
                    min_value=0.0, 
                    value=float(current_amount),
                    step=10.0
                )
            
            if st.form_submit_button("Update Budget", use_container_width=True):
                st.session_state.budget = new_budget
                new_total = sum(new_budget.values())
                st.toast(f"New total budget: {format_currency(new_total)}")
                st.success("Budget updated successfully!")
                st.rerun()
    
    # Category breakdown
    if not df_expenses.empty:
        st.subheader("Category Breakdown")
        
        # Create category cards
        categories = list(st.session_state.budget.keys())
        cols = st.columns(len(categories))
        
        for i, category in enumerate(categories):
            with cols[i]:
                spent = spent_by_category.get(category, 0)
                budget = st.session_state.budget[category]
                percentage = (spent / budget * 100) if budget > 0 else 0
                
                status = "positive" if percentage <= 80 else "negative" if percentage > 100 else "neutral"
                
                st.markdown(f"""
                <div class="category-card">
                    <h4>{category}</h4>
                      <div class="category-amount">{format_currency(spent)} / {format_currency(budget)}</div>
                    <div class="progress-bar">
                        <div class="progress-fill {status}" style="width: {min(percentage, 100):.1f}%"></div>
                    </div>
                    <div class="category-percentage">{percentage:.1f}% used</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Spending by Category")
            if spent_by_category:
                fig_pie = px.pie(
                    values=list(spent_by_category.values()),
                    names=list(spent_by_category.keys()),
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_layout(
                    font=dict(size=12),
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Monthly Spending Trend")
            daily_spending = current_month_expenses.groupby('date')['amount'].sum().reset_index()
            
            if not daily_spending.empty:
                fig_line = px.line(
                    daily_spending,
                    x='date',
                    y='amount',
                    title='Daily Spending This Month'
                )
                fig_line.update_layout(
                    font=dict(size=12),
                    height=400,
                    xaxis_title="Date",
                    yaxis_title="Amount"
                )
                st.plotly_chart(fig_line, use_container_width=True)
    
    # Recent transactions
    st.subheader("Recent Transactions")
    
    if df_expenses.empty:
        st.info("No expenses recorded yet. Add your first expense above!")
    else:
        # Display recent transactions
        recent_expenses = sorted(st.session_state.expenses, key=lambda x: x['date'], reverse=True)[:10]
        
        for expense in recent_expenses:
            st.markdown(f"""
            <div class="transaction-item">
                <div class="transaction-content">
                    <div class="transaction-main">
                        <span class="transaction-description">{expense['description']}</span>
                        <span class="transaction-category">{expense['category']}</span>
                    </div>
                    <div class="transaction-details">
                        <span class="transaction-date">{expense['date']}</span>
                        <span class="transaction-amount">{format_currency(expense['amount'])}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Execute the page logic
if __name__ == "__main__":
    main()
