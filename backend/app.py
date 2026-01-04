from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI(title="UPI Fraud Detection API")

# Input schema (MUST match frontend)
class Transaction(BaseModel):
    new_receiver: int
    device_change: int
    location_change: int
    amount_ratio: float
    night_txn: int
    high_velocity: int

@app.post("/predict")
def predict_fraud(txn: Transaction):
    # Convert input to model format (ORDER MATTERS)
    features = np.array([[
        txn.amount_ratio,
        txn.device_change,
        txn.high_velocity,
        txn.location_change,
        txn.night_txn,
        txn.new_receiver
    ]])

    prob = model.predict_proba(features)[0][1]

    # Decision logic
    if prob > 0.7:
        decision = "BLOCK"
    elif prob > 0.4:
        decision = "WARNING"
    else:
        decision = "ALLOW"

    return {
        "fraud_probability": round(float(prob), 2),
        "decision": decision
    }