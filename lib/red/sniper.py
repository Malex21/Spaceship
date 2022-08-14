"""Fichier relatif au 'sniper'
"""


class redSniper(redTeam):
	"""Classe relative au 'shooter' rouge
	"""

	def __init__(self, pos):
		"""Redéfinition des certaines fonctions
		
		Args:
		    pos (tuple): Position d'apparition (x, y) du vaisseau
		"""
		super().__init__(100, pos, ships, sniperRedSprite, 480, 90, 75)

		# self.ownership = "redblaster"
		self.firingDistance = 1600
