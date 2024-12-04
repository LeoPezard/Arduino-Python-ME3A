"""
File name      : fenetre.py
Author         : PEZARD Léo
Date           : 2024-12-03
Description    : Affichage du graphique matplotlib dans une fenêtre Tkinter.
                L'utilisateur peux choisir quel donnée il veut afficher (lux/température/tension/angle) en fonction du temps
"""

import sys
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Initlialisation des listes de chaque donnée depuis le fichier texte créé lors de l'enregistrement des valeurs
# Il ya donc dans ce fichier texte l'ensemble des valeurs depuis le début de l'enregistrement.
lux, tempR, voltage, angle, temps = [], [], [], [], []
# Ajout des valeurs dans chaque liste depuis le fichier texte
with open('values.txt', 'r') as file:
    for line in file.readlines()[1:]: #La première ligne contient des légende ("Température, Luminosité etc...")
        val = line.strip().split(',')
        lux.append(float(val[0]))
        tempR.append(float(val[1]))
        voltage.append(float(val[2]))
        angle.append(float(val[3]))
        temps.append(float(val[4]))
# Avec 'with open(...)' le fichier se ferme tout seul une fois la boucle finie


# Action du bouton pour quitter
def quit_():
    window.destroy()
    sys.exit()

# Fonction pour mettre a jour selon l'option choisie par l'utilisateur
def update_plot(selected_option):
    ax.clear() # Dès qu'un paramètre est sélectionné, l'ancien est effacé pour laisser la place au nouveau
    ax.set_title(f"Evolution of {selected_option} over time")
    ax.set_xlabel("Time")
    ax.set_ylabel(selected_option)
    if selected_option == "Lux":
        ax.plot(temps, lux, color="blue")
    elif selected_option == "Temperature":
        ax.plot(temps, tempR, color="red")
    elif selected_option == "Voltage":
        ax.plot(temps, voltage, color="green")
    elif selected_option == "Angle":
        ax.plot(temps, angle, color="orange")
    
    canvas.draw()

# Création de la fenêtre, titre et sa taille
window = tk.Tk()
window.title("Selection of data")
window.geometry('1200x900')

options = ["Lux", "Temperature", "Voltage", "Angle"]
selected_option = tk.StringVar(value=options[0]) # Valeur par défaut du dropdown permettant de sélectionner la donnée à afficher

# Menu défilant (dropdown ) qui permet de lister des valeurs qui peuvent être choisies par l'utilisateur
dropdown = ttk.Combobox(window, values=options, textvariable=selected_option)
dropdown.pack(pady=10) # Espacement autour de l'élément
dropdown.configure(font=('Arial', 30))

# Création d'un évènement 
# "Combobox" est une liste déroulante (menu dropdown)
# lambda event est une fonction anonyme, elle prend comme argument la fonction qui met à jour le graphe
# le .get() est une méthode permettant de récupérer la valeur de selected_option qui sera ensuite mise en argument de la fonction update_plot()
dropdown.bind("<<ComboboxSelected>>", lambda event: update_plot(selected_option.get()))

# Création de la figure et insertion dans la fenêtre Tkinter
fig, ax = plt.subplots(figsize=(12,7))
canvas = FigureCanvasTkAgg(fig, master=window) # interface entre Tkinter et matplotlib, j'associe la figure fig à la fenêtre window créée plus haut
canvas_widget = canvas.get_tk_widget() # ensuite ce 'canvas' est transformé en objet tkinter manipulable
canvas_widget.pack(fill = "both", expand = True) # remplir l'espace disponible et s'étend si la fenetre est agrandie/rétrécie

# Bouton pour quitter et ses attributs (texte, commande, couleur)
quit_button = tk.Button(window, text="Quit", command=quit_, bg="red", fg="white", font = 18)
quit_button.pack(pady=10)

# Récupère la valeur de selected_option pour l apasser en paramètre de la focntion 
# qui actualise le graphe
update_plot(selected_option.get()) 

#Boucle principale qui 'écoute' les interractions (clics, clavier..) et mes à jour l'interface 
window.mainloop()
