## comportement.py
from soccersimulator import SoccerAction
from .constantes import *

def foncer_vers_balle(tools):
	t = tools
	return courir_vers(t, t.PB, 1)

def courir_vers(tools, endroit, acceleration=1):
	acceleration *= maxP
	
	return SoccerAction((endroit - tools.PP).normalize() * acceleration, ZERO)

def tirer_balle_vers(tools, force, **kwargs):
	"""Renvoie un SoccerAction vers la coordonnees
	
	ou la direction au choix avec un coefficient de
	force compris entre 0 et 1.
	"""
	
	force *= maxB
	
	if tools.pres_de_la_balle():
		if "direction" in kwargs:
			return foncer_vers_balle(tools) + SoccerAction( 
			ZERO, 
			(kwargs["direction"].normalize() * force)
			)

		if "coordonnees" in kwargs:
			return foncer_vers_balle(tools) + SoccerAction( 
			ZERO, 
			(kwargs["coordonnees"] - tools.PP).normalize() * force
			)
	
	return SoccerAction(ZERO, ZERO)

def tirer_goal(tools):
	return tirer_balle_vers(tools, 1, coordonnees=tools.cible)

def random(tools):
	return SoccerAction(Vector2D.create_random(-1, 1), Vector2D.create_random(-1, 1))

def garder_but(tools):
	return 0
	
def dribler_contre_mur(tools):
	con = Conditions(tools)
	CIBLE = tools.cible
	X = tools.player_state(tools._id_team, tools._id_player).position.x
	Y = t.player_state(tools._id_team, tools._id_player).position.y
	
	if con.joueur_partie_superieure():
		return SoccerAction(
					(tools.PB - tools.PP).normalize() * maxP,
					Vector2D((GH - Y)* (CIBLE.x - X) / (GW/2 + abs(Y- GW/2)), GH).normalize() 
					* maxB
					)
	
	if not con.joueur_partie_superieure():
		return SoccerAction(
					(tools.PB - tools.PP).normalize() * maxP + tools.b_speed,
					Vector2D((GH - Y)* (CIBLE.x - X) / (GW/2 + abs(Y-GW/2)), -GH).normalize() 
					* maxB
					)

def tirer(tools):
	return (tools.cible - tools.PB).normalize() *  \
	puissance_recommandee(tools.get_distance_to_goal(), tools.get_angle_to_goal())

def retourner_au_cage(tools):
	return courir_vers(tools, tools.cage)
