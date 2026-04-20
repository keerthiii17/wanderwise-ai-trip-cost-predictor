import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("trip_cost_model.pkl")

# Page config
st.set_page_config(page_title="Trip Cost Predictor", page_icon="🌍", layout="centered")

# ---- GLASSMORPHISM CSS ----
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

/* Glass container */
.glass {
    background: rgba(255, 255, 255, 0.15);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Inputs */
input, select, textarea {
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(45deg, #ff7eb3, #ff758c);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(45deg, #ff758c, #ff7eb3);
}

/* Titles */
h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---- UI ----
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.title("🌍 Trip Cost Predictor")
st.write("✨ Plan smarter trips with AI-powered cost estimation")

with st.form("trip_form"):

    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input("Source City")
        duration_days = st.number_input("Duration (days)", min_value=1)
        accommodation = st.selectbox("Stay Type", ["budget", "mid", "luxury"])
        num_activities = st.number_input("Activities", min_value=0)

    with col2:
        destination = st.text_input("Destination City")
        num_people = st.number_input("People", min_value=1)
        travel_mode = st.selectbox("Travel Mode", ["bus", "train", "flight"])
        travel_cost = st.number_input("Travel Cost (₹)", min_value=0.0)

    submit = st.form_submit_button("Predict Cost 💰")

# ---- Prediction ----
if submit:
    if source == "" or destination == "":
        st.error("⚠️ Please fill all required fields")
    else:
        trip_data = {
            "source": source,
            "destination": destination,
            "duration_days": duration_days,
            "num_people": num_people,
            "accommodation": accommodation,
            "travel_mode": travel_mode,
            "num_activities": num_activities,
            "travel_cost": travel_cost
        }

        df = pd.DataFrame([trip_data])
        prediction = model.predict(df)[0]

        st.success(f"💸 Total Cost: ₹{round(prediction, 2)}")
        st.info(f"👤 Cost per person: ₹{round(prediction/num_people, 2)}")

st.markdown('</div>', unsafe_allow_html=True)