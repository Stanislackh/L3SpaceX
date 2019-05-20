# -- coding: utf-8 --
"""Interface pour le Client SpaceX en TKinter"""

# Created by Slackh
# Github : https://github.com/Stanislackh

from tkinter import *
from tkinter import messagebox
import pygame, pygame.midi  # Import du module pour le son
import clientSlackhInterface  # importe le client


# Centre la fenetre
def geoliste(g):
    r = [i for i in range(0, len(g)) if not g[i].isdigit()]
    return [int(g[0:r[0]]), int(g[r[0] + 1:r[1]]), int(g[r[1] + 1:r[2]]), int(g[r[2] + 1:])]


def centrefenetre(fen):
    fen.update_idletasks()
    l, h, x, y = geoliste(fen.geometry())
    fen.geometry("%dx%d%+d%+d" % (l, h, (fen.winfo_screenwidth() - l) // 2, (fen.winfo_screenheight() - h) // 2))


# Lance une musique pour le client
pygame.init()
pygame.mixer.music.load("music/Moon.mid")

"""Liste des commandes serveur"""


# CONNECT
def connect():
    clientSlackhInterface.lancementClient()
    clientSlackhInterface.message = "CONNECT " + pseudoClient
    print(clientSlackhInterface.message)

    # Envoi de la commande au serveur
    clientSlackhInterface.client.send(clientSlackhInterface.message.encode())  # Envoie la commande au serveur
    data = clientSlackhInterface.client.recv(clientSlackhInterface.BUFFER_SIZE)
    clientSlackhInterface.afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus
    if clientSlackhInterface.codeReponse == "103":  # Lance la fenetre suiveante si le code de retour est valide
        mainGame()
    elif clientSlackhInterface.tableauReponse[0] == "202":
        messagebox.showinfo("Pseudo erreur", pseudoClient + " : Nom déjà pris")
    else:
        pass


# SETROBOT
def setRobot():
    clientSlackhInterface.message = "SETROBOT " + str(posX) + " " + str(posY)
    print(clientSlackhInterface.message)

    # Envoi de la commande au serveur
    clientSlackhInterface.client.send(clientSlackhInterface.message.encode())  # Envoie la commande au serveur
    data = clientSlackhInterface.client.recv(clientSlackhInterface.BUFFER_SIZE)
    clientSlackhInterface.afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus
    poseRobot()  # Colorie la place initiale du robot


# MOVE
def move():
    clientSlackhInterface.message = "MOVE " + str(X) + " " + str(Y)
    print(clientSlackhInterface.message)

    # Envoi de la commande au serveur
    clientSlackhInterface.client.send(clientSlackhInterface.message.encode())  # Envoie la commande au serveur
    data = clientSlackhInterface.client.recv(clientSlackhInterface.BUFFER_SIZE)
    clientSlackhInterface.afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus
    majCarte()  # Envoi le nouvel état de la map après déplacement


# GETALL
def getAll():
    clientSlackhInterface.message = "GETALL"
    print(clientSlackhInterface.message)

    # Envoi de la commande au serveur
    clientSlackhInterface.client.send(clientSlackhInterface.message.encode())  # Envoie la commande au serveur
    data = clientSlackhInterface.client.recv(clientSlackhInterface.BUFFER_SIZE)
    clientSlackhInterface.afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus


# CHANGEPSEUDO
def changePseudo1():
    clientSlackhInterface.message = "CHANGEPSEUDO " + pseudoClient1
    print(clientSlackhInterface.message)

    # Envoi de la commande au serveur
    clientSlackhInterface.client.send(clientSlackhInterface.message.encode())  # Envoie la commande au serveur
    data = clientSlackhInterface.client.recv(clientSlackhInterface.BUFFER_SIZE)
    clientSlackhInterface.afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus
    if clientSlackhInterface.tableauReponse[0] == "100":
        messagebox.showinfo("Pseudo changé", "Pseudo changé en : " + pseudoClient1)
    if clientSlackhInterface.tableauReponse[0] == "202":
        messagebox.showinfo("Pseudo erreur", pseudoClient1 + " : Nom déjà pris")

# RECEIVEDATAROBOT
# ACCEPTREQUESTDATA

# PRIVATEMESS
def privateMessage():
    clientSlackhInterface.message = "PRIVATEMESS " + name + " " + chat
    print(clientSlackhInterface.message)

    # Envoi de la commande au serveur
    clientSlackhInterface.client.send(clientSlackhInterface.message.encode())  # Envoie la commande au serveur
    data = clientSlackhInterface.client.recv(clientSlackhInterface.BUFFER_SIZE)
    clientSlackhInterface.afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus


# PAUSE
def pause():
    clientSlackhInterface.message = "PAUSE"
    print(clientSlackhInterface.message)

    # Envoi de la commande au serveur
    clientSlackhInterface.client.send(clientSlackhInterface.message.encode())  # Envoie la commande au serveur
    data = clientSlackhInterface.client.recv(clientSlackhInterface.BUFFER_SIZE)
    clientSlackhInterface.afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus
    messagebox.showinfo("Mise en pause", "Robot en pause")

# ENDPAUSE
def endPause():
    clientSlackhInterface.message = "ENDPAUSE"
    print(clientSlackhInterface.message)

    # Envoi de la commande au serveur
    clientSlackhInterface.client.send(clientSlackhInterface.message.encode())  # Envoie la commande au serveur
    data = clientSlackhInterface.client.recv(clientSlackhInterface.BUFFER_SIZE)
    clientSlackhInterface.afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus
    messagebox.showinfo("Fin de pause", "Fin de la pause Robot")

# QUIT
def quit():
    clientSlackhInterface.message = "QUIT"
    print(clientSlackhInterface.message)

    # Envoi de la commande au serveur
    clientSlackhInterface.client.send(clientSlackhInterface.message.encode())  # Envoie la commande au serveur
    data = clientSlackhInterface.client.recv(clientSlackhInterface.BUFFER_SIZE)
    clientSlackhInterface.afficheLaReponse(data)  # Fait appel à la fonction qui permet de regarder les codes reçus


# HELP
def Chelp():
    # Affiche le fenêtre d'aide
    fenHelp = Tk()
    fenHelp.geometry("500x500")
    centrefenetre(fenHelp)
    fenHelp.title("HELP")

    titre = Label(fenHelp, text="Liste des commandes")
    titre.grid(column=1, row=0)

    h1 = Label(fenHelp,
               text="CONNECT <pseudo> => Permet de se connecter avec le pseudo spécifié et recevoir une copie de la carte")
    h1.grid(column=0, row=1)

    h1 = Label(fenHelp,
               text="SETROBOT <x> <y> => Pour positionner votre robot aux coordonnées x y avec x pour abscisse et y pour ordonnée")
    h1.grid(column=0, row=2)

    h1 = Label(fenHelp,
               text="MOVE <x> <y> => Permet de déplacer le robot à la coordonnée x y avec x pour abscisse et y pour ordonnée")
    h1.grid(column=0, row=3)

    h1 = Label(fenHelp, text="GETALL => Pour recevoir la liste des personnes connectées avec leurs ressources")
    h1.grid(column=0, row=4)

    h1 = Label(fenHelp, text="CHANGEPSEUDO <pseudo> => Permet de changer l'ancien pseudo par le nouveau")
    h1.grid(column=0, row=5)

    h1 = Label(fenHelp, text="RECEIVEDATAROBOT <pseudo> => Renvoi la stratégie de pseudo si il accepte")
    h1.grid(column=0, row=6)

    h1 = Label(fenHelp,
               text="ACCEPTREQUESTDATA <port> => Si vous recevez une RECEIVEDATAROBOT renvoyez cette commmande "
                    "avec le numéro de port pour établir une connexion avec celui qui vous a envoyé la requête")
    h1.grid(column=0, row=7)

    h1 = Label(fenHelp, text="PRIVATEMESS <pseudo> => Envoie un message à pseudo")
    h1.grid(column=0, row=8)

    h1 = Label(fenHelp, text="PAUSE => Mets le robot en pause")
    h1.grid(column=0, row=9)

    h1 = Label(fenHelp, text="ENDPAUSE => Après la mise en pause remet le robot en fonction")
    h1.grid(column=0, row=10)

    h1 = Label(fenHelp, text="QUIT => Pour quitter l'application")
    h1.grid(column=0, row=11)


# Création de la Grille
def grille():
    global terrain
    global carreau

    fen = Toplevel()  # Création de la fenetre grille
    fen.geometry("500x500")
    fen.title("Slackh's SpaceX Grid")

    terrain = Canvas(fen, height=500, width=500)  # Taille de la grille
    terrain.pack()

    carreau = [[terrain.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill="#FFFFFF")
                for i in range(10)] for j in range(10)]  # Génération des carreaux de la grille

    Coord = Label(fen)
    Coord.pack(pady='10px')


# Mets à jour les canvas avec le retour du serveur
def majCarte():
    # Colorie la case où le joueur est passé
    if clientSlackhInterface.tableauReponse[0] == "105":
        terrain.itemconfigure(carreau[X][Y], fill='#FF5B2A')
    if clientSlackhInterface.tableauReponse[0] == "209":
        terrain.itemconfigure(carreau[X][Y], fill='#AAAAAA')
        messagebox.showinfo("Déplacement impossible", "Un autre robot utilise cette case")


# Colorie la case a la pose du robot
def poseRobot():
    if clientSlackhInterface.tableauReponse[0] == "209":
        terrain.itemconfigure(carreau[posX][posY], fill='#AAAAAA')
        messagebox.showinfo("Déplacement impossible",
                            "Un autre robot utilise cette case, ou le déplacement est non autorisé")
    if clientSlackhInterface.tableauReponse[0] == "105":
        terrain.itemconfigure(carreau[posX][posY], fill='#FF5FFF')


# Essaye de faire correspondre la map serveur et graphique (Désolé j'ai plus d'idée pour les noms)
def depression():
    res = []
    res2 = []

    mop = clientSlackhInterface.map.split("\n")  # Stocke la map dans une liste en supprimant les \n

    for i in mop:  # Parcours la map envoyée par le client apres supprésion des \n
        res.append(i.split(":"))
        for j in res:  # Parcours res
            for k in j:  # Parcours les valeurs de res
                res2.append(k.split(","))

    res2.pop()  # Supprime le \n
    # print(res2)
    return res2

# Affiche le nombre de ressources par joueur
def afficheRessources():
    messagebox.showinfo("Affiche Ressources", clientSlackhInterface.messageRes)


"""Fenêtre principale et de commandes serveur"""


def connexionServeur():
    # Fenetre avec les commandes serveur
    global fen2

    fen2 = Tk()
    fen2.geometry("500x500")
    centrefenetre(fen2)
    fen2.title("Slackh's SpaceX Client")

    # Recuperation pseudo
    def recup():
        global pseudoClient
        pseudoClient = pseudo.get()

    titre = Label(fen2, text="Connexion au serveur")
    titre.pack()

    # Bouton pour la connexion serveur
    pseudo = Label(fen2, text="Entrez votre pseudo : ")
    pseudo.pack()

    pseudo = Entry(fen2, textvariable="")  # Entrée clavier
    pseudo.pack()

    # Image de Présentation
    Can1 = Canvas(fen2, width=300, height=300)
    photo = PhotoImage(file='images/Space2.gif')
    item = Can1.create_image(150, 150, image=photo)
    Can1.pack()

    # Valider les modifications
    boutonConnect = Button(fen2, text="Connect", command=lambda: [recup(), connect()],
                           width=15, height=5)
    boutonConnect.pack(side=LEFT, padx=5, pady=1)

    # Lancer la musique
    boutonPlay = Button(fen2, text="Music On", command=pygame.mixer.music.play, width=15, height=5)
    boutonPlay.pack(side=LEFT, padx=5, pady=1)

    # Quitter SpaceX
    boutonRetour = Button(fen2, text="Quit", command=lambda: [fen2.destroy()], width=15, height=5)
    boutonRetour.pack(side=RIGHT, padx=5, pady=1)

    # Couper la musique
    boutonStop = Button(fen2, text="Music Off", command=pygame.mixer.music.stop, width=15, height=5)
    boutonStop.pack(side=RIGHT, padx=5, pady=1)

    fen2.mainloop()


# Fenêtre principale pour les envois de commandes
def mainGame():
    # Fermer la fenetre d'acceuil
    if clientSlackhInterface.codeReponse == "103":
        fen2.destroy()

    fen3 = Tk()
    fen3.geometry("500x500")
    centrefenetre(fen3)
    fen3.title("Slackh's SpaceX Client")

    grid = grille()  # Affiche la grille
    grid

    # SETROBOT
    def recupCoord():
        global posX
        global posY
        posX = int(positionX.get())
        posY = int(positionY.get())

    titre = Label(fen3, text="Positionner le robot")
    titre.grid(column=1, row=0)

    positionX = Label(fen3, text="Coord X")
    positionX.grid(column=0, row=1)
    positionX = Entry(fen3, textvariable="")  # Entrée clavier
    positionX.grid(column=0, row=2)

    positionY = Label(fen3, text="Coord Y: ")
    positionY.grid(column=1, row=1)
    positionY = Entry(fen3, textvariable="")  # Entrée clavier
    positionY.grid(column=1, row=2)

    # Bouton envoi SETROBOT au serveur
    buttonSetrobot = Button(fen3, text="SETROBOT", command=lambda: [recupCoord(), setRobot()])
    buttonSetrobot.grid(column=2, row=2)

    # GETALL
    buttonGetall = Label(fen3, text="Avoir tous les clients et ressources")
    buttonGetall.grid(column=0, row=3)
    buttonGetall = Button(fen3, text="GETALL", command=lambda: [getAll(), afficheRessources()])
    buttonGetall.grid(column=2, row=3)

    # CHANGEPSEUDO
    def recupPseudo():
        global pseudoClient1
        pseudoClient1 = changePseudo.get()

    changePseudo = Label(fen3, text="Changer de nom")
    changePseudo.grid(column=0, row=4)
    changePseudo = Entry(fen3, textvariable="")  # Entrée clavier
    changePseudo.grid(column=1, row=4)

    buttonChangepseudo = Button(fen3, text="CHANGEPSEUDO", command=lambda: [recupPseudo(), changePseudo1()])
    buttonChangepseudo.grid(column=2, row=4)

    # PAUSE
    buttonPause = Label(fen3, text="Mets en pause le robot")
    buttonPause.grid(column=0, row=5)
    buttonPause = Button(fen3, text="PAUSE", command=lambda: [pause()])
    buttonPause.grid(column=2, row=5)

    # ENDPAUSE
    buttonEndpause = Label(fen3, text="Enleve la pause du robot")
    buttonEndpause.grid(column=0, row=6)
    buttonEndpause = Button(fen3, text=" ENDPAUSE", command=lambda: [endPause()])
    buttonEndpause.grid(column=2, row=6)

    # HELP
    buttonHelp = Label(fen3, text="Afficher l'aide")
    buttonHelp.grid(column=0, row=7)
    buttonHelp = Button(fen3, text="HELP", command=lambda: [Chelp()])
    buttonHelp.grid(column=2, row=7)

    # PRIVATEMESS
    def recupChat():
        global name
        global chat
        name = pseudo.get()
        chat = text.get()

    pseudo = Label(fen3, text="Envoyer message à :")
    pseudo.grid(column=0, row=8)
    pseudo = Entry(fen3, textvariable="")  # Entrée clavier
    pseudo.grid(column=0, row=9)

    text = Label(fen3, text="Tapez votre message")
    text.grid(column=1, row=8)
    text = Entry(fen3, textvariable="")  # Entrée clavier
    text.grid(column=1, row=9)

    # Bouton envoi PRIVATEMESS au serveur
    buttonPrivatemess = Button(fen3, text="PRIVATEMESS", command=lambda: [recupChat(), privateMessage()])
    buttonPrivatemess.grid(column=2, row=9)

    # QUIT
    buttonQuit = Label(fen3, text="Quitter l'application")
    buttonQuit.grid(column=0, row=10)
    buttonQuit = Button(fen3, text="QUIT", command=lambda: [quit(), fen3.destroy()])
    buttonQuit.grid(column=2, row=10)

    # MOVE

    def recupMove():
        global X
        global Y
        X = int(moveX.get())
        Y = int(moveY.get())

    moveX = Label(fen3, text="Bouger en X")
    moveX.grid(column=0, row=11)
    moveX = Entry(fen3, textvariable="")  # Entrée clavier
    moveX.grid(column=0, row=12)

    moveY = Label(fen3, text="Bouger en Y")
    moveY.grid(column=1, row=11)
    moveY = Entry(fen3, textvariable="")  # Entrée clavier
    moveY.grid(column=1, row=12)

    # Bouton envoi MOVE au serveur
    buttonMove = Button(fen3, text="MOVE",
                        command=lambda: [recupMove(), move(), majCarte(), depression()])
    buttonMove.grid(column=2, row=12)

    # Lancer la musique
    boutonPlay = Button(fen3, text="Music On", command=pygame.mixer.music.play)
    boutonPlay.grid(column=1, row=14)

    # Couper la musique
    boutonStop = Button(fen3, text="Music Off", command=pygame.mixer.music.stop)
    boutonStop.grid(column=2, row=14)

    fen3.mainloop()


# Lancement du Jeu
connexionServeur()
