import socket
import threading

# the configuration
HOST = '127.0.0.1'
PORT = 65432

# Chapter 6 & Option 2 Core Logic: The Data Structures
# active_clients will help us to know who is online and manage connections (Subscriber ID -> Socket Connection)
# Who is online right now? (Maps Subscriber ID -> Socket Connection)
active_clients = {} 

#this portion will help us to know who is interested in what topic (Topic -> List of Socket Connections)
# Who cares about what? (Maps Topic -> List of Subscriber IDs)
topic_subscriptions = {} 

#and this one will help us to store messages for offline subscribers (Subscriber ID -> List of missed messages)
#(Maps Subscriber ID -> List of missed messages)
offline_queue = {}

def handle_client(conn, addr):
    """This function will handle the communication with each client (Publisher or Subscriber)"""
    pass
    

def start_broker():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Broker started on {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        #create a new thread for every client (chapter 7 reference): Concurrency
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_broker()