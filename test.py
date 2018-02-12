from __future__ import absolute_import
from soccersimulator import SoccerTeam,Simulation,show_simu
from FarouckYann import get_team
import os

simu = Simulation(get_team(1))

show_simu(simu)


"""Suprime les fichiers .pyc"""
os.system("rm *.pyc")
os.system("cd FarouckYann; rm *.pyc")
