import sys
import os
import requests
import numpy as np

# Fix import path (only once)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import build_model

SERVER_URL = "http://127.0.0.1:5000"


def start_client(client_id=1):

    print(f"\n--- CLIENT {client_id} STARTED ---")

    model = build_model()

    # ---------- GET GLOBAL MODEL ----------
    try:
        res = requests.get(f"{SERVER_URL}/model", timeout=10)
        data = res.json()

        weights = data.get("weights", None)

        if not weights:
            print("⚠ No global model found, using local init")
        else:
            weights = [np.array(w, dtype=np.float32) for w in weights]
            model.set_weights(weights)
            print("✔ Global model loaded")

    except Exception as e:
        print("❌ Server not reachable:", e)
        return

    # ---------- TRAIN ----------
    x = np.random.rand(20, 224, 224, 3).astype(np.float32)
    y = np.random.randint(0, 2, (20, 1))

    model.fit(x, y, epochs=1, verbose=1)

    # ---------- SEND UPDATED WEIGHTS ----------
    weights = model.get_weights()
    safe_weights = [w.astype(np.float32).tolist() for w in weights]

    try:
        r = requests.post(
            f"{SERVER_URL}/update",
            json={"weights": safe_weights},
            timeout=10
        )
        print("✔ Updated sent:", r.json())

    except Exception as e:
        print("❌ Send failed:", e)


if __name__ == "__main__":
    start_client(1)