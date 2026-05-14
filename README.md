# Python Publish-Subscribe System (Socket-Based)

## 1. Project Title & Description
**Project Name:** A Distributed Smart Message Broker

**Description:**
This is lightweight Publish-Subscribe (Pub/Sub) messaging system built using Python's `socket` and `threading` libraries. This project demonstrates core networking concepts, concurrent client handling, and features an **Offline Message Queueing Mechanism** (Option 2 Implementation) that allows disconnected subscribers to "catch up" on missed messages when they reconnect.

---

## 2. Group / Team Members
**Repository Link:** https://github.com/JethroIsHere/pdc_pubsub.git

### Team Contributions

1. **Kurt Allen Alorro** (`@kurykatsu24`)
- Email: kurtallen.alorro@wvsu.edu.ph
- Role: Project coordinator, code lead, research lead, and final submission
- Assigned files: `broker.py`, and `README.md`
- Contribution summary: planned the project scope, organized documentation flow, lead the coding for the broker component, and finalize the requirements for project submission.

2. **Christine Joy Maravilla** (`@ChristineM24`)
- Email: christinejoy.maravilla@wvsu.edu.ph
- Role: Documentation assistant, and code contributer (integrated the subscriber).
- Assigned files: `subscriber.py`, `README.md`
- Contribution summary: finished the code, and initialized the project documentation

3. **Jazylle Mae Senibalo** (`@yllezy`)
- Email: jazyllemae.senibalo@wvsu.edu.ph
- Role: Code contributer (finalizing the publisher)
- Assigned files: `publisher.py`
- Contribution summary: Finalize the publisher with protocol marshalling and graceful exit

4. **Duke Salfred Bocala** (`@enryu`)
- Email: dukesalfredbocala4@gmail.com
- Role: Code contributer (initialize the publisher logic)
- Assigned files: `publisher.py`
- Contribution summary: initialize the publisher with basic connection setup and input loop

5. **Jethro Roland Dañocup** (`@JethroIsHere`)
- Email: danocupjethro913@gmail.com
- Role: Code management, Code Contributer (established pub/sub connection to broker)
- Assigned files: `broker.py`
- Contribution summary: implement pub/sub connection logic to broker and oversee the whole code for conflicts in the repo

---

## 3. Prerequisites / Requirements

### Programming Language
- Python 3.10 or Python 3.11

### Required Libraries / Dependencies
This project relies entirely on the Python Standard Library. No external dependencies are required. The built-in libraries used are:
- `socket` (for TCP network connections)
- `threading` (for handling multiple concurrent clients)

*Note: You do not need to install anything via pip for the core functionality.*

---

## 4. How to Run the Program

### A. Clone the repository
```powershell
git clone https://github.com/JethroIsHere/pdc_pubsub.git
cd pdc_pubsub
```

### B. Create and activate a virtual environment
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### C. Run the Publish-Subscribe System
To properly simulate the distributed system, you will need to open your terminal and split it into **three separate windows**.

**Step 1: Start the Central Broker**
In your first terminal, run the to start the server:
`python broker.py`

**Step 2: Connect a Subscriber**
In the second terminal, run the subscriber script. When prompted, enter a **Unique ID** and a **topic** to listen to:
`python subscriber.py`
`# Enter Unique Subscriber ID: User1`
`# Enter topic to subscribe to: tech`

**Step 3: Connect a Publisher & Send Live Messages**
In the third terminal, run the publisher script. Send a message to the "tech" topic using the `<topic>:<message>` format:
`python publisher.py`
`# Enter [topic:message] or 'exit' to quit: tech:New smartphone released!`

*(You will see the message instantly routed to the Subscriber terminal).*

**Step 4: Simulate a Network Crash**
To test fault tolerance, forcefully **close the Subscriber terminal** (Terminal 2) by clicking the trash can icon (Delete split terminal).

*(The Broker terminal will output: `[-] User1 went offline.`)*

**Step 5: Send Offline Messages (Time Uncoupling)**
Go back to the **Publisher terminal** (Terminal 3) and send a new message while the subscriber is offline:
`# Enter [topic:message] or 'exit' to quit: tech:AI is taking over!`

*(The Broker terminal will output: `[*] Buffered message for offline user: User1`)*

**Step 6: Reconnect & Catch-Up**
Open a new split terminal to replace the one you closed. Run the subscriber script again using the **exact same ID and topic**:
`python subscriber.py`
`# Enter Unique Subscriber ID: User1`
`# Enter topic to subscribe to: tech`

*(The subscriber will instantly receive the buffered "AI is taking over!" message through the catch-up mechanism).*

---

## Configuration Notes

- All three Python files (`broker.py`, `publisher.py`, `subscriber.py`) must be in the same root directory.
- The system is configured to run on `localhost` (127.0.0.1) using port `65432`. Ensure this port is not being blocked by a firewall or used by another application.
- To shut down the broker server cleanly, press `Ctrl + C` in the broker terminal. If it didn't work, force shut down the terminal by clicking the "trash icon".
- The `subscriber.py` relies on forceful termination to test the offline queue; do not code an explicit "exit" command for it.

---
