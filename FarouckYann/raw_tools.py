# raw_tools.py

def get_distance_between(vec1, vec2):
	return vec1.distance(vec2)

def get_angle_vectoriel(v1, v2): #non oriente
		if v1.x == 0 or v2.x == 0: 
			sys.exit("Composante horizontale nulle")
		if v1.dot(v2) == 0: return math.pi / 2
		
		else: return abs(v1.angle - v2.angle)%(2*math.pi)

def resolution_equation_second_degre(A, B, C):
	delta = B*B - 4 * A * C
	
	if delta < 0:
		print("delta negatif")
		return -1000000
	
	x1 = (-B - delta.sqrt()) / 2 /A
	x2 = (-B + delta.sqrt()) / 2 /A
	
	return (x1, x2)
