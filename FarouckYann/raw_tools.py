# raw_tools.py
import itertools
import sys
import math
from soccersimulator import SoccerAction
from .constantes import maxB, ZERO

def get_angle_vectoriel(v1, v2): #non oriente
		#if v1.x == 0 or v2.x == 0: 
			#sys.exit("Composante horizontale nulle")
		if v1.dot(v2) == 0: return math.pi / 2
		
		else: return abs(v1.angle - v2.angle)%(2*math.pi)

def resolution_equation_second_degre(A, B, C):
	delta = B*B - 4 * A * C
	
	if delta < 0:
		print("delta negatif")
		return -1000000
	
	x1 = (-B - delta.sqrt()) / 2 /A
	x2 = (-B + delta.sqrt()) / 2 /A
	
	return (x1, x2)

def predict_ball_movement(tools):
	#scalaire distance de prediction
	K = 2
	
	position_future = tools.PB + K * tools.ball.vitesse.normalize()
	return position_future

def probabilite_de_marquer(tools):
	distance_au_goal = tools.get_distance_to_goal()
	angle = tools.get_angle_to_goal()
	puissance_shoot = puissance_recommandee(distance_au_goal, angle)
	
	tab_proba = [k / 100 for k in range(0, 101)]
	return 1

def puissance_recommandee(distance_au_cage, angle):
	if angle > math.pi/2 - math.pi/6:
		return 0.5
	if distance_au_cage > 50:
		return 1
	else: return 0.8


def fonction_marquage_encodee(tools):
	listeA = tools.get_friendly_positions()
	listeB = tools.get_ennemy_positions()
	
	def distance_totale(couple):
		somme = 0
		for k in couple:
			somme += abs( (listeA[k[0]] - listeB[k[1]]).norm )

		return somme

	def fonction_marquage(code):
		couple = []
		for k in code:
			couple.append((code.index(k),k))
		return couple

	def permutation():
		permutation_possible = list(itertools.permutations([k for k in range(len(listeA))]))
		tab_meso = []

		for i in range(len(listeA) * len(listeB)):
			tab_meso.append(distance_totale(fonction_marquage(permutation_possible[i]), listeA, listeB))

		return permutation_possible.index(min(tab_meso))
	
	return permutation()

def partie_reelle(SA):
	return SoccerAction(SA.acceleration, ZERO)

def partie_imaginaire(SA):
	return SoccerAction(ZERO, SA.shoot)
	
def mult_SA(k, SA):
	return SoccerAction(k * SA.acceleration, k * SA.shoot)
