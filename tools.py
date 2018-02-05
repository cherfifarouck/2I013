#########################################################################
######## Imports ------------------------------------------------------------------------------------------ #
from soccersimulator  import Strategy, SoccerAction, Vector2D
from soccersimulator import settings
import random
import math
import sys
import pdb

#pdb.set_trace()




#########################################################################
######### Definition alias ------------------------------------------------------------------------------- #
#PP = state.player_state(id_team, id_player) ##comment regler ce probleme?
#PB = state.ball.position
# id_adverse = id_adverse(id_team)

#valeur a trouver
K = 300 # distance maximale de trajet de la balle
# valeur a trouver

maxP = settings.maxPlayerAcceleration
maxB = settings.maxBallAcceleration
GW = settings.GAME_WIDTH
GH = settings.GAME_HEIGHT

POTEAU_BAS_GAUCHE = Vector2D(0., GH/2 - settings.GAME_GOAL_HEIGHT/2)
POTEAU_HAUT_GAUCHE = Vector2D(0., GH/2 + settings.GAME_GOAL_HEIGHT/2)
POTEAU_BAS_DROIT = Vector2D(settings.GAME_WIDTH * 1., GH / 2 - settings.GAME_GOAL_HEIGHT/2)
POTEAU_HAUT_DROIT = Vector2D(settings.GAME_WIDTH * 1., GH/2 + settings.GAME_GOAL_HEIGHT/2)

CENTRE_GOAL_GAUCHE = (POTEAU_BAS_GAUCHE + POTEAU_HAUT_GAUCHE) / 2
CENTRE_GOAL_DROIT = (POTEAU_BAS_DROIT + POTEAU_HAUT_DROIT) /2

ZERO = Vector2D(0., 0.)



#########################################################################
######### Definition fonctions informations -------------------------------------------------------- #
## Renvoie le numero du joueur le plus proche dans un rayon
def get_ennemi_rayon(state, id_team, id_player, rayon): #renvoie le player_state
	PP = state.player_state(id_team, id_player).position
	liste_ennemis = []
	liste_distance = []
	
	for ennemi in state.players:
		if ennemi[0] != id_team and PP.distance(state.player_state(ennemi[0], ennemi[1]).position) < rayon:
			liste_ennemis.append( ennemi[1])
			liste_distance.append( PP.distance(state.player_state(ennemi[0], ennemi[1]).position))
		
		if liste_ennemis != []: return liste_ennemis[liste_distance.index(min(liste_distance))]
	return None

## Renvoie numero du joueur sur le chemin
def get_ennemi_obstacle(state, id_team, id_player, CIBLE, angle = math.pi /4):
	PP = state.player_state(id_team, id_player).position
	PB = state.ball.position
	CIBLE = cible(id_team)
	
	liste_objets = []
	liste_distance = []
	
	for ennemi in state.players:
		if ennemi[0] != id_team and get_angle_vectoriel(state.player_state(id_adverse(id_team), ennemi[1]).position - PB, CIBLE - PB) \
		< angle:
			liste_objets.append(ennemi[1])
			liste_distance.append(PB.distance(state.player_state(id_adverse(id_team), ennemi[1]).position))
		
	if liste_objets != []: return liste_objets[liste_distance.index(min(liste_distance))]
	else: return None

## Retourne langle non oriente entre 2 vecteurs
def get_angle_vectoriel(v1, v2): #non oriente
	if v1.x == 0 or v2.x == 0: 
		sys.exit("Composante horizontale nulle")
	if v1.dot(v2) == 0: return math.pi / 2
	
	else: return abs(v1.angle - v2.angle)%(2*math.pi)

## Retourne boolean si face au ballon
def face_au_ballon(state, id_team, id_player, CIBLE, angle_acceptant = math.pi / 12):
	PB = state.ball.position
	PP = state.player_state(id_team, id_player).position
	
	if get_angle_vectoriel((PB - PP), (CIBLE - PP)) <= angle_acceptant: return True
	else: return False

