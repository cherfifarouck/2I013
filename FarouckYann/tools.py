from __future__ import absolute_import
from soccersimulator  import Strategy, SoccerAction, Vector2D
from soccersimulator import settings
import random
import math
import sys

class MetaState(object):
	def __init__(self, state, id_team, id_player):
		self._state = state
		self._id_team = id_team
		self._id_player = id_player
		
	def __getattr__(self, attr):
		return _state.__getattr__(attr)
	
	def PP():
		return state.player_state(id_team, id_player).position
	def PB():
		return state.ball.position
	def get_cible():
		if self._id_team == 1:
			return CENTRE_GOAL_DROIT
		else: return CENTRE_GOAL_GAUCHE
	def get_ennemi_rayon(rayon): #renvoie le player_state
		PP = self.PP()
		liste_ennemis = []
		liste_distance = []
		
		for ennemi in state.players:
			if ennemi[0] != id_team and PP.distance(state.player_state(ennemi[0], ennemi[1]).position) < rayon:
				liste_ennemis.append( ennemi[1])
				liste_distance.append( PP.distance(state.player_state(ennemi[0], ennemi[1]).position))
			
			if liste_ennemis != []: return liste_ennemis[liste_distance.index(min(liste_distance))]
		return None
	def get_ennemi_obstacle(CIBLE, angle = math.pi /4):
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
	def get_angle_vectoriel(v1, v2): #non oriente
		if v1.x == 0 or v2.x == 0: 
			sys.exit("Composante horizontale nulle")
		if v1.dot(v2) == 0: return math.pi / 2
		
		else: return abs(v1.angle - v2.angle)%(2*math.pi)
	def face_au_ballon(CIBLE, angle_acceptant = math.pi / 12):
		PB = self.PB()
		PP = self.PP()
		
		if get_angle_vectoriel((PB - PP), (CIBLE - PP)) <= angle_acceptant: return True
		else: return False
	def pres_de_la_balle():
		if (self.ball.position.distance(self.player_state(_id_team, _id_player).position) \
		<= settings.BALL_RADIUS + settings.PLAYER_RADIUS):
			return True
		else: 
			return False
	def joueur_partie_superieure():
		if t.PB().y >= GH / 2: return True
		else: return False
	def cage():
		if self._id_team == 1:
			return CENTRE_GOAL_GAUCHE
		else: return CENTRE_GOAL_DROIT
	def id_adverse():
		return (self._id_team % 2)+1
	def test_proximite_ennemi():
		PP = self.PP()
		PB = self.PB()
		
		#Test de proximite par rapport a la balle
		for k in self.players:
			if k[0] != self._id_team and PB.distance(PP) > PB.distance(self.player_state(id_adverse(self._id_team), k[1]).position):
				return False
				
		return True
	def test_proximite_equipe():
		PP = self.PP()
		PB = self.PB()
			
		for allie in self.players:
			if allie[0] == self._id_team and allie[1] != self._id_player and PB.distance(self.player_state(self._id_team, allie[1]).position) < PB.distance(PP):
				return False			
		return True
	def proximite_au_but(distance):
		PB = self.PB()
		CIBLE = cible(self._id_team)
		
		if CIBLE.distance(PB) <= distance: return True
		else: return False
	def proximite_horizontale_but(distance):
		PB = self.PB()
		PP = self.PP()
		if (PB.x > GW - distance and self._id_team == 1) or (PB.x < distance and self._id_team == 2)
	def voie_libre(CIBLE, angle = math.pi/5): # renvoie boolean
		PP = self.PP()
		PB = self.PB()
		CIBLE = self.get_cible() #enlever apres
		
		for ennemi in self.players:
			if ennemi[0] != self._id_team and get_angle_vectoriel(self.player_state(id_adverse(self._id_team), ennemi[1]).position - PB, CIBLE - PB) \
			< angle:
				return False
		return True
	def possession_equipe():
		PP = self.PP()
		PB = self.PB()
		
		rayon_possession = 20 #ne pas depasser par BalleAuPied
		rayon_adverse = 35
		
		for ennemi in self.players:
			if ennemi[0] != self._id_team and PB.distance(self.player_state(id_adverse(self._id_team), ennemi[1]).position) <= rayon_adverse:
				return False
			
		for allie in self.players:
			if allie[0] == self._id_team and PB.distance(self.player_state(self._id_team, allie[1]).position) <= rayon_possession:
				return True
				
		return False
	def puissance_shoot(distance):
		if distance > K:
			return settings.maxPlayerShoot
			
		#intercept inverse
		else: return distance / K * settings.maxPlayerShoot
def closest_to_ball(state, id_team, id_player):
		PP = self.PP()
		PB = self.PB()
		CIBLE = cible(id_team)
		
		liste_objets = []
		liste_distance = []
		
		for ennemi in state.players:
			if ennemi[0] != self._id_team:
				liste_objets.append(ennemi[1])
				liste_distance.append(PB.distance(self.player_state(id_adverse(self._id_team), ennemi[1]).position))
			
		if liste_objets != []: return liste_objets[liste_distance.index(min(liste_distance))]
		else: return None
