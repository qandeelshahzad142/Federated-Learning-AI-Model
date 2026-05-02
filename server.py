from fastapi import FastAPI
import numpy as np
from model.model import build_model

app = FastAPI()

global_model = build_model()

@app.get("/model")
def get_model():
    return {
        "weights": [w.tolist() for w in global_model.get_weights()]
    }

@app.post("/update")
def update(data: dict):
    weights = [np.array(w) for w in data["weights"]]
    global_model.set_weights(weights)
    return {"status": "updated"}