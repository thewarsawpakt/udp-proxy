import threading
import socket
import queue
import time

BUFFER_SIZE = 2048
BOUND_SERVER_ADDR = ("127.0.0.1", 9090)

packet_queue = queue.Queue()

def serve(addr = ("127.0.0.1", 8080)):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)

    print(f"bound to addr {addr}, forwarding to addr {BOUND_SERVER_ADDR}")

    while True:
        message, address = s.recvfrom(BUFFER_SIZE)

        print(f"got packet of size {len(message)} from {address}")
        packet_queue.put(message)
        print("put packet into queue")

def send(data):
    print(f"sending packet of size {len(data)} to {BOUND_SERVER_ADDR}")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data, BOUND_SERVER_ADDR)

def handle():
    while True:
        try:
            send(packet_queue.get())

        except queue.Empty:
            time.sleep(0.25) # wait for a bit so that we aren't polling instantly, this will probably introduce latency.

tasks = []

for task in [handle, serve]:
    tasks.append(threading.Thread(target=task))

for task in tasks:
    task.start()
    task.join()
