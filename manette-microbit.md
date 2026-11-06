# Programme de la manette micro:bit

Le micro:bit est branché en USB à l'ordinateur. La page relais lit ce qu'il écrit sur la liaison série et le transmet au jeu ; elle lui renvoie les réactions demandées par le jeu.

## Le contrat

| Sens | Un mot par ligne |
|---|---|
| Manette → jeu | `gauche`, `droite`, `haut`, `bas`, `A`, `B`, `menu` |
| Jeu → manette | `bip`, `bien`, `mal`, `alerte`, `gagne`, `perdu`, ou un chiffre de 0 à 9 |

Le vocabulaire jeu → manette est générique : il dit ce qui se passe, pas ce que la manette doit jouer. Chaque manette choisit son son, son icône ou son geste. Un mot inconnu s'affiche sur l'écran du micro:bit.

## Version boucle (à tester en premier)

Publiée : https://makecode.microbit.org/_Tb5WrvHCc2Dq

Une boucle lit les lignes reçues. Sur le pont du parcours Objets connectés, une boucle de lecture ne perdait aucune ligne, contre environ 6 % pour l'événement « quand une donnée est reçue ».

```typescript
// Le tampon de réception fait 20 octets par défaut : on lui donne de la marge.
serial.setRxBufferSize(128)
serial.setTxBufferSize(64)
// Du jeu vers la manette : une boucle qui lit, plutôt qu'un événement qui perd des lignes.
basic.forever(function () {
    let mot = serial.readUntil(serial.delimiters(Delimiters.NewLine))
    if (mot == "bip") {
        music.play(music.tonePlayable(988, music.beat(BeatFraction.Sixteenth)), music.PlaybackMode.InBackground)
    } else if (mot == "bien") {
        music.play(music.tonePlayable(1319, music.beat(BeatFraction.Sixteenth)), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.Yes)
    } else if (mot == "mal") {
        music.play(music.tonePlayable(131, music.beat(BeatFraction.Quarter)), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.No)
    } else if (mot == "alerte") {
        music.play(music.builtInPlayableMelody(Melodies.BaDing), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.Surprised)
    } else if (mot == "gagne") {
        music.play(music.builtInPlayableMelody(Melodies.PowerUp), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.Happy)
    } else if (mot == "perdu") {
        music.play(music.builtInPlayableMelody(Melodies.Wawawawaa), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.Sad)
    } else {
        // Un chiffre (vies, tour, combo) s'affiche d'un coup, sans défiler.
        basic.showString(mot)
    }
})
// De la manette vers le jeu : l'inclinaison donne la direction, A et B les deux boutons, le logo le menu.
basic.forever(function () {
    if (input.acceleration(Dimension.X) < -300) {
        serial.writeLine("gauche")
    } else if (input.acceleration(Dimension.X) > 300) {
        serial.writeLine("droite")
    }
    if (input.acceleration(Dimension.Y) < -300) {
        serial.writeLine("haut")
    } else if (input.acceleration(Dimension.Y) > 300) {
        serial.writeLine("bas")
    }
    if (input.buttonIsPressed(Button.A)) {
        serial.writeLine("A")
    }
    if (input.buttonIsPressed(Button.B)) {
        serial.writeLine("B")
    }
    if (input.logoIsPressed()) {
        serial.writeLine("menu")
    }
    basic.pause(20)
})
```

## Version événement

Publiée : https://makecode.microbit.org/_9KwAkm9hUAi3

```typescript
// Les tampons série font 20 octets par défaut. Trop petits, ils perdent des lettres :
// à la réception pendant qu'une icône s'affiche, à l'envoi quand plusieurs mots partent ensemble.
serial.setRxBufferSize(128)
serial.setTxBufferSize(64)
// Du jeu vers la manette : un événement, et non une boucle qui lit.
// Une boucle qui attend une ligne occupe la liaison série et fait perdre des lettres à l'envoi.
serial.onDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let mot = serial.readUntil(serial.delimiters(Delimiters.NewLine))
    if (mot == "bip") {
        music.play(music.tonePlayable(988, music.beat(BeatFraction.Sixteenth)), music.PlaybackMode.InBackground)
    } else if (mot == "bien") {
        music.play(music.tonePlayable(1319, music.beat(BeatFraction.Sixteenth)), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.Yes)
    } else if (mot == "mal") {
        music.play(music.tonePlayable(131, music.beat(BeatFraction.Quarter)), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.No)
    } else if (mot == "alerte") {
        music.play(music.builtInPlayableMelody(Melodies.BaDing), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.Surprised)
    } else if (mot == "gagne") {
        music.play(music.builtInPlayableMelody(Melodies.PowerUp), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.Happy)
    } else if (mot == "perdu") {
        music.play(music.builtInPlayableMelody(Melodies.Wawawawaa), music.PlaybackMode.InBackground)
        basic.showIcon(IconNames.Sad)
    } else {
        // Un chiffre (vies, tour, combo) s'affiche d'un coup, sans défiler.
        basic.showString(mot)
    }
})
// De la manette vers le jeu : l'inclinaison donne la direction, A et B les deux boutons, le logo le menu.
basic.forever(function () {
    if (input.acceleration(Dimension.X) < -300) {
        serial.writeLine("gauche")
    } else if (input.acceleration(Dimension.X) > 300) {
        serial.writeLine("droite")
    }
    if (input.acceleration(Dimension.Y) < -300) {
        serial.writeLine("haut")
    } else if (input.acceleration(Dimension.Y) > 300) {
        serial.writeLine("bas")
    }
    if (input.buttonIsPressed(Button.A)) {
        serial.writeLine("A")
    }
    if (input.buttonIsPressed(Button.B)) {
        serial.writeLine("B")
    }
    if (input.logoIsPressed()) {
        serial.writeLine("menu")
    }
    basic.pause(20)
})
```

## Pièges constatés

- **Un onglet MakeCode resté connecté au micro:bit vole des caractères** sur la liaison série : la page reçoit des mots tronqués (`guche`, `ba`). La page relais l'affiche en alerte orange après 3 mots inconnus en 2 secondes. Fermer l'onglet, ou ⋯ à côté de Télécharger → Déconnecter.
- Les tampons série du micro:bit font 20 octets par défaut. Une icône ou un texte qui défile pendant la réception les fait déborder : d'où les mots courts, `setRxBufferSize(128)` et `setTxBufferSize(64)`.
- `basic.showString` d'un mot long bloque la boucle le temps du défilement : réserver l'affichage aux chiffres.
- Un interrupteur sur P0 : `pins.setAudioPinEnabled(false)`, sinon le son passe par P0.
