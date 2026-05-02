from client.client import start_client

if __name__ == "__main__":
    weights, acc = start_client(1)
    print("\nFINAL ACCURACY:", acc)