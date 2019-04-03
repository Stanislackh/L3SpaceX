import socket
from threading import Thread


class ListenClient(Thread):
    def __init__(self, ip, port, clientSo):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientSo = clientSo
        self.listJoueur = {}
        self.listRessource = {}
        self.etatPlayer = {}
        self.carte = []
        self.map2Player = ""

    def CreerCarte(self):
        for i in range(1, 11):
            for j in range(1, 10):
                self.carte.append(0)
        for k in range(1, 11):
            self.carte.append(0)

    def DepotJoueur(self, x, y):
        x = x
        y = y
        cour = 0
        cour2 = 0
        while cour < ((x - 1) * 10):
            cour += 1
        while cour2 < y - 1:
            cour2 += 1
        self.carte[cour + cour2] = 1

    def ConvertMap2Player(self):
        map2Player = ""

        compt = 1

        for i in self.carte:
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

    def run(self):
        try:
            print("connexion from " + self.ip)
            while True:
                data = self.clientSo.recv(1024)
                print(data)
                if data:
                    data = data.decode()
                    print(data)
                    com = data.split(" ")
                    print(com)
                    if com[0] == "CONNECT":

                        """réponse a la commande CONNECT"""

                        if com[1]:
                            if len(com[1]) < 3 or len(com[1]) > 10:
                                reponse = "211"
                            elif adresse_client in self.listJoueur:
                                reponse = "200"
                            elif com[1] in self.listJoueur.values():
                                reponse = "202"
                            else:
                                self.listJoueur[adresse_client] = com[1]
                                self.listRessource[com[1]] = 0
                                self.etatPlayer[adresse_client] = "play"
                                print(self.listJoueur)
                                print(self.listRessource)
                                print(self.etatPlayer)
                                ListenClient.ConvertMap2Player(self)
                                reponse = "103 " + self.map2Player
                        else:
                            reponse = "297"

                    elif com[0] == "SETROBOT":

                        """réponse a la commande SETROBOT"""

                        if com[1] and com[2]:
                            print(self.listJoueur)
                            print(self.listRessource)
                            print(self.etatPlayer)
                            if not adresse_client in self.listJoueur:
                                reponse = "201"
                            elif (adresse_client in self.listJoueur.values()) in self.carte:
                                reponse = "215"
                            elif com[1] < 1 or com[1] > 10 or com[2] < 1 or com[2] > 10:
                                reponse = "209"
                            elif self.carte[com[1] * 10 + com[2] - 1] != 0:
                                reponse = "214"
                            else:
                                ListenClient.DepotJoueur(com[1], com[2])
                                ListenClient.ConvertMap2Player()
                                reponse = "100 " + self.map2Player

                        else:
                            reponse = "297"

                    elif com[0] == "MOVE":

                        """réponse a la commande MOVE"""

                        if com[1] and com[2]:
                            if not adresse_client in self.listJoueur:
                                reponse = "201"
                            elif self.listJoueur.values(adresse_client) in self.carte:
                                reponse = "215"
                            elif com[1] < 1 or com[1] > 10 or com[2] < 1 or com[2] > 10:
                                reponse = "209"
                            elif self.carte[com[1] * 10 + com[2] - 1] != 0:
                                reponse = "214"
                            elif self.etatPlayer[adresse_client] == "pause":
                                reponse = "212"
                            # elif case pas a coté:
                            else:
                                # deplacer le robot
                                reponse = "105 " + self.map2Player

                        else:
                            reponse = "297"

                    elif com[0] == "GETALL":

                        """réponse a la commande GETALL"""

                        if not adresse_client in self.listJoueur:
                            reponse = "201"
                        else:
                            reponse = "101 "
                            for cle, valeur in self.listRessource.items():
                                reponse += cle + ":" + valeur + ","
                                reponse = reponse[:-1]

                    elif com[0] == "CHANGEPSEUDO":

                        """réponse a la commande CHANGEPSEUDO"""

                        if com[1]:
                            if len(com[1]) < 3 or len(com[1]) > 10:
                                reponse = "211"
                            elif not com[1] in self.listJoueur.values():
                                reponse = "202"
                            else:
                                val = self.listRessource.pop(self.listJoueur[adresse_client])
                                self.listJoueur[adresse_client] = com[1]
                                self.listRessource[com[1]] = val
                                reponse = "100"
                        else:
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

                        if self.etatPlayer[adresse_client] == "pause":
                            reponse = "212"
                        elif self.listJoueur.values(adresse_client) not in self.carte:
                            reponse = "214"
                        else:
                            self.etatPlayer[adresse_client] = "pause"
                            reponse = "100"

                    elif com[0] == "ENDPAUSE":

                        """réponse a la commande ENDPAUSE"""

                        if self.etatPlayer[adresse_client] == "play":
                            reponse = "205"
                        elif self.listJoueur.values(adresse_client) not in self.carte:
                            reponse = "214"
                        else:
                            self.etatPlayer[adresse_client] = "play"
                            reponse = "100"

                    elif com[0] == "QUIT":

                        """réponse a la commande QUIT"""

                        if adresse_client not in self.listJoueur:
                            reponse = "201"
                        else:
                            del self.listRessource[self.listJoueur.get(adresse_client)]
                            del self.listJoueur[adresse_client]
                            del self.etatPlayer[adresse_client]
                            self.clientSo.close()
                            # envoie a tous qu'un joueur s'est déconecter

                    else:

                        """réponse a une commande non existante"""

                        reponse = "298"

                reponse = reponse.encode()
                self.clientSo.send(reponse)

        finally:
            self.clientSo.close()


sockserveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockserveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servadress = ("localhost", 3000)
sockserveur.bind(servadress)
while True:
    sockserveur.listen(30)
    print("en attente de connexion")
    (connexion, (adresse_client, port)) = sockserveur.accept()
    newThread = ListenClient(adresse_client, port, connexion)
    newThread.start()
