from fastapi import FastAPI
import numpy as np
from model.model import build_model

app = FastAPI()

global_model = build_model()
global_weights = None


@app.get("/")
def home():
    return {"message": "Server is running"}


@app.get("/model")
def get_model():
    global global_weights

    if global_weights is None:
        return {"weights": None}

    return {"weights": [w.tolist() for w in global_weights]}


@app.post("/update")
def update(data: dict):
    global global_weights

    weights = data["weights"]
    global_weights = [np.array(w) for w in weights]

    global_model.set_weights(global_weights)

    return {"status": "updated"}