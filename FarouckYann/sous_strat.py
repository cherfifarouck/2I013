## sous_strat.py
from .tools import MetaState
from .conditions import *
from .comportement import *
from .raw_tools import *
from .comportement import *
from .strat import Gardien
import math

##Deplacement avec balle
def finition(tools): #derniers metres
	con = Conditions(tools)
	
	if con.condition_de_tir():
		return tirer_goal(tools) + foncer_vers_balle(tools)
		
	elif not con.condition_de_tir():
		return balle_au_pied(tools)
def degagement(tools):
	con = Conditions(tools)
	if con.balle_dangereuse() and not con.voie_libre(tools.cible):
		ennemi_obstruction = tools.get_position_adversaire1v1() #implementer une fonction qui retourne la position du joueur qui fait obstruction
		return tirer_balle_vers(tools, 1., direction= (ennemi_obstruction - tools.PB).angle + math.pi / 4)
	
	else: return shooter_goal(tools)
def degagement1v1(tools):
	con = Conditions(tools)
	if con.balle_dangereuse() and not con.voie_libre(tools.cible):
		print("balle dangereuse et voie pas llibre")
		ennemi = tools.get_position_adversaire1v1()
		
		if con.etre_colle_au_mur_lateral(ennemi):
				if tools.closest_mur_lateral(ennemi) == "haut":
					endroit = Vector2D(
					ennemi.x, 
					ennemi.y / 2)
				else:
					endroit = Vector2D(
					ennemi.x,
					(GH - ennemi.y) / 2)
		
		else:
				if tools.closest_mur_lateral(ennemi) == "haut":
					endroit = Vector2D(
					ennemi.x, 
					(GH - ennemi.y) / 2)
				else:
					endroit = Vector2D(
					ennemi.x,
					ennemi.y / 2)
		
		return tirer_balle_vers(tools, 1., coordonnees=endroit) + foncer_vers_balle(tools)
	
	else: 
		return shooter_goal(tools) + foncer_vers_balle(tools)
def balle_au_pied(tools, coord=[ZERO], plot=0):
		precision_drible = 0.27
		if coord == [ZERO]:
			print("je rentre la ou je dois")
			return dribler_vers(tools, precision_drible, tools.cible)
			
		coordonnees = Vector2D(coord[plot].x, coord[plot].y)
		plot += 1
		return [dribler_vers(tools, precision_drible, prochaine_direction), plot]
def deviation(tools, angle): #1v1
		direction = (tools.get_position_adversaire1v1() - tools.PB)
		direction.angle += angle
		direction = direction.normalize()
		
		#print("direction", tools._state.player_state(1,0).vitesse)
		#return SoccerAction(Vector2D(1., 0.), ZERO)
		return foncer_vers_balle(tools) + \
		tirer_balle_vers(tools, 0.22, direction=direction)
def deviation_centrale(tools, angle): #1v1
		direction = (tools.get_position_adversaire1v1() - tools.PP)
		direction.angle += angle
		direction = direction.normalize()
		
		#print("direction", tools._state.player_state(1,0).vitesse)
		#return SoccerAction(Vector2D(1., 0.), ZERO)
		return foncer_vers_balle(tools) + \
		tirer_balle_vers(tools, 0.22, direction=direction)
def drible1(tools):
	con = Conditions(tools)
	angle = math.pi / 5
	
	if con.rendre_symetrique(con.joueur_partie_superieure(), not con.joueur_partie_superieure()):
		return deviation(tools, angle)
	else:
		return deviation(tools, -angle)
def drible2(tools):
	return 0
def manoeuvre_devasion(tools):
	return drible1(tools)

##Deplacement sans balle
def tacler(tools):
	con = Conditions(tools)
	vitesse = 0.8
	
	if con.rendre_symetrique(con.joueur_partie_superieure(), not con.joueur_partie_superieure()):
		angle = math.pi / 3
	else: angle = -math.pi / 3
	return partie_reelle(fonceur_predict(tools)) + tirer_balle_vers(tools, vitesse, direction=angle)
def attente(tools, position=ZERO):
	position = Vector2D(GW/3, GH/2)
	return SoccerAction(ZERO, ZERO)
def random_strat(tools):
	return random(tools)
def garder_distance(tools, proportion=0.23):
	return courir_vers(tools, tools.PB + (tools.cage - tools.PB) * proportion) 
def garder_distance_offensif(tools):
	return garder_distance(tools) + mult_SA(0.28, tacler(tools))
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
	
	if tools.proximity_ball_goal_ami() == "loin":
		print("loin")
		return garder_distance(tools)
	
	elif tools.proximity_ball_goal_ami() == "medium":
		print("med")
		#on assume que le joueur ennemi va perdre la balle des quil tire
		#if tools.pres_de_la_balle(tools.get_closest_ennemy_to_ball()) : return fonceur_predict(tools) ##bloquer cette action!
		return garder_distance_offensif(tools)
		
	elif tools.proximity_ball_goal_ami() == "proche":
		print("chepro")
		return Gardien().compute_strategy(tools._state, tools._id_team, tools._id_player)
