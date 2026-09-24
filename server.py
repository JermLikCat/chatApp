import socket, pickle

class Server:
    def __init__(self):
        self.clients = []
        self.address = "localhost"
        self.port = 6767
    def run(self):
        with socket.socket() as server:
            server.bind(self.address, self.port)
            server.listen(1)

            conn, _ = server.accept()

            with conn:
                data = conn.recv(4096)
                message = pickle.loads(data)
                