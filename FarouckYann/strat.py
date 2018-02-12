from __future__ import absolute_import
from soccersimulator import Strategy, SoccerAction,Vector2D
from soccersimulator import settings
from .tools import *



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
		
	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CIBLE = cible(id_team)
		
		A = placement(state, id_team, id_player, "defenseur droit", strategie = "ultra offensive")
		return vecteur_placement(state, id_team, id_player, place)

#####Autre strategie
## Strategie aleatoire
class RandomStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	def compute_strategy(self,state,id_team,id_player):
		return SoccerAction(Vector2D.create_random(-1,1),Vector2D.create_random())

## Strategie attente
class Strat(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	def compute_strategy(self,state,id_team,id_player):
		PP = state.player_state(id_team, id_player).position
		A = Vector2D(GW/3, GH/2)
		return SoccerAction(ZERO, ZERO)

# Shoot aleatoirement dans la balle		
class entraineur(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Random")
	def compute_strategy(self, state, id_team, id_player):
		if pres_de_la_balle(state, id_team, id_player):
			return SoccerAction(ZERO, Vector2D.create_random().normalize()* maxB * 0.7)
		else: return Fonceur2().compute_strategy(state, id_team, id_player)

#Test interecept		
class test_intercept(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Random")
	def compute_strategy(self, state, id_team, id_player): ### Prendre en compte que on 
		#refait les calculs a chaque etape meme si les parametres nont pas change parce qu on arrive pas a recuperer ca du simulateur, stocker variable etc
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		I = intercept(state, id_team, id_player)
		
		return SoccerAction(I-PP, ZERO)

## Test rapidite par rapport au fonceur
class test_rapidite_intercept(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Random")
	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		return SoccerAction((PB-PP).normalize()*maxP, ZERO)
		
#####Strategie d'equipe
## Passe
class PasseA234(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Passe")
		
	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CIBLE = state.player_state(id_team, (id_player +1) % nb_players(state, id_team)).position
		
		#Variables
		distance_derriere_balle = 1.49 #<1.50
		
		distance_de_separation = 28
		angle_de_separation = 2*math.pi / nb_players(state, id_team)
		position = Vector2D( GW/2, GH/2) + Vector2D(angle = id_player * \
		angle_de_separation, norm = distance_de_separation)
		
		rayon_detection_balle = 25
		vitesse_max_balle = 10
		distance = 60
		angle_acceptant = math.pi / 10
		
		#engagement
		if PB.x == GW/2 and id_team == 2: # changer en t=0 #garder le meme nb aleatoire
			return SoccerAction((PB - PP).normalize() * maxP, ZERO)
		
		if test_proximite_equipe(state, id_team, id_player) and (PB.distance(PP) <= \
		rayon_detection_balle or state.ball.vitesse <= vitesse_max_balle):
			return place_et_passe(state, id_team, id_player, CIBLE, distance_derriere_balle)
		
		if position.distance(PP) <= 5:
			return SoccerAction(ZERO, ZERO)
			
		else: return SoccerAction( (position - PP).normalize() * maxP, ZERO)
#####Strategies defensives
##Gardien (defense)
class Gardien(Strategy): #probleme de degagement vector2D
	def __init__(self):
		Strategy.__init__(self, "Gardien")
	
	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		GOAL = cage(id_team)
		CIBLE = cible(id_team)
		
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
class GarderDistance(Strategy):
	def __init__(self):
		Strategy.__init__(self, "Garder distance")

	def compute_strategy(self, state, id_team, id_player):
		
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CAGE = cage(id_team)
		CIBLE = cible(id_team)
		
		coefficient = 0.33
		
		if pres_de_la_balle(state, id_team, id_player): 
			return SoccerAction((PB - PP) + coefficient* (CAGE - PB), (CIBLE-PB).normalize()*maxB)
		else: return SoccerAction((PB - PP) + coefficient* (CAGE - PB), Vector2D(0., 0.)) 

#Strategie garder distance avancee PAS SYMETRIQUE
class L2(Strategy):
	def __init__(self):
		Strategy.__init__(self, "L2")
	
	def compute_strategy(self, state, id_team, id_player):
		
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		coefficient = 0.33
		CIBLE = cible(id_team)
		CAGE = cage(id_team)
				
		
		if (PB.x >= 4*GW/7 and id_team == 1) or (PB.x <= 3* GW/7 and id_team == 2):
			return Fonceur2().compute_strategy(state, id_team, id_player)
			
		else:
			if  PB.distance(PP) > PB.distance(state.player_state(2,0).position):
				return GarderDistance().compute_strategy(state, id_team, id_player)
		
			else: 
				return Fonceur2().compute_strategy(state, id_team, id_player)

#Contenir joueur specifique
class Marquage(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Fonceur")
		
	def compute_strategy(self, state, id_team, id_player):
		PP = state.player_state(id_team, id_player).position
		PB = state.ball.position
		CIBLE = cible(id_team)
		GOAL = cage(id_team)
		distance = 15
		
		listeAMarquer = [k for k in state.players] #plus ou moins
		joueur = listeAMarquer[0][1]
		listeAMarquer = listeAMarquer[1::len(listeAMarquer)+1]
		
		return SoccerAction( ((state.player_state(id_adverse(id_team), joueur).position - PP) + distance * \
		(GOAL - state.player_state(id_adverse(id_team), joueur).position).normalize() ).normalize() * maxP, Vector2D(0., 0.))





		
		
