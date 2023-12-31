import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Fonction pour gérer la communication avec un client
def handle_client(client_socket, adresse):
    while True:
        # Recevoir des données du client
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        # Afficher le message reçu et le diffuser à d'autres clients
        print(f"Message reçu de {adresse} : {data}")
        diffuser(data, client_socket)

    # Fermer le socket client lorsque la boucle se termine
    client_socket.close()

# Fonction pour diffuser un message à tous les clients
def diffuser(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                # Envoyer le message à chaque client (sauf l'expéditeur)
                client.send(message.encode('utf-8'))
            except:
                # Retirer le client s'il y a un problème d'envoi
                clients.remove(client)

# Fonction pour démarrer le serveur
def start_server():
    # Créer un objet socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associer le socket à une adresse et un port spécifiques
    server.bind(('0.0.0.0', 12345))
    # Écouter les connexions entrantes
    server.listen(2)

    print("Le serveur écoute sur le port 12345...")

    while True:
        # Accepter une connexion client
        client_socket, addr = server.accept()
        # Ajouter le socket client à la liste des clients
        clients.append(client_socket)

        # Créer un thread pour gérer la communication avec le client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

# Configurer l'interface graphique du serveur
server_window = tk.Tk()
server_window.title("Serveur de messagerie")

# Créer un widget de texte déroulant pour enregistrer les messages
log_text = scrolledtext.ScrolledText(server_window, width=40, height=10)
log_text.pack(padx=10, pady=10)

# Liste pour stocker les sockets des clients
clients = []

# Démarrer le serveur dans un thread séparé
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Démarrer la boucle d'événements Tkinter
server_window.mainloop()
