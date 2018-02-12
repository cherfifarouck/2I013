from __future__ import absolute_import
from .strat import *
from soccersimulator import SoccerTeam

def get_team(nb_players):
	myteam = SoccerTeam(name="Real")
	if nb_players == 1:
		myteam.add("J1" ,Fonceur3())
	if nb_players == 2:
		myteam.add("J1", Fonceur3())
		myteam.add("J2" ,Fonceur3())
	if nb_players == 3:
		myteam.add("J1" ,Fonceur3())
		myteam.add("J2", Fonceur3())
		myteam.add("J3" ,Fonceur3())
	if nb_players == 4:
		myteam.add("J1" ,Fonceur3())	
		myteam.add("J2", Fonceur3())
		myteam.add("J3" ,Fonceur3())
		myteam.add("J4" ,Fonceur3())
	return myteam 


def get_team_challenge(num):
	myteam= SoccerTeam(name="Real")
	if num == 1:
		myteam.add("Joueur Chal"+str(num),Fonceur3())
	return myteam
