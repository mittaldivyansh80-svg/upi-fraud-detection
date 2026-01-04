import streamlit as st
import requests

st.set_page_config(page_title="UPI Fraud Detection", page_icon="🔐")

st.title("🔐 AI-Based UPI Fraud Detection System")
st.write("Enter transaction details to check fraud risk")

# =========================
# USER INPUTS
# =========================
amount = st.number_input("Transaction Amount (₹)", min_value=1.0, value=1000.0)
txn_time = st.slider("Transaction Time (Hour)", 0, 23, 12)

new_receiver = st.checkbox("New Receiver?")
device_change = st.checkbox("New Device?")
location_change = st.checkbox("Location Changed?")
high_velocity = st.checkbox("Multiple Transactions in Short Time?")

# =========================
# FEATURE ENGINEERING
# (MUST MATCH BACKEND)
# =========================
amount_ratio = float(amount / 2000)
night_txn = int(1 if txn_time <= 5 else 0)

# =========================
# BUTTON ACTION
# =========================
if st.button("Check Fraud Risk"):

    payload = {
        "new_receiver": int(new_receiver),
        "device_change": int(device_change),
        "location_change": int(location_change),
        "amount_ratio": float(amount_ratio),
        "night_txn": int(night_txn),
        "high_velocity": int(high_velocity)
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload,
            timeout=5
        )

        if response.status_code != 200:
            st.error("❌ Backend error. Please check FastAPI terminal.")
        else:
            result = response.json()
            prob = result["fraud_probability"]
            decision = result["decision"]

            st.subheader("Result")

            if decision == "BLOCK":
                st.error(f"🚨 FRAUD DETECTED\n\nRisk Score: {prob}")
            elif decision == "WARNING":
                st.warning(f"⚠️ SUSPICIOUS TRANSACTION\n\nRisk Score: {prob}")
            else:
                st.success(f"✅ SAFE TRANSACTION\n\nRisk Score: {prob}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend server not running. Please start FastAPI.")
    except Exception as e:
        st.error(f"❌ Error: {e}")