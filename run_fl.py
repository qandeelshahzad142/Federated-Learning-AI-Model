from server.server import start_server
from client.client import start_client


def client_wrapper(client_id, global_weights):
    return start_client(client_id, global_weights)


def main():
    start_server(client_wrapper)


if __name__ == "__main__":
    main()