## Retourn boolean si authorization de tirer
def pres_de_la_balle(state, id_team, id_player):
	if (state.ball.position.distance(state.player_state(id_team, id_player).position) \
	<= settings.BALL_RADIUS + settings.PLAYER_RADIUS):
		return True
	else: 
		return False

## Renvoie cage ennemis
def cible(id_team):
	if id_team == 1:
		return CENTRE_GOAL_DROIT
	else: return CENTRE_GOAL_GAUCHE

## Renvoie cage a defendre
def cage(id_team):
	if id_team == 1:
		return CENTRE_GOAL_GAUCHE
	else: return CENTRE_GOAL_DROIT

## Renvoie id_team_ennemi
def id_adverse(id_team):
	return (id_team % 2)+1

#inutile avec des equipes equilibres
## Plus proche de la balle dans lequipe ennemie
def test_proximite_ennemi(state, id_team, id_player):
	PP = state.player_state(id_team, id_player).position
	PB = state.ball.position
	
	#Test de proximite par rapport a la balle
	for k in state.players:
		if k[0] != id_team and PB.distance(PP) > PB.distance(state.player_state(id_adverse(id_team), k[1]).position):
			return False
			
	return True

## Plus proche de la balle dans ton equipe
def test_proximite_equipe(state, id_team, id_player):
	PP = state.player_state(id_team, id_player).position
	PB = state.ball.position
		
	for allie in state.players:
		if allie[0] == id_team and allie[1] != id_player and PB.distance(state.player_state(id_team, allie[1]).position) < PB.distance(PP):
			return False			
	return True

## Renvoie boolean
def proximite_au_but(state, id_team, id_player, distance):
	PB = state.ball.position
	CIBLE = cible(id_team)
	
	if CIBLE.distance(PB) <= distance: return True
	else: return False

## Renvoie boolean voie libre au but
def voie_libre(state, id_team, id_player, CIBLE, angle = math.pi/5): # renvoie boolean
	PP = state.player_state(id_team, id_player).position
	PB = state.ball.position
	CIBLE = cible(id_team) #enlever apres
	
	#corriger une erreur ou le joueur est sur la balle lorsqu'il veut tirer
	for ennemi in state.players:
		if ennemi[0] != id_team and get_angle_vectoriel(state.player_state(id_adverse(id_team), ennemi[1]).position - PB, CIBLE - PB) \
		< angle:
			return False
	return True

## Renvoie boolean possession equipe
def possession_equipe(state, id_team, id_player):
	PP = state.player_state(id_team, id_player).position
	PB = state.ball.position
	
	rayon_possession = 20 #ne pas depasser par BalleAuPied
	rayon_adverse = 35
	
	for ennemi in state.players:
		if ennemi[0] != id_team and PB.distance(state.player_state(id_adverse(id_team), ennemi[1]).position) <= rayon_adverse:
			return False
		
	for allie in state.players:
		if allie[0] == id_team and PB.distance(state.player_state(id_team, allie[1]).position) <= rayon_possession:
			return True
			
	return False

## Renvoie le nombre de joueurs dans lequipe
def nb_players(state, id_team):
	nombre = 0
	for joueur in state.players:
		if joueur[0] == id_team: nombre += 1
	return nombre

## modelisation lineaire par morceau de la deceleration dun joueur, voir graphe
def distance_a_decelerer(vitesse): 
	if vitesse >= 0 and vitesse < 0.1: return 0
	if vitesse >= 0.1 and vitesse < 0.52: return 14.4 * vitesse + 1.8
	if  vitesse > 0.52 and vitesse < 1.001: return 9.4
	else: print("Error: out of bounds speed", vitesse)

# A corriger
## Renvoie le coefficient de puissance en fonction de la distance
def puissance_shoot(distance):
	if distance > K:
		return settings.maxPlayerShoot
		
	#intercept inverse
	else: return distance / K * settings.maxPlayerShoot

