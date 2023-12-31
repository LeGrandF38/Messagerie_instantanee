import socket 
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_text.insert(tk.END, message + '\n')
        except:
            print("Erreur lors de la réception du message.")
            client_socket.close()
            break

def send_message():
    message = message_entry.get()
    client_socket.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

# Configurer l'interface graphique du client
client_window = tk.Tk()
client_window.title("Client de messagerie")

chat_text = scrolledtext.ScrolledText(client_window, width=40, height=10)
chat_text.pack(padx=10, pady=10)

message_entry = Entry(client_window, width=30)
message_entry.pack(pady=10)

send_button = Button(client_window, text="Envoyer", command=send_message)
send_button.pack()

# Configurer le client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

# Démarrer un thread pour recevoir les messages du serveur
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

client_window.mainloop()
