/**
 * Manette micro:bit pour MakeCode Arcade.
 * La page relais reçoit les mots du micro:bit par la liaison série et les transmet au jeu :
 * la manette appuie alors sur les mêmes boutons que le clavier. Rien à faire dans le jeu.
 */
/** Ce que la manette sait faire, quel que soit le jeu. */
enum ReactionManette {
    //% block="bip"
    Bip,
    //% block="bien"
    Bien,
    //% block="mal"
    Mal,
    //% block="alerte"
    Alerte,
    //% block="gagne"
    Gagne,
    //% block="perdu"
    Perdu
}

//% color="#1e90ff" icon="" block="Manette"
namespace manette {
    // Un bit par bouton, dans l'ordre de la page relais.
    const BOUTONS = [controller.left, controller.right, controller.up, controller.down, controller.A, controller.B, controller.menu]
    let precedent = 0

    function recevoir(msg: Buffer) {
        const etat = msg[0]
        for (let i = 0; i < BOUTONS.length; i++) {
            const bit = 1 << i
            // Seuls les boutons qui changent sont touchés : le clavier garde la main sur les autres.
            if ((etat & bit) != (precedent & bit)) BOUTONS[i].setPressed((etat & bit) != 0)
        }
        precedent = etat
    }
    control.simmessages.onReceived("manette", recevoir)
    // Chaque nouvelle scène (écran de démarrage, game over) a ses propres événements :
    // on y rebranche la réception, sinon la manette ne répond plus.
    game.addScenePushHandler(function () {
        control.simmessages.onReceived("manette", recevoir)
    })

    // Les réactions de la manette, dans l'ordre de l'énumération ReactionManette.
    const MOTS = ["bip", "bien", "mal", "alerte", "gagne", "perdu"]

    /**
     * Demande une réaction à la manette. Chaque manette choisit son son, son image ou son geste.
     */
    //% block="manette réagir $reaction"
    //% weight=100
    export function reagir(reaction: ReactionManette) {
        envoyer(MOTS[reaction])
    }

    /**
     * Affiche un chiffre de 0 à 9 sur la manette : des vies, un tour, un combo.
     */
    //% block="manette afficher $nombre"
    //% nombre.min=0 nombre.max=9
    //% weight=90
    export function afficher(nombre: number) {
        envoyer(convertToText(Math.constrain(Math.round(nombre), 0, 9)))
    }

    /**
     * Envoie un mot libre à la manette, qui doit savoir quoi en faire.
     * @param mot le mot à envoyer, 5 lettres au plus
     */
    //% block="manette envoyer $mot"
    //% mot.defl="bip"
    //% advanced=true
    export function envoyer(mot: string) {
        control.simmessages.send("manette-retour", Buffer.fromUTF8(mot))
    }
}
