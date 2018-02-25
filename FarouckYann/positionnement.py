# comportement.py

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

## Placement par defaut
def placement(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CIBLE = cible(id_team)
		
		A = placement(state, id_team, id_player, "defenseur droit", strategie = "ultra offensive")
		return vecteur_placement(state, id_team, id_player, place)
