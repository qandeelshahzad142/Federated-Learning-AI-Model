import os
import requests
import numpy as np
from model.model import build_model

SERVER_URL = "http://127.0.0.1:5050"
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs.txt')

def write_log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def start_client(client_id):
    print(f"\n--- CLIENT {client_id} STARTED ---")
    write_log(f"Client {client_id} | Status: Started")
    model = build_model()

    # GET GLOBAL MODEL
    try:
        res = requests.get(f"{SERVER_URL}/model")
        data = res.json()
        if data["weights"] is not None:
            weights = [np.array(w) for w in data["weights"]]
            model.set_weights(weights)
            print("✔ Loaded global model")
            write_log(f"Client {client_id} | Status: Loaded global model")
        else:
            print("⚠ No global model yet")
    except Exception as e:
        print("❌ Server not reachable:", e)
        write_log(f"Client {client_id} | Status: Server not reachable")
        return

    # TRAIN
    X = np.random.rand(20, 224, 224, 3)
    y = np.random.randint(0, 2, 20)
    history = model.fit(X, y, epochs=1, verbose=1)

    # LOG ACCURACY
    accuracy = float(history.history['accuracy'][0])
    loss = float(history.history['loss'][0])
    print(f"✔ Training done — Accuracy: {accuracy:.4f} Loss: {loss:.4f}")
    write_log(f"Client {client_id} | Accuracy: {accuracy:.4f}")
    write_log(f"Client {client_id} | Loss: {loss:.4f}")

    # SEND UPDATE
    weights = [w.tolist() for w in model.get_weights()]
    requests.post(f"{SERVER_URL}/update", json={
        "weights": weights,
        "client_id": client_id,
        "accuracy": accuracy,
    })
    print("✔ Sent updated weights")
    write_log(f"Client {client_id} | Status: Sent updated weights")

if __name__ == "__main__":
    import sys
    cid = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    start_client(cid)