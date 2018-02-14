## sous_strat.py
from tools import MetaState
from conditions import *
from comportement import *
from raw_tools import *

def fonceur_strat(state, id_team,id_player):
	tools = MetaState(state, id_team, id_player)
	return courir_vers_balle(tools) + tirer_goal(tools)

def random_strat(state, id_team, id_player):
	tools = MetaState(state, id_team, id_player)
	return random(tools)

def furtive(state, id_team, id_player):
	t = MetaState(state, id_team, id_player)
	
	#TRIGO
	distance_but = GW/4
	CIBLE = t.get_cible()
	PP = t.PP()
	PB = t.PB()
	X = t.player_state(t._id_team, t._id_player).position.x
	Y = t.player_state(t._id_team, t._id_player).position.y
	
	if t.proximite_horizontale_but(distance_but): 
		return tirer_goal(t) + courir_vers_balle(t)
		
	
	if not t.proximite_horizontale_but(distance_but):
		return courir_vers_balle(t) + dribler_contre_mur(t)

## Le dribleur / balle au pied
def balle_au_pied(state, id_team, id_player, plot=0, coord=[]):
		tools = MetaState(state, id_team, id_player)
		t = tools
		
		PB = t.PB()
		PP = t.PP()
		
		precision_drible = 0.27
		prochaine_direction = Vector2D(coord[plot].x, coord[plot].y)
		plot += 1
		
		return (tirer_balle_vers(t, prochaine_direction, precision_drible), plot)

# a update
def murs(state, id_team, id_player):
	t = MetaState(state, id_team, id_player)
	
	PP = t.PP()
	PB = t.PB()
	CIBLE = t.get_cible()
	rayon = 10 #sujet a modification
	angle = math.pi/4
	
	if t.possession_equipe():
		if t.test_proximite_equipe():
			if t.voie_libre(CIBLE, angle) != True:
				if state.player_state(t.id_adverse(), t.get_ennemi_obstacle\
				(CIBLE, angle)).position.distance\
				(PP) <= rayon:
					return furtive()(state, id_team, id_player)
			
				else:
					return balle_au_pied(state, id_team, id_player)
			
			if t.voie_libre(CIBLE, angle):
				return balle_au_pied(state, id_team, id_player)
			
		else: return placement(state, id_team, id_player, "defenseur central", strategie = "normale")
	else: return fonceur(state, id_team, id_player)
			
def meta_strat(self, state, id_team, id_player):
	t = MetaState(state, id_team, id_player)

	PP = t.PP()
	PB = t.PB()
	CIBLE = t.get_cible()
	
	#rapidite
	ennemi = state.player_state(t.id_adverse(), t.closest_to_ball()).position
	if t.get_distance_to(PB) > t.get_distance_between(PB, ennemi): 
		return fonceur(state, id_team, id_player)
	
	#separation murs
	if abs(PB.y - GH /2) >= 4 * GH /10:
		return furtive(state, id_team, id_player)
	
	#degagement
	if con_rendre_symetrique(PB.x <= GW / 4, PB.x >= 3 * GW / 4, t):
		return fonceur(state, id_team, id_player)
	
	#droit au but
	if con_rendre_symetrique(PB.x >= 2 * GW / 3, PB.x <= GW / 3, t):
		return fonceur(state, id_team, id_player)

	#Defense intelligente PAS SYMETRIQUE
	if con_rendre_symetrique(PB.x > GW / 4 and PB.x <= GW / 2, PB.x < 3 *GW / 4 and PB.x >= GW / 2, t):
		return L2(state, id_team, id_player)

	#Pu
	else: return garder_distance(state, id_team, id_player)

