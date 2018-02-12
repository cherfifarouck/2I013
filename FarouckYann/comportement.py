## comportement.py

def courir_vers_balle(tools):
	t = tools
	return SoccerAction( (t.PB() - t.PP).normalize() * maxP, ZERO)
	
def tirer_goal(tools):
	t = tools
	if t.pres_de_la_balle():
		return SoccerAction( ZERO, ( t.get_cible() - t.PP() ) .normalize() * maxB)

def dribler_balle(tools):
	coefficient_drible = 0.27
	t = tools
	
	return courir_vers_balle(t) + coefficient_drible * tirer_goal(t)

def random(tools):
	t = tools
	return SoccerAction(Vector2D.create_random(-1, 1), Vector2D.create_random(-1, 1))

def garder_but(tools):
	
