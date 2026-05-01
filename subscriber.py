import socket

HOST = '127.0.0.1'
PORT = 65432

def start_subscriber():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    # this is Important: this ask for a Unique ID for catch-up functionality
    sub_id = input("Enter your Unique Subscriber ID (e.g., User1): ")
    topic = input("Enter topic to subscribe to: ")
    
    # SUB:topic:ID
    client.sendall(f"SUB:{topic}:{sub_id}".encode('utf-8'))
    
    print(f"[*] Registered as {sub_id}. Waiting for messages on {topic}...")
    try:
        while True:
            data = client.recv(1024).decode('utf-8')
            if data:
                print(f"[Message Received]: {data.strip()}")
            else:
                break
    except KeyboardInterrupt:
        print("\n[!] Exiting subscriber...")
    except Exception:
        print("\n[!] Connection lost.")
    finally:
        client.close()

if __name__ == "__main__":
    start_subscriber()