import socket

def test_connection(host='10.0.181.29', port=5100):
    print("1. Creating the socket configuration...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Restrict blocking to a maximum of 3 seconds
    client_socket.settimeout(3.0) 
    
    try:
        print(f"2. Attempting connection to {host}:{port}... (Checking if blocked here)")
        client_socket.connect((host, port))
        print("   -> Success: Connected to server!")
        
        message = "Diagnostic ping"
        print("3. Sending bytes down the wire...")
        client_socket.sendall(message.encode('utf-8'))
        print("   -> Success: Data sent!")
        
        print("4. Waiting to receive response from server... (Checking if blocked here)")
        response = client_socket.recv(1024)
        print(f"   -> Success: Received back: {response.decode('utf-8')}")
        
    except socket.timeout:
        print("\n[DIAGNOSIS] The script timed out! Look at the last step printed above to see exactly where it froze.")
    except ConnectionRefusedError:
        print("\n[DIAGNOSIS] Connection Refused. No server is listening on that port at all.")
    except Exception as e:
        print(f"\n[DIAGNOSIS] Unexpected error: {e}")
    finally:
        client_socket.close()
        print("\n5. Socket safely closed.")

if __name__ == "__main__":
    test_connection()
