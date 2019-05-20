# -- coding: utf-8 --
""" Création d'un client pour le projet 'SpaceX' qui doit implémenter la RFC établie et ce client doit pouvoir
communiquer avec les serveurs de Brian, Guillaume et Vincent."""

# Created by Slackh
# Github : https://github.com/Stanislackh

"""Version Interface"""

from socket import *
from threading import Thread
import sys

nouvelleIP = "localhost"  # Variable à changer pour se connecter au serveur

"""Classes pour gérer les Threads"""

class ThreadCommandes(Thread):  # Permet de lancer le thread qui exécute les commandes
    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket

    def run(self):
        global message

        # listeMessages = ["CONNECT", "SETROBOT", "MOVE", "GETALL", "CHANGEPSEUDO", "RECEIVEDATAROBOT",
        #                  "ACCEPTREQUESTDATA", "PRIVATEMESS", "PAUSE", "ENDPAUSE", "QUIT"]

        message = ""  # Initialise le message à envoyer au serveur
        # print(message)
        #
        # while message != "QUIT":
        #     print("Tapez HELP pour avoir la liste des commandes !")
        #     message = input("Entrez votre commande : ")  # Entrée clavier
        #
        #     if message == "":  # Si le message est vide refait une demande d'entrée clavier
        #         print("Tapez HELP pour avoir la liste des commandes !")
        #         message = input("Entrez votre commande : ")  # Entrée clavier
        #
        #     elif message == "HELP":  # Renvoie la liste des commandes disponibles
        #         afficheCommandes()
        #
        #     else:
        #         client.send(message.encode())  # Envoie la commande au serveur
        #         data = client.recv(BUFFER_SIZE)
        #         afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus


class ThreadClient2Client(Thread):  # Créer le Thread pour la connexion inter Client
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):  # Permet de lancer le thread
        disc = socket(AF_INET, SOCK_STREAM)
        disc.connect((self.ip, self.port))
        ecu = False
        while ecu == False:
            data = client.recv(BUFFER_SIZE)
            texte = data.decode()
            last = texte[-2:]  # Stocke les 2 derniers caractères du message
            print(texte)
            if last == "\!":  # Si les caractères de fin sont \! le datafile du robot a été envoyé
                ecu = True


"""Gestion de l'affichage"""


def afficheLaReponse(reponse):  # Permet de chercher dans les dictionnaires pour afficher le message correspondant
    global tableauReponse
    global codeReponse

    reponse = reponse.decode()
    tableauReponse = reponse.split(" ")  # Sépare le code serveur et les infos supplémentaires
    codeReponse = tableauReponse[0]

    if codeReponse in okDico.keys():  # Cherche dans les codes valides du serveur
        if codeReponse == "100":  # La commande s'est bien éxécutée
            print("Commande éxécutée")
        elif codeReponse == "101":  # Affiche tous les cleints connectés avec leurs ressources
            pseudoRessources(tableauReponse)
        elif codeReponse == "102":  # Renvoi les données de la stratégie du client
            renvoiDonnee(tableauReponse)
        elif codeReponse == "103":  # Affiche la carte initiale
            afficheCarte(tableauReponse)
        elif codeReponse == "104":  # Demande la stratégie d'un client
            demandeData(tableauReponse)
        elif codeReponse == "105":  # Affiche la carte mise à jour
            afficheCarte(tableauReponse)
        elif codeReponse == "106":
            messagePrive(tableauReponse)  # Envoi un message privé au client spécifié
        else:
            print("WTF c'est quoi ce code ?")
    else:
        for key, valeur in errorDico.items():  # Cherche dans les codes d'erreur du serveur
            if codeReponse == key:
                print(valeur)


"""Gestion des informations supplémentaires envoyés du serveur"""


