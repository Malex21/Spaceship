"""Fichier relatif au 'blaster'
"""


class redBlaster(redTeam):
	"""Classe relative au 'blaster' rouge
	"""

	def __init__(self, pos):
		"""Redéfinition des certaines fonctions
		
		Args:
		    pos (tuple): Position d'apparition (x, y) du vaisseau
		"""
		super().__init__(150, pos, ships, blasterRedSprite, 600, 30, 40)

		# self.ownership = "redblaster"
