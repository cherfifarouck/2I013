from __future__ import absolute_import
from soccersimulator import Strategy, SoccerAction,Vector2D
from soccersimulator import settings
from .tools import *

<<<<<<< HEAD
class Gardien(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Gardien")
=======


class FonceurStrategy(Strategy):
    def __init__(self):
        super(FonceurStrategy,self).__init__("Fonceur")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)


class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random(-0.5,0.5),Vector2D.create_random(-0.5,0.5))


## Strategie ligne droite
class LigneDroite(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Fonceur")
		
	def compute_strategy(self, state, id_team, id_player, coef = 0.3):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CIBLE = cible(id_team)
		
		if CIBLE.x < 10:
			coefficient = -1
		else: coefficient = 1
		if pres_de_la_balle(state, id_team, id_player) == True:
			return SoccerAction((PB -PP).normalize() * maxP, Vector2D(coefficient * settings.maxPlayerShoot, 0.))
			#return SoccerAction((PB -PP).normalize() * maxP, Vector2D(angle = (CIBLE - PB).angle + math.pi/2, norm = 1.))
			
		else: return SoccerAction((PB-PP).normalize() * coef* maxP, Vector2D(0.,0.))

## Strategie fonceur bourrin pas dengagement
class Fonceur1(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Fonceur")
		
	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CIBLE = cible(id_team)
		
		if PB.x == GW/2: return LigneDroite().compute_strategy(state, id_team, id_player, 0.35)
		
		#strategie fonceur basique
		if pres_de_la_balle(state, id_team, id_player):
			return SoccerAction(
				maxP * (CIBLE - PP).normalize(),
				maxB *(CIBLE - PB).normalize() 
				)
			
		else: return SoccerAction((PB - PP).normalize() * maxP, Vector2D(0., 0.) )

## Fonceur precis par rapport a la distance au cage
class Fonceur2(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Contre la montre")

	def compute_strategy(self, state, id_team, id_player):
		PB = state.ball.position
		PP = state.player_state(id_team, id_player).position
		CIBLE = cible(id_team)
		
		if pres_de_la_balle(state, id_team, id_player):
			return SoccerAction(
				maxP * (CIBLE - PP).normalize(),
				((2* maxB - maxP) 
				/ GW * CIBLE.distance(PB) + maxP / 2) * (CIBLE - PB).normalize()
				)
				
		else: return SoccerAction((PB - PP).normalize() * maxP, Vector2D(0., 0.) )

## Fonceur predict ball
class Fonceur3(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Predictions")

	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		
		coefficient = 1
		CIBLE = cible(id_team)
		
		if pres_de_la_balle(state, id_team, id_player):
			return SoccerAction((CIBLE - PP).normalize() * maxP, (CIBLE - PB).normalize() * maxB/1.5)
			
		else:
			return SoccerAction((PB + coefficient * state.ball.vitesse -PP ).normalize() *maxP, Vector2D(0., 0))

## Fonceur precis par rapport a la distance au cage (ECOLE)
class FonceurEcole(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Contre la montre")

	def compute_strategy(self, state, id_team, id_player):
		PB = state.ball.position
		PP = state.player_state(id_team, id_player).position
		
		#determiner lequipe
		CIBLE = cible(id_team)
		
		if pres_de_la_balle(state, id_team, id_player) == True and PB.x == GW/2: # engagement
			return SoccerAction(
				maxP * (PB - PP).normalize(),
				maxB * 0.85 * ((-CIBLE.distance(PP))/ (GW/2) + 2) * (CIBLE - PB).normalize()
				)
		
		if pres_de_la_balle(state, id_team, id_player) == True and not PB.x == GW/2: #finition
			return SoccerAction(
				maxP * (PB - PP).normalize(),
				maxB * 2.8 * ((-CIBLE.distance(PP))/ (GW/2) + 2) * (CIBLE - PB).normalize() #2.8
				)
				
		else: return SoccerAction((PB - PP).normalize() * maxP, Vector2D(0., 0.) )


		
## Tir par rapport au murs
class Furtive(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Langle incident")

	def compute_strategy(self, state, id_team, id_player):
		#TRIGO
		CIBLE = cible(id_team)
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		X = state.player_state(id_team, id_player).position.x
		Y = state.player_state(id_team, id_player).position.y
		
		if pres_de_la_balle(state, id_team, id_player) == True:
			if (PB.x > 3* GW / 4 and id_team == 1) or (PB.x < GW / 4 and id_team == 2): 
				return Fonceur2().compute_strategy(state, id_team, id_player)
				
			if (PB.x <= 3* GW / 4 and id_team == 1) or (PB.x >= GW / 4 and id_team == 2):
				if PB.y >= GH / 2:
					return SoccerAction(
						(PB - PP).normalize() * maxP,
						Vector2D((GH - Y)* (CIBLE.x - X) / (GW/2 + abs(Y- GW/2)), GH).normalize() 
						* maxB
						)
				
				if PB.y < GH / 2:
					return SoccerAction(
						(PB - PP).normalize() * maxP + state.ball.vitesse,
						Vector2D((GH - Y)* (CIBLE.x - X) / (GW/2 + abs(Y-GW/2)), -GH).normalize() 
						* maxB
						)
			
		else: return SoccerAction(PB + 6.5* state.ball.vitesse - PP, Vector2D(0., 0.) )

## Le dribleur / balle au pied
class BalleAuPied(Strategy): #donner une destination au drible
	def __init__(self):
		Strategy.__init__(self, "Le bo jeu")

	def compute_strategy(self, state, id_team, id_player, **kwargs): #standalone method and useable class
		PB = state.ball.position
		PP = state.player_state(id_team, id_player).position
		
		if kwargs == {}:
			coordonnees = cible(id_team)
			
		if "coordonnees" in kwargs.keys():
			coordonnees = kwargs["coordonnees"]
		
		if pres_de_la_balle(state, id_team, id_player):
			return SoccerAction(
				maxP * (PB - PP).normalize(),
				maxB * 0.27 * (coordonnees - PB).normalize()
				)
				
		else: return SoccerAction((PB - PP).normalize() * maxP, Vector2D(0., 0.) )

## Engagement de base
class Engagement(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Engagement")
		
	def compute_strategy(self, state, id_team, id_player):
		PB = state.ball.position
		PP = state.player_state(id_team, id_player).position
		CIBLE = cible(id_team)
		
		 #a remplacer par t=0
		if PB.x == GW /2:
			for ennemi in state.players:
				print("distances ",state.player_state(ennemi[0], ennemi[1]).position.distance(PB), PB.distance(PP)) # distances egale bizarre
				if state.player_state(ennemi[0], ennemi[1]).position.distance(PB) == PB.distance(PP):
					if pres_de_la_balle(state, id_team, id_player):
						return SoccerAction(maxB * (PB - PP).normalize(), (CIBLE - PP).normalize() * maxB)
					
					else:
						return SoccerAction(maxB * (PB - PP).normalize(), ZERO)

## Meta furtive
class Murs(Strategy):
		def __init__(self):
			Strategy.__init__(self, "feru de murs")
		
		def compute_strategy(self, state, id_team, id_player):
			PP = state.player_state(id_team, id_player).position
			PB = state.ball.position
			CIBLE = cible(id_team)
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
			
## Meta Strat division 1/4
class MetaStrat(Strategy):
	def __init__(self):
		Strategy.__init__(self, "La strategie pour toute les dominer")

	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CIBLE = cible(id_team)
		
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

## Attaque amelioree, meta attaque
class Attaque(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Attaque amelioree")
		
	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CIBLE = cible(id_team)
		
		distance_goal = 25
		distance_joueur = 35
		angle_deviation = math.pi /4
		
		#if PB.x == GW/2: 
			#return Engagement().compute_strategy(state, id_team, id_player)
				
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
			
## Placement par defaut
class Placement(Strategy):
	def __init__(self):
		Strategy.__init__(self, "placement")
>>>>>>> d7d98b0213e18837da170177df70f51342343d2f
		
	def compute_strategy(self, state, id_team, id_player):
		return SoccerAction(ZERO, ZERO)
		
class Gardien(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Gardien")
		
	def compute_strategy(self, state, id_team, id_player):
		
		
class Gardien(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Gardien")
		
	def compute_strategy(self, state, id_team, id_player):
	
class Gardien(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Gardien")
		
	def compute_strategy(self, state, id_team, id_player):
		
