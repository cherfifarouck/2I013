from __future__ import absolute_import
from soccersimulator  import Strategy, SoccerAction, Vector2D
from soccersimulator import settings
from .constantes import *
import random
import math
import sys


class MetaState(object):
	def __init__(self, state, id_team, id_player):
		self._state = state
		self._id_team = id_team
		self._id_player = id_player
		
	def __getattr__(self, attr):
		return self._state.__getattribute__(attr)
	
	@property
	def PP(self):
		return self._state.player_state(self._id_team, self._id_player).position
	@property
	def PB(self):
		return self.ball.position
	@property
	def cible(self):
		if self._id_team == 1:
			return CENTRE_GOAL_DROIT
		else: return CENTRE_GOAL_GAUCHE
	@property
	def cage(self):
		if self._id_team == 1:
			return CENTRE_GOAL_GAUCHE
		else: return CENTRE_GOAL_DROIT
	@property
	def speed(self):
		return self.player_state(self._id_team, self._id_player).vitesse
	@property
	def b_speed(self):
		return self.ball.vitesse
	@property
	def p_speed(self):
		return self._state.player_state(self._id_team, self._id_player).vitesse
	
	def pres_de_la_balle(self, *args):
		if args != ():
			objet = args[0]
		else: objet = self.PP
		
		if self.get_distance_between(objet, self.PB) \
		<= RAYON_ACTION:
			return True
		else: 
			return False
	def get_distance_to(self, vec2D):
		return self.player_state(self._id_team, self._id_player).position.distance(vec2D)
	def get_distance_to_ball(self):
		return self.get_distance_to(self.PB)
	def get_distance_to_goal(self):
		return self.get_distance_to(self.cible)
	def get_distance_between(self, vec1, vec2):
		return vec1.distance(vec2)
	def get_ennemi_rayon(self, rayon): #renvoie le player_state
		PP = self.PP()
		liste_ennemis = []
		liste_distance = []
		
		for ennemi in state.players:
			if ennemi[0] != id_team and PP.distance(state.player_state(ennemi[0], ennemi[1]).position) < rayon:
				liste_ennemis.append( ennemi[1])
				liste_distance.append( PP.distance(state.player_state(ennemi[0], ennemi[1]).position))
			
			if liste_ennemis != []: return liste_ennemis[liste_distance.index(min(liste_distance))]
		return None
	def get_ennemi_obstacle(self, CIBLE, angle = math.pi /4):
		PP = self.PP()
		PB = self.PB()
		CIBLE = cible(_id_team)
		
		liste_objets = []
		liste_distance = []
		
		for ennemi in state.players:
			if ennemi[0] != _id_team and self.get_angle_vectoriel(self.player_state(self.id_adverse(_id_team), ennemi[1]).position - PB, CIBLE - PB) \
			< angle:
				liste_objets.append(ennemi[1])
				liste_distance.append(PB.distance(self.player_state(self.id_adverse(_id_team), ennemi[1]).position))
			
		if liste_objets != []: return liste_objets[liste_distance.index(min(liste_distance))]
		else: return None
	def get_friendly_positions(self):
		states = [state for state in self.players if state[0] == self._id_team]
		return [self.player_state(state[0], state[1]).position for state in states]
	def get_ennemy_positions(self):
		states = [state for state in self.players if state[0] != self._id_team]
		return [self.player_state(state[0], state[1]).position for state in states]
	def get_position_adversaire1v1(self):
		return self.player_state(self.id_adverse(), 0).position
	def get_angle_to_goal(self):
		return (self.cible - self.PB).angle
	def get_position_from_state(self, state):
		return self.player_state(state[0], state[1]).position
	def id_adverse(self):
		return (self._id_team % 2)+1
	def proximite_horizontale_but(self, distance):
		PB = self.PB()
		PP = self.PP()
		if con_rendre_symetrique(PB.x > GW - distance, PB.x < distance):
			return True
		return False
	def proximity_ball_goal_ami(self):
		distance = self.get_distance_between(self.ball.position, self.cage)
		if distance <= 30: return "proche"
		elif distance <= 80: return "medium"
		else: return "loin"
	
	def puissance_shoot(self, distance):
		if distance > K:
			return settings.maxPlayerShoot
			
		#intercept inverse
		else: return distance / K * settings.maxPlayerShoot
	def get_closest_friendly_to_ball(self):
		liste_amie = self.get_friendly_positions()
		liste_distance = [self.get_distance_between(friendly, self.PB) for friendly in liste_amie]
		return liste_amie[liste_distance.index(min(liste_distance))]
	def get_closest_ennemy_to_ball(self):
		liste_ennemie = self.get_ennemy_positions()
		liste_distance = [self.get_distance_between(ennemi, self.PB) for ennemi in liste_ennemie]
		return liste_ennemie[liste_distance.index(min(liste_distance))]

	def parametre_score(self):
		score_ami = self._state.get_score_team(self._id_team)
		score_ennemi = self._state.get_score_team(self._id_team % 2 +1)
		
		if score_ami == score_ennemi: return "egalite"
		if abs(score_ami - score_ennemi) >= 3:
			if score_ami > score_ennemi: return "avance comfortable"
			else: return "cest la merde"
		if score_ami > score_ennemi: return "petite avance"
		else: return "petit retard"

	def intercept_ball(self):
			""" Intercept plus efficacement la balle. """
			##Parameters
			distance_annulation = 15
			vitesse_danulation = 0
			coefficient_prediction = 10
			
			if self.get_distance_to_ball() <= distance_annulation or self.b_speed < vitesse_danulation:
				return self.PB
			
			else:
				point_interception = self.PB + coefficient_prediction * self.b_speed.normalize()
				return point_interception
