import os
import readline
import socket as s
import sys
import threading

from des import decrypt, encrypt

KEY = "T1KIB146"
PORT = 5000
PROMPT = "[OUT] Message : "

def receive(sock):
    for line in sock.makefile("r"):
        cipher = line.strip()
        print(f"\r\033[K[IN] ciphertext : {cipher}")
        try:
            print(f"[IN] Message : {decrypt(cipher, KEY)}")
        except ValueError:
            print("[IN] failed to decrypt")
        print("\n" + PROMPT + readline.get_line_buffer(), end="", flush=True)
    print("\n[!] Other side disconnected.")
    os._exit(0)

def send(sock):
    while True:
        try:
            message = input(PROMPT)
        except (EOFError, KeyboardInterrupt):
            break
        if message == "/quit":
            break
        if message:
            cipher = encrypt(message, KEY)
            sock.sendall((cipher + "\n").encode())
            print(f"[OUT] ciphertext : {cipher}\n")
    sock.close()

def main():
    if sys.argv[1] == "server":
        server = s.socket(s.AF_INET, s.SOCK_STREAM)
        server.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", PORT))
        server.listen(1)
        print(f"[*] Waiting for connection")
        sock, addr = server.accept()
        print(f"[*] Connected with {addr[0]}")
    else:
        sock = s.create_connection((sys.argv[1], PORT))
        print(f"[*] Connected to {sys.argv[1]}")
    print("[*] Type to chat (Enter to send, /quit to exit)\n")
    threading.Thread(target=receive, args=(sock,), daemon=True).start()
    send(sock)

if __name__ == "__main__":
    main()
