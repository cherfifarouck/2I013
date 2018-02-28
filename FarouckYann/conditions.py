from raw_tools import *
from .constantes import *
from .tools import *

## condition.py Boolean

class Conditions(MetaState):
	def __init__(self, tools):
		self.tools = tools
		self._state = tools._state
		self._id_team = tools._id_team
		self._id_player = tools._id_player
		
	def __getattr__(self, attr):
		if attr in self.tools.__dict__.keys():
			return self.tools.__getattribute__(attr)
		else:
			return self.tools._state.__getattribute__(attr)
		
	# supprimer "con_"
	def rendre_symetrique(self, condition1, condition2):
			if condition1 and self._id_team == 1 or condition2 and self._id_team == 2:
				return True
			
			if condition2 and self._id_team == 1 or condition1 and self._id_team == 2:
				return False


	def face_au_ballon(self, CIBLE, angle_acceptant = math.pi / 12):
		if get_angle_vectoriel((self.PB - PP), (CIBLE - self.PP)) <= angle_acceptant: return True
		else: return False
		
	def joueur_partie_superieure(self):
		if self.PB().y >= GH / 2: return True
		else: return False
	
	def proximite_to_ball(self, distance):
		if self.get_distance_to_ball() <= distance: return True
		else: return False
	
	def proximite_au_but(self, distance):
		PB = self.PB()
		CIBLE = cible(self._id_team)
		
		if CIBLE.distance(PB) <= distance: return True
		else: return False
	
	def goal_ami_couvert(self):
		joueurs_amis = self.get_friendly_positions()
		
		for player in joueurs_amis:
			if self.faire_obstacle(self.PB, self.cage, player):
				return True
				
		return False
	
	def ennemi_eloigne_de_ses_cages1v1(self):
		if self.get_distance_to(self.cible) < self.get_distance_between(self.get_position_adversaire1v1, self.cible):
			return True
		else: return False
	
	def ennemi_devant_moi(self):
		if self.get_distance_between(self.PP, self.cage) >= \
		self.get_distance_between(self.cage, self.get_position_adversaire1v1()):
			return True
		else: return False


	def closest_to_ball_in_team(self):
		if self.get_distance_between(self.get_closest_friendly_to_ball(), self.PB) == \
		self.get_distance_to(self.PB):
			return True
		
		else: return False 
	
	def closest_to_ball(self):
		if self.closest_to_ball_in_team() and \
		self.get_distance_to(self.PB) < self.get_distance_between(self.get_closest_ennemy_to_ball(), self.PB):
			return True
		return False

	def possession_equipe(self):
		liste_amie = self.get_friendly_positions()
		liste_ennemie = self.get_ennemy_positions()
		
		rayon_possession = 20 #ne pas depasser par BalleAuPied
		rayon_adverse = 35
		
		for ennemi in liste_ennemie:
			if self.get_distance_between(ennemi, self.PB()) <= rayon_adverse:
				return False
			
		for allie in liste_amie:
			if self.get_distance_between(allie, self.PB()) <= rayon_possession:
				return True
				
		return False

	def goal_ennemi_couvert(self):
		return voie_libre(self.get_cible())
		
	def condition_de_tir(self, seuil=0.5):
		if probabilite_de_marquer(self.t)  >= seuil:
			return True
		return False

	def engagement(self): #simplification
		# la balle est pas au milieu a lengagement rt self.PB == Vector2D(GW / 2, GH / 2))
		#print(self.PB, Vector2D(GW / 2, GH / 2))
		#print(("condition",self.PB == Vector2D(GW / 2, GH / 2)))
		return self.PB == Vector2D(GW / 2, GH / 2)
	
	def ennemi_eloigne1v1(self):
		if self.proximity_ball_goal_ami() == "proche":
			return False
		return True
	
	def voie_libre(self, CIBLE, angle = math.pi/5):
		liste_position_ennemi = self.get_ennemy_positions()
		
		for ennemi in liste_ennemi:
			if faire_obstacle(self.PB, CIBLE, ennemi, angle):
				return False
		return True
	
	def faire_obstacle(self, A, B, obstacle, angle=math.pi / 5):
		if get_angle_vectoriel(obstacle - A, B - A) < angle:
			return True
		else: return False


	def seuil_de_reussite(self):
		return 0

	def balle_dangereuse(self):
		if self.proximity_ball_goal_ami() == "proche" and self.get_angle_to_goal() < math.pi / 2 or  self.get_distance_between(self.PB, self.cage) < 20:
			return True
		else: return False
