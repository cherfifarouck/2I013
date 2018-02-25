from __future__ import absolute_import
from soccersimulator import Strategy, SoccerAction,Vector2D
from soccersimulator import settings
from .sous_strat import *
from .tools import *

class Gardien(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Gardien")

	def compute_strategy(self, state, id_team, id_player):
		return gardien(state, id_team, id_player)
		
class Defenseur(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Defenseur")
		
	def compute_strategy(self, state, id_team, id_player):
		return fonceur_strat(state, id_team, id_player)
		
class Milieu(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Milieu")
		
	def compute_strategy(self, state, id_team, id_player):
		return fonceur_strat(state, id_team, id_player)
	
class Attaquant(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Attaquant")
		
	def compute_strategy(self, state, id_team, id_player):
		return fonceur_strat(state, id_team, id_player)
