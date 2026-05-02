from fastapi import FastAPI
import numpy as np
from model.model import build_model

app = FastAPI()

# 🔥 Build model
global_model = build_model()

# 🔥 FORCE INITIALIZATION (VERY IMPORTANT FIX)
dummy_input = np.zeros((1, 224, 224, 3))
global_model.predict(dummy_input)

# Store client updates
client_updates = []

# ------------------------------
# Root endpoint
# ------------------------------
@app.get("/")
def home():
    return {"message": "Server is running"}

# ------------------------------
# Send global model weights
# ------------------------------
@app.get("/model")
def get_model():
    try:
        weights = global_model.get_weights()
        return {"weights": [w.tolist() for w in weights]}
    except Exception as e:
        return {"error": str(e)}

# ------------------------------
# Receive client updates
# ------------------------------
@app.post("/update")
def update(data: dict):
    global client_updates

    try:
        weights = [np.array(w) for w in data["weights"]]
        client_updates.append(weights)

        # 🔁 Apply FedAvg after 2 clients
        if len(client_updates) >= 2:
            new_weights = []

            for layer_weights in zip(*client_updates):
                new_weights.append(np.mean(layer_weights, axis=0))

            global_model.set_weights(new_weights)
            client_updates = []

            return {"status": "aggregated"}

        return {"status": "waiting"}

    except Exception as e:
        return {"error": str(e)}