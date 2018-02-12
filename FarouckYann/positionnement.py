"# comportement
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

## Placement par defaut
class Placement(Strategy):
	def __init__(self):
		Strategy.__init__(self, "placement")
		
	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CIBLE = cible(id_team)
		
		A = placement(state, id_team, id_player, "defenseur droit", strategie = "ultra offensive")
		return vecteur_placement(state, id_team, id_player, place)
