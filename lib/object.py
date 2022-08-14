"""Fichier contenant les méthodes relatives aux objets physiques
"""


class Object(pygame.sprite.Sprite):
    """Classe commune aux objets physiques
    
    Attributes:
        angle (float): Angle de l'objet, relatif à l'axe horizontal vers la droite, counter-clockwise == positif, en rad
        angleMomentum (float): Mouvement angulaire de l'objet, counter-clockwise (en rad)
        direction (Vector2): Direction de l'objet
        drawPos (tuple): Position d'affichage de l'objet, relatif au vaisseau joueur
        dying (bool): Si True, l'object est à supprimer
        dyingCounter (int): Temps nécessaire pour mourir
        explosionSprites (list): Images d'explosion
        forces (list): Forces appliquées à l'objet : Définit le mouvement / tick ([x, y])
        HP (int): Points de vie de l'objet. 0 == 'Mort'.
        image (image): Image de l'objet
        mask (pygame.mask.Mask): Masque de l'object, en gros : Sa hitbox
        mass (int): Masse en Kilogrammes (Init en tonnes)
        originalImage (Image): Image original de l'objet, utilisée pour tourner sans perdre la qualité
        originalOriginalImage (Image): Image original de l'objet, pour des raisons de stockage
        pos (list): Position de l'objet sur l'écran.
        previousPos (list): TODO : Collisions
        rect (rect): Surface d'affichage de l'objet, utile internement
        relative_x (int): Distance relative entre le joueur et l'objet sur l'axe X
        relative_y (int): Distance relative entre le joueur et l'objet sur l'axe Y
        savedRect (pygame.rect.Rect): TODO : Collisions
        spriteExplosionCounter (int): Temps entre chaque frame de l'explosion
        vectDistanceToPlayer (Vector2): Vecteur distance allant de l'objet au joueur
        velocity (Vector2): Vecteur vitesse de l'objet
        x (int): Coordonnée X de l'objet
        y (int): Coordonnée Y de l'objet
    
    Deleted Attributes:
        mouvement (Vector2): Vecteur mouvement de l'objet
        originalOriginialImage(Image): Image original de l'objet, pour des raisons de stockage
        drawRect (Rect): Position où mettre l'objet, il s'agit d'un Rect nécessaire à l'affichage
        Ec (float): Énergie cinétique en Newton
        mask (mask): Hitbox de l'objet
        angleAbsolu (float): L'angle toujours positif du vaisseau, relatif à l'axe horizontal, et clockwise
    """

    def __init__(self, life, pos, groupe, image, mass):
        """Constructeur de l'objet
        
        Args:
            life (int): PV de l'objet
            pos (tuple): Position de départ
            groupe (list): Groupe Pygame où mettre l'objet
            image (image): Image de l'objet à afficher
            mass (int): Masse de l'objet en tonnes
        """

        super().__init__(groupe)

        objects.add(self)

        self.forces = [0, 0]  # [x, y]
        self.HP = life

        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos  # La 'vraie' position de l'objet

        self.velocity = Vector2(self.forces)

        self.relative_x = self.x  # - player.x
        self.relative_y = self.y  # - player.y

        # Position relative au vaisseau Joueur
        self.drawPos = (self.relative_x + centered_screenWidth,
                        self.relative_y + centered_screenHeight)
        # Il s'agit de la position d'affichage de l'objet sur l'écran
        # Relative car le vaisseau est au milieu de l'écran en tout temps

        self.vectDistanceToPlayer = - \
            Vector2(self.drawPos[0] - centered_screenWidth, self.drawPos[1] - centered_screenHeight)

        self.image = image
        self.originalImage = image

        # self.rect = self.image.get_rect(center=self.pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.angleMomentum = 0.0
        self.angle = 0.0  # à droite !

        self.dying = False
        self.dyingCounter = len(explosionImages) - 1
        self.spriteExplosionCounter = 0
        self.explosionSprites = iter(explosionImages)

        self.originalOriginalImage = image

        self.mass = mass * 1000  # Ici, mass est converti en Kg.
        if int(self.mass) == self.mass:  # si la masse n'a pas de virgules
            self.mass = int(self.mass)

        # self.Ec = 0.5 * self.mass * self.velocity.magnitude_squared()
        # 1/2 * m * v² , vive la physique

        # Initialise la direction vers la droite
        self.direction = Vector2(cos(self.angle), sin(self.angle))
        #  Utilise l'angle pour former un vecteur direction normalisé en utilisant le cercle trigonométrique
        #  cos(angle) retourne la longueur X du vecteur, sin(angle) la longueur Y, selon les axes du cercle.

    def __repr__(self):
        """Print customisé pour le debug
        """
        return f"""
---------------------------------------------------------------------------(Rounded)
        object {self.__class__.__name__} of mass = {self.mass} kg, and HP = {self.HP}
        Position is {round(self.x, 2), round(self.y, 2)}
        Forces are {round(self.forces[0], 2), round(self.forces[1], 2)}
        Angle : {round(self.angle, 2)} | AngleMomentum : {round(self.angleMomentum, 2)}
        Absolute Angle : {round(self.angleAbsolu, 2)}
        Velocity : {round(self.velocity.magnitude(), 2)} | Kinetic Energy : {round(self.Ec, 2)}
---------------------------------------------------------------------------
        """

    def die(self):
        """Fonction qui supprime l'objet
        """
        self.dying = True
        self.kill()

    def explode(self):
        """Le sprite va prendre les images d'une explosion, puis mourir
        """

        self.dying = True

        self.forces[0] *= 0.96
        self.forces[1] *= 0.96

        if self.spriteExplosionCounter == 0:

            if self.dyingCounter == 0:
                self.die()
            self.spriteExplosionCounter = 8
            self.dyingCounter -= 1
            self.originalImage = next(self.explosionSprites)

        self.spriteExplosionCounter -= 1

    def willExpire(self):
        """Si l'objet est trop éloigné, il disparaît, pour des raisons d'opti
        """
        if self.vectDistanceToPlayer.magnitude_squared() > 3686400:  # Pour des raisons d'opti
            # Équivalent à self.vectDistanceToPlayer.magnitude > 1920 * 2
            self.die()

    def rotate(self):
        """Permet de tourner l'objet
        """
        self.angle += self.angleMomentum

        self.image = pygame.transform.rotate(
            self.originalImage, - degrees(self.angle))  # Pourquoi ?
        self.rect = self.image.get_rect(center=self.drawPos)
        # self.rect = self.image.get_rect(center=self.pos)
        # redéfinition des attributs rect, image pour appliquer la rotation

        self.direction.update((cos(self.angle), sin(self.angle)))

    def getCollideTime(self, other):
        """Fonction qui rend le multiple du vecteur vitesse de chacun où la collision aurait eu lieu
        
        Args:
            other (Object): Objet avec qui trouver le temps de collision exact
        """

        self.savedRect = self.rect
        other.savedRect = other.rect

        self.previousPos = (self.pos[0] - self.velocity[0], self.pos[1] - self.velocity[1])
        other.previousPos = (other.pos[0] - other.velocity[0], other.pos[1] - other.velocity[1])

        self.savedRect.center = self.previousPos
        other.savedRect.center = other.previousPos

        while not pygame.sprite.collide_mask(self, other):

            self.savedRect.move_ip(self.velocity.elementwise() * 0.1)
            other.savedRect.move_ip(other.velocity.elementwise() * 0.1)

    def getNormalToSurface(self, myMask, other, collidePos):
        """Fonction qui retourne le vecteur normale à la surface fournie
        
        Args:
            myMask (Mask): Mask de l'objet qui appelle cette fonction
            other (Mask): Mask de l'autre objet
            collidePos (tuple): Position du point de collision entre les deux masks
        
        No Longer Returned:
            Vector2: Vecteur normal relatif à la collision
        """
        x, y = collidePos

        dx = myMask.overlap_area(other, (x + 1, y)) - myMask.overlap_area(other, (x - 1, y))
        dy = myMask.overlap_area(other, (x, y + 1)) - myMask.overlap_area(other, (x, y - 1))

        normal = -Vector2(dx, dy)
        """
        if normal.magnitude_squared() == 0:

            # sweep alg
        """

    def collisionManage(self):
        """Fonction qui vérifie la collision contre les autres objets
        """

        objects.remove(self)
        # Pour empêcher une collision avec soi-même

        collisionsPotentielles = pygame.sprite.spritecollide(self, objects, False, pygame.sprite.collide_circle)
        # Regarde les objets enfreignant le rectangle de self, pour éviter de générer les masks de tout les objets

        objects.add(self)

        if collisionsPotentielles:

            self.mask = pygame.mask.from_surface(self.image, threshold=254)

        for other in collisionsPotentielles:

            other.mask = pygame.mask.from_surface(other.image, threshold=254)

            if other.dying:
                continue

            if pygame.sprite.collide_mask(self, other) is not None:

                """
                self.mask = pygame.mask.from_surface(self.image, threshold=254)
                other.mask = pygame.mask.from_surface(other.image, threshold=254)

                collide_position = self.getCollideTime(other)
                normal = self.getNormalToSurface(self.mask, other.mask, collide_position)

                drawVector(normal, centeredPos(collide_position), "normal", (0, 200, 200))

                if normal.magnitude_squared() == 0:

                    continue

                normal.normalize_ip()

                self.normalVelocity = self.velocity.project(normal)
                other.normalVelocity = other.velocity.project(normal)

                self.finalNormalVel = None
                other.finalNormalVel = None

                self.finalNormalVel = (self.mass - other.mass) * self.normalVelocity + 2 * other.mass * other.normalVelocity
                self.finalNormalVel /= self.mass + other.mass

                other.finalNormalVel = (other.mass - self.mass) * other.normalVelocity + 2 * self.mass * self.normalVelocity
                other.finalNormalVel /= other.mass + self.mass

                damage = (self.finalNormalVel - other.finalNormalVel).magnitude()

                self.velocity = -self.finalNormalVel
                self.forces = self.velocity.xy

                other.velocity = other.finalNormalVel
                other.forces = other.velocity.xy
                """

                global score

                damage = (self.velocity - other.velocity).magnitude()

                if isinstance(self, Bullet):
                    if self.owner == "player":
                        player.HP += 2 if isinstance(other, Asteroid) else 6
                        player.ammo += 4
                        player.fuel += 8
                        if isinstance(other, redTeam) and other.HP - damage <= 0:
                            score += 25
                        elif isinstance(other, Asteroid) and other.HP - damage <= 0:
                            score += 5
                    if isinstance(other, redTeam):
                        if self.owner == other.ownership:
                            continue

                if isinstance(self, redTeam):
                    if isinstance(other, Bullet):
                        if self.ownership == other.owner:
                            continue

                if isinstance(self, Player):
                    if other.HP - damage <= 0:
                        if isinstance(other, redTeam):
                            player.HP += 3
                            score += 25

                if isinstance(self, Player):
                    self.shieldCounter = 300
                    if self.shieldHP > 0:
                        self.shieldHP -= damage
                        self.shieldAlphaCounter = 255
                        other.HP -= damage
                        continue
                elif isinstance(other, Player):
                    other.shieldCounter = 300
                    if other.shieldHP > 0:
                        other.shieldHP -= damage
                        other.shieldAlphaCounter = 255
                        self.HP -= damage
                        continue

                self.HP -= damage
                other.HP -= damage

    def update(self):
        """Actualise la position de l'objet selon les forces appliquées.
        """
        self.x += self.forces[0]  # pos X += force X
        self.y += self.forces[1]  # pos Y += force Y
        self.pos = (self.x, self.y)

        self.relative_x = self.x - player.x
        self.relative_y = self.y - player.y
        self.drawPos = (self.relative_x + centered_screenWidth,
                        self.relative_y + centered_screenHeight)

        # self.rect.center = self.pos
        self.rect.center = self.drawPos  # modifie l'emplacement d'affichage vers ces coordonéees
        self.velocity = Vector2(self.forces)

        self.vectDistanceToPlayer = - \
            Vector2(self.drawPos[0] - centered_screenWidth, self.drawPos[1] - centered_screenHeight)

        # self.Ec = 0.5 * self.mass * self.velocity.magnitude_squared()  # TODO : Calculer ça avant collision

        self.rotate()
        self.willExpire()

        if not self.dying:

            self.collisionManage()

            if self.HP <= 0:
                self.explode()

        else:
            self.explode()

    def draw(self):
        """Fonction qui dessine l'objet sur sa position
        """

        if abs(self.relative_x) - self.rect.w < centered_screenWidth and\
           abs(self.relative_y) - self.rect.h < centered_screenHeight:
            screen.blit(self.image, self.rect)

    def debug(self):
        """Affiche les vecteurs relatifs à l'objet
        """
        drawVector(self.direction * 50, self.drawPos, "Direction")
        drawVector(self.velocity * 15, self.drawPos, "Velocity", color=(200, 50, 70))
        # drawVector(self.vectDistanceToPlayer, self.drawPos, "Dist", color=(0, 255, 0))
