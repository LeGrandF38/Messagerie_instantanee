import socket 
import threading
import tkinter as tk
from tkinter import scrolledtext

def handle_client(client_socket, address):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        print(f"Message reçu de {address}: {data}")
        broadcast(data, client_socket)

    client_socket.close()

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(2)

    print("Le serveur écoute sur le port 12345...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

# Configurer l'interface graphique du serveur
server_window = tk.Tk()
server_window.title("Serveur de messagerie")

log_text = scrolledtext.ScrolledText(server_window, width=40, height=10)
log_text.pack(padx=10, pady=10)

clients = []

# Démarrer le serveur dans un thread séparé
server_thread = threading.Thread(target=start_server)
server_thread.start()

server_window.mainloop()
