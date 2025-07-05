import socket
import cv2
import numpy as np
from pynput import keyboard, mouse
import threading

# Setup server
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 12345
server_sock.bind((ip, port))
server_sock.listen()
print("Listening for connection...")
client_sock, address = server_sock.accept()
print("Connected from", address)

# --- Utility: recv exact size ---
def recv_all(sock, size):
    data = b''
    while len(data) < size:
        part = sock.recv(size - len(data))
        if not part:
            return None
        data += part
    return data

# --- Send text over socket ---
def send_text(msg):
    try:
        data = msg.encode()
        header = b'T' + str(len(data)).zfill(10).encode()
        client_sock.sendall(header + data)
    except Exception as e:
        print(f"[send_text] Error: {e}")

# --- Keyboard listener ---
def on_press(key):
    try:
        send_text(f"key {key.char}")
    except AttributeError:
        send_text(f"s_key {key}")

# --- Mouse listener ---
def on_move(x, y):
    send_text(f"move {x} {y}")

def on_click(x, y, button, pressed):
    send_text(f"click {button} {'pressed' if pressed else 'released'} {x} {y}")

def on_scroll(x, y, dx, dy):
    send_text(f"scroll {'down' if dy < 0 else 'up'} {x} {y}")

# --- Receiver thread (receive frames + events) ---
def receiver_loop():
    while True:
        msg_type = recv_all(client_sock, 1)
        if not msg_type:
            break

        length_data = recv_all(client_sock, 10)
        if not length_data:
            break

        try:
            payload_len = int(length_data.decode())
        except ValueError:
            print("Invalid length received")
            break

        payload = recv_all(client_sock, payload_len)
        if not payload:
            break

        if msg_type == b'T':
            try:
                text = payload.decode()
                print("[Text]", text)
            except Exception as e:
                print("[!] Text decode failed:", e)

        elif msg_type == b'F':
            frame = cv2.imdecode(np.frombuffer(payload, np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow("Remote Screen", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    client_sock.close()
    cv2.destroyAllWindows()

# --- Start everything ---
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

receiver_thread = threading.Thread(target=receiver_loop, daemon=True)
receiver_thread.start()

keyboard_listener.join()
mouse_listener.join()
receiver_thread.join()
