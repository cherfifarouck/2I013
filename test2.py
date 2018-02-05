from __future__ import absolute_import
from soccersimulator import SoccerTeam,Simulation,show_simu
from strat import *

Barca = SoccerTeam(name="Barcelone")
Real = SoccerTeam(name="Real Madrid")

def run_deux_joueurs():
	Barca.add("J1", Attaque())
	Real.add("J2", MetaStrat())
def run_strat_passe():
	Barca.add("J1", MetaStrat())
	Barca.add("Gardien barca", Gardien())
	Real.add("J2", PasseA234())
	Real.add("J3", PasseA234())
	#Real.add("defenseur", L2())
	Real.add("Gardien real", Gardien())
def run_furtive_contre_normal():
	Barca.add("J1", Attaque())
	#Barca.add("J3", Fonceur2())
	Real.add("J2", Gardien())
def run_strategie_L2():
	Barca.add("Fonceur", Fonceur2())
	Barca.add("Gardien barca", Gardien())
	Real.add("Attaque", Attaque())
	Real.add("Gardien real", Gardien())
	Real.add("Def", GarderDistance())
	

#run_deux_joueurs()
#run_strat_passe()
run_furtive_contre_normal()
#run_strategie_L2()

#Creation d'une partie
simu = Simulation(Barca,Real)
#Jouer et afficher la partie
show_simu(simu)
