"""Fichier contenant les méthodes relatives aux balles
"""


class Bullet(Object):
    """Classe spécifique aux balles, munitions cinétiques
    
    Attributes:
        angle (float): Angle de la balle, direction
        forces (list): Forces [x, y] de la balle
    """

    def __init__(self, life, pos, groupe, image, forces, angle, mass, owner=None):
        """Initialise la balle tirée !
        
        Args:
            life (int): Résistance de la balle : Détruite si == 0
            pos (tuple): Position de départ de la balle
            groupe (list): Groupe où mettre la balle
            image (image): Image de la munition, à changer
            forces (list): Forces de départ de la balle
            angle (float): Angle, direction, de la balle
            mass (int): Masse de la balle en KG (introduit en tonnes)
            owner (str, optional): Nom du type de vaisseau qui a tiré la balle
        """
        super().__init__(life, pos, groupe, image, mass)

        self.forces = forces
        self.angle = angle

        self.owner = owner

    def explode(self):
        """Override de Object.explode() pour éviter l'explosion des balles
        """
        self.die()
