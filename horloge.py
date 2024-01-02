import time
import signal

heure_actuelle = (16, 10, 30)
alarme = None
mode_12h = False
en_pause = False

def afficher_heure():
    global heure_actuelle
    if not en_pause:
        heure_actuelle = (heure_actuelle[0], heure_actuelle[1], heure_actuelle[2] + 1)
        if heure_actuelle[2] == 60:
            heure_actuelle = (heure_actuelle[0], heure_actuelle[1] + 1, 0)
            if heure_actuelle[1] == 60:
                heure_actuelle = (heure_actuelle[0] + 1, 0, 0)
                if heure_actuelle[0] == 24:
                    heure_actuelle = (0, 0, 0)

def regler_alarme():
    global alarme
    while True:
        heures = int(input("Entrez l'heure de l'alarme (0-23): "))
        minutes = int(input("Entrez les minutes de l'alarme (0-59): "))
        secondes = int(input("Entrez les secondes de l'alarme (0-59): "))
        
        if 0 <= heures <= 23 and 0 <= minutes <= 59 and 0 <= secondes <= 59:
            alarme = (heures, minutes, secondes)
            break
        else:
            print("Erreur : Veuillez entrer des valeurs valides pour l'heure, les minutes et les secondes.")

def verifier_alarme():
    global heure_actuelle, alarme
    if alarme is not None and heure_actuelle == alarme:
        print("Alarme! Il est temps!")

def choisir_format_heure():
    global mode_12h
    while True:
        choix = input("Choisissez le format d'heure (12h ou 24h): ").lower()
        
        if choix == "12h" or choix == "24h":
            mode_12h = choix == "12h"
            break
        else:
            print("Erreur : Veuillez choisir entre '12h' et '24h'.")

def afficher_heure_format():
    global heure_actuelle, mode_12h
    if mode_12h:
        heure = heure_actuelle[0] % 12
        if heure == 0:
            heure = 12
        am_pm = "AM" if heure_actuelle[0] < 12 else "PM"
        print(f"{heure:02d}:{heure_actuelle[1]:02d}:{heure_actuelle[2]:02d} {am_pm}", end='\r')
    else:
        print(f"{heure_actuelle[0]:02d}:{heure_actuelle[1]:02d}:{heure_actuelle[2]:02d}", end='\r')

def mettre_en_pause(signal, frame):
    global en_pause
    en_pause = not en_pause
    print("L'horloge est en pause." if en_pause else "L'horloge a repris.")

# Associer le signal SIGINT (Ctrl+C) à la fonction mettre_en_pause
signal.signal(signal.SIGINT, mettre_en_pause)

regler_alarme()
choisir_format_heure()

while True:
    afficher_heure()
    verifier_alarme()
    afficher_heure_format()

    if en_pause:
        reprise = input("L'horloge est en pause. Appuyez sur 'R' pour la relancer : ").lower()
        if reprise == 'r':
            en_pause = False
            print("L'horloge a repris.")

    time.sleep(1)
