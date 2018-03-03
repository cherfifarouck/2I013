from __future__ import absolute_import
from soccersimulator import Strategy, SoccerAction,Vector2D
from soccersimulator import settings
import math
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
		self.debug = 0
		
	def compute_strategy(self, state, id_team, id_player):
		def compteur(self, id_tim):
			if id_tim == 1: return 0
			self.debug += 1
			print("tag", self.debug)
			
		def debug_init(self, id_tim):
			self.debug = 0
			print("tag 0")
		
		##Parameters
		rayon_zone_de_confiance = 4.3
		##End parameters
		
		tools = MetaState(state, id_team, id_player)
		con = Conditions(tools)
		
		#debug_init(self, id_team)
		#compteur(self, id_team)
		
		# Determination de la /phase/ de strategie:
		def phase_of_strat(tools):
			if con.condition_engagement():
				return "undetermined"
				
			elif tools.get_distance_to_ball() < \
			tools.get_distance_between(tools.get_position_adversaire1v1(), tools.PB) or \
			tools.get_distance_to_ball() < rayon_zone_de_confiance:
				return "offensive" #synonyme de avoir la balle
			
			else: 
				return "defensive"
		
		phase = phase_of_strat(tools)
		#if id_team == 2: print(phase)
		
		def defense():
			#compteur(self, id_team)
			if con.goal_ami_couvert():
				return decision_defensive(tools)
			
			#compteur(self, id_team)
			
			if not con.goal_ami_couvert(): ## paremetre de langle
				#compteur(self, id_team)
				if con.ennemi_devant_moi():
					return retourner_au_cage(tools)
				
				#compteur(self, id_team)
				if not con.ennemi_devant_moi():
					#compteur(self, id_team)
					if con.balle_dangereuse(): ## paremetre de la distance au goal
						return retourner_au_cage(tools)
					
					#compteur(self, id_team)
					if not con.balle_dangereuse():
						return garder_distance(tools) ## paremetre de la distance a garder
		
		def offense():	
			# recuperation de balle
			#compteur(self, id_team)
			if con.condition_degagement():
				return degagement1v1(tools)
			
			#compteur(self, id_team)
			if tools.get_distance_to(tools.get_position_adversaire1v1()) <= 15 \
			and not con.voie_libre(tools.cible, math.pi / 6):
				return manoeuvre_devasion(tools)
			
			else: 
				#compteur(self, id_team)
				return finition(tools)
		
		def ambiguous():
			#compteur(self, id_team)
			if con.condition_engagement():
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
		return balle_au_pied(tools)
		
class Test2(Strategy):
	def __init__(self):
		Strategy.__init__(self, "1 vs 1")
		
	def compute_strategy(self, state, id_team, id_player):
		tools = MetaState(state, id_team, id_player)
		return garder_distance(tools)
