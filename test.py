from soccersimulator.mdpsoccer import Simulation, SoccerState
from soccersimulator.gui import show_simu
from soccersimulator.utils import Vector2D
from __init__ import get_team


state=SoccerState.create_initial_state(1,1)
state.player_state(1,0).position=Vector2D(120,45)
state.ball.position=state.player_state(1,0).position

simu = Simulation(get_team(1),get_team(1))
show_simu(simu)
simu.start()
