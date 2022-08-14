"""Fichier principale permettant de tourner le jeu

Attributes:
    asteroids (list): Liste contenants les images des différents types d'astéroïdes
    bullets (pygame.sprite.Group): Groupe contenant toutes les balles
    centered_screenHeight (int): Moitié de la hauteur de l'écran
    centered_screenWidth (int): Moitié de la largeur de l'écran
    clock (pygame.time.Clock): Gère le jeu tel qu'il tourne un certain nombre de fois par seconde
    highscore (int): Le meilleur score de la session
    key (list): Tableau des booléens relatifs à chaque touche du clavier
    loop (bool): Gère la boucle du jeu
    myFont (pygame.font.Font): Police d'écriture de base
    objects (pygame.sprite.Group): Groupe gérant tout les objets physique
    pi_mul_2 (float): Shortcut pour plus de perf
    possibleEnemies (list): Liste des classes ennemies
    restart (bool): Si True, le jeu est prêt à être relancé
    screen (Surface): Surface où sont dessinées les objects
    screenInfo (VideoInfo): Toutes les informations relatifs à l'écran
    ships (pygame.sprite.Group): Groupe relatif aux vaisseaux
    stars (set): Liste de positions et caractéristiques des étoiles
    tickRate (int): Le nombre de fois où le jeu tourne par seconde
    vecFont (pygame.font.Font): Police d'écriture spécifique aux vecteurs

Deleted Attributes:
    player (Player): Le vaisseau du joueur
"""

import pygame
import glob

import pygame.locals
import pygame.gfxdraw
from pygame import Vector2

from math import cos, sin, degrees, pi, radians, atan2, floor, exp, copysign
from itertools import cycle
from random import randint, choice, uniform


pygame.init()

clock = pygame.time.Clock()
tickRate = 60
randomTick: int

restart = False

highscore = 0

pi_mul_2 = 2 * pi


# paramètres écran

screenInfo = pygame.display.Info()

screenWidth, screenHeight = screenInfo.current_w, screenInfo.current_h
screen = pygame.display.set_mode((screenWidth, screenHeight))

screen.fill((20, 20, 20))

centered_screenWidth = screenWidth // 2
centered_screenHeight = screenHeight // 2
#  Centrées sur le centre de l'écran

loop = True
# boucle du programme

key = None  # init de clavier

stars = set()


def execfile(filename):
    """Exécute un fichier .py dans la même instance : Disparu depuis Python 2 :(
    
    Args:
        filename (str): Chemin vers le fichier à exécuter
    """
    with open(filename, "rb") as f:
        exec(compile(f.read(), filename, 'exec'), globals())


execfile("lib/object.py")
execfile("lib/bullet.py")
execfile("lib/ship.py")
execfile("lib/player.py")
execfile("lib/asteroid.py")
execfile("lib/red/redTeam.py")
execfile("lib/red/blaster.py")
execfile("lib/red/shooter.py")
execfile("lib/red/sniper.py")

possibleEnemies = [redShooter, redSniper, redBlaster]

objects = pygame.sprite.Group()  # Groupe tenant tout les objets, donc tout ce qui est physique
ships = pygame.sprite.Group()  # Groupe tenant tout les vaisseaux.
asteroids = pygame.sprite.Group()  # Groupe tenant tout les astéroïdes
bullets = pygame.sprite.Group()

myFont = pygame.freetype.SysFont("arial", 10)
vecFont = pygame.freetype.SysFont("arial", 10, italic=True)

# surroundings = pygame.Rect((0, 0), (screenWidth, screenHeight))
# surroundings.center = (centered_screenWidth, centered_screenHeight)


def chargerImages():
    """Charge toutes les images utilisées dans des variables globales
    """
    global VaisseauJoueur, asteroidImages, bulletImage, explosionImages
    global shooterRedSprite, blasterRedSprite, sniperRedSprite

    VaisseauJoueur = pygame.image.load("assets/playerSprites/Vaisseau.jpg").convert_alpha()
    VaisseauJoueur = pygame.transform.scale(VaisseauJoueur, (64, 64))

    asteroidImages = [pygame.image.load(i).convert_alpha()
                      for i in glob.glob("assets/asteroids/asteroid*.png")]
    # retourne toute les images d'astéroïdes dans une liste

    bulletImage = pygame.image.load("assets/bullet.png").convert_alpha()
    bulletImage = pygame.transform.scale(bulletImage, (10, 10))

    explosionImages = [pygame.image.load(i).convert_alpha()
                       for i in sorted(glob.glob("assets/explosionSprites/*.png"))]

    shooterRedSprite = pygame.image.load("assets/redTeamSprites/redShooter.png")
    blasterRedSprite = pygame.image.load("assets/redTeamSprites/redBlaster.png")
    sniperRedSprite = pygame.image.load("assets/redTeamSprites/redSniper.png")


def centeredPos(pos):
    """Fonction qui retourne la position centrée sur l'écran
    
    Args:
        pos (iter): Position à centrer
    
    Returns:
        tuple: Position centrée au milieu de l'écran
    """

    return (pos[0] + centered_screenWidth, pos[1] + centered_screenHeight)


def drawVector(Vector, startPos, name, color=(255, 0, 0)):
    """Dessine le vecteur sur l'écran : DEBUG
    
    Args:
        Vector (Vector2): Le vecteur à dessiner
        startPos (tuple): La position d'où dessiner le vecteur
        name (str): Nom du vecteur à afficher
        color (tuple, optional): Couleur du vecteur
    """

    pygame.draw.aaline(screen, color, startPos, (startPos[0] + Vector[0], startPos[1] + Vector[1]))

    textPos = Vector2(startPos) + Vector
    if not (textPos[0] < 0 or textPos[1] < 0):  # Pour contrer un bug pygame, voir CdC
        vecFont.render_to(screen, textPos, name, fgcolor=color)


