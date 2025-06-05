import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_css, check_authentication, format_currency, get_country_info, render_sidebar

# Page configuration
st.set_page_config(page_title="Expense Calculator", page_icon="🧮", layout="wide")

# Load custom CSS
load_css()

# Check authentication
check_authentication()

if st.session_state.get("logged_in", False):
    render_sidebar()

# Cost data by country and lifestyle
COST_DATA = {
    "United States": {
        "budget": {"rent": 800, "food": 250, "transport": 80, "utilities": 100, "entertainment": 100, "other": 120},
        "moderate": {"rent": 1200, "food": 400, "transport": 120, "utilities": 150, "entertainment": 200, "other": 180},
        "comfortable": {"rent": 1800, "food": 600, "transport": 200, "utilities": 200, "entertainment": 400, "other": 300}
    },
    "United Kingdom": {
        "budget": {"rent": 700, "food": 200, "transport": 100, "utilities": 120, "entertainment": 80, "other": 100},
        "moderate": {"rent": 1000, "food": 350, "transport": 150, "utilities": 180, "entertainment": 150, "other": 170},
        "comfortable": {"rent": 1500, "food": 500, "transport": 250, "utilities": 250, "entertainment": 300, "other": 250}
    },
    "Canada": {
        "budget": {"rent": 600, "food": 200, "transport": 70, "utilities": 80, "entertainment": 70, "other": 80},
        "moderate": {"rent": 900, "food": 300, "transport": 100, "utilities": 120, "entertainment": 150, "other": 130},
        "comfortable": {"rent": 1300, "food": 450, "transport": 180, "utilities": 180, "entertainment": 250, "other": 200}
    },
    "Australia": {
        "budget": {"rent": 800, "food": 250, "transport": 90, "utilities": 100, "entertainment": 100, "other": 110},
        "moderate": {"rent": 1200, "food": 400, "transport": 140, "utilities": 150, "entertainment": 180, "other": 180},
        "comfortable": {"rent": 1700, "food": 600, "transport": 220, "utilities": 220, "entertainment": 350, "other": 280}
    },
    "Germany": {
        "budget": {"rent": 500, "food": 180, "transport": 60, "utilities": 80, "entertainment": 60, "other": 70},
        "moderate": {"rent": 750, "food": 280, "transport": 90, "utilities": 120, "entertainment": 120, "other": 120},
        "comfortable": {"rent": 1100, "food": 400, "transport": 150, "utilities": 180, "entertainment": 200, "other": 180}
    }
}

