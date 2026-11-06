# Sources du tutoriel plateforme

`../../plateforme.md` est généré : ne pas le modifier à la main.

| Fichier | Rôle |
|---|---|
| `tuto-source.md` | Le texte du tutoriel. `@@JRES@@`, `@@HEROS@@` et `@@GIF@@` sont remplacés à la construction |
| `tuiles.py` | Dessine les tuiles (sol, terre, brique, pièce, lave, drapeau) et le niveau, produit `niveau.jres` et `tilemap.g.ts.txt` (renommé en `.ts` pour un projet) |
| `heros.txt` | L'image du héros |
| `plateforme.gif` | Le GIF de la boîte d'accueil |
| `construire.py` | Assemble `plateforme.md` |

```bash
python3 tuiles.py               # niveau du tutoriel : murs sur le sol seulement, l'élève dessine ceux des briques
python3 tuiles.py --tous-murs   # niveau complet (niveau-murs.jres), pour le jeu final et le GIF
python3 construire.py
```

Après un push, **MakeCode garde l'ancienne version du tutoriel en cache**. Seule une version créée depuis MakeCode (Importer → GitHub, puis créer une version) vide ce cache.

## Le format du niveau dans le jres

`data` est en base64 une chaîne hexadécimale : `10`, largeur et hauteur sur 2 octets petit-boutiens, un octet par tuile (index dans `tileset`), puis les murs ligne par ligne, une valeur par tuile (`2` = mur), les deux valeurs de chaque paire inversées.

## Tester sans publier

Les pages `tuto-local.html` et `projet-local.html` ouvrent l'éditeur en mode « controller » et lui injectent le tutoriel ou le projet par message, sans rien publier. Servir le dossier en local (`python3 -m http.server 8767`) avec `tutoriel.md`, `plat-main.ts`, `plat-demo.ts`, `plat-tilemap.g.jres` et `plat-tilemap.g.ts` à côté. Les scripts puppeteer (`tester.js`, `boite.js`, `filmer.js`) passent les étapes, ouvrent les catégories et filment le simulateur ; ils utilisent le puppeteer-core du dépôt du livre (`outils/blocs/node_modules`).

## Le jeu final

Publié avec la manette : https://arcade.makecode.com/_dm7fipEA3PX7

```typescript
scene.setBackgroundColor(9)
tiles.setCurrentTilemap(tilemap`niveau1`)
let heros = sprites.create(img`
    . . . . . . f f f f . . . . . .
    . . . . f f 5 5 5 5 f f . . . .
    . . . f 5 5 5 5 5 5 5 5 f . . .
    . . f 5 5 5 5 5 5 5 5 5 5 f . .
    . . f 5 5 f f f f f f 5 5 f . .
    . . f 5 f d d d d d d f 5 f . .
    . . f f d d f d d f d d f f . .
    . . . f d d f d d f d d f . . .
    . . . f d d d d d d d d f . . .
    . . . . f d d 2 2 d d f . . . .
    . . . f 8 f d d d d f 8 f . . .
    . . f 8 8 8 f f f f 8 8 8 f . .
    . . f d f 8 8 8 8 8 8 f d f . .
    . . . f f 8 8 8 8 8 8 f f . . .
    . . . . f f f . . f f f . . . .
    . . . . f f . . . . f f . . . .
    `, SpriteKind.Player)
controller.moveSprite(heros, 80, 0)
heros.ay = 400
scene.cameraFollowSprite(heros)
tiles.placeOnTile(heros, tiles.getTileLocation(1, 3))
info.setLife(3)
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    if (heros.isHittingTile(CollisionDirection.Bottom)) {
        heros.vy = -200
        manette.reagir(ReactionManette.Bip)
    }
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`piece`, function (sprite, location) {
    tiles.setTileAt(location, assets.tile`transparency16`)
    info.changeScoreBy(1)
    manette.reagir(ReactionManette.Bien)
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`lave`, function (sprite, location) {
    if (heros.tileKindAt(TileDirection.Center, assets.tile`lave`)) {
        info.changeLifeBy(-1)
        tiles.placeOnTile(heros, tiles.getTileLocation(1, 3))
        manette.reagir(ReactionManette.Mal)
        manette.afficher(info.life())
    }
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`drapeau`, function (sprite, location) {
    manette.reagir(ReactionManette.Gagne)
    game.over(true)
})
```

## Le pilote automatique du GIF

Ajouté à la fin du jeu final pour filmer une partie gagnée. Il appuie sur A au lieu de régler `vy` : un bouton gardé enfoncé ne déclenche qu'un saut, d'où l'impulsion une image sur deux.

```typescript
// Pilote automatique, pour filmer le GIF seulement
let sauts = [108, 262, 350, 434, 514]
let impulsion = false
game.onUpdate(function () {
    controller.right.setPressed(true)
    let sauter = false
    for (let s of sauts) {
        if (heros.x >= s && heros.x < s + 12) {
            sauter = true
        }
    }
    impulsion = sauter && !(impulsion)
    controller.A.setPressed(impulsion)
})
```

## Pièges constatés

- Une plateforme posée à une tuile au-dessus du sol laisse 16 pixels : le héros passe dessous mais ne peut pas y sauter.
- Le héros touche souvent deux tuiles de lave à la fois, et « lorsque … chevauche » se déclenche une fois par tuile : le `si la tuile centre … est lave` évite de perdre deux vies.
- Dans la boîte à outils d'un tutoriel, les blocs arrivent avec `mySprite` et des valeurs par défaut : les blocs `blockconfig.global` et `blockconfig.local` les font arriver avec `heros`, `vx 80 vy 0`, `location`.
- Le bloc « définir [tuile] à » arrive avec « col 0 ligne 0 », pas avec `location`.
- Certains blocs restent en anglais dans l'éditeur lui-même (« camera suit sprite », « location », « Player », « My Tiles » / « Gallery ») : le texte les cite tels qu'ils s'affichent.
