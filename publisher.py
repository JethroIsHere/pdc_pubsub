import socket

HOST = '127.0.0.1'
PORT = 65432

def start_publisher():
    # setting first the connection to the broker
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    print("--- Publisher Node Active ---")
    
    # Basic input loop
    while True:
        user_input = input("Enter [topic:message] or 'exit' to quit: ")
        
        if user_input.lower() == 'exit':
            break

    client.close()
    print("[!] Publisher closed.")

if __name__ == "__main__":
    start_publisher()