def angleBetweenVectors(Vector1, Vector2):
    """Retourne l'angle entre deux vecteurs, TEST
    
    Args:
        Vector1 (Vector2): Premier vecteur
        Vector2 (Vector2): Deuxième vecteur
    
    Returns:
        float: Angle entre les deux vecteurs, en radians
    """

    angleResultant = atan2(Vector1.cross(Vector2), Vector1.dot(Vector2))

    return angleResultant


def visibleCurseur(option):
    """Change la visibilité du curseur windows
    
    Args:
        option (bool): True si le curseur doit être visible, False sinon.
    """

    if option is True:
        pygame.mouse.set_visible(True)
    else:
        pygame.mouse.set_visible(False)


def loopControl():
    """Contrôle la loop du jeu
    """
    global loop
    if key[pygame.K_ESCAPE]:
        loop = False


def toggleDebug():
    """Contrôle l'affichage des vecteurs relatifs aux objects
    """
    if key[pygame.K_F1]:
        for instance in objects:
            instance.debug()


def _randomTick():
    """Permet de créer une variable aléatoire utile pour le déroulement des évènements du jeu
    """
    global randomTick

    randomTick = randint(0, 10000)


def manageAsteroid():
    """Gère l'apparition d'astéroïdes
    """
    dist = 1200
    if randomTick < 5000 and len(asteroids) < 50:
        position = (floor(player.x + randint(-dist, -(dist * 0.2))
                          if randint(0, 1) == 1 else floor(player.x + randint(dist * 0.2, dist))),
                    floor(player.y + randint(-dist, -(dist * 0.2))
                          if randint(0, 1) == 1 else floor(player.y + randint(dist * 0.2, dist))))

        asteroids.add(Asteroid(position))


def manageStars():
    """Gère l'affichage des étoiles
    """
    for (starPosX, starPosY), layer, color in stars:

        drawPosX = int(starPosX - player.x * layer) % screenWidth
        drawPosY = int(starPosY - player.y * layer) % screenHeight

        pygame.gfxdraw.pixel(screen, drawPosX, drawPosY, color)


def genStars():
    """Fait apparaître des étoiles au lancement
    """
    for _ in range(randint(3000, 12000)):
        stars.add(((randint(0, screenWidth), randint(0, screenHeight)),
                   1 / randint(3, 12), (randint(170, 255), randint(170, 255), randint(170, 255))))
        # (Pos, layer, color)


def manageEnemies():
    """Fait apparaître des ennemis
    """
    dist = 1200
    if randomTick < 500 and len(ships) < 6:
        position = (int(player.x + randint(-dist, -(dist * 0.5))
                        if randint(0, 1) == 1 else randint(dist * 0.5, dist)),
                    int(player.y + randint(-dist, -(dist * 0.5))
                        if randint(0, 1) == 1 else randint(dist * 0.5, dist)))

        ships.add(choice(possibleEnemies)(position))


def updateGame():
    """Fonction qui actualise tout les objects, et affiche tout : C'est un Tick
    """

    manageStars()
    manageAsteroid()
    manageEnemies()

    objects.update()
    objects.draw(screen)

    pygame.event.pump()
    pygame.display.flip()


chargerImages()

"""
position = (floor(centered_screenWidth + randint(-200, -(200 * 0.5))
                  if randint(0, 1) == 1 else randint(200 * 0.5, 200)),
            floor(centered_screenHeight + randint(-200, -(200 * 0.5))
                  if randint(0, 1) == 1 else randint(200 * 0.5, 200)))

asteroids.add(Asteroid(position))
"""

genStars()

visibleCurseur(False)

while loop:

    objects = pygame.sprite.Group()
    ships = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player(300, (centered_screenWidth, centered_screenHeight), ships, 500, 40)

    score = 0

    while loop:

        clock.tick(tickRate)

        screen.fill((20, 20, 20))  # Toujours en premier !

        key = pygame.key.get_pressed()  # Partie clavier, j'espère
        loopControl()
        toggleDebug()
        _randomTick()

        if restart is True:

            myFont.render_to(screen, (centered_screenWidth * 0.5, centered_screenHeight * 0.5),
                             "GAME OVER", fgcolor=(200, 30, 30), size=165)
            myFont.render_to(screen, (centered_screenWidth // 1.5, centered_screenHeight),
                             f"Your score is {score}", fgcolor=(30, 100, 120), size=40)
            if score > highscore:
                myFont.render_to(screen, (centered_screenWidth // 1.5, centered_screenHeight * 1.2),
                                 f"New highscore ! Previous was {highscore}", fgcolor=(30, 100, 120), size=40)
            else:
                myFont.render_to(screen, (centered_screenWidth // 1.5, centered_screenHeight * 1.2),
                                 f"Highscore : {highscore}", fgcolor=(30, 150, 120), size=40)
            myFont.render_to(screen, (centered_screenWidth // 1.5, centered_screenHeight * 1.4),
                             "Press enter to restart", fgcolor=(30, 100, 120), size=60)

            if key[pygame.K_RETURN] is True:
                break

        updateGame()

    restart = False
    highscore = score if score > highscore else highscore


visibleCurseur(True)

pygame.quit()
