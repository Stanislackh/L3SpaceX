import socket, random, sys
from threading import Thread


class ListenClient(Thread):
    listJoueur = {}
    listRessource = {}
    etatPlayer = {}
    carte = []

    def __init__(self, ip, port, clientSo):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientSo = clientSo
        self.map2Player = ""

    def CreerCarte(self):
        for i in range(1, 11):
            for j in range(1, 10):
                ress = random.randint(1, 100)
                if ress >= 90:
                    ListenClient.carte.append(1)
                else:
                    ListenClient.carte.append(0)
        for k in range(1, 11):
            ress = random.randint(1, 100)
            if ress >= 90:
                ListenClient.carte.append(1)
            else:
                ListenClient.carte.append(0)

    def DepotJoueur(self, x, y, name):
        x = x
        y = y
        cour = 0
        cour2 = 0
        while cour < ((x - 1) * 10):
            cour += 1
        while cour2 < y - 1:
            cour2 += 1
        if ListenClient.carte[cour + cour2] == 1:
            ListenClient.listRessource[name] += 1
        ListenClient.carte[cour + cour2] = name

    def ConvertMap2Player(self):
        self.map2Player = ""

        compt = 1

        for i in ListenClient.carte:
            if compt % 10 != 0:
                if i == 0 or i == 1:
                    self.map2Player += "0,"
                else:
                    self.map2Player += i + ","
            else:
                if compt != 100:
                    if i == 0 or i == 1:
                        self.map2Player += "0:"
                    else:
                        self.map2Player += i + ":"
                else:
                    if i == 0 or i == 1:
                        self.map2Player += "0"
                    else:
                        self.map2Player += i
            compt += 1

    def run(self):
        try:
            print("connexion from " + self.ip)
            while True:
                data = self.clientSo.recv(1024)
                if data:
                    data = data.decode()
                    com = data.split(" ")
                    if com[0] == "CONNECT":

                        """réponse a la commande CONNECT"""

                        if len(com) == 2:
                            if len(com[1]) < 3 or len(com[1]) > 10:
                                reponse = "211"
                            elif adresse_client in ListenClient.listJoueur:
                                reponse = "200"
                            elif com[1] in ListenClient.listJoueur.values():
                                reponse = "202"
                            else:
                                ListenClient.listJoueur[adresse_client] = com[1]
                                ListenClient.listRessource[com[1]] = 0
                                ListenClient.etatPlayer[adresse_client] = "play"
                                ListenClient.ConvertMap2Player(self)
                                reponse = "103 " + self.map2Player
                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "SETROBOT":

                        """réponse a la commande SETROBOT"""

                        if len(com) == 3:
                            if not adresse_client in ListenClient.listJoueur:
                                reponse = "201"
                            elif ListenClient.listJoueur[adresse_client] in ListenClient.carte:
                                reponse = "215"
                            elif int(com[1]) < 1 or int(com[1]) > 10 or int(com[2]) < 1 or int(com[2]) > 10:
                                reponse = "209"
                            elif ListenClient.carte[(int(com[1]) - 1) * 10 + int(com[2]) - 1] != 0 and \
                                    ListenClient.carte[(int(com[1]) - 1) * 10 + int(com[2]) - 1] != 1:
                                reponse = "214"
                            else:
                                ListenClient.DepotJoueur(self, int(com[1]), int(com[2]),
                                                         ListenClient.listJoueur[adresse_client])
                                ListenClient.ConvertMap2Player(self)
                                reponse = "100 " + self.map2Player

                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    # a tester
                    elif com[0] == "MOVE":

                        """réponse a la commande MOVE"""

                        if len(com) == 3:
                            if not adresse_client in ListenClient.listJoueur:
                                reponse = "201"
                            elif ListenClient.listJoueur[adresse_client] not in ListenClient.carte:
                                reponse = "214"
                            elif int(com[1]) < 1 or int(com[1]) > 10 or int(com[2]) < 1 or int(com[2]) > 10:
                                reponse = "209"
                            elif ListenClient.carte[(int(com[1]) - 1) * 10 + int(com[2]) - 1] != 0 and \
                                    ListenClient.carte[(int(com[1]) - 1) * 10 + int(com[2]) - 1] != 1:
                                reponse = "214"
                            elif ListenClient.etatPlayer[adresse_client] == "pause":
                                reponse = "212"
                            else:
                                val = 0
                                for i in ListenClient.carte:
                                    if i == ListenClient.listJoueur[adresse_client]:
                                        break
                                    val += 1
                                if val == ListenClient.listJoueur[adresse_client]:
                                    reponse = "209"
                                else:
                                    ListenClient.carte[val] = 0
                                    ListenClient.DepotJoueur(self, int(com[1]), int(com[2]),
                                                             ListenClient.listJoueur[adresse_client])
                                    ListenClient.ConvertMap2Player(self)
                                    reponse = "105 " + self.map2Player

                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "GETALL":

                        """réponse a la commande GETALL"""

                        if not adresse_client in ListenClient.listJoueur:
                            reponse = "201"
                        else:
                            reponse = "101 "
                            for cle, valeur in ListenClient.listRessource.items():
                                reponse += cle + ":" + str(valeur) + ","
                                reponse = reponse[:-1]

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "CHANGEPSEUDO":

                        """réponse a la commande CHANGEPSEUDO"""

                        if len(com) == 2:
                            if len(com[1]) < 3 or len(com[1]) > 10:
                                reponse = "211"
                            elif com[1] in ListenClient.listJoueur.values():
                                reponse = "202"
                            else:
                                val = ListenClient.listRessource.pop(ListenClient.listJoueur[adresse_client])
                                ListenClient.listJoueur[adresse_client] = com[1]
                                ListenClient.listRessource[com[1]] = val
                                reponse = "100"
                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    # a tester
                    elif com[0] == "RECEIVEDATAROBOT":

                        """réponse a la commande RECEIVEDATAROBOT"""

                        ...

                    # a tester
                    elif com[0] == "ACCEPTREQUESTDATA":

                        """réponse a la commande ACCEPTREQUESTDATA"""

                        ...

                    # a tester
                    elif com[0] == "PRIVATEMESS":

                        """réponse a la commande PRIVATEMESS"""

                        if len(com) == 3:
                            if com[1] in ListenClient.listJoueur.values():
                                reponse = com[2]
                                for nono in ListenClient.listJoueur:
                                    if ListenClient.listJoueur[nono] == com[1]:
                                        reponse = reponse.encode()
                                        # nono.send(reponse)
                                reponse = "100"
                            elif com[1] not in ListenClient.listJoueur.values():
                                reponse = "204"
                            elif com[2] == "":
                                reponse = "207"
                            elif not adresse_client in ListenClient.listJoueur:
                                reponse = "201"
                            else:
                                reponse = "208"

                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "PAUSE":

                        """réponse a la commande PAUSE"""

                        if self.etatPlayer[adresse_client] == "pause":
                            reponse = "212"
                        elif self.listJoueur[adresse_client] not in self.carte:
                            reponse = "214"
                        else:
                            self.etatPlayer[adresse_client] = "pause"
                            reponse = "100"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "ENDPAUSE":

                        """réponse a la commande ENDPAUSE"""

                        if self.etatPlayer[adresse_client] == "play":
                            reponse = "205"
                        elif self.listJoueur[adresse_client] not in self.carte:
                            reponse = "214"
                        else:
                            self.etatPlayer[adresse_client] = "play"
                            reponse = "100"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    # a tester
                    elif com[0] == "QUIT":

                        """réponse a la commande QUIT"""

                        if adresse_client not in ListenClient.listJoueur:
                            reponse = "201"
                            reponse = reponse.encode()
                            self.clientSo.send(reponse)
                        else:
                            reponse = "100"
                            reponse = reponse.encode()
                            self.clientSo.send(reponse)
                            reponse = ListenClient.listJoueur[adresse_client] + "s'est déconecter"
                            reponse = reponse.encode()
                            del ListenClient.listRessource[ListenClient.listJoueur.get(adresse_client)]
                            del ListenClient.listJoueur[adresse_client]
                            del ListenClient.etatPlayer[adresse_client]
                            for nono in ListenClient.listJoueur:
                                # nono.send(reponse)
                                pass
                            break
                    else:

                        """réponse a une commande non existante"""

                        reponse = "298"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)
                else:
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
    newThread.CreerCarte()
    newThread.start()

    del newThread
