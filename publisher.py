import socket

HOST = '127.0.0.1'
PORT = 65432

def start_publisher():
    # setting first the connection to the broker
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    print("--- Publisher Node Active ---")
    print("Format: <topic>:<message> (e.g., news:Hello World)") # <- Added instructions
    
    try: # <- Added try/except block
        while True:
            user_input = input("Enter [topic:message] or 'exit' to quit: ")
            
            if user_input.lower() == 'exit':
                break
            
            if ":" not in user_input:
                print("Error: Use the format topic:message")
                continue

            # format the message according to protocol
            # we will prefix it with PUB: so that the Broker knows this is a publish action
            full_message = f"PUB:{user_input}\n"
            
            # Send the encoded string (Marshalling)
            client.sendall(full_message.encode('utf-8'))
            # --------------------------------
            
    except KeyboardInterrupt:
        pass
    finally:
        client.close()
        print("[!] Publisher closed.")

if __name__ == "__main__":
    start_publisher()