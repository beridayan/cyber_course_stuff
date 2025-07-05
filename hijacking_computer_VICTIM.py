from pynput import keyboard, mouse
import socket
import cv2
import numpy as np
import mss
import threading

# Connect to server
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 12345
server_sock.connect((ip, port))
print("Connected")

def send_text(msg):
    data = msg.encode()
    header = b'T' + str(len(data)).zfill(10).encode()
    server_sock.sendall(header + data)

def send_frame(frame_bytes):
    header = b'F' + str(len(frame_bytes)).zfill(10).encode()
    server_sock.sendall(header + frame_bytes)

def screen_sender():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            _, encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            data = encoded.tobytes()
            try:
                send_frame(data)
            except Exception as e:
                print(f"Error sending frame: {e}")
                break

def recv_all(sock, size):
    data = b''
    while len(data) < size:
        part = sock.recv(size - len(data))
        if not part:
            return None
        data += part
    return data

def receiver_loop():
    while True:
        # read 1 byte for message type
        msg_type = recv_all(server_sock, 1)
        if not msg_type:
            break

        # read 10 bytes for length
        length_data = recv_all(server_sock, 10)
        if not length_data:
            break

        try:
            payload_len = int(length_data.decode())
        except:
            print("Invalid length")
            break

        # read payload
        payload = recv_all(server_sock, payload_len)
        if not payload:
            break

        if msg_type == b'T':
            try:
                text = payload.decode()
                print("Text message:", text)
            except:
                print("Decode failed")

# start everything
screen_thread = threading.Thread(target=screen_sender, daemon=True)
receiver_thread = threading.Thread(target=receiver_loop, daemon=True)

screen_thread.start()
receiver_thread.start()

screen_thread.join()
receiver_thread.join()
