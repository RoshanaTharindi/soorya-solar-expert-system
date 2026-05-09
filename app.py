import streamlit as st
import clips

st.set_page_config(page_title="Sri Lanka Solar Expert", layout="centered")
st.title("☀️ Soorya Bala Sangramaya Advisor")

env = clips.Environment()
env.load("soorya_logic.clp") # Loads the file above

# --- UI WITH BETTER DESCRIPTIONS ---
u = st.number_input("Average Monthly Electricity Consumption (kWh)", value=150, min_value=0)

g_options = {"offset-bill": "1 - Offset my monthly bill", "generate-income": "2 - Generate extra income"}
g = st.selectbox("Primary Goal", options=list(g_options.keys()), format_func=lambda x: g_options[x])

b_options = {"low": "1 - Low (< 800,000 LKR)", "medium": "2 - Medium (800,000 LKR - 1,500,000 LKR)", "high": "3 - High (> 1,500,000 LKR)"}
b = st.selectbox("Upfront Budget", options=list(b_options.keys()), format_func=lambda x: b_options[x])

if st.button("Consult Expert System"):
    env.reset()
    # Passes the raw symbols to the engine
    env.assert_string(f"(user-data (monthly-units {u}) (primary-goal {g}) (budget {b}))")
    env.run()
    
    for fact in env.facts():
        if fact.template.name == "recommendation":
            st.success(f"**Recommendation:** {fact['scheme']}")
            st.write(f"**Engineering Reasoning:** {fact['reasoning']}")