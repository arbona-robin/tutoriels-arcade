# Tutoriels MakeCode Arcade

Tutoriels en français pour le parcours Maker Junior, extension pour jouer avec une manette micro:bit, et page relais entre les deux.

## Tutoriels

| Tutoriel | Lien |
|---|---|
| Skillmap du jeu de tir (séances 1 à 3) | https://arcade.makecode.com/--skillmap#github:arbona-robin/tutoriels-arcade/jeu-de-tir |
| Jeu de plateforme | https://arcade.makecode.com/?lang=fr#tutorial:https://github.com/arbona-robin/tutoriels-arcade/plateforme |

Un tutoriel par fichier `.md` à la racine, déclaré dans `files` de `pxt.json`. Les fichiers `.ts` du dépôt sont ajoutés au programme de chaque tutoriel : c'est ce qui apporte les blocs Manette. Aucun autre `.ts` ne doit donc traîner dans le dépôt ; le code micro:bit et les sources sont rangés dans des fichiers Markdown ou `.txt`.

## La chaîne

```
micro:bit ──USB série──▶ page relais ──postMessage──▶ jeu Arcade (simulateur)
          ◀── réactions ──            ◀── manette-retour ──
```

| Élément | Où |
|---|---|
| Extension Arcade (blocs **Manette**) | [`manette.ts`](manette.ts) |
| Programme du micro:bit | [`manette-microbit.md`](manette-microbit.md) |
| Page relais | [`relais/index.html`](relais/index.html) |
| Jeu de tir des séances communes | [`sources/jeu-de-tir`](sources/jeu-de-tir) |
| Sources du tutoriel plateforme | [`sources/plateforme`](sources/plateforme) |

## Extension manette

Dans MakeCode Arcade, **Extensions**, puis colle l'adresse de ce dépôt :

```
https://github.com/arbona-robin/tutoriels-arcade
```

- La manette appuie sur les mêmes boutons que le clavier (`controller.X.setPressed`) : le jeu se programme et se teste au clavier, la manette se branche ensuite sans rien changer.
- Seuls les boutons qui changent sont touchés : le clavier garde la main sur les autres.
- Chaque nouvelle scène (écran de démarrage, game over) a ses propres événements : l'extension y rebranche la réception.
- Au premier message de la manette, le jeu se tait (`music.setVolume(0)`) : les sons, c'est la manette qui les joue.
- Blocs : `manette réagir [bip, bien, mal, alerte, gagne, perdu]`, `manette afficher [0-9]`, et en avancé `manette envoyer [mot]`.

## Page relais

Chrome ou Edge (WebSerial). Ouvrir `relais/index.html` servi en local (`python3 -m http.server`), coller le lien de partage du jeu, **Charger**, puis **Connecter la manette**.

- Le jeu tourne dans le lecteur `---run` ; la page écrit dans le simulateur imbriqué (`iframe.contentWindow.frames[0]`), parce que le lecteur ne relaie pas les messages du parent.
- Le lecteur renvoie chaque message du jeu deux fois : la copie qui porte `srcFrameIndex` est ignorée.
- Un bouton reste appuyé 100 ms après le dernier mot reçu ; l'état est envoyé au changement, et renvoyé toutes les 300 ms.
- Reconnexion automatique du port déjà autorisé (`getPorts`, événement `connect`).
- Alerte orange si 3 mots inconnus arrivent en 2 secondes : un onglet MakeCode est sans doute encore connecté au micro:bit.
