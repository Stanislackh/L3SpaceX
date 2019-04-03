""" Création d'un client pour le projet 'SpaceX' qui doit implémenter la RFC établie et ce client doit pouvoir
communiquer avec les serveurs de Brian, Guillaume et Vincent."""

# Created by Slackh
# https://github.com/Stanislackh

from socket import *
from threading import Thread
import sys

"""Classes pour gérer les Threads"""


class ThreadEcoute(Thread):  # Permet de lancer le thread d'écoute serveur
    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            reponse = self.socket.recv(BUFFER_SIZE)
            afficheLaReponse(reponse)


class ThreadClient2Client(Thread):  # Créer le Thread pour la connexion inter Client
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):  # Permet de lancer le thread
        BUFFER_SIZE = 1024
        disc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        disc.connect((self.ip, self.port))
        ecu = False
        while ecu == False:
            data = disc.recv(BUFFER_SIZE)
            text = data.decode()
            last = text[-2:]
            print(text)
            if last == "\!":
                ecu = True


"""Gestion de l'affichage"""


def afficheLaReponse(reponse):  # Permet de chercher dans les dictionnaires pour afficher le message correspondant
    reponse = reponse.decode()
    tableauReponse = reponse.split(" ")
    codeReponse = tableauReponse[0]

    for key, value in okDico.items():  # Cherche dans les codes valides du serveur
        if codeReponse in key:
            print(value)

    for key, valeur in errorDico.items():  # Cherche dans les codes d'erreur du serveur
        if codeReponse in key:
            print(valeur)


def afficheCommandes():  # Fonction pour afficher toutes les commandes

    print("CONNECT <pseudo> => Permet de se connecter avec le pseudo spécifié et recevoir une copie de la carte")
    print("SETROBOT <x> <y> => Pour positionner votre robot aux coordonnées x y avec x pour abscisse "
          "et y pour ordonnée")
    print("MOVE <x> <y> => Permet de déplacer le robot à la coordonnée x y avec x pour abscisse et y pour ordonnée")
    print("GETALL => Pour recevoir la liste des personnes connectées avec leurs ressources")
    print("CHANGEPSEUDO <pseudo> => Permet de changer l'ancien pseudo par le nouveau")
    print("RECEIVEDATAROBOT <pseudo> => Renvoi la stratégie de pseudo si il accepte")
    print("ACCEPTREQUESTDATA <port> => Si vous recevez une RECEIVEDATAROBOT renvoyez cette commmande avec le numéro"
          " de port pour établir une connexion avec celui qui vous a envoyé la requête")
    print("PRIVATEMESS <pseudo> => Envoie un message à pseudo")
    print("PAUSE => Mets le robot en pause")
    print("ENDPAUSE => Après la mise en pause remet le robot en fonction")
    print("QUIT => Pour quitter l'application")


""" Dictionnaires des codes serveur"""

# Dictionnaire des erreurs serveurs
errorDico = {
    "200": "Client déjà connecté",
    "201": "Client non connecté",
    "202": "Ce pseudo est déjà pris",
    "203": "Le robot est déjà en pause",
    "204": "Le pseudo rentré n'existe pas",
    "205": "Le robot est déjà actif",
    "206": "Le robot n'a rien fait pas de data disponible",
    "207": "Le message est vide",
    "208": "Le client demandé est pas connecté",
    "209": "La position demandée est non valide",
    "210": "Trop de client, réessayer plus tard",
    "211": "le pseudo rentré est trop court ou trop long doit être compris entre 3 et 10 caractères",
    "212": "Le robot est déjà en pause faites ENDPAUSE pour pouvoir lui donner des ordres",
    "213": "Argument invalide faites HELP pour voir les arguments",
    "214": "Client connecté mais le robot n'est pas mis en place",
    "215": "Le robot est déjà sur la carte",
    "297": "Pas assez d'arguments",
    "298": "La requête n'est pas reconnue",
    "299": "Erreur Interne"
}

# Dictionnaire des réponses ok du serveur
okDico = {
    "100": "Request Sucessfull",
    "101": "Retourne la liste des pseudos avec leurs ressources",
    "102": "Renvoie les données tranférées",
    "103": "Connection établie et renvoie la carte",
    "104": "Renvoie l'IP et le port pour communiquer avec un autre client",
    "105": "Renvoie la carte mise à jour"
}

"""Partie Connexion au serveur"""

if len(sys.argv) != 2:  # Si il y a pas 2 arguments renvoi le message d'erreur
    print("Usage: {} <port>".format(sys.argv[0]))
    sys.exit(1)

adresseIP = "localhost"  # Adresse IP du serveur
portServeur = 3000  # Port d'écoute du serveur
BUFFER_SIZE = 1024  # Taille du tampon

client = socket(AF_INET, SOCK_STREAM)  # Création de la socket
client.connect((adresseIP, portServeur))  # Demande de connexion à l'adresse et port indiqué
print("Connexion vers " + adresseIP + " établie avec succès")  # Message de connexion réussie

# Crée le Thread pour écouter le serveur
threadReceiving = ThreadEcoute(client)
threadReceiving.start()

message = ""  # Initialise le message à envoyer au serveur

while message != "QUIT":
    print("Tapez help pour avoir la liste des commandes !")
    message = input("Entrez votre commande : ")

    if message == "HELP":  # Renvoie la liste des commandes disponibles
        afficheCommandes()

    else:
        client.send(message.encode())  # Envoie la commande au serveur
        data = client.recv(BUFFER_SIZE)
        afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus

threadReceiving.join()  # Termine le thread
client.close()  # Ferme la connexion avec le serveur
