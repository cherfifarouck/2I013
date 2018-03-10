from soccersimulator  import Strategy, SoccerAction, Vector2D
from .tools import SuperState, Comportement, get_random_SoccerAction
from .briques import ComportementNaif,ConditionAttaque,ConditionDefenseur,fonceur, defenseur

class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return get_random_SoccerAction()

class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Fonceur")
    def compute_strategy(self,state,id_team,id_player):
        I = ConditionAttaque(ComportementNaif(SuperState(state,id_team,id_player)))
        return fonceur(I)

class DefenseurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Defenseur")
    def compute_strategy(self,state,id_team,id_player):
        I = ConditionDefenseur(ComportementNaif(SuperState(state,id_team,id_player)))
        return defenseur(I)

class FonceurTestStrategy(Strategy):
    def __init__(self, strength=None):
        Strategy.__init__(self,"Fonceur")
        self.strength = strength
    def compute_strategy(self,state,id_team,id_player):
        C = ComportementNaif(SuperState(state,id_team,id_player))
        if self.strength:
            C.SHOOT_COEF = self.strength
        I = ConditionAttaque(C)
        return fonceur(I)



