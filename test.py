from __future__ import absolute_import
from soccersimulator import SoccerTeam,Simulation,show_simu
from FarouckYann import * #get_team
import os

team1 = SoccerTeam(name="Real")
team2 = SoccerTeam(name="Barca")
team1.add("J1", UnVUn())
team2.add("J2", UnVUn())
#simu = Simulation(team1, team2)
simu = Simulation(get_team(1), get_team(1))

show_simu(simu)

"""Appelle un script bash qui suprime les fichiers *.pyc"""
os.system("bash clean.sh")

## rajouter des dribles
# fix le degagement faire quil tire aussi vers la haut
## faire attention au degagement lors de la recuperation de balle
