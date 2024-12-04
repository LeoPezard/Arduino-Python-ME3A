"""
File name      : Projet_pezard.py
Author         : PEZARD Léo
Date           : 2024-12-03
Description    : Code python du projet Python/arduino Polytech ME 2024
"""
import serial
import time
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


ser = serial.Serial("COM3", 9600)
# Création du fichier texte et écriture de la première ligne
monfichier = open('values.txt', 'w')
monfichier.write("Luminosity | Temperature | Vpannel |  Theta  | Time \n")

# Listes des valeurs qui vont contenir les données
lux, tempR, vpannel, theta, temps = [], [], [], [], []
list_datas = [lux, tempR, vpannel, theta]
# Etats pour définir pause et quitter par la suite
is_paused = False
quit_state = False
# Pour créer le graphe animé
plt.ion()

# Création de 4 graphes dans 1 figure
fig, axes = plt.subplots(2, 2, figsize= (13,7))
fig.suptitle('Temperature, Luminosity, Voltage and Angle over time') # Titre général de la figure
lines = []
# Pour légender les graphes indépendemment, chacun sa légende, sa couleur, son titre mais surtout sa limite en ordonnées
# Sous forme de dictionnaire pour éviter de faire des lignes en répétitions, il suffira d'aller chercher les clefs-valeurs lors de la création des graphiques
properties = [
    {"color": "red", "label": "Temperature (°C)", "ylabel": "Temperature (°C)", "ylimit": (18, 30)},
    {"color": "blue", "label": "Luminosity", "ylabel": "Luminosity (Lux)", "ylimit": (50, 700)},
    {"color": "green", "label": "Voltage of the pannel", "ylabel": "Voltage (Volt)", "ylimit": (0, 5)},
    {"color": "orange", "label": "Servomotor angle", "ylabel": "θ (Degrees)", "ylimit": (-5, 185)}
]
# Boucle pour initialiser les graphiques, leur attribuer une légende, limites d'axes en ordonnées, titres des axes...
for ax, prop in zip(axes.flatten(), properties):
    line, = ax.plot([], [], color=prop["color"], label = prop["label"])
    ax.set_ylabel(prop["ylabel"], color = prop["color"])
    ax.tick_params(axis = "y", labelcolor = prop["color"])
    ax.set_xlabel('Time (sec)')
    ax.set_ylim(*prop["ylimit"])
    # Liste contenant les graphes
    lines.append(line)


# Fonciton lorsque le bouton quit est cliqué
def quit_event(_):
    global quit_state # variable globale (pas en argument) définie à la ligne 19
    quit_state = True # état pour arréter la boucle plus tard
    print("Closing of the application...")
    monfichier.close() # Fermeture du fichier texte
    plt.close(fig) # Fermeture de la figure
    ser.close() # Fermeture du port 
    time.sleep(1)
    # Lancement d'un autre programme (fenêtre demandant d'afficher les données sur la totalité du temps,
    # ou demandant de quitter)
    os.system('python3 fenetre.py') 


# Fonctions pause et resume changeant l'état de la variable globale de pause
def pause(_):
    global is_paused
    print("Paused...")
    is_paused = True

def resume(_):
    global is_paused
    print("Resuming...")
    is_paused = False

# Création des boutons
quit_button = plt.axes([0.65, 0.0, 0.15, 0.075]) # position du bouton
button = Button(quit_button, 'Quit',color = 'red') # Création de l'élément bouton avec Matplotlib, contenu et couleur
button.on_clicked(quit_event) # Action du bouton une fois cliqué

pause_button = plt.axes([0.42, 0.0, 0.15, 0.075])
button_pause = Button(pause_button, 'Pause', color = 'orange')
button_pause.on_clicked(pause)

resume_button = plt.axes([0.2, 0.0, 0.15, 0.075])
button_resume = Button(resume_button, 'Resume', color = 'yellow')
button_resume.on_clicked(resume)

# Compteur pour le temps
cnt = 1
while not quit_state: # Etat quitté à False
    if not is_paused : # Non en pause ==> Play
        try :
            # Lecture des valeurs sur le port arduino, création d'une liste remplie avec les valeurs à chaque boucle
            data = ser.readline().decode().strip().split(',')
            if len(data) == 4: # Vérifier que on lit bien 4 valeurs
                # Ajout de chaque valeur de data à sa lista associée
                for i in range(len(list_datas)):
                    list_datas[i].append(float(data[i]))
                # Exemple : la première valeur reçue par arduino est la luminosité et la première liste de list_datas
                # est lux. J'ajoute donc data[1] (=valeur de la luminosité) à list_datas[1] (=lux)
                print(f'Values read by arduino : {data}')
                # time.sleep(1)
                temps.append(cnt) # Compteur de 1 seconde après chaque time.sleep(1) donc chaque seconde 
                cnt+=1
                # Ecriture des valeurs dans le fichier (j'écris uniquement la dernière valeur de la liste)
                monfichier.write(f"{lux[-1]}, {tempR[-1]}, {vpannel[-1]}, {theta[-1]}, {temps[-1]} \n")

                # Réorganisation des graphes : 
                # pour chaque graphe (line), je lui associe en ordonnée les 20 dernières valeurs de sa représentation
                # et les 20 dernières valeurs du temps en abscisse (choix personnel pour afficher que les 20 dernières secondes)
                for line, data in zip(lines, [tempR, lux, vpannel, theta]):
                    line.set_data(temps[-20:], data[-20:])

                # Moins de place pour la liste du temps
                temps = temps[-20:]
                for ax in axes.flatten(): # Redimensionnement des asbcisses de chaque graphe
                    ax.set_xlim(min(temps), max(temps))

                fig.canvas.draw() # Pour redessiner immédiatement la figure et ses changements
                fig.canvas.flush_events() #Pour vider la file d'attente d'évenements de la figure (ex clics de souris ou maj graphiques)

        except KeyboardInterrupt:
            # Pouvoir quitter avec Ctrl+C
            quit_event(None) # Doit prendre un argument car il est attribué au bouton quitter
    else:
        plt.pause(0.3) # Permet de laisser une pause dans la boucle while et minimiser les bugs de la figure 
        #(surtout lorsque les boutons sont cliqués)
        time.sleep(0.1) # Presque pareil mais sur le code en général


