import streamlit as st

# Title
st.title("Arterial ED Probability Calculator")

st.write("Please enter the patient's characteristics below:")

# Checkboxes using exact names
dm_duration = st.checkbox("DM duration (≥10 years)")
neuropathy = st.checkbox("Neuropathy (Present)")

st.divider()

# Residual Cholesterol broken down into 2 parts
st.subheader("Residual Cholesterol")
st.caption("Calculated as: Total Cholesterol - (HDL + LDL)")
col1, col2 = st.columns(2)
with col1:
    total_chol = st.number_input("Total Cholesterol (mg/dL)", min_value=0.0, value=0.0, step=1.0)
with col2:
    hdl_ldl = st.number_input("HDL + LDL Combined (mg/dL)", min_value=0.0, value=0.0, step=1.0)

rc_value = total_chol - hdl_ldl if total_chol > 0 else 0

st.divider()

# NLR broken down into 2 parts
st.subheader("NLR")
st.caption("Calculated as: Neutrophils / Lymphocytes")
col3, col4 = st.columns(2)
with col3:
    neutrophils = st.number_input("Neutrophils (Absolute count)", min_value=0.0, value=0.0, step=0.1)
with col4:
    lymphocytes = st.number_input("Lymphocytes (Absolute count)", min_value=0.0, value=0.0, step=0.1)

nlr_value = neutrophils / lymphocytes if lymphocytes > 0 else 0

st.divider()

# Calculation Logic
score = 0
if dm_duration:
    score += 2
if neuropathy:
    score += 3
if rc_value >= 25:
    score += 1
if nlr_value >= 2.2:
    score += 3

# Probability mapping dictionary based on Table 7
prob_map = {
    0: 1.6, 1: 3.4, 2: 6.9, 3: 13.4, 4: 24.6,
    5: 40.7, 6: 59.1, 7: 75.3, 8: 86.5, 9: 93.1
}

# Display Results
if st.button("Calculate Probability", type="primary"):
    probability = prob_map.get(score, 0)
    
    st.markdown(f"### Total Risk Score: **{score}**")
    st.markdown(f"### Probability of Arterial ED: **{probability}%**")

# Expandable Detail
with st.expander("How we are calculating this"):
    st.markdown("""
    This calculator generates a risk score based on the Simplified Risk Score System derived from regression coefficients[cite: 1]. 
    
    **Point Allocations (Table 6)[cite: 1]:**
    * **DM duration (≥10 years):** +2 Points[cite: 1]
    * **Residual Cholesterol (≥25 mg/dL):** +1 Point[cite: 1]
    * **NLR (≥2.2):** +3 Points[cite: 1]
    * **Neuropathy (Present):** +3 Points[cite: 1]
    
    The total points are summed together to create a final score between 0 and 9. This score is then mapped to the probability of arterial erectile dysfunction[cite: 1].
    
    **Probability Mapping (Table 7)[cite: 1]:**
    * Score 0 = 1.6%[cite: 1]
    * Score 1 = 3.4%[cite: 1]
    * Score 2 = 6.9%[cite: 1]
    * Score 3 = 13.4%[cite: 1]
    * Score 4 = 24.6%[cite: 1]
    * Score 5 = 40.7%[cite: 1]
    * Score 6 = 59.1%[cite: 1]
    * Score 7 = 75.3%[cite: 1]
    * Score 8 = 86.5%[cite: 1]
    * Score 9 = 93.1%[cite: 1]
    """)