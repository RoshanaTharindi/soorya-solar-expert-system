import streamlit as st
import clips
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Solar Investment Advisor", layout="wide")

# --- 2. ADVANCED CSS INJECTION (COMPACT SOLAR THEME) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* THE SOLAR BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #fef3c7 100%);
        background-attachment: fixed;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* THE FLOATING CARD */
    [data-testid="stMainBlockContainer"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 20px 40px; 
        box-shadow: 0px 20px 50px rgba(245, 158, 11, 0.15); 
        border-top: 6px solid #f59e0b; 
        margin-top: 2vh; 
        margin-bottom: 2vh;
        max-width: 1200px; 
    }

    /* COMPACT HEADERS */
    h1 { font-size: 2.2rem !important; margin-bottom: 0px !important; padding-bottom: 0px !important;}
    h2 { font-size: 1.8rem !important; color: #92400e !important; }
    h3 { font-size: 1.3rem !important; margin-bottom: 0.5rem !important; color: #92400e !important; }
    h4 { font-size: 1.1rem !important; color: #92400e !important; margin-top: 15px !important;}
    p { color: #451a03 !important; }
    label { font-weight: 600 !important; color: #78350f !important; font-size: 0.9rem !important; }

    /* SOLAR BUTTON STYLING */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #f59e0b 0%, #ea580c 100%); 
        color: white;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 10px 20px;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #ea580c 0%, #c2410c 100%);
        box-shadow: 0 8px 16px rgba(234, 88, 12, 0.25);
        color: white;
    }

    /* COMPACT METRICS & FIX TRUNCATION */
    [data-testid="stMetricValue"] {
        font-size: 1.2rem !important; 
        white-space: normal !important; 
        line-height: 1.2 !important;
        color: #92400e !important; 
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
    }

    /* INFO BOX STYLING */
    div[data-testid="stWebsocket"] + div div[data-testid="stNotification"], .stAlert {
        background-color: #fffbeb !important;
        border-left: 4px solid #f59e0b !important;
        color: #78350f !important;
        padding: 10px !important;
    }
    
    /* CUSTOM LINK STYLING */
    .resource-link {
        display: block;
        padding: 8px 12px;
        margin-bottom: 8px;
        background-color: #fffbeb;
        border-radius: 6px;
        border-left: 3px solid #ea580c;
        text-decoration: none;
        color: #92400e;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .resource-link:hover {
        background-color: #fef3c7;
        color: #ea580c;
        transform: translateX(4px);
    }
    
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER SECTION (Adjusted for wider real logo) ---
# Gave col1 more width (1.5) to accommodate the rectangular logo
col1, col2 = st.columns([1.5, 10])
with col1:
    # Load the official logo
    st.image("soorya-bala-logo.jpg", width=160) 
with col2:
    st.title("Solar Investment Advisor")
    st.markdown("<p style='color: #78350f; font-size: 1rem; margin-top: 5px;'>Analyze your energy profile against CEB/LECO tariffs to find your optimal 'Soorya Bala Sangramaya' scheme.</p>", unsafe_allow_html=True)

st.divider()

# --- 4. SIDE-BY-SIDE DESKTOP LAYOUT ---
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown("### Your Household Profile")
    
    with st.expander("Understanding Your Options", expanded=False):
        st.markdown("""
        **Financial Goals:**
        * **Offset my monthly bill:** Priority is to eliminate a high bill. CEB saves excess energy as credits.
        * **Generate extra income:** CEB pays you directly for electricity. You must generate more power than you consume.
        
        **Budget Brackets:**
        * **Low (< 800k LKR):** ~2-3 kW system.
        * **Medium (800k - 1.5M LKR):** ~5-7 kW system.
        * **High (> 1.5M LKR):** 10kW+ system with dedicated export.
        """)

    u = st.number_input("Average Monthly Electricity Consumption (kWh)", value=150, min_value=0, step=10)
    
    g_options = {"offset-bill": "Offset my monthly bill", "generate-income": "Generate extra income"}
    g = st.selectbox("Primary Financial Goal", options=list(g_options.keys()), format_func=lambda x: g_options[x])
    
    b_options = {"low": "Low (< 800k LKR)", "medium": "Medium (800k - 1.5M LKR)", "high": "High (> 1.5M LKR)"}
    b = st.selectbox("Upfront Budget Bracket", options=list(b_options.keys()), format_func=lambda x: b_options[x])

    st.write("") # Spacer
    submit = st.button("Generate Custom Solar Plan")

    # --- NEW: OFFICIAL RESOURCES SECTION ---
    st.markdown("#### 📚 Official Resources")
    st.markdown("""
        <a href="https://www.energy.gov.lk/en/soorya-bala-sangramaya" target="_blank" class="resource-link">
            📄 Implementation Guidelines & Policy Details
        </a>
        <a href="https://www.energy.gov.lk/en/soorya-bala-sangramaya" target="_blank" class="resource-link">
            🏦 Approved Bank Loan Schemes & Credit Lines
        </a>
    """, unsafe_allow_html=True)


with right_col:
    if submit:
        with st.spinner('Analyzing CEB regulations...'):
            time.sleep(1.0)
            
            env = clips.Environment()
            env.load("soorya_logic.clp")
            env.reset()
            env.assert_string(f"(user-data (monthly-units {u}) (primary-goal {g}) (budget {b}))")
            env.run()
            
            recommendation_found = False
            for fact in env.facts():
                if fact.template.name == "recommendation":
                    scheme = fact['scheme']
                    reasoning = fact['reasoning']
                    recommendation_found = True
            
        if recommendation_found:
            st.success("Analysis Complete")
            st.markdown(f"## Recommended: {scheme}")
            
            with st.expander("Read the engineering reasoning behind this choice", expanded=True):
                st.write(reasoning)
                
            st.markdown("### Expected Impact")
            m1, m2, m3 = st.columns([1, 1.2, 1.2]) 
            m1.metric(label="System Viability", value="High")
            
            if "Net Metering" in scheme:
                 m2.metric(label="Bill Offset", value="Up to 100%")
                 m3.metric(label="Contract Length", value="20 Years")
            elif "Accounting" in scheme:
                 m2.metric(label="Export Tariff", value="Rs. 22.00/kWh")
                 m3.metric(label="Fixed Rate", value="First 7 Years")
            else:
                 m2.metric(label="Export Strategy", value="100% Sell")
                 m3.metric(label="Meter Type", value="Dedicated Export")
                 
        else:
            st.error("We couldn't determine a valid scheme. Please try adjusting your inputs.")
            
    else:
        st.markdown("### Output Dashboard")
        st.info("Enter your profile details on the left and click **Generate Custom Solar Plan** to see your analysis.")