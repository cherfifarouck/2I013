from FarouckYann.profAI import ParamSearch
from FarouckYann.profAI import FonceurTestStrategy
from FarouckYann.constantes import *
from numpy import arange, linspace
import random
import time

def prufung(strategy, param_tag, params, show=False):
	exp = ParamSearch(strategy, {param_tag: params})
	exp.start(show=show)
	return exp.get_res()

def new_generation_parametre(old_gen, gen_size):
	#formatting and sorting
	format_data = [(k[0], old_gen[k]) for k in old_gen]
	format_data = sorted(format_data, key=lambda x: x[1], reverse=True)
	
	#natural selection
	top_data = [format_data[k] for k in range(len(format_data)) if k <= len(format_data) // 4]
	new_gen = [k[0] for k in top_data]
	print("les parametres", new_gen)
	
	#time.sleep(1000)
	
	#repopulation of next generation
	params = random_coupling(new_gen, gen_size)
	print("on sort du random coupling et meme du next gen param")
	
	#ne pas oublier que les params sont dans une liste
	#retour = ()
	#for k in params:
		#retour += (k,)
	return params

def random_coupling(gen, gen_size):
	parent_pop_size = len(gen)
	single_people_name = [k for k in range(len(gen))]
	new_gen = []
	i = 0
	
	print("debut", single_people_name)
	
	#size of generation stays constant over the years
	while len(new_gen) <= gen_size:
		if len(single_people_name) <= 1:
			single_people_name = [k for k in range(parent_pop_size)]
		
		match1 = random.choice(single_people_name)
		single_people_name.remove(match1)
		
		match2 = random.choice(single_people_name)
		single_people_name.remove(match2)		
		
		baby = gen[match1] + gen[match2]
		new_gen.append(baby)
		
		print(match1, match2)
		print("bebezz", new_gen)
		#time.sleep(1)
	
	print(new_gen)
	
	return new_gen

def generation_loop(number):
	params = linspace(0, maxB, 8)
	size = len(params)
	
	for k in range(number):
		gen = prufung(FonceurTestStrategy(), 'strength', params)
		params = new_generation_parametre(gen, size)
		
		
	print("new_gen(data)", new_gen)

generation_loop(10)

