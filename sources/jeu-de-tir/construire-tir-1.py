"""Construit tir-1.md, l'activité 1 de la skillmap du jeu de tir, à partir de s1.ts.

Usage : python3 construire-tir-1.py [dossier]   (dossier : celui de s1.ts, tir-1.gif, axes.png)
Les images (GIF d'ouverture, schéma des axes) sont intégrées au tutoriel : une image
servie ailleurs ne s'affiche pas toujours dans l'éditeur.
"""
import base64
import os
import re
import sys

ICI = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
code = open(os.path.join(ICI, "s1.ts")).read()
V, T, E = re.findall(r"img`([^`]*)`", code)


def ind(s, n):
    return "\n".join(" " * n + l.strip() for l in s.strip("\n").split("\n") if l.strip())


def data(fichier, mime):
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(ICI, fichier), "rb").read()).decode()


def hl(s):
    return "// @highlight\n" + s


def blocs(*parts):
    return "```blocks\n" + "\n".join(parts) + "\n```"


BASE = "scene.setBackgroundColor(15)"
CREA = f"let heros = sprites.create(img`\n{ind(V, 4)}\n    `, SpriteKind.Player)"
POS = "heros.setPosition(20, 60)"
MOV = "controller.moveSprite(heros, 0, 100)"
ECRAN = "heros.setStayInScreen(true)"
TIR = f"controller.A.onEvent(ControllerButtonEvent.Pressed, function () {{\n    let tir = sprites.createProjectileFromSprite(img`\n{ind(T, 8)}\n        `, heros, 150, 0)\n}})"
TIR_SEUL = f"let tir = sprites.createProjectileFromSprite(img`\n{ind(T, 4)}\n    `, heros, 150, 0)"
ENNEMI_CREA = f"let ennemi = sprites.create(img`\n{ind(E, 4)}\n    `, SpriteKind.Enemy)\nennemi.setPosition(160, randint(10, 110))"


def ennemi(extra=""):
    return (f"game.onUpdateInterval(900, function () {{\n    let ennemi = sprites.create(img`\n{ind(E, 8)}\n        `, SpriteKind.Enemy)\n"
            f"    ennemi.setPosition(160, randint(10, 110)){extra}\n}})")


VITESSE = "\n    // @highlight\n    ennemi.vx = -40\n    // @highlight\n    ennemi.setFlag(SpriteFlag.AutoDestroy, true)"
COLL = ("sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Enemy, function (sprite, otherSprite) {\n"
        "    sprites.destroy(sprite)\n    sprites.destroy(otherSprite, effects.fire, 200)\n})")