## resolution equation du second degre dans R
def resolution_second_degre(A,B,C):
	delta = B**2 -  4*A*C
	if delta < 0: return None
	
	t1 = (-B - math.sqrt(delta)) / (2*A)
	t2 = (-B + math.sqrt(delta)) / (2*A)
	tab = [t1,t2]
	
	return tab

## approxime le point dinterception entre la balle et le joueur
def intercept(state, id_team, id_player): 
# cree de la lenteur sur les lignes droites & probleme avec les rebonds & probleme avec 
# la proximite & probleme reste coince dans les murs	
	PP = state.player_state(id_team, id_player).position # ET approximation dabsence de frottement
	PB = state.ball.position
	vP = settings.maxPlayerSpeed
	vB = state.ball.vitesse
	veB = state.ball.vitesse.normalize()
	BP_vB = (PP- PB).dot(veB)
	dPB = (PP - PB).norm
	distance = 7
	
	# limites de la modelisation, get exceptions
	if get_angle_vectoriel(state.ball.vitesse, state.player_state(id_team, id_player).vitesse) \
	< math.pi /10: return PB
	if state.ball.vitesse == 0: return PB
	if PB.distance(PP) <= distance: return PB
	
	# Equation: t^2 (vP^2 - vB^2) +t (2 cos phi * PB) - PB^2
	
	A = vP ** 2 - vB.norm**2
	B = 2* BP_vB
	C = - (dPB**2)
	
	t = resolution_second_degre(A,B,C)
	if t == None: return PB
	if min(t) <= 0:	tmin = max(t)
	else: tmin = min(t)
	
	I = PB + tmin* vB
	print(I)
	return I

## renvoie le numero du joueur ennemi
def closest_to_ball(state, id_team, id_player):
	PP = state.player_state(id_team, id_player).position
	PB = state.ball.position
	CIBLE = cible(id_team)
	
	liste_objets = []
	liste_distance = []
	
	for ennemi in state.players:
		if ennemi[0] != id_team:
			liste_objets.append(ennemi[1])
			liste_distance.append(PB.distance(state.player_state(id_adverse(id_team), ennemi[1]).position))
		
	if liste_objets != []: return liste_objets[liste_distance.index(min(liste_distance))]
	else: return None



