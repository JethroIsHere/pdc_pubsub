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
    print(f"[!] Handling connection from {addr}")
    current_sub_id = None                                 # this tracks who's this specific thread belongs to
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')        # Receive data (chapter 4 reference): Marshalling/Unmarshalling
            if not data:
                break            
            print(f"[*] Received: {data}")

            # The Subscriber Logic: We need to know who they are and what they want to subscribe to
            if data.startswith("SUB:"):
                # Protocol: SUB:topic:sub_id
                parts = data.split(":")
                if len(parts) == 3:
                    topic, sub_id = parts[1], parts[2]
                    current_sub_id = sub_id
                    active_clients[sub_id] = conn          # mark subscriber as online

                    # register them to the topic
                    if topic not in topic_subscriptions:
                        topic_subscriptions[topic] = []
                    if sub_id not in topic_subscriptions[topic]:
                        topic_subscriptions[topic].append(sub_id)
                        
                    conn.sendall(f"CONFIRM: Subscribed to {topic} as {sub_id}\n".encode('utf-8'))
                    
                    # a catch-up mechanism if they have missed messages while offline, send them now
                    if sub_id in offline_queue and len(offline_queue[sub_id]) > 0:
                        conn.sendall(f"[*] Catching up! You missed {len(offline_queue[sub_id])} messages:\n".encode('utf-8'))
                        for missed_msg in offline_queue[sub_id]:
                            conn.sendall(f"[MISSED] {missed_msg}\n".encode('utf-8'))
                        
                        offline_queue[sub_id] = []             #clear the queue so they don't get them again
                        
            # The Publisher logic: know the topic and message then forward to the right subscribers
            elif data.startswith("PUB:"):
                parts = data.split(":", 2)
                if len(parts) == 3:
                    topic, message = parts[1], parts[2]
                    formatted_msg = f"FROM {topic}: {message}\n"
                    
                    # this is to check who needs this message
                    if topic in topic_subscriptions:
                        for target_sub_id in topic_subscriptions[topic]:
                            if target_sub_id in active_clients:                      # if the user is currently online let's send it live
                                try:
                                    active_clients[target_sub_id].sendall(formatted_msg.encode('utf-8'))   #send it live
                                except:
                                    # If the send fails, they dropped unexpectedly, so we should clean up and queue the message for them
                                    del active_clients[target_sub_id]
                                    if target_sub_id not in offline_queue:
                                        offline_queue[target_sub_id] = []
                                    offline_queue[target_sub_id].append(formatted_msg)
                            else:
                                #user is known to be offline, so we queue the message...
                                if target_sub_id not in offline_queue:
                                    offline_queue[target_sub_id] = []
                                offline_queue[target_sub_id].append(formatted_msg)
                                print(f"[*] Buffered message for offline user: {target_sub_id}")

    except Exception as e:                                                                          # handles unexpected socket closures or other errors
        pass
    finally:
        # cleanup on disconnect (remove from active clients and print status)
        if current_sub_id in active_clients:
            del active_clients[current_sub_id]
            print(f"[-] {current_sub_id} went offline.")
        conn.close()

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