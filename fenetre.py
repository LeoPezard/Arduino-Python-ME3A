"""
File name      : fenetre.py
Author         : PEZARD Léo
Date           : 2024-12-03
Description    : Création d'une fenêtre Tkinter pour demander à l'utilisateur s'il veut réellement quitter l'appllication ou 
                s'il veut afficher des données en grand sur l'intégralité du temps d'enregistrement.
                La fenêtre contient uniquement deux boutons et un texte
"""

import tkinter as tk
import os, sys

# Cas pour lancer l'affichage des donnés sur le temps total
def button1_action():
    window.destroy()
    os.system('python3 values_display.py')

# Cas pour quitter la fenêtre et tout fermer
def button2_action():
    window.destroy()
    sys.exit()

window = tk.Tk() # création de la fenêtre

# Texte que l'utilisateur va lire
label = tk.Label(window, text="Do you want to see the entire data one by one ? ", font=("Arial", 14))
label.pack(pady=20) # Marges pour laisser de l'espace entre les éléments


# Boutons, contenu des boutons et leurs commandes
button1 = tk.Button(window, text="Yes", command=button1_action)
button1.pack(side="left", padx=20, pady=10)

button2 = tk.Button(window, text="Quit", command=button2_action)
button2.pack(side="right", padx=20, pady=10)

window.mainloop() # Ouverture de la fenêtre
