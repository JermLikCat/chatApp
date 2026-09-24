import socket

def start_tcp_client(host='10.0.181.29', port=5100):
    # Create an IPv4 (AF_INET), TCP (SOCK_STREAM) socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the target server
        client_socket.connect((host, port))
        
        # Strings must be encoded to bytes before transmission
        message = "Hello, Server!"
        client_socket.sendall(message.encode('utf-8'))
        
        # Receive data from the server (1024 bytes buffer size)
        response = client_socket.recv(1024)
        print(f"Received from server: {response.decode('utf-8')}")

if __name__ == '__main__':
    start_tcp_client()