#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

arguments = [
    "je suis avocat depuis l'hiver de l'été dernier",
    "je connais personnellement un hungénieur",
    "j'ai mangé des vers avec Billy Crystal",
    "je suis avocat depuis la naissance",
    "j'ai une papetterie en bas de chez moi",
    "je prends le bus tout seul",
]

pejorative = [
    "PDG",
    "Ménestrel",
    "Démocrate",
    "Fasciste",
    "Spécialiste",
]

prelude = [
    "Sortez immédiatement de mon officine, ou",
    "La prochaine fois que vous me dites d'arrêter,",
    "Arrêtez de dire non, ou",
    'Vous dites encore une fois "mais",',
    "Sortez ou",
    "Quittez immédiatement cette salle, ou",
    "Fermez votre petite gueule, ou",
]

verb = [
    "arrache",
    "casse",
    "bouche",
    "repeint",
    "coupe",
    "découpe",
    "défonce",
    "ponce",
    "écarte",
    "broie",
]

body_part = [
    "les particules",
    "le crâne",
    "un oeil",
    "l'anus",
    "le cul",
    "les cheveux",
    "les nichons",
    "l'urètre",
    "le périné",
    "les testicules",
    "la gueule",
]

item = [
    "du flan",
    "une clef à molette",
    "un stylo et des plumes",
    "de la purée",
    "une mouette",
    "un coupe-ongles",
    "un grille-pain",
    "du papier abrasif",
    "un massicot",
    "une chaîne de vélo",
]

person = [
    "un ostéopathe",
    "le Pape",
    "votre mère",
    "Brejnev",
    "un âne",
    "ma mère",
    "Jean-Marie Le Pen",
    "Rick Astley",
    "ma voisine",
]

statement = [
    "s'en fera rembourser le dos",
    "en aura mal au cul",
    "en perdrait ses couilles",
    "en chiera des perles",
    "s'en teindrait la touffe",
    "s'en mordrait les couilles",
    "en vomirait son déjeuner",
]

def marcadet():
    return (random.choice(prelude) + " je vous " + random.choice(verb) + " " +
           random.choice(body_part) + " avec " + random.choice(item) +
           " que même " + random.choice(person) + " " +
           random.choice(statement) + " !")

def main():
    print marcadet()

if __name__ == "__main__":
    main()
