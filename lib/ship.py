"""Fichier contenant les méthodes relatives aux vaisseaux
"""


class Ship(Object):

    """Classe commune aux vaisseaux

    Attributes:
        ammoClock (int): Horloge qui règle la cadence de tire sans utiliser de "multithreading"
        ammoTimer (TYPE): Description
        fireOffset (TYPE): Description
        firingMouvementImages (list): Liste des images du vaisseau avec le propulseur ET le(s) éclat(s) du(des) canon(s)
        forceTir (list): Les forces que va recevoir la ou les balle(s) tirées par le vaisseau
        HP (int): PV du vaisseau
        maxHP (int): PV maximum du vaisseau
        mouvementImages (list): Liste des images du vaisseau avec le propulseur activé
        propulseur (float): Valeur de la force générée par le propulseur du vaisseau
        puissanceCanon (int): Valeur de la puissance du ou des canon(s) du vaisseau
        spriteChangeCounter (int): Clock qui va delayer l'affichage des futurs sprites de propulsion
        spriteFiringCounter (int): Clock qui va définir le temps d'affichage des éclats des canons lors du tir

    Deleted Attributes:
        angle (float): Direction du vaisseau en rad, counter-clockwise
    """

    def __init__(self, life, pos, groupe, image, mass, puissanceCanon, ammoTimer, fireOffset=0):
        """Constructeur du vaisseau

        Args:
            life (int): PV du vaisseau
            pos (tuple): Position de départ
            groupe (list): Groupe Pygame où mettre le vaisseau
            image (image): Image du vaisseau
            mass (int): Masse du vaisseau en kilogrammes (introduit en tonnes)
            puissanceCanon (int): Puissance du canon. Plus c'est élevé plus la balle tirée est rapide
            ammoTimer (int): Temps entre chaque tire. Correspond à un délai entre tirs de ammoTimer/60 secondes
            fireOffset (int, optional): Point d'apparition décalé de la balle tirée
        """

        super().__init__(life, pos, groupe, image, mass)

        self.propulseur = 0.0
        # La force du propulseur du vaisseau

        self.ammoClock = 0
        # Clock qui cadence la vitesse des tirs

        self.maxHP = life

        self.fireOffset = fireOffset

        self.puissanceCanon = puissanceCanon
        # Puissance des tirs du vaisseau

        self.forceTir = [self.puissanceCanon * cos(self.angle) + self.forces[0],
                         self.puissanceCanon * sin(self.angle) + self.forces[1]]
        # Fonctionne en tandem avec puissance canon, c'est les forces du bullet tiré par le vaisseau

        self.mouvementImages = []
        self.firingMouvementImages = []
        # Différents sprites pour afficher le propulseur et l'explosion des tirs !

        self.spriteFiringCounter = 0
        # Délais en ticks de l'affichage de l'explosion devant le(s) canon(s) du vaisseau
        self.spriteChangeCounter = 0
        # Délaits en ticks entre l'affichage des différents sprites du vaisseau en propulsion

        self.ammoTimer = ammoTimer
        self.width, self.height = self.rect.w, self.rect.h

    def fire(self):
        """Fait tirer des balles du vaisseau
        """

        self.ammoClock -= 1 if self.ammoClock != 0 else 0

        if self.ammoClock == 0:

            bullets.add(Bullet(1, (self.x + cos(self.angle) * self.fireOffset + self.fireOffset * sin(self.angle),
                                   self.y + sin(self.angle) * self.fireOffset - self.fireOffset * cos(self.angle)),
                               bullets, bulletImage, self.forceTir, self.angle, 0.05, self.ownership))

            self.ammoClock = self.ammoTimer

    def healthbar(self):
        """Affiche une barre de vie
        """

        drawRectPos = (self.drawPos[0] - self.width * 0.33, self.drawPos[1] + self.height * 0.5)
        pygame.draw.rect(screen, (190, 30, 30), (drawRectPos, (self.maxHP / 10, 5)))
        pygame.draw.rect(screen, (0, 255, 0), (drawRectPos, (self.HP / 10, 5)))

        if isinstance(self, Player):
            pygame.draw.rect(screen, (255, 0, 255), (drawRectPos,
                                                     (self.fuel / self.max_fuel * (self.maxHP / 10), 2)))
            myFont.render_to(screen, (drawRectPos[0] - 10, drawRectPos[1]),
                             f"{self.ammo}", fgcolor=(255, 255, 255), size=10)
            pygame.draw.rect(screen, (0, 70, 255), ((drawRectPos[0], drawRectPos[1] + 2),
                                                    (self.shieldHP / self.max_shieldHP * (self.maxHP / 10), 3)))

    def update(self):
        """Actualise le vaisseau
        """

        super().update()

        self.forces[0] += cos(self.angle) * self.propulseur
        self.forces[1] += sin(self.angle) * self.propulseur
        # Permet d'ajouter aux forces le travail du propulseur !

        if not self.dying:
            self.healthbar()

        if self.HP > self.maxHP:
            self.HP = self.maxHP

        self.forceTir = [self.puissanceCanon * cos(self.angle) + self.forces[0],
                         self.puissanceCanon * sin(self.angle) + self.forces[1]]
