from __future__ import absolute_import
from soccersimulator import SoccerTeam
from .strat import Gardien, Defenseur, Milieu, Attaquant, UnVUn, Test, Test2

def get_team(nb_players):
	myteam = SoccerTeam(name="Real")
	if nb_players == 1:
		myteam.add("J1", UnVUn())
	if nb_players == 2:
		myteam.add("J1", UnVUn())
		myteam.add("J2", Gardien())
	if nb_players == 3:
		myteam.add("J1", Attaquant())
		myteam.add("J2", Attaquant())
		myteam.add("J3", Attaquant())
	if nb_players == 4:
		myteam.add("J1", Attaquant())	
		myteam.add("J2", Attaquant())
		myteam.add("J3", Attaquant())
		myteam.add("J4", Attaquant())
	return myteam 


def get_team_challenge(num):
	myteam= SoccerTeam(name="Real")
	if num == 1:
		myteam.add("Joueur Chal"+str(num),Fonceur3())
	return myteam
