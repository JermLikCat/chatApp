import socket

def start_client(host='10.0.181.29', port=5100):
    # 1. Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 2. Connect to the server
        client_socket.connect((host, port))
        print(f"[CONNECTED] Connected to server at {host}:{port}")
        
        # 3. Define and send the message (must be encoded to bytes)
        message = "Hello, Server! This is the client."
        client_socket.sendall(message.encode('utf-8'))
        print(f"[SENT] {message}")
        
        # 4. Receive response from the server (buffer size 1024 bytes)
        response = client_socket.recv(1024)
        print(f"[RECEIVED] Server reply: {response.decode('utf-8')}")
        
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to the server. Is the server running?")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        # 5. Always close the connection
        client_socket.close()
        print("[CLOSED] Connection closed.")

if __name__ == "__main__":
    start_client()