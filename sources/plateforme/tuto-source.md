# Jeu de plateforme

```jres
@@JRES@@
```

```template
scene.setBackgroundColor(9)
```

## Un jeu de plateforme @showdialog

Ton héros court, saute de plateforme en plateforme, ramasse des pièces et évite la lave jusqu'au drapeau.

![Le jeu que tu vas créer](@@GIF@@)

Tu connais déjà les sprites, le score et les vies. Ici, trois choses sont nouvelles :

- le **plan des tuiles**, qui dessine le niveau ;
- la **gravité**, qui fait retomber le héros ;
- la **caméra**, qui suit le héros dans un niveau plus grand que l'écran.

## Le niveau

Le niveau est déjà dessiné. Il est fait de **tuiles** : des carrés de 16 pixels posés sur une grille.

- :tree: Dans ``||scene:Scène||``, glisse ``||scene:définir plan des tuiles à||`` dans ``||loops(noclick):au démarrage||``.
- :mouse pointer: Clique sur la petite image du bloc. Dans l'onglet **Mes ressources**, choisis **niveau1**.

Le début du niveau s'affiche dans le simulateur.

```blocks
scene.setBackgroundColor(9)
// @highlight
tiles.setCurrentTilemap(tilemap`niveau1`)
```

## Le héros

- :paper plane: Dans ``||sprites:Sprites||``, glisse ``||variables(sprites):définir heros à sprite de type Player||`` à la fin de ``||loops(noclick):au démarrage||``.
- :mouse pointer: Clique sur le carré gris et dessine ton héros, ou choisis-le dans la **Galerie**.
- :game: Dans ``||controller:Contrôleur||``, ajoute ``||controller:déplacer heros avec les boutons vx 80 vy 0||``.

**vx** est la vitesse quand on appuie sur gauche ou droite, **vy** sur haut ou bas. Dans un jeu de plateforme, on ne monte pas avec la flèche du haut : on saute. **vy** reste donc à 0.

```blockconfig.local
let heros = sprites.create(img`
@@HEROS@@
    `, SpriteKind.Player)
```

```blocks
scene.setBackgroundColor(9)
tiles.setCurrentTilemap(tilemap`niveau1`)
// @highlight
let heros = sprites.create(img`
@@HEROS@@
    `, SpriteKind.Player)
// @highlight
controller.moveSprite(heros, 80, 0)
```

## La gravité

Ton héros flotte en l'air. Il faut une force qui le tire vers le bas : la **gravité**.

- :paper plane: Dans ``||sprites:Sprites||``, glisse ``||sprites:définir heros ay (accélération selon y) à 400||`` à la fin de ``||loops(noclick):au démarrage||``.

Le héros tombe, et le sol l'arrête : les tuiles de sol, de terre et de brique sont des **murs**.

```blockconfig.local
let heros: Sprite = null
heros.ay = 400
```

~hint Vitesse ou accélération ? 💡

---

**vy** est une vitesse : le héros descend toujours au même rythme. **ay** est une accélération : il tombe de plus en plus vite, comme une vraie chute.

hint~

```blocks
scene.setBackgroundColor(9)
tiles.setCurrentTilemap(tilemap`niveau1`)
let heros = sprites.create(img`
@@HEROS@@
    `, SpriteKind.Player)
controller.moveSprite(heros, 80, 0)
// @highlight
heros.ay = 400
```

## La caméra

Le niveau est plus large que l'écran. Quand le héros va à droite, il sort de l'image.

- :tree: Dans ``||scene:Scène||``, glisse ``||scene:camera suit sprite||`` à la fin de ``||loops(noclick):au démarrage||`` et choisis **heros**.

Essaie : avance vers la droite avec les flèches.

```blocks
scene.setBackgroundColor(9)
tiles.setCurrentTilemap(tilemap`niveau1`)
let heros = sprites.create(img`
@@HEROS@@
    `, SpriteKind.Player)
controller.moveSprite(heros, 80, 0)
heros.ay = 400
// @highlight
scene.cameraFollowSprite(heros)
```

## Le point de départ

Le héros apparaît au milieu de l'écran. On le pose au début du niveau.

