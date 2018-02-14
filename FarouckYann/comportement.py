## comportement.py

def foncer_vers_balle(tools):
	t = tools
	return courir_vers(t, t.PB(), maxP)

def courir_vers(tools, endroit, acceleration=1):
	t = tools
	acceleration *= maxP
	
	return SoccerAction((t.PP() - endroit).normalize() * acceleration, ZERO)

def tirer_balle_vers(tools, force, **kwargs):
	"""Renvoie un SoccerAction vers la coordonnees
	
	ou la direction au choix avec un coefficient de
	force compris entre 0 et 1.
	"""
	
	t = tools
	force *= maxP
	
	if t.pres_de_la_balle():
		if "direction" in kwargs:
			return courir_vers_balle(t) + SoccerAction( 
			ZERO, 
			(kwargs.keys("direction").normalize() * force)
			)

		if "coordonnees" in kwargs:
			return courir_vers_balle(t) + SoccerAction( 
			ZERO, 
			(kwargs.keys("coordonnees") - t.PP()).normalize() * force
			)

def tirer_goal(tools):
	t = tools
	return tirer_balle_vers(t, maxB, coordonnees=t.get_cible())

def random(tools):
	t = tools
	return SoccerAction(Vector2D.create_random(-1, 1), Vector2D.create_random(-1, 1))

def garder_but(tools):
	return 0
	
def dribler_contre_mur(tools):
	t = tools
	PB = t.PB()
	PP = t.PP()
	X = t.player_state(t._id_team, t._id_player).position.x
	Y = t.player_state(t._id_team, t._id_player).position.y
	
	if t.joueur_partie_superieure():
		return SoccerAction(
					(PB - PP).normalize() * maxP,
					Vector2D((GH - Y)* (CIBLE.x - X) / (GW/2 + abs(Y- GW/2)), GH).normalize() 
					* maxB
					)
	
	if not t.joueur_partie_superieure():
		return SoccerAction(
					(PB - PP).normalize() * maxP + state.ball.vitesse,
					Vector2D((GH - Y)* (CIBLE.x - X) / (GW/2 + abs(Y-GW/2)), -GH).normalize() 
					* maxB
					)
