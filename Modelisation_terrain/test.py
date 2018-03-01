class DecisionTree(object):
	def __init__(self):
		self.noeuds = []
		
	def addNode(node):
		self.noeuds.append(node)
		

class DecisionNode(object):
	def __init__(self, description, parent, condition, consequence):
		self.description = description
		self, parent = parent
		self.condition = condition
		self.consequence = consequence
		
		self.id_team = parent.id_team
		self.id_player = parent.id_player
		self.state = parent.state

## exemple

n1 = Node(Decision defensive, PB - PP < 30, fonceur_predict())
n2 = Node(Decision defensive
n3 = 
