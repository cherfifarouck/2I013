## sous_strat.py

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
		if t.joueur_partie_superieure():
			return SoccerAction(
				(PB - PP).normalize() * maxP,
				Vector2D((GH - Y)* (CIBLE.x - X) / (GW/2 + abs(Y- GW/2)), GH).normalize() 
				* maxB
				)
		
		if not t.joueur_partie_superieure()
			return SoccerAction(
				(PB - PP).normalize() * maxP + state.ball.vitesse,
				Vector2D((GH - Y)* (CIBLE.x - X) / (GW/2 + abs(Y-GW/2)), -GH).normalize() 
				* maxB
				)
	
	else: return t.courir_vers_balle()

## Le dribleur / balle au pied
def balle_au_pied(state, id_team, id_player, **kwargs): #standalone method and useable class
		tools = MetaState(state, id_team, id_player)
		t = tools
		
		PB = t.PB()
		PP = t.PP()
		
		if kwargs == {}:
			coordonnees = cible(id_team)
			
		if "coordonnees" in kwargs.keys():
			coordonnees = kwargs["coordonnees"]
		
		return dribler_balle(t)

# a update
def murs(state, id_team, id_player):
	t = MetaState(state, id_team, id_player)
	
	PP = t.PP()
	PB = t.PB()
	CIBLE = t.get_cible()
	rayon = 10 #sujet a modification
	angle = math.pi/4
	
	if possession_equipe(state, id_team, id_player):
		if test_proximite_equipe(state, id_team, id_player):
			if voie_libre(state, id_team, id_player, CIBLE, angle) != True:
				if state.player_state(id_adverse(id_team), get_ennemi_obstacle\
				(state, id_team, id_player, CIBLE, angle)).position.distance\
				(PP) <= rayon:
					return Furtive().compute_strategy(state, id_team, id_player)
			
				else:
					return BalleAuPied().compute_strategy(state, id_team, id_player)
			
			if voie_libre(state, id_team, id_player, CIBLE, angle):
				return BalleAuPied().compute_strategy(state, id_team, id_player)
			
		else: return placement(state, id_team, id_player, "defenseur central", strategie = "normale")
	else: return Fonceur3().compute_strategy(state, id_team, id_player)
			
def meta_strat(self, state, id_team, id_player):
	t = MetaState(state, id_team, id_player)

	PP = t.PP()
	PB = t.PB()
	CIBLE = t.get_cible()
	
	#rapidite
	ennemi = state.player_state(id_adverse(id_team), closest_to_ball(state, id_team, id_player)).position
	if PB.distance(PP) > PB.distance(ennemi): 
		return Fonceur3().compute_strategy(state, id_team, id_player)
	
	#separation murs
	if abs(PB.y - GH /2) >= 4 * GH /10:
		return Furtive().compute_strategy(state, id_team, id_player)
	
	#degagement
	if (PB.x <= GW / 4 and id_team == 1) or (PB.x >= 3 * GW / 4 and id_team == 2):
		return Fonceur1().compute_strategy(state, id_team, id_player)
	
	#droit au but
	if (PB.x >= 2 * GW / 3 and id_team == 1) or (PB.x <= GW / 3 and id_team ==2):
		return Fonceur1().compute_strategy(state, id_team, id_player)

	#Defense intelligente PAS SYMETRIQUE
	if (PB.x > GW / 4 and PB.x <= GW / 2 and id_team == 1) or \
	(PB.x < 3 *GW / 4 and PB.x >= GW / 2 and id_team == 2):
		return L2().compute_strategy(state, id_team, id_player)

	#Pu
	else: return GarderDistance().compute_strategy(state, id_team, id_player)

