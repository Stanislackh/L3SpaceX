# -- coding: utf-8 --

import socket, random
from threading import Thread
from datetime import datetime

# Ceci est tous les dictionnaire dont j'ai besoin pour stocker les joueurs ou la map

listJoueur = {}
listRessource = {}
etatPlayer = {}
carte = []
pourRepondre = {}
memRep = {}
coord = {}
map2Player = ""


def CreerCarte():  # Def permettant de creer la carte de jeu

    for i in range(1, 11):

        for j in range(1, 10):
            ress = random.randint(1, 100)

            if ress >= 67:
                nbRess = random.randint(1, 5)
                carte.append(nbRess)

            else:
                carte.append(0)

    for k in range(1, 11):
        ress = random.randint(1, 100)

        if ress >= 67:
            nbRess = random.randint(1, 5)
            carte.append(nbRess)

        else:
            carte.append(0)


CreerCarte()  # Création de la map a l'ouverture du serveur


class ListenClient(Thread):  # class permettant l'écoute d'un client

    def __init__(self, ip, port, clientSo):

        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientSo = clientSo

    def DepotJoueur(self, x, y, name):  # Def permettant de poser un joueur sur la map

        x = x
        y = y
        cour = 0
        cour2 = 0

        while cour < (x * 10):
            cour += 1

        while cour2 < y:
            cour2 += 1

        if carte[cour + cour2] in [1, 2, 3, 4, 5]:
            listRessource[name] += carte[cour + cour2]

        carte[cour + cour2] = name

    # Def permettant de modifier la map en une chaine de caractère afin de l'envoyer au client
    def ConvertMap2Player(self):

        map2Player2 = ""

        compt = 1

        for i in carte:

            if compt % 10 != 0:

                if i in [0, 1, 2, 3, 4, 5]:
                    map2Player2 += "0,"

                else:
                    map2Player2 += i + ","
            else:

                if compt != 100:

                    if i in [0, 1, 2, 3, 4, 5]:
                        map2Player2 += "0:"

                    else:
                        map2Player2 += i + ":"

                else:

                    if i in [0, 1, 2, 3, 4, 5]:
                        map2Player2 += "0"

                    else:
                        map2Player2 += i

            compt += 1

        return map2Player2

    def run(self):  # Le coeur du programme

        try:

            traceback = open('tracebackServeurSpaceX.txt', 'a')
            traceback.write(str(self.clientSo))
            traceback.write(" connected to the serveur at " + str(datetime.now()) + "\n")
            traceback.close()

            while True:
                data = self.clientSo.recv(1024)  # Reception d'une commande de la part du client

                if data:
                    data = data.decode()
                    com = data.split(" ")

                    if com[0] == "CONNECT":  # Si la commande est CONNECT

                        if len(com) == 2:  # Verifie si il y a le bon nombre de paramètre

                            if len(com[1]) < 3 or len(com[1]) > 10:  # Vérifie si le pseudo est entre 3 et 10 caractères
                                reponse = "211"

                            # Vérifie qu'il n'est pas déjà connecté sinon renvoie le code 200
                            elif self.clientSo in listJoueur:
                                reponse = "200"

                            # Vérification que le pseudo n'est pas déja pris sinon renvoie le code 202
                            elif com[1] in listJoueur.values():
                                reponse = "202"

                            # Vérifie qu'il n'y a pas déja 10 personnes de connectées sinon renvoie le code 210
                            elif len(listJoueur) == 10:
                                reponse = "210"

                            else:  # Si tout est OK renpli les dictionaire et renvoie le code 103 + la map
                                listJoueur[self.clientSo] = com[1]
                                listRessource[com[1]] = 0
                                etatPlayer[self.clientSo] = "play"
                                pourRepondre[self.clientSo] = self.clientSo
                                map2Player = ListenClient.ConvertMap2Player(self)
                                reponse = "103 " + map2Player

                        else:  # Si le nombre de paramètre n'est pas bon renvoie le code 297
                            reponse = "297"

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("CONNECT" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "SETROBOT":  # Si la commande est SETROBOT

                        if len(com) == 3:  # Verifie si il y a le bon nombre de paramètre

                            # Vérifie que le client est connecté sinon renvoie le code 201
                            if not self.clientSo in listJoueur:
                                reponse = "201"

                            # Vérifie que le client n'est pas sur la carte sinon renvoie le code 215
                            elif listJoueur[self.clientSo] in carte:
                                reponse = "215"

                            # Vérifie que les coordonnéé sont pas hors de la map sinon renvoie le code 214
                            elif int(com[1]) < 0 or int(com[1]) > 9 or int(com[2]) < 0 or int(com[2]) > 9:
                                reponse = "214"

                            # Vérifie que les coordonnéé sont autour du client sinon renvoie le code 209
                            elif carte[(int(com[1])) * 10 + int(com[2])] not in [0, 1, 2, 3, 4, 5]:
                                reponse = "209"

                            else:  # si tout est OK pose le client seur la map et lui renvoie avec le code 105
                                ListenClient.DepotJoueur(self, int(com[1]), int(com[2]),
                                                         listJoueur[self.clientSo])
                                map2Player = ListenClient.ConvertMap2Player(self)
                                # for nono in listJoueur:
                                #     if nono != self.clientSo:
                                #         reponse2 = "105 " + map2Player
                                #         reponse2 = reponse2.encode()
                                #         pourRepondre[nono].send(reponse2)
                                reponse = "105 " + map2Player
                                coord[self.clientSo] = (int(com[1]), int(com[2]))

                        else:  # Si le nombre de paramètre n'est pas bon renvoie le code 297
                            reponse = "297"

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("SETROBOT" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "MOVE":  # Si la commande est MOVE

                        if len(com) == 3:  # Verifie si il y a le bon nombre de paramètre

                            # Vérifie que le client est connecté sinon renvoie le code 201
                            if not self.clientSo in listJoueur:
                                reponse = "201"

                            # Vérifie que le client est sur la carte sinon renvoie le code 214
                            elif listJoueur[self.clientSo] not in carte:
                                reponse = "214"

                            # Vérifie que les coordonnéé sont pas hors de la map sinon renvoie le code 214
                            elif int(com[1]) < 0 or int(com[1]) > 9 or int(com[2]) < 0 or int(com[2]) > 9:
                                reponse = "214"

                            # Vérifie que les coordonnéé sont autour du client sinon renvoie le code 209
                            elif carte[(int(com[1])) * 10 + int(com[2])] not in [0, 1, 2, 3, 4, 5]:
                                reponse = "209"

                            # Vérifie que le client n'est pas en pause
                            elif etatPlayer[self.clientSo] == "pause":
                                reponse = "212"

                            # si tout est OK déplace le client sur la map et lui renvoie avec le code 105
                            elif coord[self.clientSo][0] in [int(com[1]) - 1, int(com[1]), int(com[1]) + 1] and \
                                    coord[self.clientSo][1] in [int(com[2]) - 1, int(com[2]), int(com[2]) + 1] and \
                                    coord[self.clientSo] != (int(com[1]), int(com[2])):
                                val = 0

                                for i in carte:

                                    if i == listJoueur[self.clientSo]:
                                        break
                                    val += 1

                                carte[val] = 0
                                ListenClient.DepotJoueur(self, int(com[1]), int(com[2]),
                                                         listJoueur[self.clientSo])
                                map2Player = ListenClient.ConvertMap2Player(self)
                                coord[self.clientSo] = (int(com[1]), int(com[2]))
                                # for nono in listJoueur:
                                #     if nono != self.clientSo:
                                #         reponse2 = "105 " + map2Player
                                #         reponse2 = reponse2.encode()
                                #         pourRepondre[nono].send(reponse2)
                                reponse = "105 " + map2Player

                            else:  # Sinon la case est déjà occupé et rnevoie le code 209
                                reponse = "209"

                        else:  # Si le nombre de paramètre n'est pas bon renvoie le code 297
                            reponse = "297"

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("MOVE" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "GETALL":  # Si la commande est GETALL

                        # Vérifie que le client est connecté sinon renvoie le code 201
                        if not self.clientSo in listJoueur:
                            reponse = "201"

                        else:  # sinon renvoie la liste des client connecté ainsi que leurs ressources
                            reponse = "101 "

                            for cle, valeur in listRessource.items():
                                reponse += cle + ":" + str(valeur) + ","
                            reponse = reponse[:-1]

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("GETALL" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "CHANGEPSEUDO":  # Si la commande est CHANGEPSEUDO

                        if len(com) == 2:  # Verifie si il y a le bon nombre de paramètre

                            if len(com[1]) < 3 or len(com[1]) > 10:  # Vérifie si le pseudo est entre 3 et 10 caractères
                                reponse = "211"

                            # Vérification que le pseudo n'est pas déja pris sinon renvoie le code 202
                            elif com[1] in listJoueur.values():
                                reponse = "202"

                            # si tout est OK modifie le pseudo du joueur partout ou il le faut et renvoie le code 100
                            else:
                                val = listRessource.pop(listJoueur[self.clientSo])
                                val2 = pourRepondre.pop(self.clientSo)
                                pos = 0

                                if listJoueur[self.clientSo] in carte:

                                    for i in carte:

                                        if i == listJoueur[self.clientSo]:
                                            break
                                        pos += 1

                                    carte[pos] = com[1]

                                map2Player = ListenClient.ConvertMap2Player(self)
                                listJoueur[self.clientSo] = com[1]
                                listRessource[com[1]] = val
                                pourRepondre[self.clientSo] = val2
                                reponse = "100"

                        else:  # Si le nombre de paramètre n'est pas bon renvoie le code 297
                            reponse = "297"

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("CHANGEPSEUDO" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "RECEIVEDATAROBOT":  # Si la commande est RECEIVEDATAROBOT

                        if len(com) == 2:  # Verifie si il y a le bon nombre de paramètre

                            # Vérifie que le joueur dont les data sont demandé existe
                            if com[1] in listJoueur.values():

                                for nono in listJoueur:  # cherche le joueur demandé

                                    if listJoueur[nono] == com[1]:  # et envoie ip + port a ce dernier
                                        reponse = "104" + str(self.ip) + str(self.port)
                                        reponse = reponse.encode()
                                        pourRepondre[nono].send(reponse)
                                        memRep[com[1]] = listJoueur[self.clientSo]
                                    reponse = "100"

                            # Vérifie que le joueur dont les data sont demandé existe sinon renvoie le code 204
                            elif com[1] not in listJoueur.values():
                                reponse = "204"

                            # Vérifie que le client est connecté sinon renvoie le code 201
                            elif not self.clientSo in listJoueur:
                                reponse = "201"

                            # Vérifie que le joueur dont les data sont demandé en a a envoyer sinon renvoie le code 206
                            elif com[1] not in carte:
                                reponse = "206"

                            else:  # Si la personne demandé n'existe pas renvoie le code 208
                                reponse = "208"

                        else:  # Si le nombre de paramètre n'est pas bon renvoie le code 297
                            reponse = "297"

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("RECEIVEDATAROBOT" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "ACCEPTREQUESTDATA":  # Si la commande est ACCEPTREQUESTDAT

                        if len(com) == 2:  # Verifie si il y a le bon nombre de paramètre

                            # Vérifie que le joueur a qui les data vont être envoyer existe sinon renvoie le code 204
                            if memRep[listJoueur[self.clientSo]] not in listJoueur.values():
                                reponse = "204"

                            # Vérifie que le client est connecté sinon renvoie le code 201
                            elif not self.clientSo in listJoueur:
                                reponse = "201"

                            # Vérifie que le joueur dont les data sont demandé en a a envoyer sinon renvoie le code 206
                            elif memRep[listJoueur[self.clientSo]] not in carte:
                                reponse = "206"

                            # Vérifie que le joueur dont les data sont demandé existe
                            elif memRep[listJoueur[self.clientSo]] in listJoueur.values():

                                for cle, valeur in memRep.items():  # cherche le joueur demandé

                                    if valeur == listJoueur[self.clientSo]:

                                        for cle2, valeur2 in listJoueur.items():

                                            if valeur2 == cle:  # et envoie le port a ce dernier
                                                reponse = "102" + com[1]
                                                reponse = reponse.encode()
                                                pourRepondre[cle2].send(reponse)
                                                break
                                del memRep[listJoueur[cle2]]
                                reponse = "100"

                            else:  # Si la personne demandé n'existe pas renvoie le code 208
                                reponse = "208"

                        else:  # Si le nombre de paramètre n'est pas bon renvoie le code 297
                            reponse = "297"

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("ACCEPTREQUESTDATA" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "PRIVATEMESS":  # Si la commande est PRIVATEMESS

                        if len(com) >= 3:  # Verifie si il y a le bon nombre de paramètre

                            # Vérifie que le joueur a qui le message va être envoyer existe
                            if com[1] in listJoueur.values():

                                i = 2
                                rep = ""

                                while len(com) > i:
                                    rep += com[i] + " "
                                    i += 1
                                rep = rep[:-1]
                                reponse = "100"

                                for nono in listJoueur:  # cherche le joueur demandé

                                    if listJoueur[nono] == com[1]:
                                        reponse2 = "102" + rep
                                        reponse2 = reponse2.encode()
                                        pourRepondre[nono].send(reponse2)

                            # Vérifie que le joueur a qui les data vont être envoyer existe sinon renvoie le code 204
                            elif com[1] not in listJoueur.values():
                                reponse = "204"

                            # Vérifie que le message n'est pas vide sinon renvoie le code 207
                            elif com[2] == "":
                                reponse = "207"

                            # Vérifie que le client est connecté sinon renvoie le code 201
                            elif not self.clientSo in listJoueur:
                                reponse = "201"

                            else:  # Si la personne demandé n'existe pas renvoie le code 208
                                reponse = "208"

                        else:  # Si le nombre de paramètre n'est pas bon renvoie le code 297
                            reponse = "297"

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("PRIVATEMESS" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "PAUSE":  # Si la commande est PAUSE

                        # Vérifie que le joueur n'est pas déjà en pause sinon renvoie le code 212
                        if etatPlayer[self.clientSo] == "pause":
                            reponse = "212"

                        # Vérifie que le client est sur la carte sinon renvoie le code 214
                        elif listJoueur[self.clientSo] not in carte:
                            reponse = "214"

                        else:  # si tout est OK met le joueur en état de pause et renvoie le code 100
                            etatPlayer[self.clientSo] = "pause"
                            reponse = "100"

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("PAUSE" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "ENDPAUSE":  # Si la commande est ENDPAUSE

                        # Vérifie que le joueur n'est pas déjà en play sinon renvoie le code 205
                        if etatPlayer[self.clientSo] == "play":
                            reponse = "205"

                        # Vérifie que le client est sur la carte sinon renvoie le code 214
                        elif listJoueur[self.clientSo] not in carte:
                            reponse = "214"

                        else:  # si tout est OK met le joueur en état de play et renvoie le code 100
                            etatPlayer[self.clientSo] = "play"
                            reponse = "100"

                        traceback = open('tracebackServeurSpaceX.txt', 'a')
                        traceback.write("ENDPAUSE" + " to " + str(listJoueur[self.clientSo]) + " " + str(datetime.now()) + "\n")
                        traceback.close()

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "QUIT":  # Si la commande est QUIT

                        # Vérifie que le client est connecté sinon renvoie le code 201
                        if self.clientSo not in listJoueur:
                            reponse = "201"
                            reponse = reponse.encode()
                            self.clientSo.send(reponse)

                        else:  # sinon supprime le joueur partout ou il doit l'être apres avoir envoyer le code 100
                            reponse = "100"
                            reponse = reponse.encode()
                            self.clientSo.send(reponse)

                            traceback = open('tracebackServeurSpaceX.txt', 'a')
                            traceback.write(str(listJoueur[self.clientSo]) + " deconnected at " + str(datetime.now()) + "\n")
                            traceback.close()

                            # reponse = listJoueur[self.clientSo] + "s'est déconecter"
                            # reponse = reponse.encode()
                            val = 0

                            # Vérifie si le joueur est sur la map pour le supprimer sur cette dernière
                            if listJoueur[self.clientSo] in carte:

                                for i in carte:

                                    if i == listJoueur[self.clientSo]:
                                        break
                                    val += 1
                                carte[val] = 0

                            map2Player = ListenClient.ConvertMap2Player(self)
                            del listRessource[listJoueur.get(self.clientSo)]
                            del listJoueur[self.clientSo]
                            del etatPlayer[self.clientSo]
                            del pourRepondre[self.clientSo]

                            # Vérifie si le joueur est sur la map pour le supprimer sur cette dernière
                            if self.clientSo in coord:

                                del coord[self.clientSo]

                            # for nono in listJoueur:
                            #     pourRepondre[nono].send(reponse)

                            break
                    else:  # Si le joueur n'est pas connecter renvoie le code 298

                        """réponse a une commande non existante"""

                        reponse = "298"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)
                else:  # Si le joueur envoie une commande non existante renvoie le code 298
                    reponse = "298"

                    reponse = reponse.encode()
                    self.clientSo.send(reponse)
        finally:
            self.clientSo.close()


sockserveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockserveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servadress = ("192.168.43.215", 3000)
sockserveur.bind(servadress)

while True:  # ouvre les Threads pour chaque client
    sockserveur.listen(30)
    print("en attente de connexion")
    (connexion, (adresse_client, port)) = sockserveur.accept()
    newThread = ListenClient(adresse_client, port, connexion)
    newThread.start()

    del newThread  # le supprime a la fin
