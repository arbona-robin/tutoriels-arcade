"""Construit les tutoriels du jeu de tir à partir de leurs sources lisibles.

    python3 construire.py

Pour chaque NOM.source.md de ce dossier, écrit ../../NOM.md (à la racine du dépôt) :
- img`heros` devient le dessin de images/heros.txt, en entier ;
- une image locale, ![…](fichier.gif), est intégrée au tutoriel : une image servie
  ailleurs ne s'affiche pas toujours dans l'éditeur MakeCode.

Le texte et les programmes se modifient dans les .source.md, jamais dans les .md générés.
"""
import base64
import glob
import os
import re

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
TYPES = {".gif": "image/gif", ".png": "image/png", ".jpg": "image/jpeg"}


def dessin(nom, retrait):
    lignes = open(os.path.join(ICI, "images", nom + ".txt")).read().split("\n")
    marge = " " * (retrait + 4)
    return "img`\n" + "\n".join(marge + l for l in lignes if l.strip()) + "\n" + marge + "`"


def remplacer_dessins(texte):
    sortie = []
    for ligne in texte.split("\n"):
        retrait = len(ligne) - len(ligne.lstrip(" "))
        sortie.append(re.sub(r"img`(\w+)`", lambda m: dessin(m.group(1), retrait), ligne))
    return "\n".join(sortie)


def integrer_images(texte):
    def remplacer(m):
        fichier = m.group(2)
        ext = os.path.splitext(fichier)[1].lower()
        if fichier.startswith(("http", "data:")) or ext not in TYPES:
            return m.group(0)
        donnees = base64.b64encode(open(os.path.join(ICI, fichier), "rb").read()).decode()
        return f"![{m.group(1)}](data:{TYPES[ext]};base64,{donnees})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", remplacer, texte)


for source in sorted(glob.glob(os.path.join(ICI, "*.source.md"))):
    nom = os.path.basename(source)[: -len(".source.md")]
    texte = integrer_images(remplacer_dessins(open(source).read()))
    open(os.path.join(RACINE, nom + ".md"), "w").write(texte)
    print(f"{nom}.md")
