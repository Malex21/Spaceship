"""Fichier relative aux vaisseaux rouges
"""


class redTeam(Ship):
    """Classe relative au 'shooter' rouge
    
    Attributes:
        angle (float): Angle de l'objet, relatif à l'axe horizontal vers la droite, counter-clockwise == positif, en rad
        distToPlayer (float): Distance entre le vaisseau et le joueur
        dotFront (float): Valeur du produit scalaire entre direction et vecDistToPlayer
        firingDistance (int): Distance de tir maximum
        forces (list): Forces du vaisseau
        ownership (str): Nom d'appartenance donné à la balle tirée
        propulseur (float): Accélération actuelle du propulseur
    """

    def __init__(self, life, pos, groupe, image, mass, puissanceCanon, ammoTimer):
        """Redéfinition des certaines fonctions
        
        Args:
            life (int): PV du vaisseau
            pos (tuple): Position de départ
            groupe (list): Groupe Pygame où mettre le vaisseau
            image (image): Image du vaisseau
            mass (int): Masse du vaisseau en kilogrammes (introduit en tonnes)
            puissanceCanon (TYPE): Description
        """
        super().__init__(life, pos, groupe, image, mass, puissanceCanon, ammoTimer)

        self.distToPlayer: float
        self.firingDistance = 1000

        self.ownership = "red"
        self.forces = [player.forces[0], player.forces[1]]

        self.angle = uniform(-pi_mul_2, pi_mul_2)

    def fire_if_player_in_front(self):
        """Fonction qui fait tirer le vaisseau si le joueur est devant
        """
        self.dotFront = self.direction * self.vectDistanceToPlayer.normalize()
        if self.dotFront > 0.90 and self.distToPlayer < self.firingDistance:
            self.fire()

    def turn_to_player(self):
        """Fonction qui fait tourner l'ennemi vers le joueur
        """

        self.angleMomentum += (angleBetweenVectors(self.direction, self.vectDistanceToPlayer) * 0.01)
        self.angleMomentum *= 0.7 if self.dotFront >= 0 else 1

    def move(self):
        """Fonction qui fait bouger le vaisseau
        """
        if self.distToPlayer > 500:
            self.propulseur += 0.0005
        elif self.distToPlayer < 300:
            self.propulseur -= 0.0005
        else:
            self.propulseur *= 0.8
        if abs(self.propulseur) > 0.12:
            self.propulseur = copysign(0.12, self.propulseur)

    def update(self):
        """Fonction qui actualise l'ennemi
        """
        super().update()

        self.distToPlayer = self.vectDistanceToPlayer.magnitude()

        if not self.dying:
            self.fire_if_player_in_front()
            self.turn_to_player()
            self.move()
