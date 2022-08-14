"""Fichier contenant les méthodes relatives au joueur
"""


class Player(Ship):

    """Classe spécifique au vaisseau du joueur
    
    Attributes:
        ammoClock (int): Horlorge qui règle la cadence de tire sans utiliser de "multithreading"
        firingImage (TYPE): Description
        firingMouvementImages (list): Liste des images du vaisseau avec le propulseur ET les éclats des canons
        image (image): Image actuelle du vaisseau joueur
        mouvementImages (list): Liste des images du vaisseau avec le propulseur activé
        originalImage (image): Sert d'image "anchor" à tourner pour générer l'image actuelle, susceptible de changer
        spriteFiringCounter (int): Clock qui va définir le temps d'affichage des éclats des canons lors du tir
    
    Deleted Attributes:
        angle (float): Angle du joueur en rad counter-clockwise
        toTurnTest (float): Test d'une fonction qui utilise un truc complexe que je comprends pas, négatif == à gauche
        puissanceCanon (int): Valeur de la puissance des canons du joueur
        angleMomentum (float): Mouvement angulaire du joueur
        spriteChangeCounter (int): Clock qui va delayer l'affichage des futurs sprites de propulsion
    """

    def __init__(self, life, pos, groupe, mass, puissanceCanon):
        """Constructeur du joueur
        
        Args:
            life (int): PV du joueur
            pos (tuple): Position de départ
            groupe (list): Groupe Pygame où mettre le vaisseau
            mass (int): Masse du vaisseau joueur en tonnes
            puissanceCanon (int): Puissance des canons du joueur
        """

        self.image = VaisseauJoueur

        super().__init__(life, pos, groupe, self.image, mass, puissanceCanon, 30, 20)

        self.mouvementImages = cycle([pygame.transform.scale(pygame.image.load(i).convert_alpha(), (64, 64))
                                      for i in glob.glob("assets/playerSprites/vaisseau*.png")])
        self.firingMouvementImages = cycle([pygame.transform.scale(pygame.image.load(i).convert_alpha(), (64, 64))
                                            for i in glob.glob("assets/playerSprites/firingvaisseau*.png")])
        self.firingImage = pygame.transform.scale(
            pygame.image.load("assets/playerSprites/firing.png").convert_alpha(), (64, 64))

        self.fuel = 600  # 5 secondes continues
        self.max_fuel = self.fuel
        self.fuelTimer = 0

        self.ammo = 40
        self.ammoReloadTimer = 300
        self.max_ammo = self.ammo

        self.shieldHP = 150
        self.max_shieldHP = self.shieldHP
        self.shieldCounter = 0

        self.shieldAlphaCounter = 0

    def manageCounters(self):
        """Fonction qui gère les "clocks" du vaisseau
        """
        self.ammoClock -= 1 if self.ammoClock != 0 else 0
        self.spriteFiringCounter -= 1 if self.spriteFiringCounter != 0 else 0
        self.spriteChangeCounter -= 1 if self.spriteChangeCounter != 0 else 0

        # print(self.ammoClock, self.spriteFiringCounter, self.spriteChangeCounter)

    def updateSpriteMouvement(self, utiliseLePropulseur):
        """Fonction qui va afficher le feu bleu du propulseur lors du mouvement, et l'effet des canons
        
        Args:
            utiliseLePropulseur (bool): True si le propulseur est en cours d'utilisation
        """
        if self.spriteFiringCounter != 0 and utiliseLePropulseur:  # si le vaisseau tire et bouge
            if self.spriteChangeCounter == 0:  # Si il temps de changer le sprite
                self.originalImage = next(self.firingMouvementImages)
        elif self.spriteFiringCounter != 0 and not utiliseLePropulseur:  # si le vaisseau tire juste
            self.originalImage = self.firingImage
        elif not self.spriteFiringCounter != 0 and utiliseLePropulseur:  # si le vaisseau bouge
            if self.spriteChangeCounter == 0:
                self.originalImage = next(self.mouvementImages)
        else:
            self.originalImage = self.originalOriginalImage

    def fire(self):
        """Fait tirer deux bullets du vaisseau
        """

        if self.ammoClock == 0 and self.ammo >= 2:

            self.ammoReloadTimer = 300

            bullets.add(Bullet(1, (self.pos[0] + cos(self.angle) * 20 + 20 * sin(self.angle),
                                   self.pos[1] + sin(self.angle) * 20 - 20 * cos(self.angle)),
                               bullets, bulletImage, self.forceTir, self.angle, 0.05, "player"))
            bullets.add(Bullet(1, (self.pos[0] + cos(self.angle) * 20 - 20 * sin(self.angle),
                                   self.pos[1] + sin(self.angle) * 20 + 20 * cos(self.angle)),
                               bullets, bulletImage, self.forceTir, self.angle, 0.05, "player"))
            self.ammoClock = 30
            self.ammo -= 2

            self.spriteFiringCounter = 8

    def kbControl(self):
        """Touches de contrôle du vaisseau
        """
        if key[pygame.K_UP] and self.fuel > 0:

            self.propulseur += 0.001 if self.propulseur < 0.2 else 0
            self.fuel -= 2
            self.fuelTimer = 30 if self.fuel > 0 else 90

        else:  # diminution progressive du propulseur

            self.propulseur *= 0.7 if self.propulseur > 0.08 else 0

        if key[pygame.K_RIGHT]:

            self.angleMomentum += 0.001

        if key[pygame.K_LEFT]:

            self.angleMomentum -= 0.001

        if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            self.angleMomentum *= 0.80 if abs(self.angleMomentum) > 0.001 else 0

        if key[pygame.K_SPACE]:
            self.fire()

    def manageFuel(self):
        """Gère l'essence
        """
        if self.fuelTimer == 0:
            self.fuel = (self.fuel + 8) if self.fuel <= self.max_fuel else self.max_fuel
        self.fuelTimer -= 1 if self.fuelTimer > 0 else 0

    def manageAmmo(self):
        """Gère les munitions
        """
        self.ammoReloadTimer -= 1 if self.ammoReloadTimer > -60 else -60
        if self.ammoReloadTimer == 0:
            self.ammo += 2
        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo

    def manageShield(self):
        """Gère le bouclier
        """
        if self.shieldCounter == 0:
            self.shieldHP += 1
        self.shieldCounter -= 1 if self.shieldCounter > 0 else 0
        if self.shieldHP > self.max_shieldHP:
            self.shieldHP = self.max_shieldHP

        pygame.gfxdraw.filled_circle(screen, int(self.drawPos[0]), int(self.drawPos[1]), 36,
                                     (0, 255, 255, self.shieldAlphaCounter))

        self.shieldAlphaCounter -= 5 if self.shieldAlphaCounter > 0 else 0

    def update(self):
        """Actualise le joueur !
        """
        global restart, score

        super().update()

        if not self.dying:
            self.manageCounters()
            self.updateSpriteMouvement(key[pygame.K_UP] and self.fuel > 0)
            self.kbControl()
            self.manageFuel()
            self.manageAmmo()
            self.manageShield()

        else:
            restart = True
