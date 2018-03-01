from soccersimulator import settings, Vector2D

######### Definition alias ------------------------------------------------------------------------------- #
#PP = state.player_state(id_team, id_player) ##comment regler ce probleme? MetaBall
#PB = state.ball.position
# id_adverse = id_adverse(id_team)

#valeur a trouver
K = 300 # distance maximale de trajet de la balle
# valeur a trouver

RAYON_ACTION = settings.BALL_RADIUS + settings.PLAYER_RADIUS

maxP = settings.maxPlayerAcceleration
maxB = settings.maxBallAcceleration
GW = settings.GAME_WIDTH
GH = settings.GAME_HEIGHT

POTEAU_BAS_GAUCHE = Vector2D(0., GH/2 - settings.GAME_GOAL_HEIGHT/2)
POTEAU_HAUT_GAUCHE = Vector2D(0., GH/2 + settings.GAME_GOAL_HEIGHT/2)
POTEAU_BAS_DROIT = Vector2D(settings.GAME_WIDTH * 1., GH / 2 - settings.GAME_GOAL_HEIGHT/2)
POTEAU_HAUT_DROIT = Vector2D(settings.GAME_WIDTH * 1., GH/2 + settings.GAME_GOAL_HEIGHT/2)

CENTRE_GOAL_GAUCHE = (POTEAU_BAS_GAUCHE + POTEAU_HAUT_GAUCHE) / 2
CENTRE_GOAL_DROIT = (POTEAU_BAS_DROIT + POTEAU_HAUT_DROIT) /2

ZERO = Vector2D(0., 0.)
