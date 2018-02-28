from __future__ import absolute_import
from soccersimulator import Strategy, SoccerAction,Vector2D
from soccersimulator import settings
class Gardien(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Gardien")

	@staticmethod
	def compute_strategy(state, id_team, id_player):
		tools = MetaState(state, id_team, id_player)
		return gardien(tools)
		

from .sous_strat import *
from .tools import *


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
		""" Description  complete de notre attaquant:
		"""
		
		return fonceur_strat(state, id_team, id_player)

class UnVUn(Strategy):
	""" Strategie 1v1 based sur un certain nombre
	
	de sous_strat et de conditions. Voir le fichier arbre
	de decision 1v1 pour suivre le decision making 
	de la classe unVun.
	"""
	
	def __init__(self):
		""" POURQUOI ON UTILISE PAS UN SUPER"""
		Strategy.__init__(self, "1 vs 1")
		#self.parametre = parametre
		
	def compute_strategy(self, state, id_team, id_player):
		##Parameters
		rayon_zone_de_confiance = 0
		##End parameters
		
		tools = MetaState(state, id_team, id_player)
		con = Conditions(tools)
		
		# Determination de la /phase/ de strategie:
		def phase_of_strat(tools):
			if con.engagement():
				return "undetermined"
				
			elif tools.get_distance_to_ball() - rayon_zone_de_confiance < \
			tools.get_distance_between(tools.get_position_adversaire1v1(), tools.PB):
				return "offensive"
			
			else: 
				return "defensive"
		
		phase = phase_of_strat(tools)
		#print("donc phase =", phase)
		
		def defense():
			if not con.goal_ami_couvert():
				if con.ennemi_devant_moi():
					return retourner_au_cage(tools)
					
				else:
					if con.balle_dangereuse():
						return retourner_au_cage(tools)
						
					else:
						return garder_distance(tools)
						
			else:
				return decision_defensive(tools)
		
		def offense():
			if con.closest_to_ball():
				return fonceur_predict(tools)
			
			elif con.proximite_to_ball(rayon_zone_de_confiance):
				if not con.ennemi_eloigne_de_ses_cages1v1():
					fonceur_strat(tools)
				
				else: 
					if not con.goal_ennemi_couvert():
						if con.conditions_de_tir():
							return tirer()
						
						else:
							balle_au_pied(tools)
							
					else:
						return decision_offensive()
		
		def ambiguous():
			if con.engagement():
				return strategie_engagement1v1(tools)
				
			else:
				return fonceur_predict(tools)
		
		available_strategies = {"defensive" : defense,
		"offensive" : offense,
		"undetermined" : ambiguous,
		}
		# Apply strategy
		return available_strategies[phase]()

class Test(Strategy):
	def __init__(self):
		Strategy.__init__(self, "1 vs 1")
		
	def compute_strategy(self, state, id_team, id_player):
		tools = MetaState(state, id_team, id_player)
		return garder_distance(tools)
