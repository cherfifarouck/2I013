## comportement.py
import math
from soccersimulator import SoccerAction
from .constantes import *
from .conditions import Conditions
from .raw_tools import *
from tools import *
from random import uniform

def foncer_vers_balle(tools, speed=1):
	return courir_vers(tools, tools.PB, speed)

def dribler_vers(tools, precision_drible=0.25, endroit=ZERO):
	return foncer_vers_balle(tools) + tirer_balle_vers(tools, precision_drible, coordonnees=endroit)

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

def shooter_goal(tools):
	return tirer_balle_vers(tools, 1, coordonnees=tools.cible)

def tirer_goal(tools):
	con = Conditions(tools)
	
	if not con.voie_libre(tools.cible, math.pi / 10):
		return tirer_R1(tools)
	
	elif con.voie_libre(tools.cible, math.pi / 10):
		return tirer_soutenu(tools)
		
	else:
		return shooter_goal(tools)

def tirer_soutenu(tools):
	return tirer_balle_vers(
	tools,
	puissance_recommandee(
	tools.get_distance_to_goal(), 
	tools.get_angle_to_goal()), 
	coordonnees=tools.cible)

def tirer_R1(tools):
	con = Conditions(tools)
	
	coin_sup = tools.cible + Vector2D(0., 4* settings.GAME_GOAL_HEIGHT/10)
	coin_inf = tools.cible - Vector2D(0., 4* settings.GAME_GOAL_HEIGHT/10)
	
	if uniform(0, 1) > 0.7:
		proba = -1
	else: proba = 1
	
	if con.joueur_partie_superieure():
		proba *= 1
	else: proba *= -1
	
	if proba == 1:
		coin = coin_inf
	else:
		coin = coin_sup
	
	return tirer_balle_vers(
	tools,
	puissance_recommandee(
	tools.get_distance_to_goal(),
	tools.get_angle_to_goal()),
	coordonnees=coin)

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

def retourner_au_cage(tools):
	return courir_vers(tools, tools.cage + 5* (tools.PB - tools.cage).normalize())

def recuperation(tools, prochaine_balle):
	endroit = tools.intercept_ball()# + (intercept_ball() - prochaine_balle).normalize() * (0.8 * RAYON_ACTION)
	return courir_vers(tools, endroit) + tirer_goal(tools)

def triangle(tools):
	return courir_vers(tools, tools.intercept_ball(), 0.5) + shooter_goal(tools)

def capter_balle(tools):
	if tools.pres_de_la_balle(): return SoccerAction(ZERO, -0.2 * tools.b_speed)
	else: return SoccerAction(ZERO, ZERO)
