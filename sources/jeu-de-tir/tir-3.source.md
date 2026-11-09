# Ta manette réagit

```template
game.splash("Mon jeu de tir", "Appuie sur A pour jouer")
scene.setBackgroundColor(15)
let heros = sprites.create(img`heros`, SpriteKind.Player)
heros.setPosition(20, 60)
controller.moveSprite(heros, 0, 100)
heros.setStayInScreen(true)
info.setLife(3)
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    let tir = sprites.createProjectileFromSprite(img`tir`, heros, 150, 0)
})
game.onUpdateInterval(900, function () {
    let ennemi = sprites.create(img`ennemi`, SpriteKind.Enemy)
    ennemi.setPosition(160, randint(10, 110))
    ennemi.vx = -40
    ennemi.setFlag(SpriteFlag.AutoDestroy, true)
})
sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Enemy, function (sprite, otherSprite) {
    sprites.destroy(sprite)
    sprites.destroy(otherSprite, effects.fire, 200)
    info.changeScoreBy(1)
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function (sprite, otherSprite) {
    sprites.destroy(otherSprite)
    info.changeLifeBy(-1)
    scene.cameraShake(4, 500)
})
game.onUpdateInterval(1000, function () {
    if (Math.percentChance(15)) {
        let coeur = sprites.create(img`coeur`, SpriteKind.Food)
        coeur.setPosition(160, randint(10, 110))
        coeur.vx = -30
        coeur.setFlag(SpriteFlag.AutoDestroy, true)
    }
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.Food, function (sprite, otherSprite) {
    sprites.destroy(otherSprite)
    info.changeLifeBy(1)
})
game.onUpdateInterval(3000, function () {
    let decor = sprites.create(img`decor`, SpriteKind.Player)
    decor.setPosition(160, randint(0, 120))
    decor.vx = -15
    decor.z = -1
    decor.setFlag(SpriteFlag.Ghost, true)
    decor.setFlag(SpriteFlag.AutoDestroy, true)
})
```

## Ta manette réagit @showdialog

Ton jeu va parler à ta manette micro:bit : elle sonne et s'allume quand tu détruis un ennemi, quand tu es touché, et elle affiche tes vies.

Les blocs sont dans la catégorie **Manette**.

## Au départ

Ta manette affiche tes vies dès que la partie commence.

- :gamepad: Dans ``||manette:Manette||``, prends ``||manette:manette afficher||`` et place-le dans ``||loops(noclick):au démarrage||``, juste sous **définir vie à 3**.
- :id card: Dans son trou, mets ``||info:vie||`` de ``||info:Info||``.

L'écran de démarrage attend la touche A : quand ce bloc s'exécute, ta manette est déjà branchée.

```blockconfig.local
manette.afficher(info.life())
```

```blocks
game.splash("Mon jeu de tir", "Appuie sur A pour jouer")
scene.setBackgroundColor(15)
let heros = sprites.create(img`heros`, SpriteKind.Player)
heros.setPosition(20, 60)
controller.moveSprite(heros, 0, 100)
heros.setStayInScreen(true)
info.setLife(3)
// @highlight
manette.afficher(info.life())
```

## Un ennemi détruit

Ta manette félicite chaque ennemi détruit.

- :gamepad: Dans ``||manette:Manette||``, prends ``||manette:manette réagir bien||`` et place-le à la fin du bloc **quand sprite de type Projectile chevauche otherSprite de type Enemy**.

```blockconfig.local
manette.reagir(ReactionManette.Bien)
```

```blocks
sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Enemy, function (sprite, otherSprite) {
    sprites.destroy(sprite)
    sprites.destroy(otherSprite, effects.fire, 200)
    info.changeScoreBy(1)
    // @highlight
    manette.reagir(ReactionManette.Bien)
})
```

## Touché

Ta manette prévient quand tu es touché, et montre les vies qui te restent.

- :gamepad: À la fin du bloc **quand sprite de type Player chevauche otherSprite de type Enemy**, ajoute ``||manette:manette réagir||`` et choisis **mal**.
- :gamepad: Puis ``||manette:manette afficher||``, avec ``||info:vie||`` de ``||info:Info||`` dans son trou.

```blockconfig.local
manette.reagir(ReactionManette.Mal)
manette.afficher(info.life())
```

```blocks
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function (sprite, otherSprite) {
    sprites.destroy(otherSprite)
    info.changeLifeBy(-1)
    scene.cameraShake(4, 500)
    // @highlight
    manette.reagir(ReactionManette.Mal)
    // @highlight
    manette.afficher(info.life())
})
```

## Le cœur aussi

Un cœur attrapé change aussi tes vies.

- :gamepad: À la fin du bloc **quand sprite de type Player chevauche otherSprite de type Food**, ajoute ``||manette:manette afficher||`` avec ``||info:vie||``.

```blocks
sprites.onOverlap(SpriteKind.Player, SpriteKind.Food, function (sprite, otherSprite) {
    sprites.destroy(otherSprite)
    info.changeLifeBy(1)
    // @highlight
    manette.afficher(info.life())
})
```

## Partage ton jeu @showdialog

Clique sur **Terminé**, puis sur **Partager**, et copie le lien de ton jeu.

C'est ce lien que tu colles dans la page relais, pour jouer avec ta manette.