md = f'''# Ton premier jeu de tir

```template
{BASE}
```

## Ton premier jeu de tir @showdialog

Ton héros vole de haut en bas, tire, et détruit les ennemis qui foncent sur lui.

![Le jeu à la fin de la séance]({data("tir-1.gif", "image/gif")})

Tu dessines tout toi-même : ton héros, son tir, tes ennemis. Pas d'idée ? Un vaisseau spatial.

## Ton héros

- :paper plane: Dans ``||sprites:Sprites||``, glisse ``||variables(sprites):définir heros à sprite de type Player||`` dans ``||loops(noclick):au démarrage||``.
- :mouse pointer: Clique sur le carré gris et dessine ton héros.

Il doit regarder vers la droite : c'est de ce côté qu'il tirera.

~hint Bien dessiner en pixel art 💡

---

- Commence par la silhouette, d'une couleur sombre.
- Trois ou quatre couleurs suffisent.
- Une couleur plus claire sur le dessus donne du volume.

La **Galerie** propose des dessins tout faits. Un dessin à toi rend ton jeu unique.

hint~

```blockconfig.local
{CREA}
```

{blocs(BASE, hl(CREA))}

## À gauche de l'écran

- :paper plane: Dans ``||sprites:Sprites||``, ajoute ``||sprites:définir la position de heros à x 20 y 60||``.

![L'écran : x va de 0 à 160 vers la droite, y de 0 à 120 vers le bas. Le point 0, 0 est en haut à gauche.]({data("axes.png", "image/png")})

**x** se compte vers la droite, **y** vers le bas, à partir du coin en haut à gauche.

{blocs(BASE, CREA, hl(POS))}

## De haut en bas

- :game: Dans ``||controller:Contrôleur||``, ajoute ``||controller:déplacer heros avec les boutons vx 0 vy 100||``.

**vx** vaut 0 : ton héros ne va ni à gauche ni à droite. Il ne bouge que de haut en bas.

Essaie avec les flèches du clavier : monte tout en haut. Que se passe-t-il ?

{blocs(BASE, CREA, POS, hl(MOV))}

## Reste à l'écran

Ton héros sort de l'écran, et tu le perds.

- :paper plane: Dans ``||sprites:Sprites||``, ajoute ``||sprites:définir heros rester à l'écran ON||``.

Essaie de nouveau : il s'arrête au bord.

{blocs(BASE, CREA, POS, MOV, hl(ECRAN))}

## Le tir

- :game: Dans ``||controller:Contrôleur||``, sors ``||controller:quand bouton A est appuyé||``.
- :paper plane: Dedans, mets ``||variables(sprites):définir tir à projectile depuis heros avec vx 150 vy 0||``.
- :mouse pointer: Clique sur le carré gris et dessine ton tir : petit, 3 ou 4 pixels de haut.

Essaie : la touche **espace** du clavier est le bouton A.

```blockconfig.local
{TIR_SEUL}
```

{blocs(hl(TIR))}

## Les ennemis arrivent

- :circle: Dans ``||game:Jeu||``, sors ``||game:quand mise à jour du jeu chaque 900 ms||``.
- :paper plane: Dedans, mets ``||variables(sprites):définir ennemi à sprite de type Enemy||`` et dessine ton ennemi.
- :paper plane: Ajoute ``||sprites:définir la position de ennemi à x 160 y||``.
- :calculator: Pour **y**, prends ``||math:choisir aléatoirement entre 10 et 110||`` dans ``||math:Maths||``.

Un ennemi apparaît toutes les 900 ms, au bord droit, à une hauteur différente à chaque fois.

```blockconfig.local
{ENNEMI_CREA}
```

{blocs(hl(ennemi()))}

## Ils foncent sur toi

- :paper plane: Dans le même bloc, ajoute ``||sprites:définir ennemi vx (vitesse selon x) à -40||``.
- :paper plane: Puis ``||sprites:définir ennemi destruction automatique ON||``.

La vitesse est négative : l'ennemi va vers la gauche.

~hint Pourquoi la destruction automatique ? 💡

---

Sans elle, un ennemi sorti de l'écran continue d'exister. Au bout de quelques minutes, ils sont des centaines et le jeu ralentit.

hint~

```blockconfig.local
let ennemi: Sprite = null
ennemi.vx = -40
ennemi.setFlag(SpriteFlag.AutoDestroy, true)
```

{blocs(ennemi(VITESSE))}

## Touché !

- :paper plane: Dans ``||sprites:Sprites||``, sors ``||sprites:quand sprite de type Projectile chevauche otherSprite de type Enemy||``.
- :paper plane: Dedans, mets ``||sprites:détruire sprite||`` : **sprite** est le tir, il disparaît.
- :paper plane: Ajoute un second ``||sprites:détruire sprite||``, et clique sur son **+** : choisis l'effet **feu**, pendant **200** ms.
- :mouse pointer: Glisse le **otherSprite** rouge, en haut du bloc **quand**, à la place de **sprite** dans ce second **détruire** : **otherSprite** est l'ennemi touché, il explose.

```blockconfig.local
sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Enemy, function (sprite, otherSprite) {{
}})
sprites.destroy(sprite)
```

{blocs(hl(COLL))}

## Le temps du pixel art

Ton jeu marche. Prends maintenant le temps de soigner tes dessins.

- :mouse pointer: Clique sur chaque dessin pour le retoucher : ton héros, son tir, ton ennemi.
- :mouse pointer: Change la couleur du fond dans ``||scene(noclick):définir couleur d'arrière-plan||``.

Teste après chaque retouche : un ennemi trop sombre sur un fond sombre ne se voit plus.

## Bravo @showdialog

Ton premier jeu de tir marche. Clique sur **Terminé**, puis, en haut de l'écran, sur **Partager** : donne un nom à ton jeu et copie son lien. Pas besoin de compte. Ce lien te permet de rouvrir ton jeu sur n'importe quel ordinateur.

```blockconfig.global
let heros: Sprite = null
heros.setPosition(20, 60)
controller.moveSprite(heros, 0, 100)
heros.setStayInScreen(true)
{TIR_SEUL}
```
'''
open(os.path.join(ICI, "tir-1.md"), "w").write(md)
print("tir-1.md", len(md), "octets")