def attaque(self, state, id_team, id_player):
	t = MetaState(state, id_team, id_player)

	PP = t.PP()
	PB = t.PB()
	CIBLE = t.get_cible()
	
	distance_goal = 25
	distance_joueur = 35
	angle_deviation = math.pi /4
	
	if t.pres_de_la_balle(): 
		if t.proximite_au_but(distance_goal) == True or \
		(t.voie_libre(CIBLE) == True and t.get_distance_between(PB, CIBLE) < 40):
			print("proche des buts voie libre assez proche")
			return fonceur(state, id_team, id_player)
		
		if t.voie_libre(CIBLE):
			print("voie libre")
			return balle_au_pied(state, id_team, id_player, coordonnees = CIBLE)
		
		if not t.voie_libre(CIBLE):
			print("voie po libre")
			ennemi = t.get_ennemi_obstacle(CIBLE)
			ennemi_ = state.player_state(t.id_adverse(), ennemi)
			deplacement = (state.player_state(t.id_adverse(), ennemi).position - PB)
			deplacement.norm = 0.21
			
			#commencer drible
			if get_distance_between(ennemi_.position, PP) < distance_joueur:
				print("ennemi proche")
				#on se rapproche des murs
				
				coef = 1
				if abs(PB.x - CIBLE.x) <2:
					angle_deviation += math.pi/8
					coef = -1
				
				if con_rendre_symetrique(PB.y >= GH/2, PB.y < GH/2, t):
					deplacement.angle += coef * angle_deviation
					return foncer_vers_balle(t) + tirer_balle_vers(t, maxB, direction=deplacement)
				else:
					deplacement.angle -= coef * angle_deviation
					return foncer_vers_balle(t) + tirer_balle_vers(t, maxB, direction=deplacement)
			
			else: 
				print("placement")
				return balle_au_pied([CIBLE])
			
	#prendre linitiative
	if t.test_proximite_equipe():
		print("je suis le plus proche dans lequipe")
		return courir_vers_balle(t)
	else: placement(t, "attaquant", strat="ultra offensive")

def attente(self,state,id_team,id_player, position):
	t = MetaState(state, id_team, id_player)
	position = Vector2D(GW/3, GH/2)
	PP = t.PP()
	
	return SoccerAction(ZERO, ZERO)

def passe_a_2_3_4(self, state, id_team, id_player):
	return 0

def gardien(self, state, id_team, id_player):
	t = MetaState(state, id_team, id_player)

	PP = t.PP()
	PB = t.PB()
	GOAL = t.cage()
	CIBLE = t.get_cible()
	
	coefficient_entrainement = 0.44
	distanceAuCage = 10
	
	if pres_de_la_balle(state, id_team, id_player):
		return tirer_balle_vers(tools, coefficient_entrainement, coordonnees=CIBLE)
	
	#aspect visuel du deplacement
	if con_rendre_symetrique(PB.x >= GW/2, PB.x < GW/2, t):
		return courir_vers(t, distanceAuCage * (PB - GOAL).normalize(), 0.30)
		
	if not con_rendre_symetrique(PB.x >= GW/2, PB.x < GW/2, t): 
		return courir_vers(t, distanceAuCage * (PB - GOAL).normalize(), 0.75)

def garder_distance(self, state, id_team, id_player):
		t = MetaState(state, id_team, id_player)
		
		PP = t.PP()
		PB = t.PB()
		CAGE = t.get_cage()
		CIBLE = t.cible()
		distance = 0.33
		
		return courir_vers(t, (CAGE - PB).normalize() * distance) 

def L2(self, state, id_team, id_player):
	t = MetaState(state, id_team, id_player)
	
	PP = t.PP()
	PB = t.PB()
	coefficient = 0.33
	CIBLE = t.get_cible()
	CAGE = t.cage()
			
	
	if con_rendre_symetrique(PB.x >= 4*GW/7, PB.x <= 3* GW/7, t):
		return fonceur(state, id_team, id_player)
		
	else:
		if  t.get_distance_to(PB) > t.get_distance_between(PB, state.player_state(2,0).position):
			return garder_distance(state, id_team, id_player)
	
		else: 
			return fonceur(state, id_team, id_player)

#Contenir joueur specifique
def marquage(self, state, id_team, id_player):
	t = MetaState(state, id_team, id_player)

	PP = t.PP()
	PB = t.PB()
	CIBLE = t.get_cible()
	GOAL = t.cage()
	distance = 15
	
	listeAMarquer = [k for k in state.players] #plus ou moins
	joueur = listeAMarquer[0][1]
	listeAMarquer = listeAMarquer[1::len(listeAMarquer)+1]
	
	return courir_vers(t, (GOAL - state.player_state(t.id_adverse(), joueur).position).normalize() * distance)