- :tree: Dans ``||scene:Scène||``, glisse ``||scene:placer heros sur||`` à la fin de ``||loops(noclick):au démarrage||``.
- :tree: Dans le trou du bloc, mets ``||scene:plan des tuiles col 1 ligne 3||``.

Le héros apparaît en l'air et tombe sur le sol. Les colonnes et les lignes se comptent à partir de 0, en haut à gauche.

```blocks
scene.setBackgroundColor(9)
tiles.setCurrentTilemap(tilemap`niveau1`)
let heros = sprites.create(img`
@@HEROS@@
    `, SpriteKind.Player)
controller.moveSprite(heros, 80, 0)
heros.ay = 400
scene.cameraFollowSprite(heros)
// @highlight
tiles.placeOnTile(heros, tiles.getTileLocation(1, 3))
```

## Le saut

Le bouton A fait sauter le héros, mais seulement s'il est posé sur quelque chose. Sinon, il pourrait sauter en l'air à l'infini.

- :game: Dans ``||controller:Contrôleur||``, sors ``||controller:quand bouton A est appuyé||``.
- :random: Dedans, mets un ``||logic:si alors||``.
- :tree: Dans ``||scene:Scène||``, prends ``||scene:heros touche-t'il le mur bas||`` et mets-le dans la condition du **si**.
- :paper plane: Dans ``||sprites:Sprites||``, prends ``||sprites:définir heros vy (vitesse selon y) à -200||`` et mets-le dans le **si**.

La vitesse est négative, parce que vers le haut, y diminue.

```blockconfig.local
let heros: Sprite = null
heros.vy = -200
```

```blocks
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    if (heros.isHittingTile(CollisionDirection.Bottom)) {
        heros.vy = -200
    }
})
let heros: Sprite = null
```

## Les murs des plateformes

Saute sur une plateforme de briques : ton héros passe à travers ! Une tuile n'arrête le héros que si c'est un **mur**. Le sol en est déjà un, les briques pas encore.

- :mouse pointer: Dans ``||loops(noclick):au démarrage||``, clique sur l'image du niveau, dans ``||scene(noclick):définir plan des tuiles à||``.
- :mouse pointer: Clique sur le bouton **Dessinez les murs**, à droite des carrés de couleur. Les murs déjà posés apparaissent en rouge.
- :mouse pointer: Avec le crayon, colorie en rouge toutes les briques des plateformes, puis clique sur **Terminé**.

Rejoue : ton héros peut maintenant monter sur les plateformes.

## Les pièces

Quand le héros touche une pièce, elle disparaît et le score monte.

- :tree: Dans ``||scene:Scène||``, sors ``||scene:lorsque sprite de type Player chevauche à location||``.
- :mouse pointer: Choisis la **pièce** dans le menu de la tuile.
- :tree: Dedans, mets ``||scene:définir à location||``. Laisse la tuile vide (le damier) : la pièce est remplacée par du vide.
- :mouse pointer: Vérifie que le bloc dit bien **location**. Sinon, glisse le **location** rouge du haut du bloc **lorsque** dans le trou : c'est l'endroit où se trouve la pièce touchée.
- :id card: Dans ``||info:Info||``, ajoute ``||info:modifier le score de 1||``.

```blockconfig.local
let location: tiles.Location = null
tiles.setTileAt(location, assets.tile`transparency16`)
```

```blocks
scene.onOverlapTile(SpriteKind.Player, assets.tile`piece`, function (sprite, location) {
    tiles.setTileAt(location, assets.tile`transparency16`)
    info.changeScoreBy(1)
})
```

## La lave

La lave fait perdre une vie et renvoie le héros au départ.

- :id card: Dans ``||loops(noclick):au démarrage||``, ajoute ``||info:définir vie à 3||``.
- :tree: Sors un deuxième ``||scene:lorsque sprite de type Player chevauche à location||`` et choisis la **lave**.
- :random: Dedans, mets un ``||logic:si alors||``.
- :tree: Dans la condition, mets ``||scene:la tuile centre par rapport à heros est||`` et choisis la **lave**.
- :id card: Dans le **si**, mets ``||info:modifier la vie de -1||``.
- :tree: Puis ``||scene:placer heros sur plan des tuiles col 1 ligne 3||``, comme au départ.

Quand il n'y a plus de vie, la partie s'arrête toute seule.

~hint Pourquoi ce si ? 💡

---

