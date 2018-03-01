## sous_strat.py
from .tools import MetaState
from .conditions import *
from .comportement import *
from .raw_tools import *
from .comportement import *
from .strat import Gardien

##Deplacement avec balle

def balle_au_pied(tools, coord=[ZERO], plot=0):
		precision_drible = 0.27
		if coord == [ZERO]:
			return dribler_vers(tools, precision_drible, tools.cible)
			
		coordonnees = Vector2D(coord[plot].x, coord[plot].y)
		plot += 1
		return [dribler_vers(tools, precision_drible, prochaine_direction), plot]
def deviation(tools, angle): #si pres de la balle
		direction = tools.p_speed
		direction.angle += angle
		direction = direction.normalize()
		
		return fonceur_predict(tools)
		
		#print("direction", tools._state.player_state(1,0).vitesse)
		#return SoccerAction(Vector2D(1., 0.), ZERO)
		return foncer_vers_balle(tools) + \
			SoccerAction(0.,
			maxB * 0.22 * direction)
def drible1(tools):
	con = Conditions(tools)
	angle = math.pi / 5
	
	if con.joueur_partie_superieure():
		return deviation(tools, angle)
	else:
		return deviation(tools, -angle)
def drible2(tools):
	return 0
def manoeuvre_devasion(tools):
	return drible1(tools)

##Deplacement sans balle
def attente(tools, position=ZERO):
	position = Vector2D(GW/3, GH/2)
	return SoccerAction(ZERO, ZERO)
def random_strat(tools):
	return random(tools)
def garder_distance(tools, proportion=0.23):
		return courir_vers(tools, tools.PB + (tools.cage - tools.PB) * proportion) 
def marquage(tools):
	distance = 15
	
	id_a_marquer = fonction_marquage_encodee(tools)[tools.id_player]
	position = self.player_state(self.id_adverse, id_a_marquer).position
	
	return courir_vers(tools, (tools.PP - position) + (self.cage - positon).normalize() * distance)
def place_et_passe(tools, CIBLE, distance_derriere_balle = 1.49):
	con = Conditions(tools)
	player_shoot = puissance_recommandee(tools.get_distance_to(CIBLE), (CIBLE - tools.PP).angle)
	# rayon_ralentissement = distance_a_decelerer(state.player_state(id_team, id_player).vitesse.norm)
	
	if tools.pres_de_la_balle() and \
	tools.get_distance_to_ball() <= rayon_ralentissement and not con.face_au_ballon(CIBLE):
		# ralentir
		return SoccerAction( ZERO, ZERO)
			
	if tools.pres_de_la_balle() and tools.face_au_ballon(CIBLE):
		#shoot
		return tirer_balle_vers(tools, player_shoot, coordonnees=CIBLE)
	
	else: 
		#courir
		return fonceur_predict(tools)


##Strategie finale simple
def fonceur_strat(tools):
	return foncer_vers_balle(tools) + shooter_goal(tools)
def fonceur_predict(tools):
	prochaine_balle = tools.cible
	return recuperation(tools, prochaine_balle)
def furtive(tools):
	con = Conditions(tools)
	
	#TRIGO
	distance_but = GW/4
	CIBLE = tools.cible
	X = tools.player_state(t._id_team, t._id_player).position.x
	Y = tools.player_state(t._id_team, t._id_player).position.y
	
	if con.proximite_horizontale_but(distance_but): 
		return tirer_goal(tools) + courir_vers_balle(tools)
	
	if not con.proximite_horizontale_but(distance_but):
		return courir_vers_balle(tools) + dribler_contre_mur(tools)
def gardien(tools):
	con = Conditions(tools)
	coefficient_entrainement = 0.44
	distanceAuCage = 10
	
	if tools.get_distance_between(tools.get_closest_ennemy_to_ball(), tools.PB) > tools.get_distance_to_ball() + 20 and tools.b_speed < 2:
		print("je vais predire la balle")
		if con.balle_dangereuse():
			return fonceur_predict(tools) # degagement
		else:
			return fonceur_predict(tools) # a terme faire une passe ici
			
	if con.situation1v1_gardien():
		return triangle(tools)
	
	if tools.pres_de_la_balle():
		return tirer_balle_vers(tools, coefficient_entrainement, coordonnees=tools.cible)
	
	#aspect visuel du deplacement
	position_par_defaut = tools.cage + distanceAuCage * (tools.PB - tools.cage).normalize()
	if con.rendre_symetrique(tools.PB.x >= GW/2, tools.PB.x < GW/2):
		return courir_vers(tools, position_par_defaut, 0.30)
		
	if not con.rendre_symetrique(tools.PB.x >= GW/2, tools.PB.x < GW/2): 
		return courir_vers(tools, position_par_defaut, 0.75)
def strategie_engagement1v1(tools):
	return fonceur_strat(tools)

##Autre
def decision_defensive(tools):
	con = Conditions(tools)
	
	if con.plus_proche(1) < 0:
		return fonceur_predict(tools)
	if tools.proximity_ball_goal_ami() == "loin":
		return fonceur_predict(tools)
	
	elif tools.proximity_ball_goal_ami() == "medium":
		#on assume que le joueur ennemi va perdre la balle des quil tire
		if tools.pres_de_la_balle(tools.get_closest_ennemy_to_ball()) : return fonceur_predict(tools)
		else: return garder_distance(tools)
		
	elif tools.proximity_ball_goal_ami() == "proche":
		return Gardien().compute_strategy(tools._state, tools._id_team, tools._id_player)

def attaque(tools):
	con = Conditions(tools)
	distance_goal = 25
	distance_joueur = 35
	angle_deviation = math.pi /4
	
	if tools.pres_de_la_balle(): 
		if tools.proximite_au_but(distance_goal) == True or \
		(con.voie_libre(tools.cible) == True and tools.get_distance_between(tools.PB, tools.cible) < 40):
			print("proche des buts voie libre assez proche")
			return fonceur(tools)
		
		if con.voie_libre(self.cible):
			print("voie libre")
			return balle_au_pied(tools, coordonnees=tools.cible)
		
		if not con.voie_libre(tools.cible):
			print("voie po libre")
			ennemi = tools.get_ennemi_obstacle(tools.cible)
			ennemi_ = tools.player_state(tools.id_adverse(), ennemi)
			deplacement = (state.player_state(t.id_adverse(), ennemi).position - PB)
			deplacement.norm = 0.21
			
			#commencer drible
			if tools.get_distance_between(ennemi_.position, PP) < distance_joueur:
				print("ennemi proche")
				#on se rapproche des murs
				
				coef = 1
				if abs(PB.x - CIBLE.x) <2:
					angle_deviation += math.pi/8
					coef = -1
				
				if con.rendre_symetrique(PB.y >= GH/2, PB.y < GH/2, tools):
					deplacement.angle += coef * angle_deviation
					return foncer_vers_balle(tools) + tirer_balle_vers(tools, 1., direction=deplacement)
				else:
					deplacement.angle -= coef * angle_deviation
					return foncer_vers_balle(tools) + tirer_balle_vers(tools, 1., direction=deplacement)
			
			else: 
				print("placement")
				return balle_au_pied([CIBLE])
			
	#prendre linitiative
	if tools.test_proximite_equipe():
		print("je suis le plus proche dans lequipe")
		return courir_vers_balle(tools)
	else: placement(tools, "attaquant", strat="ultra offensive")