# Pour le code 101 => Retourne la liste des pseudos avec leurs ressources
def pseudoRessources(tableauReponse):
    global joueurRessources
    global messageRes

    listePseudos = tableauReponse[1]  # Récupère la liste des pseudos avec les ressources
    infos = listePseudos.split(",")  # Sépare les pseudos et ressources dans une liste

    messageRes = ""  # Initialise la chaîne réponse

    for element in infos:  # Cherche l'élément dans les infos
        joueurRessources = element.split(":")  # Sépare le pseudo et les nombre de ressouce
        messageRes += joueurRessources[0] + " " + joueurRessources[1] + "\n"
    print(messageRes)  # Affiche le pseudo et la ressource


# Pour le code 102 => Renvoie les données tranférées
def renvoiDonnee(tableauReponse):
    pass


# Pour le code 103 & 105 => Renvoie la carte ou la carte t
def afficheCarte(tableauReponse):
    global map
    carte = tableauReponse[1]  # Stocke la carte envoyée par le serveur
    map = ""  # Initialise la carte à afficher

    for i in carte:
        map += i
        # if i == ":":  # A chaque : fait un retour à la ligne
        #     map += "\n"

        if i == ",":  # Remplace les , par des espaces
            map += ""
    map += ":"  # Rajoute : à la dernière ligne
    print(map)
    return map


# Pour le code 104 => Renvoie l'IP et le port pour communiquer avec un autre client
def demandeData(tableauReponse):  # Demande les data du client spécifié
    # print(tableauReponse[1])  # Affiche l' Ip du client TEST
    # print(tableauReponse[2])  # Affiche le port de reception du client TEST

    # Lance le thread pour la communication inter clients
    threadReceiving2 = ThreadClient2Client(client)
    threadReceiving2.start()
    threadReceiving2.join()


def accepteData():  # Accepte de partager les data avec le client qui lui a demandé
    pass


# Pour le code 106 => l'envoi de message privé
def messagePrive(tableauReponse):
    print("Je suis passé" + "/n")
    print(tableauReponse[1])


""" Aide """


def afficheCommandes():  # Fonction pour afficher toutes les commandes

    print("CONNECT <pseudo> => Permet de se connecter avec le pseudo spécifié et recevoir une copie de la carte")
    print("SETROBOT <x> <y> => Pour positionner votre robot aux coordonnées x y avec x pour abscisse"
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
    "210": "Trop de client, réessayez plus tard",
    "211": "le pseudo rentré est trop court ou trop long doit être compris entre 3 et 10 caractères",
    "212": "Le robot est en pause faites ENDPAUSE pour pouvoir lui donner des ordres",
    "213": "Argument invalide faites HELP pour voir les arguments",
    "214": "Client connecté mais le robot n'est pas mis en place",
    "215": "Le robot est déjà sur la carte",
    "297": "Nombre d'aguments invalide",
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
    "105": "Renvoie la carte mise à jour",
    "106": "Message privé reçu"
}

"""Partie Connexion au serveur"""


def lancementClient():
    if len(sys.argv) != 2:  # Si il y a pas 2 arguments renvoi le message d'erreur
        print("Usage: {} <port>".format(sys.argv[0]))
        sys.exit(1)

    """Variables globales"""

    global adresseIP
    global portServeur
    global client
    global BUFFER_SIZE

    # adresseIP = "192.168.43.215"  # Adresse serveur de Brian
    # adresseIP = "192.168.43.76"  # Adresse serveur de Guillaume
    # adresseIP = "172.31.190.92"  # Adresse serveur de Vincent
    adresseIP = nouvelleIP
    portServeur = 3000  # Port d'écoute du serveur
    BUFFER_SIZE = 1024  # Taille du tampon

    client = socket(AF_INET, SOCK_STREAM)  # Création de la socket
    client.connect((adresseIP, portServeur))  # Demande de connexion à l'adresse et port indiqué
    print("Connexion vers " + adresseIP + " établie avec succès")  # Message de connexion réussie

    # Crée le Thread pour lancer les commandes
    threadReceiving = ThreadCommandes(client)
    threadReceiving.start()

    # while True:  # Ecoute le serveur
    #
    #     threadReceiving.join()  # Termine le thread des commandes
    #     client.close()  # Ferme la connexion avec le serveur
    #     break

    print("Vous avez quitté SpaceX à bientôt ! :)")


if __name__ == '__main__':
    lancementClient()