def main():
    st.markdown("""
    <div class="breadcrumb">
        <span>🎓 StudyAbroad Platform</span> > <span>Expense Calculator</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("🧮 Lifestyle-Based Expense Calculator")
    st.markdown("Estimate your monthly expenses based on your lifestyle preferences and destination country")
    
    # Feature description
    with st.expander("ℹ️ How This Calculator Works", expanded=False):
        st.markdown("""
        **This calculator helps you estimate living costs for studying abroad:**
        
        - **Pre-built estimates** for 5 popular study destinations with lifestyle options
        - **Customizable sliders** to adjust costs based on your personal preferences  
        - **Comparison tool** to see costs across different countries side by side
        - **Custom budget mode** where you can set your own budget ranges
        - **Currency conversion** based on your selected destination
        - **Emergency fund recommendations** and money-saving tips
        
        Choose between budget, moderate, or comfortable lifestyles, then fine-tune each category to match your needs.
        """)
    
    # Budget mode selection
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("📊 Calculator Mode")
    with col2:
        budget_mode = st.selectbox(
            "Mode",
            ["Pre-built Estimates", "Custom Budget"],
            help="Choose between pre-built estimates or set your own budget ranges"
        )
    
    if budget_mode == "Pre-built Estimates":
        # Calculator form
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.expander("📍 Select Destination & Lifestyle", expanded=False):
                country = st.selectbox(
                    "Country",
                    list(COST_DATA.keys()),
                    index=list(COST_DATA.keys()).index(st.session_state.selected_country) if st.session_state.selected_country in COST_DATA else 0,
                    help="Select your study destination"
                )
                country_info = get_country_info()
                currency_symbol = country_info[country]['symbol']

                lifestyle = st.selectbox(
                    "Lifestyle Preference",
                    ["budget", "moderate", "comfortable"],
                    format_func=lambda x: {
                        "budget": "💰 Budget - Essential needs only",
                        "moderate": "🏠 Moderate - Balanced lifestyle",
                        "comfortable": "✨ Comfortable - Higher quality living"
                    }[x],
                    help="Choose your preferred lifestyle level"
                )

            with st.expander("🎯 Customize Your Expenses", expanded=False):
                st.markdown("Adjust the base estimates according to your specific needs:")
            
            # Get base costs
            base_costs = COST_DATA[country][lifestyle].copy()
            
            # Custom adjustments
            custom_costs = {}
            
            custom_costs['rent'] = st.slider(
                "🏠 Rent & Accommodation",
                min_value=0,
                max_value=3000,
                value=base_costs['rent'],
                step=50,
                help="Monthly rent, utilities may be separate"
            )
            
            custom_costs['food'] = st.slider(
                "🍽️ Food & Groceries",
                min_value=0,
                max_value=800,
                value=base_costs['food'],
                step=25,
                help="Groceries and dining out"
            )
            
            custom_costs['transport'] = st.slider(
                "🚌 Transportation",
                min_value=0,
                max_value=400,
                value=base_costs['transport'],
                step=10,
                help="Public transport, bike, occasional taxi"
            )
            
            custom_costs['utilities'] = st.slider(
                "⚡ Utilities",
                min_value=0,
                max_value=300,
                value=base_costs['utilities'],
                step=10,
                help="Electricity, water, internet, phone"
            )
            
            custom_costs['entertainment'] = st.slider(
                "🎉 Entertainment & Social",
                min_value=0,
                max_value=500,
                value=base_costs['entertainment'],
                step=25,
                help="Movies, dining out, social activities"
            )
            
            custom_costs['other'] = st.slider(
                "🛍️ Other Expenses",
                min_value=0,
                max_value=400,
                value=base_costs['other'],
                step=25,
                help="Shopping, personal care, miscellaneous"
            )
    
    else:  # Custom Budget mode
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.expander("🎯 Customize Your Expenses", expanded=False):
                st.subheader("📍 Your Custom Budget")
                st.markdown("Set your own budget ranges for each category:")
            
                country = st.session_state.selected_country
                country_info = get_country_info()
                currency_symbol = country_info[country]['symbol']
            
                custom_costs = {}
            
                custom_costs['rent'] = st.number_input(
                f"🏠 Rent & Accommodation ({currency_symbol})",
                min_value=0,
                max_value=5000,
                value=800,
                step=50,
                help="Set your preferred monthly rent budget"
            )
            
                custom_costs['food'] = st.number_input(
                f"🍽️ Food & Groceries ({currency_symbol})",
                min_value=0,
                max_value=1000,
                value=300,
                step=25,
                help="Set your monthly food budget"
            )
            
                custom_costs['transport'] = st.number_input(
                f"🚌 Transportation ({currency_symbol})",
                min_value=0,
                max_value=500,
                value=100,
                step=10,
                help="Set your monthly transport budget"
            )
            
                custom_costs['utilities'] = st.number_input(
                f"⚡ Utilities ({currency_symbol})",
                min_value=0,
                max_value=400,
                value=120,
                step=10,
                help="Set your monthly utilities budget"
            )
            
                custom_costs['entertainment'] = st.number_input(
                f"🎉 Entertainment & Social ({currency_symbol})",
                min_value=0,
                max_value=800,
                value=150,
                step=25,
                help="Set your monthly entertainment budget"
            )
            
                custom_costs['other'] = st.number_input(
                f"🛍️ Other Expenses ({currency_symbol})",
                min_value=0,
                max_value=500,
                value=100,
                step=25,
                help="Set your budget for miscellaneous expenses"
            )
            
                lifestyle = "custom"  # Set lifestyle for custom mode
    
    with col2:
        st.subheader("💰 Your Monthly Budget Breakdown")
        
        # Calculate totals
        total_monthly = sum(custom_costs.values())
        total_yearly = total_monthly * 12
        
        # Display summary cards
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-content">
                    <h3>Monthly Total</h3>
                    <div class="metric-value">{format_currency(total_monthly, country)}</div>
                    <div class="metric-change neutral">{country}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-content">
                    <h3>Yearly Total</h3>
                    <div class="metric-value">{format_currency(total_yearly, country)}</div>
                    <div class="metric-change neutral">{lifestyle.title()} lifestyle</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Monthly Budget Breakdown", expanded=False):
            st.subheader("📊 Expense Breakdown")

            # Create pie chart
            categories = list(custom_costs.keys())
            amounts = list(custom_costs.values())
        
            # Format category names
            category_labels = {
                'rent': '🏠 Rent',
                'food': '🍽️ Food',
                'transport': '🚌 Transport',
                'utilities': '⚡ Utilities',
                'entertainment': '🎉 Entertainment',
                'other': '🛍️ Other'
            }

            formatted_labels = [category_labels[cat] for cat in categories]

            fig_pie = px.pie(
                values=amounts,
                names=formatted_labels,
                title="Monthly Expense Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                font=dict(size=12),
                showlegend=True,
                height=400
            )

            st.plotly_chart(fig_pie, use_container_width=True)

            # Detailed breakdown
            st.subheader("📋 Detailed Breakdown")

            for category, amount in custom_costs.items():
                percentage = (amount / total_monthly) * 100
                icon = category_labels[category].split()[0]
                name = category_labels[category].split()[1]

                st.markdown(f"""
                <div class="expense-breakdown-item">
                    <div class="expense-header">
                        <span class="expense-icon">{icon}</span>
                        <span class="expense-name">{name}</span>
                        <span class="expense-amount">{format_currency(amount, country)}</span>
                    </div>
                    <div class="expense-bar">
                        <div class="expense-fill" style="width: {percentage:.1f}%"></div>
                    </div>
                    <div class="expense-percentage">{percentage:.1f}% of total budget</div>
                </div>
                """, unsafe_allow_html=True)
    
    with st.expander("🌍 Country Comparison", expanded=False):
        st.markdown("Compare costs across different countries for the same lifestyle")

        # Create comparison data
        comparison_data = []
        for country_name, lifestyle_data in COST_DATA.items():
            total_cost = sum(lifestyle_data[lifestyle].values())
            comparison_data.append({
                'Country': country_name,
                'Monthly Cost': total_cost,
                'Yearly Cost': total_cost * 12
            })

        # Sort by monthly cost
        comparison_data.sort(key=lambda x: x['Monthly Cost'])

        # Display comparison
        cols = st.columns(len(comparison_data))

        for i, data in enumerate(comparison_data):
            with cols[i]:
                is_selected = data['Country'] == country
                card_class = "comparison-card selected" if is_selected else "comparison-card"

                st.markdown(f"""
                <div class="{card_class}">
                    <h4>{data['Country']}</h4>
                    <div class="comparison-monthly">{get_country_info()[data['Country']]['symbol']}{data['Monthly Cost']:,.0f}/month</div>
                    <div class="comparison-yearly">{get_country_info()[data['Country']]['symbol']}{data['Yearly Cost']:,.0f}/year</div>
                    <div class="comparison-lifestyle">{lifestyle.title()} lifestyle</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Tips and recommendations
    with st.expander("💡 Money-Saving Tips", expanded=False):
        tips_by_lifestyle = {
        "budget": [
            "🏠 Consider shared accommodation or student dormitories",
            "🍽️ Cook at home and buy groceries in bulk",
            "🚌 Use student discounts for public transportation",
            "📚 Take advantage of free university facilities and events",
            "💳 Look for student discount cards and deals"
        ],
        "moderate": [
            "🏠 Balance location and cost - slightly farther from city center",
            "🍽️ Mix of home cooking and occasional dining out",
            "🚌 Monthly transport passes often offer better value",
            "🎉 Set aside a specific budget for entertainment",
            "💰 Track expenses regularly to stay on budget"
        ],
        "comfortable": [
            "🏠 Invest in good location and amenities for quality of life",
            "🍽️ Enjoy local cuisine but be mindful of spending",
            "🚗 Consider convenience vs cost for transportation",
            "🎉 Plan bigger experiences and activities",
            "💳 Use cashback and rewards credit cards responsibly"
        ]
    }
    
        current_tips = tips_by_lifestyle[lifestyle]

        for tip in current_tips:
            st.markdown(f"""
            <div class="tip-item">
                <span class="tip-text">{tip}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("🚨 Emergency Fund Recommendation", expanded=False):
        emergency_fund = total_monthly * 3  # 3 months of expenses

        st.markdown(f"""
        <div class="emergency-fund-card">
            <h4>💰 Recommended Emergency Fund</h4>
            <div class="emergency-amount">{format_currency(emergency_fund, country)}</div>
            <div class="emergency-description">
                Having 3 months of expenses saved can help you handle unexpected situations like
                medical emergencies, travel costs, or temporary income loss.
            </div>
        </div>
        """, unsafe_allow_html=True)

# Execute the page logic
if __name__ == "__main__":
    main()
