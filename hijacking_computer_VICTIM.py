from pynput import keyboard, mouse
import socket
server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 12345
server_sock.connect((ip,port))
print("connected")

# --- Keyboard handler ---
def on_press(key):
    try:
        print(f"Key pressed: {key.char}")
        server_sock.send((f"key {key.char}").encode())
    except AttributeError:
        print(f"Special key: {key}")
        server_sock.send((f"s_key {key}").encode())


# --- Mouse handlers ---
def on_move(x, y):
    print(f"Pointer moved to {(x, y)}")
    server_sock.send((f"move {(x, y)}").encode())


def on_click(x, y, button, pressed):
    print(f"{'Pressed' if pressed else 'Released'} at {(x, y)} with {button}")
    server_sock.send((f"click {button}").encode())
    server_sock.send((f"{(x, y)}").encode())

    

def on_scroll(x, y, dy):
    print(f"Scrolled {'down' if dy < 0 else 'up'}")
    server_sock.send((f"Scrolled {'down' if dy < 0 else 'up'}").encode())

# Start both listeners in non-blocking way
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll
)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()


