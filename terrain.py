from __future__ import absolute_import
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

GW = 150.
GH = 90.

#print(np.arange(0., 1., 0.1))
def graphe_distance_a_decelerer():
	plt.plot([0,1.8,3.6,5.4,7.2,9.,9.5,9.8,9.6,9.2,9.56] )
	plt.xlabel("Vitesse (1/10)")
	plt.ylabel("Distance parcourue avant arret")
	plt.show()

def terrain():
	fig, ax = plt.subplots(num ="Terrain de foot")
	ax.set_xlim((0,150))
	ax.set_ylim((0,90))
	
	shapes = [
		#field
		patches.Rectangle(
			(0., 0.),   # (x,y)
			GW,          # width
			GH,          # height
			fill = False,
			edgecolor = None
		),
		
		#ring
		plt.Circle(
			(GW/2, GH/2.), 
			radius = 10.,
			fill = False
		),
		
		#goal position
		plt.Circle(
			(0, GH/2.), 
			radius = 8.,
			fill = False,
			color = "Blue",
			alpha = 0.5,
		),
		
		plt.Circle(
			(GW, GH/2.), 
			radius = 8.,
			fill = False,
			color = "Blue",
			alpha = 0.5,
		),
	]
	
	lines = [
		#milieu de terrain
		plt.Line2D(
			(GW/2, GW/2),
			(0, GH),
			color = "Black"
		),
		
		#goal_gauche
		plt.Line2D(
			(0., 0.),
			(GH/2 + 5, GH/2 - 5),
			color = "Red",
			lw = 4.
		),
		
		#goal_droit
		plt.Line2D(
			(GW, GW),
			(GH/2 + 5, GH/2 -5),
			color = "Blue",
			lw = 4.
		),
		
		#delimitation terrain
		plt.Line2D(
			(GW/4, GW/4),
			(0, GH),
			color = "Black",
			lw = 1.,
			alpha = 0.4,
		),
		
		plt.Line2D(
			(3*GW/4, 3*GW/4),
			(0, GH),
			color = "Black",
			lw = 1.,
			alpha = 0.4,
		),
		
		plt.Line2D(
			(0, GW),
			(GH/2, GH/2),
			color = "Black",
			lw = 1.,
			alpha = 0.4,
		),
	]
	
	for s in shapes:
		ax.add_patch(s)
	
	for l in lines:
		ax.add_line(l)
	
	plt.savefig("Terrain.png")
	plt.show()
	
#graphe_distance_a_decelerer()
terrain()

#if __name__ == '__main__':
    #import sys
    #sys.exit(main(sys.argv))
