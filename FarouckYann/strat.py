from __future__ import absolute_import
from soccersimulator import Strategy, SoccerAction,Vector2D
from soccersimulator import settings
class Gardien(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Gardien")
		self.retour_au_cage = 0

	def compute_strategy(self, state, id_team, id_player):
		tools = MetaState(state, id_team, id_player)
		position_par_defaut = tools.cage + 10 * (tools.PB - tools.cage).normalize()
		
		if tools.pres_de_la_balle() and gardien(tools) == triangle(tools):
			self.retour_au_cage = 1
						
		if self.retour_au_cage == 1:
			if tools.get_distance_to(position_par_defaut) <= 5:
				self.retour_au_cage = 0
			return courir_vers(tools, position_par_defaut, 0.75) + shooter_goal(tools)
		 
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
		#self.derniere_decision = 0
		#self.time_decision = 0
		#self.parametre = parametre
		
	def compute_strategy(self, state, id_team, id_player):
		##Parameters
		rayon_zone_de_confiance = 15
		##End parameters
		
		tools = MetaState(state, id_team, id_player)
		con = Conditions(tools)
		
		# Determination de la /phase/ de strategie:
		def phase_of_strat(tools):
			if con.engagement():
				return "undetermined"
				
			elif tools.get_distance_to_ball() + rayon_zone_de_confiance < \
			tools.get_distance_between(tools.get_position_adversaire1v1(), tools.PB) or \
			tools.get_distance_to_ball() < rayon_zone_de_confiance:
				return "offensive"
			
			else: 
				return "defensive"
		
		phase = phase_of_strat(tools)
		#print(phase)
		
		def defense():
			if not con.goal_ami_couvert(): ## paremetre de langle
				if con.ennemi_devant_moi():
					return retourner_au_cage(tools)
					
				else:
					if con.balle_dangereuse(): ## paremetre de la distance au goal
						return retourner_au_cage(tools)
						
					else:
						return garder_distance(tools) ## paremetre de la distance a garder
						
			else:
				return decision_defensive(tools)
		
		def offense():
			if True: #con.proximite_to_ball(rayon_zone_de_confiance):
				if not con.ennemi_eloigne_de_ses_cages1v1():
					if con.condition_de_tir(): ## dribler goal
						print("tag1")
						return tirer_goal(tools) + foncer_vers_balle(tools) ## Mettre la condition condition_de_tir au dessus une fois quelle sera au point
					
					else:
						print("tag2")
						return balle_au_pied(tools)
				
				else: 
					if not con.goal_ennemi_couvert():
						if con.condition_de_tir():
							print("fonceur2")
							return tirer_goal(tools)
						
						else:
							print("fonceur3")
							balle_au_pied(tools)
							
					else:
						print("fonceur4")
						return manoeuvre_devasion(tools)
			
			elif con.closest_to_ball():
				print("kektier")
				return fonceur_predict(tools)
				
			print("arriver au bout de offense")
		
		def ambiguous():
			if con.engagement():
				return strategie_engagement1v1(tools)
				
			else:
				return fonceur_predict(tools)
		
		available_strategies = {"defensive" : defense,
		"offensive" : offense,
		"undetermined" : ambiguous,
		}
		
		return available_strategies[phase]()

class Test(Strategy):
	def __init__(self):
		Strategy.__init__(self, "1 vs 1")
		
	def compute_strategy(self, state, id_team, id_player):
		tools = MetaState(state, id_team, id_player)
		return manoeuvre_devasion(tools)
		
class Test2(Strategy):
	def __init__(self):
		Strategy.__init__(self, "1 vs 1")
		
	def compute_strategy(self, state, id_team, id_player):
		tools = MetaState(state, id_team, id_player)
		return strategie_engagement1v1(tools)
