from FarouckYann.profAI import ParamSearch
from FarouckYann.profAI import FonceurTestStrategy
from FarouckYann.constantes import *
from numpy import arange, linspace, mean
import random
import time

RECOMMENDED_NUMBER_OF_LOOP = 8
RECOMMENDED_NUMBER_OF_PARAMETERS = 16

def average(l):
	return sum(l)/len(l)

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
	
	#repopulation of next generation
	params = random_coupling(new_gen, gen_size)
	return params

def random_coupling(gen, gen_size):
	parent_pop_size = len(gen)
	single_people_name = [k for k in range(len(gen))]
	new_gen = []
	i = 0
	
	#size of generation stays constant over the years
	while len(new_gen) < gen_size:
		if len(single_people_name) <= 1:
			single_people_name = [k for k in range(parent_pop_size)]
		
		match1 = random.choice(single_people_name)
		single_people_name.remove(match1)
		
		match2 = random.choice(single_people_name)
		single_people_name.remove(match2)		
		
		baby = (gen[match1] + gen[match2]) / 2
		new_gen.append(baby)
	
	return new_gen

def mutate_parameters(param):
	param = [round(k*1000)/1000 for k in param]
	
	for n in range(len(param)):
		for m in range(len(param)):
			if param[n] == param[m]:
				param[m] += random.uniform(-0.05, 0.05)
	
	return param

def verification_convergence(params, alpha):
	maxi, mini = max(params), min(params)
	if maxi - mini < alpha:
		return True

def generation_loop(number):
	params = linspace(0, maxB, RECOMMENDED_NUMBER_OF_PARAMETERS)
	size = len(params)
	
	def record_data(data):
		with open("./FarouckYann/profAI/data.txt", "a") as f1:
			f1.write(data+'\n')
	
	for k in range(number):
		gen = prufung(FonceurTestStrategy(), 'strength', params)
		params = mutate_parameters(new_generation_parametre(gen, size))
		if verification_convergence(params, 0.25):
			record_data(str(average(params)))
			return average(params)
	
	record_data(str(average(params)))
	return average(params)

def loop_generation_test():
	
	while 1:
		generation_loop(RECOMMENDED_NUMBER_OF_LOOP)

loop_generation_test()
