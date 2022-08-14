"""Fichier relatif au 'shooter'
"""


class redShooter(redTeam):
	"""Classe relative au 'shooter' rouge
	"""

	def __init__(self, pos):
		"""Redéfinition des certaines fonctions
		
		Args:
		    pos (tuple): Position d'apparition (x, y) du vaisseau
		"""
		super().__init__(90, pos, ships, shooterRedSprite, 300, 16, 15)

		# self.ownership = "redshooter"
