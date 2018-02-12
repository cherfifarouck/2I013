from __future__ import absolute_import
from soccersimulator import SoccerTeam,Simulation,show_simu
from FarouckYann import get_team
import os

#simu = Simulation(get_team(1),get_team(2))
#simu = Simulation(get_team(1),get_team(3))
simu = Simulation(get_team(1),get_team(4))
#simu = Simulation(get_team(1),get_team(2))
#simu = Simulation(get_team(2),get_team(4))
#simu = Simulation(get_team(3),get_team(4))

show_simu(simu)


"""Suprime les fichiers .pyc"""
os.system("rm *.pyc")
os.system("cd FarouckYann; rm *.pyc")
