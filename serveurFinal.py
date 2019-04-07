# -- coding: utf-8 --

import socket, random
from threading import Thread

listJoueur = {}
listRessource = {}
etatPlayer = {}
carte = []
pourRepondre = {}
memRep = {}
coord = {}


def CreerCarte():
    for i in range(1, 11):
        for j in range(1, 10):
            ress = random.randint(1, 100)
            if ress >= 90:
                carte.append(1)
            else:
                carte.append(0)
    for k in range(1, 11):
        ress = random.randint(1, 100)
        if ress >= 90:
            carte.append(1)
        else:
            carte.append(0)


CreerCarte()


class ListenClient(Thread):

    def __init__(self, ip, port, clientSo):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientSo = clientSo
        self.map2Player = ""

    def DepotJoueur(self, x, y, name):
        x = x
        y = y
        cour = 0
        cour2 = 0
        while cour < ((x - 1) * 10):
            cour += 1
        while cour2 < y - 1:
            cour2 += 1
        if carte[cour + cour2] == 1:
            listRessource[name] += 1
        carte[cour + cour2] = name

    def ConvertMap2Player(self):
        self.map2Player = ""

        compt = 1

        for i in carte:
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
            print(self.clientSo)
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
                            elif self.clientSo in listJoueur:
                                reponse = "200"
                            elif com[1] in listJoueur.values():
                                reponse = "202"
                            else:
                                listJoueur[self.clientSo] = com[1]
                                listRessource[com[1]] = 0
                                etatPlayer[self.clientSo] = "play"
                                pourRepondre[self.clientSo] = self.clientSo
                                ListenClient.ConvertMap2Player(self)
                                reponse = "103 " + self.map2Player
                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "SETROBOT":

                        """réponse a la commande SETROBOT"""

                        if len(com) == 3:
                            if not self.clientSo in listJoueur:
                                reponse = "201"
                            elif listJoueur[self.clientSo] in carte:
                                reponse = "215"
                            elif int(com[1]) < 1 or int(com[1]) > 10 or int(com[2]) < 1 or int(com[2]) > 10:
                                reponse = "209"
                            elif carte[(int(com[1]) - 1) * 10 + int(com[2]) - 1] != 0 and \
                                    carte[(int(com[1]) - 1) * 10 + int(com[2]) - 1] != 1:
                                reponse = "214"
                            else:
                                ListenClient.DepotJoueur(self, int(com[1]), int(com[2]),
                                                         listJoueur[self.clientSo])
                                ListenClient.ConvertMap2Player(self)
                                reponse = "100 " + self.map2Player
                                coord[self.clientSo] = (int(com[1]), int(com[2]))

                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    # a tester / finir (regarder si il se déplace d'une case)
                    elif com[0] == "MOVE":

                        """réponse a la commande MOVE"""

                        if len(com) == 3:
                            if not self.clientSo in listJoueur:
                                reponse = "201"
                            elif listJoueur[self.clientSo] not in carte:
                                reponse = "214"
                            elif int(com[1]) < 1 or int(com[1]) > 10 or int(com[2]) < 1 or int(com[2]) > 10:
                                reponse = "209"
                            elif carte[(int(com[1]) - 1) * 10 + int(com[2]) - 1] != 0 and \
                                    carte[(int(com[1]) - 1) * 10 + int(com[2]) - 1] != 1:
                                reponse = "214"
                            elif etatPlayer[self.clientSo] == "pause":
                                reponse = "212"
                            elif coord[self.clientSo][0] in [int(com[1])-1, int(com[1]), int(com[1])+1] and coord[self.clientSo][1] in [int(com[2])-1, int(com[2]), int(com[2])+1] and coord[self.clientSo] != (int(com[1]),int(com[2])):
                                val = 0
                                for i in carte:
                                    if i == listJoueur[self.clientSo]:
                                        break
                                    val += 1
                                carte[val] = 0
                                ListenClient.DepotJoueur(self, int(com[1]), int(com[2]),
                                                         listJoueur[self.clientSo])
                                ListenClient.ConvertMap2Player(self)
                                coord[self.clientSo] = (int(com[1]), int(com[2]))
                                reponse = "105 " + self.map2Player
                            else:
                                reponse = "209"

                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "GETALL":

                        """réponse a la commande GETALL"""

                        if not self.clientSo in listJoueur:
                            reponse = "201"
                        else:
                            reponse = "101 "
                            for cle, valeur in listRessource.items():
                                reponse += cle + ":" + str(valeur) + ","
                                reponse = reponse[:-1]

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "CHANGEPSEUDO":

                        """réponse a la commande CHANGEPSEUDO"""

                        if len(com) == 2:
                            if len(com[1]) < 3 or len(com[1]) > 10:
                                reponse = "211"
                            elif com[1] in listJoueur.values():
                                reponse = "202"
                            else:
                                val = listRessource.pop(listJoueur[self.clientSo])
                                val2 = pourRepondre.pop(self.clientSo)
                                listJoueur[self.clientSo] = com[1]
                                listRessource[com[1]] = val
                                pourRepondre[self.clientSo] = val2
                                reponse = "100"
                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    # a tester
                    elif com[0] == "RECEIVEDATAROBOT":

                        """réponse a la commande RECEIVEDATAROBOT"""

                        if len(com) == 2:
                            if com[1] in listJoueur.values():
                                for nono in listJoueur:
                                    if listJoueur[nono] == com[1]:
                                        reponse = "104" + self.ip + self.port
                                        reponse = reponse.encode()
                                        pourRepondre[nono].send(reponse)
                                        memRep[com[1]] = listJoueur[self.clientSo]
                                    reponse = "100"
                            elif com[1] not in listJoueur.values():
                                reponse = "204"
                            elif not self.clientSo in listJoueur:
                                reponse = "201"
                            elif com[1] not in carte:
                                reponse = "206"
                            else:
                                reponse = "208"
                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    # a tester
                    elif com[0] == "ACCEPTREQUESTDATA":

                        """réponse a la commande ACCEPTREQUESTDATA"""

                        if len(com) == 2:
                            if memRep[listJoueur[self.clientSo]] not in listJoueur.values():
                                reponse = "204"
                            elif not self.clientSo in listJoueur:
                                reponse = "201"
                            elif memRep[listJoueur[self.clientSo]] not in carte:
                                reponse = "206"
                            elif memRep[listJoueur[self.clientSo]] in listJoueur.values():
                                for cle, valeur in memRep.items():
                                    if valeur == listJoueur[self.clientSo]:
                                        for cle2, valeur2 in listJoueur.items():
                                            if valeur2 == cle:
                                                reponse = "10" + com[1]
                                                reponse = reponse.encode()
                                                pourRepondre[cle2].send(reponse)
                                                break
                                del memRep[listJoueur[cle2]]
                                reponse = "100"
                            else:
                                reponse = "208"
                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    # a tester
                    elif com[0] == "PRIVATEMESS":

                        """réponse a la commande PRIVATEMESS"""

                        if len(com) >= 3:
                            if com[1] in listJoueur.values():
                                i = 2
                                rep = ""
                                while len(com) > i:
                                    rep += com[i] + " "
                                    i += 1
                                rep = rep[:-1]
                                reponse = "102" + rep
                                for nono in listJoueur:
                                    if listJoueur[nono] == com[1]:
                                        reponse = reponse.encode()
                                        pourRepondre[nono].send(reponse)
                                reponse = "100"
                            elif com[1] not in listJoueur.values():
                                reponse = "204"
                            elif com[2] == "":
                                reponse = "207"
                            elif not self.clientSo in listJoueur:
                                reponse = "201"
                            else:
                                reponse = "208"

                        else:
                            reponse = "297"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "PAUSE":

                        """réponse a la commande PAUSE"""

                        if etatPlayer[self.clientSo] == "pause":
                            reponse = "212"
                        elif listJoueur[self.clientSo] not in carte:
                            reponse = "214"
                        else:
                            etatPlayer[self.clientSo] = "pause"
                            reponse = "100"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    elif com[0] == "ENDPAUSE":

                        """réponse a la commande ENDPAUSE"""

                        if etatPlayer[self.clientSo] == "play":
                            reponse = "205"
                        elif listJoueur[self.clientSo] not in carte:
                            reponse = "214"
                        else:
                            etatPlayer[self.clientSo] = "play"
                            reponse = "100"

                        reponse = reponse.encode()
                        self.clientSo.send(reponse)

                    # a tester (envoie de message a d'autre client)
                    elif com[0] == "QUIT":

                        """réponse a la commande QUIT"""

                        if self.clientSo not in listJoueur:
                            reponse = "201"
                            reponse = reponse.encode()
                            self.clientSo.send(reponse)
                        else:
                            reponse = "100"
                            reponse = reponse.encode()
                            self.clientSo.send(reponse)
                            reponse = listJoueur[self.clientSo] + "s'est déconecter"
                            reponse = reponse.encode()
                            val = 0
                            if listJoueur[self.clientSo] in carte:
                                for i in carte:
                                    if i == listJoueur[self.clientSo]:
                                        break
                                    val += 1
                                carte[val] = 0
                            del listRessource[listJoueur.get(self.clientSo)]
                            del listJoueur[self.clientSo]
                            del etatPlayer[self.clientSo]
                            del pourRepondre[self.clientSo]
                            del coord[self.clientSo]
                            for nono in listJoueur:
                                pourRepondre[nono].send(reponse)
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
    newThread.start()

    del newThread
