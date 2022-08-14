"""Fichier contenant la classe relative aux astéroïdes
"""


class Asteroid(Object):
    """Classe qui représente les astéroïdes
    
    Attributes:
        angle (float): Angle de l'astéroïde
        angleMomentum (float): Moment angulaire de l'astéroïde
        forces (list): Forces de mouvement
        HP (int): PV de l'astéroïde
        image (image): Image choisie pour l'astéroïde
        mass (int): Masse de l'astéroïde
        randomSeed (int): Booléen random
        scale (tuple): Ratios de chaque dimension de l'astéroïde entre l'image original et l'image réel
        scaleFactor (int): Facteur de grandissement
    """

    def __init__(self, pos):
        """Initialise l'astéroïde
        
        Args:
            pos (tuple): Position de départ
        
        Deleted Parameters:
            life (int): PV de l'objet
            image (image): Image de l'objet à afficher
        """
        self.randomSeed = randint(0, 1)
        if self.randomSeed == 0:
            self.scaleFactor = randint(50, 90)
            self.scale = (self.scaleFactor, self.scaleFactor * uniform(0.7, 1.3))
        else:
            self.scaleFactor = randint(50, 90)
            self.scale = (self.scaleFactor * uniform(0.7, 1.3), self.scaleFactor)
        self.image = pygame.transform.scale(choice(asteroidImages), self.scale)
        self.mass = (self.scale[0] * self.scale[1] * 5) // 1000
        # Le 5 est arbitraire, mass est en tonnes d'où le // 1000

        self.HP = self.mass * uniform(2.2, 3.6)

        super().__init__(self.HP, pos, objects, self.image, self.mass)

        self.angle = angleBetweenVectors(
            self.direction, self.vectDistanceToPlayer) + randint(-10, 10)
        self.forces = [uniform(0.8, 1.2) * cos(self.angle) + player.forces[0] * 1.02,
                       uniform(0.8, 1.2) * sin(self.angle) + player.forces[1] * 1.02]
        self.angleMomentum = uniform(-0.050, 0.050)