#########################################################################
######### Definition fonctions comportement ----------------------------------------------------- #
## Renvoie un placement (position) dynamique par defaut
def placement(state, id_team, id_player, pos, liste_positions_occupees = [], **kwargs):
	tableau_strategies = ["defaut", "defensive" , "offensive" , "contre-attaque", "centre", "ultra-offensive"] #etc
	positions = ["defenseur droit", "defenseur gauche", "defenseur central", "allie", "goalie", "attaquant", "pointe"]
	liste_positions_occupees = []
	vecteur_pos = ZERO
	
	if "strategie" in kwargs.keys():
		strat = kwargs["strategie"]
	else: strat = "strategie defaut"
	
	#Coefficient equipe 0 ou 1
	if id_team == 0:
		c1 = 1
	else: c1 = -1
	
	if not possession_equipe(state, id_team, id_player):
		distance_retraite = -c1 * 10

	if pos == "goalie":
		if strat == "ultra-offensive":
			vecteur_pos.x = GW/2 - c1 * GW/4
			vecteur_pos.y = GH/2
			return vecteur_pos
		
		else:
			return Gardien().compute_strategy(state, id_team, id_player)
	if pos == "defenseur central":
		if strat == "ultra offensive":
			vecteur_pos.x = GW/2 + c1 * GW/5 + distance_retraite
			vecteur_pos.y = GH/2
			return vecteur_pos
			
		else:
			vecteur_pos.x = GW/2 - c1* 1/5 *GW + distance_retraite
			vecteur_pos.y = GH/2
			return vecteur_pos
	if pos == "defenseur droit":
		if strat == "ultra offensive":
			vecteur_pos.x = GW/2 + c1 * GW/5 + distance_retraite
			vecteur_pos.y = GH/2 - c1 * GH/4
			return vecteur_pos
			
		else:
			vecteur_pos.x = GW/2 - c1* 1/5 *GW + distance_retraite
			vecteur_pos.y = GH/2 - c1 * 1/4 * GH
			return vecteur_pos
	if pos == "defenseur gauche":
		if strat == "ultra offensive":
			vecteur_pos.x = GW/2 + c1 * GW/5 + distance_retraite
			vecteur_pos.y = GH/2 + c1 * GH/4
			return vecteur_pos
			
		else:
			vecteur_pos.x = GW/2 - c1* 1/5 *GW + distance_retraite
			vecteur_pos.y = GH/2 + c1 * 1/4
			return vecteur_pos
	if pos == "ailier":
		if "defenseur droit" in liste_positions_occupees:
			if strat == "ultra offensive":
				vecteur_pos.x = GW/2 + c1 * GW/4 + distance_retraite
				vecteur_pos.y = GH/2 + c1 * GW/4
				return vecteur_pos
			
			else:
				vecteur_pos.x = GW/2 - c1 * GW/5 + distance_retraite
				vecteur_pos.y = GH/2 + c1 * GH/4
				return vecteur_pos		
				
		if "defenseur gauche" in liste_positions_occupees:
			if strat == "ultra offensive":
				vecteur_pos.x = GW/2 + c1 * GW/4 + distance_retraite
				vecteur_pos.y = GH/2 - c1 * GW/4
				return vecteur_pos
			
			else:
				vecteur_pos.x = GW/2 + c1 * GW/5 + distance_retraite
				vecteur_pos.y = GH/2 - c1 * GH/4
				return vecteur_pos	
	if pos == "attaquant":
		if strat == "ultra offensive":
			vecteur_pos.x = GW/2 + c1 * GW/4 + distance_retraite
			vecteur_pos.y = GH /2
			
		else:
			vecteur_pos.x = GW/2 + c1* GW/6 + distance_retraite
			vecteur_pos.y = GH /2	

def vecteur_placement(state, id_team, id_player, A):
	PB = state.ball.vitesse
	PP = state.player_state(id_team, id_player).position
	
	deplacement = (A - PP + k*(PB -A).normalize()).normalize * maxP
	return SoccerAction(deplacement, ZERO)

## Placement derriere la balle et passe a cible
# ameliorer dabord prediction de intercept
# verifier si limprecision est juste due  a langle BPA ou au vecteur direction aussi
def place_et_passe(state, id_team, id_player, CIBLE, distance_derriere_balle = 1.49):
	PP = state.player_state(id_team, id_player).position
	PB = state.ball.position
	player_shoot = puissance_shoot((CIBLE - PP).norm)
	rayon_ralentissement = distance_a_decelerer(state.player_state(id_team, id_player).vitesse.norm)
	
	if pres_de_la_balle(state, id_team, id_player) and \
	PB.distance(PP) <= rayon_ralentissement and not face_au_ballon(state, id_team, id_player, CIBLE):
		# ralentir
		return SoccerAction( ZERO, ZERO)
			
	if pres_de_la_balle(state, id_team, id_player) and face_au_ballon(state, id_team, id_player, CIBLE):
		#shoot
		return SoccerAction(ZERO, (CIBLE-PP).normalize() * maxB*player_shoot )
	
	else: 
		#courir
		return SoccerAction( (PB- PP + (PB - CIBLE).normalize() * distance_derriere_balle).normalize()* maxP, ZERO)

## Deplacement le bo jeu
def deviation(state, id_team, id_player, angle): #si pres de la balle
	PB = state.ball.position
	PP = state.player_state(id_team, id_player).position
	
	direction = state.player_state(id_team, id_player).vitesse
	direction.angle += angle
	direction = direction.normalize()
	
	return SoccerAction(
		maxP * (PB - PP).normalize(),
		maxB * 0.22 * direction
		)
