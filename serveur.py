"""Création d'un serveur gérant une carte contenant des ressources dans le cadre d’une simulation de comportements de
robots."""

import socket

print("serveur ouvert")

ADRESSE = ''
PORT = 6789

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((ADRESSE, PORT))
serveur.listen(10)
client, adresse_client = serveur.accept()
print(adresse_client, " viens de se connecter")

"""Création d'une map pour le serveur"""

map = []
for i in range(1, 11):
    for j in range(1, 10):
        map.append(0)
for k in range(1, 11):
    map.append(0)

"""Création d'une map pour le client"""

map2Player = ""

"""Fonction permettant le depot d'un robot sur la map du serveur"""


def DepotJoueur(x, y):
    x = x
    y = y
    cour = 0
    cour2 = 0
    while cour < ((x - 1) * 10):
        cour += 1
    while cour2 < y - 1:
        cour2 += 1
    map[cour + cour2] = 1


"""Fonction qui converti la map du serveur en chaine de caractere lisible par le client"""


def ConvertMap2Player():
    map2Player = ""

    compt = 1

    for i in map:
        if compt % 10 != 0:
            if i == 0:
                map2Player += "0,"
            else:
                map2Player += "1,"
        else:
            if compt != 100:
                if i == 0:
                    map2Player += "0:"
                else:
                    map2Player += "1:"
            else:
                if i == 0:
                    map2Player += "0"
                else:
                    map2Player += "1"
        compt += 1


"""Création de la liste des joueurs"""

listJoueur = {}
listRessource = {}
etatPlayer = {}

"""reception de la commande du client"""

donnee = client.recv(1024)
donnee = donnee.decode()

if not donnee:
    reponse = "299"
else:
    print(donnee, " receptionné")

    com = donnee.split(" ", 1)

    if com[0] == "CONNECT":

        """réponse a la commande CONNECT"""

        try:
            if com[1]:
                if len(com[1]) < 3 or len(com[1]) > 10:
                    reponse = "211"
                elif adresse_client in listJoueur:
                    reponse = "200"
                elif not com[1] in listJoueur.values():
                    reponse = "202"
                else:
                    listJoueur[adresse_client] = com[1]
                    listRessource[com[1]] = 0
                    etatPlayer[adresse_client] = "play"
                    ConvertMap2Player()
                    reponse = "103 " + map2Player
        except:
            reponse = "297"

    elif com[0] == "SETROBOT":

        """réponse a la commande SETROBOT"""

        try:
            if com[1] and com[2]:
                if not adresse_client in listJoueur:
                    reponse = "201"
                elif listJoueur.values(adresse_client) in map:
                    reponse = "215"
                elif com[1] < 1 or com[1] > 10 or com[2] < 1 or com[2] > 10:
                    reponse = "209"
                elif map[com[1] * 10 + com[2] - 1] != 0:
                    reponse = "214"
                else:
                    DepotJoueur(com[1], com[2])
                    ConvertMap2Player()
                    reponse = "100 " + map2Player

        except:
            reponse = "297"

    elif com[0] == "MOVE":

        """réponse a la commande MOVE"""

        try:
            if com[1] and com[2]:
                if not adresse_client in listJoueur:
                    reponse = "201"
                elif listJoueur.values(adresse_client) in map:
                    reponse = "215"
                elif com[1] < 1 or com[1] > 10 or com[2] < 1 or com[2] > 10:
                    reponse = "209"
                elif map[com[1] * 10 + com[2] - 1] != 0:
                    reponse = "214"
                elif etatPlayer[adresse_client] == "pause":
                    reponse = "212"
                # elif case pas a coté:
                else:
                    # deplacer le robot
                    reponse = "105 " + map2Player

        except:
            reponse = "297"

    elif com[0] == "GETALL":

        """réponse a la commande GETALL"""

        if not adresse_client in listJoueur:
            reponse = "201"
        else:
            reponse = "101 "
            for cle, valeur in listRessource.items():
                reponse += cle + ":" + valeur + ","
                reponse = reponse[:-1]

    elif com[0] == "CHANGEPSEUDO":

        """réponse a la commande CHANGEPSEUDO"""

        try:
            if com[1]:
                if len(com[1]) < 3 or len(com[1]) > 10:
                    reponse = "211"
                elif not com[1] in listJoueur.values():
                    reponse = "202"
                else:
                    val = listRessource.pop(listJoueur[adresse_client])
                    listJoueur[adresse_client] = com[1]
                    listRessource[com[1]] = val
                    reponse = "100"
        except:
            reponse = "297"

    elif com[0] == "RECEIVEDATAROBOT":

        """réponse a la commande RECEIVEDATAROBOT"""

        ...

    elif com[0] == "ACCEPTREQUESTDATA":

        """réponse a la commande ACCEPTREQUESTDATA"""

        ...

    elif com[0] == "PRIVATEMESS":

        """réponse a la commande PRIVATEMESS"""

        ...

    elif com[0] == "PAUSE":

        """réponse a la commande PAUSE"""

        if etatPlayer[adresse_client] == "pause":
            reponse = "212"
        elif listJoueur.values(adresse_client) not in map:
            reponse = "214"
        else:
            etatPlayer[adresse_client] = "pause"
            reponse = "100"

    elif com[0] == "ENDPAUSE":

        """réponse a la commande ENDPAUSE"""

        if etatPlayer[adresse_client] == "play":
            reponse = "205"
        elif listJoueur.values(adresse_client) not in map:
            reponse = "214"
        else:
            etatPlayer[adresse_client] = "play"
            reponse = "100"

    elif com[0] == "QUIT":

        """réponse a la commande QUIT"""

        if adresse_client not in listJoueur:
            reponse = "201"
        else:
            del listRessource[listJoueur.get(adresse_client)]
            del listJoueur[adresse_client]
            del etatPlayer[adresse_client]
            client.close()
            # envoie a tous qu'un joueur s'est déconecter

    else:

        """réponse a une commande non existante"""

        reponse = "298"

    reponse = reponse.encode()
    client.send(reponse)

print("fermeture de la connection avec le client")
client.close()
print("arret du serveur")
serveur.close()
