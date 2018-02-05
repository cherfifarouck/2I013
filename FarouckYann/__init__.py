from __future__ import absolute_import
from .strat import *
from soccersimulator import SoccerTeam

def get_team (nb_team):
	
	if nb_team == 1:
		myteam = SoccerTeam(name="Paris")
		myteam.add("J1" ,FonceurEcole())
	if nb_team == 2:
		myteam = SoccerTeam(name="Lille")
		myteam.add("J2", Marquage())
	if nb_team == 3:
		
		myteam = SoccerTeam(name="Real")

		myteam.add("J1", Attaque())
	if nb_team == 4:
		myteam = SoccerTeam(name="Canard")
		myteam.add("J1",LigneDroite())
		
	return myteam 


def get_team_challenge(num):
	myteam= SoccerTeam(name="Barca")
	if num == 1:
		myteam.add("Joueur Chal"+str(num),RandomStrategy())
	return myteam
