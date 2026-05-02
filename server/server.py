import os
from fastapi import FastAPI
import numpy as np
from model.model import build_model

app = FastAPI()
global_model = build_model()
round_number = 0
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs.txt')

def write_log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

@app.get("/model")
def get_model():
    return {
        "weights": [w.tolist() for w in global_model.get_weights()]
    }

@app.post("/update")
def update(data: dict):
    global round_number
    weights = [np.array(w) for w in data["weights"]]
    global_model.set_weights(weights)

    round_number += 1
    client_id = data.get("client_id", "?")
    accuracy = data.get("accuracy", 0.0)

    write_log(f"Round {round_number} | Accuracy: {accuracy:.4f}")
    write_log(f"Server | Round {round_number} | Client {client_id} update received")

    return {"status": "updated", "round": round_number}