def attaque(self, state, id_team, id_player):
	t = MetaState(state, id_team, id_player)

	PP = t.PP()
	PB = t.PB()
	CIBLE = t.get_cible()
	
	distance_goal = 25
	distance_joueur = 35
	angle_deviation = math.pi /4
	
	if pres_de_la_balle(state, id_team, id_player): 
		if proximite_au_but(state, id_team, id_player, distance_goal) == True or \
		(voie_libre(state, id_team, id_player, CIBLE) == True and PB.distance(CIBLE) < 40):
			print("proche des buts voie libre assez proche")
			return Fonceur2().compute_strategy(state, id_team, id_player)
		
		if voie_libre(state, id_team, id_player, CIBLE):
			print("voie libre")
			return BalleAuPied().compute_strategy(state, id_team, id_player, coordonnees = CIBLE)
		
		if not voie_libre(state, id_team, id_player, CIBLE):
			print("voie po libre")
			ennemi = get_ennemi_obstacle(state, id_team, id_player, CIBLE)
			ennemi_ = state.player_state(id_adverse(id_team), ennemi)
			deplacement = (state.player_state(id_adverse(id_team), ennemi).position - PB)
			deplacement.norm = 0.21
			
			#commencer drible
			if ennemi_.position.distance(PP) < distance_joueur:
				print("ennemi proche")
				#on se rapproche des murs
				
				coef = 1
				if abs(PB.x - CIBLE.x) <2:
					angle_deviation += math.pi/8
					coef = -1
				
				if (PB.y >= GH/2 and id_team == 1) or (PB.y < GH/2 and id_team == 2):
					deplacement.angle += coef * angle_deviation
					return SoccerAction((PB- PP).normalize()*maxP, deplacement * maxB)
				else:
					deplacement.angle -= coef * angle_deviation
					return SoccerAction((PB- PP).normalize()*maxP, deplacement * maxB)
			
			else: 
				print("placement")
				return BalleAuPied().compute_strategy(state, id_team, id_player, coordonnees = CIBLE)
			
	#prendre linitiative
	if test_proximite_equipe(state, id_team, id_player):
		print("je suis le plus proche dans lequipe")
		return SoccerAction((PB-PP).normalize() * maxP, ZERO)
	else: placement(state, id_team, id_player, "attaquant", strat = "ultra offensive")

def attente(self,state,id_team,id_player, position:
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
		return SoccerAction(ZERO, (CIBLE - PB).normalize() * coefficient_entrainement *maxB)
	
	#aspect visuel du deplacement
	if (PB.x >= GW/2 and id_team == 1) or (PB.x < GW/2 and id_team==2):
		return SoccerAction( ((GOAL - PP) + distanceAuCage*\
		((PB -GOAL).normalize())).normalize() * 0.30* maxP, ZERO)
		
	else: return SoccerAction( ((GOAL - PP) + distanceAuCage*\
	((PB -GOAL).normalize())).normalize() * 0.75* maxP, ZERO)

## Strategie garder distance par rapport a la balle, aligner avec les goals
def garder_distance(self, state, id_team, id_player):
		t = MetaState(state, id_team, id_player=
		
		PP = t.PP()
		PB = t.PB()
		CAGE = t.get_cage()
		CIBLE = t.cible()
		
		coefficient = 0.33
		
		if pres_de_la_balle(state, id_team, id_player): 
			return SoccerAction((PB - PP) + coefficient* (CAGE - PB), (CIBLE-PB).normalize()*maxB)
		else: return SoccerAction((PB - PP) + coefficient* (CAGE - PB), Vector2D(0., 0.)) 

def L2(self, state, id_team, id_player):
	t = MetaState(state, id_team, id_player)
	
	PP = t.PP()
	PB = t.PB()
	coefficient = 0.33
	CIBLE = t.get_cible()
	CAGE = t.cage()
			
	
	if (PB.x >= 4*GW/7 and id_team == 1) or (PB.x <= 3* GW/7 and id_team == 2):
		return Fonceur2().compute_strategy(state, id_team, id_player)
		
	else:
		if  PB.distance(PP) > PB.distance(state.player_state(2,0).position):
			return GarderDistance().compute_strategy(state, id_team, id_player)
	
		else: 
			return Fonceur2().compute_strategy(state, id_team, id_player)

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
	
	return SoccerAction( ((state.player_state(id_adverse(id_team), joueur).position - PP) + distance * \
	(GOAL - state.player_state(id_adverse(id_team), joueur).position).normalize() ).normalize() * maxP, Vector2D(0., 0.))