Le héros fait 16 pixels de large, comme une tuile. Il touche souvent deux tuiles de lave à la fois, et le bloc **lorsque** se déclenche alors deux fois. Sans le **si**, il perdrait deux vies d'un coup. Avec le **si**, au deuxième passage le héros est déjà revenu au départ : rien ne se passe.

hint~

```blocks
scene.setBackgroundColor(9)
tiles.setCurrentTilemap(tilemap`niveau1`)
let heros = sprites.create(img`
@@HEROS@@
    `, SpriteKind.Player)
controller.moveSprite(heros, 80, 0)
heros.ay = 400
scene.cameraFollowSprite(heros)
tiles.placeOnTile(heros, tiles.getTileLocation(1, 3))
// @highlight
info.setLife(3)
scene.onOverlapTile(SpriteKind.Player, assets.tile`lave`, function (sprite, location) {
    if (heros.tileKindAt(TileDirection.Center, assets.tile`lave`)) {
        info.changeLifeBy(-1)
        tiles.placeOnTile(heros, tiles.getTileLocation(1, 3))
    }
})
```

## Le drapeau

Le drapeau, tout au bout, fait gagner la partie.

- :tree: Sors un troisième ``||scene:lorsque sprite de type Player chevauche à location||`` et choisis le **drapeau**.
- :circle: Dans ``||game:Jeu||``, mets ``||game:jeu terminé||`` dedans. Laisse **VICTOIRE**.

Joue ton niveau jusqu'au bout !

```blocks
scene.onOverlapTile(SpriteKind.Player, assets.tile`drapeau`, function (sprite, location) {
    game.over(true)
})
```

## La manette

Branche ta manette micro:bit : elle sonne et s'allume quand il se passe quelque chose dans le jeu.

- :game: Dans ``||manette:Manette||``, mets ``||manette:manette réagir bip||`` dans **quand bouton A est appuyé**, sous le saut.
- :game: Dans le bloc des **pièces**, ajoute ``||manette:manette réagir||`` et choisis **bien**.
- :game: Dans le **si** de la **lave**, ajoute ``||manette:manette réagir||`` avec **mal**, puis ``||manette:manette afficher||``. Mets-y ``||info:vie||``, de la catégorie ``||info:Info||``.
- :game: Dans le bloc du **drapeau**, ajoute ``||manette:manette réagir||`` avec **gagne**, avant **jeu terminé**.

Ouvre la page relais, connecte la manette et joue : incline pour avancer, A pour sauter.

```blocks
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    if (heros.isHittingTile(CollisionDirection.Bottom)) {
        heros.vy = -200
        // @highlight
        manette.reagir(ReactionManette.Bip)
    }
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`piece`, function (sprite, location) {
    tiles.setTileAt(location, assets.tile`transparency16`)
    info.changeScoreBy(1)
    // @highlight
    manette.reagir(ReactionManette.Bien)
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`lave`, function (sprite, location) {
    if (heros.tileKindAt(TileDirection.Center, assets.tile`lave`)) {
        info.changeLifeBy(-1)
        tiles.placeOnTile(heros, tiles.getTileLocation(1, 3))
        // @highlight
        manette.reagir(ReactionManette.Mal)
        // @highlight
        manette.afficher(info.life())
    }
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`drapeau`, function (sprite, location) {
    // @highlight
    manette.reagir(ReactionManette.Gagne)
    game.over(true)
})
let heros: Sprite = null
```

## À toi de jouer @showdialog

Ton jeu de plateforme marche. Maintenant, rends-le à toi :

- clique sur l'image du niveau pour le **redessiner** : allonge-le, ajoute des trous, des pièces, de la lave ;
- dessine tes propres tuiles avec le pinceau de l'éditeur ;
- ajoute des **ennemis** qui patrouillent, comme dans le jeu de tir ;
- donne d'autres réactions à ta **manette** : un chiffre pour le score, un son quand tu perds.

```blockconfig.global
let heros: Sprite = null
controller.moveSprite(heros, 80, 0)
scene.cameraFollowSprite(heros)
tiles.placeOnTile(heros, tiles.getTileLocation(1, 3))
heros.isHittingTile(CollisionDirection.Bottom)
heros.tileKindAt(TileDirection.Center, assets.tile`lave`)
```
