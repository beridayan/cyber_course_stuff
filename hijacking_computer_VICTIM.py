from pynput import keyboard, mouse
import socket
import cv2
import numpy as np
import mss
import threading
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

mouse = MouseController()
keyboard = KeyboardController()
# Connect to server
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '10.0.0.25'
port = 12345
server_sock.connect((ip, port))
print("Connected")
special_keys = {
    'Key.space': Key.space,
    'Key.enter': Key.enter,
    'Key.shift': Key.shift,
    'Key.ctrl': Key.ctrl,
    'Key.alt': Key.alt,
    'Key.esc': Key.esc,
    'Key.backspace': Key.backspace,
    'Key.tab': Key.tab,
    'Key.up': Key.up,
    'Key.down': Key.down,
    'Key.left': Key.left,
    'Key.right': Key.right,
}
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
def update_pos(text):
    parts = text.split()
    type = parts[0]

    if type == "move":
        
        mouse.position = (int(parts[1]), int(parts[2]))
        print('Now we have moved it to {}'.format(
            mouse.position))

    elif type == "click":
        if parts[1] == "Button.left":
            mouse.press(Button.left)
            mouse.release(Button.left)
        else:
            mouse.press(Button.right)
            mouse.release(Button.right)

    elif type == "scroll":
        if parts[1] == "down":
            mouse.scroll(0, -1)  

        else:
            mouse.scroll(0, 1)  
    elif type == "key" :
        keyboard.press(parts[1])
        keyboard.release(parts[1])
    elif type == "s_key":
        keyboard.press( special_keys.get(parts[1], parts[1]))
        keyboard.release(special_keys.get(parts[1], parts[1]))






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
                update_pos(text)

            except:
                print("Decode failed")

# start everything
screen_thread = threading.Thread(target=screen_sender, daemon=True)
receiver_thread = threading.Thread(target=receiver_loop, daemon=True)

screen_thread.start()
receiver_thread.start()

screen_thread.join()
receiver_thread.join()
