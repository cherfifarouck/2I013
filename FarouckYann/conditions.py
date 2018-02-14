## condition.py

def con_rendre_symetrique(condition1, condition2, tools):
		t = tools
		
		if condition1 and t._id_team == 1 or condition2 and t._id_team == 2:
			return True
		
		if condition2 and t._id_team == 1 or condition1 and t._id_team == 2:
			return False
