# Python Publish-Subscribe System (Socket-Based)

A lightweight Publish-Subscribe (Pub/Sub) messaging system built from scratch using Python's `socket` and `threading` libraries. 

This project demonstrates core networking concepts, concurrent client handling, and features an **Offline Message Queueing Mechanism** (Option 2 Implementation) that allows disconnected subscribers to "catch up" on missed messages when they reconnect.

## Features
* **Topic-Based Routing:** Subscribers only receive messages for the specific topics they register to.
* **Concurrency:** The broker uses multithreading to handle multiple publishers and subscribers simultaneously.
* **Offline Message Buffering:** If a subscriber disconnects, the broker safely queues incoming messages for their subscribed topics. Upon reconnection (using their unique ID), the broker immediately sends all missed messages.
* **Custom Protocol:** Uses a lightweight TCP string-parsing protocol for communication (`PUB:` and `SUB:` actions).
* **Graceful Disconnects:** Clients handle `Ctrl+C` inputs to cleanly drop connections without crashing the server.

## Project Structure
* **`broker.py`**: The central messaging server. It manages connections, routes messages, and handles the `offline_queue` state.
* **`publisher.py`**: The producer client used to send messages to the broker.
* **`subscriber.py`**: The consumer client used to listen for messages from the broker.

## How to Run

### 1. Start the Broker
You must start the central broker first. Open a terminal and run:
```bash
python broker.py
```
*(The broker will start listening on `127.0.0.1:65432`)*

### 2. Start a Subscriber
Open a new terminal and run:
```bash
python subscriber.py
```
* **Enter Unique ID:** (e.g., `User1`) - *Important for offline catch-up!*
* **Enter Topic:** (e.g., `news`, `sports`, `tech`)

### 3. Start a Publisher
Open another new terminal and run:
```bash
python publisher.py
```
* **Publish messages using the format:** `<topic>:<message>`
* *Example:* `news:Hello World!`

## Testing the Offline Queue (Option 2)
1. Start the `broker`.
2. Start a `subscriber`, type unique user ID, eg. **"User1"**, and topic **"tech"**.
3. Now, start a `publisher` from another split terminal and send a few messages to the **"tech"** topic. The format should be 'topic:message' (e.g., `tech:New smartphone released!`, `tech:AI is taking over!`).
4. Let's simulate the crash. Close the `subscriber` terminal by force delete that split terminal.
5. Notice the broker terminal says `[*] User1 is offline`.
6. Go back t a `publisher` and send a few messages to the **"tech"** topic (e.g., `tech:New smartphone released!`, `tech:AI is taking over!`).
7. Notice the broker terminal says `[*] Buffered message for offline user: Alice`.
8. Start the `subscriber` again through a new split terminal, using the **SAME ID** (**"User1"**) and topic **"tech"**.
9. The subscriber will instantly receive the missed messages through the catch-up mechanism!

## Protocol Details
This system uses a custom text-based protocol over TCP byte streams:
* **Subscribe Command:** `SUB:<topic>:<subscriber_id>`
* **Publish Command:** `PUB:<topic>:<message>`
* **Broker Relay:** `FROM <topic>: <message>\n`

---
