#active matter simulation using python
"""Jagat Kafle"""

#import the libraries
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

#parameters
v0           = 2.0      #velocity
eta          = 0.5      #random fluctuation in angle
L            = 10       #box size
R            = 1.0      #interaction radius
dt           = 0.2      #time step
Nt           = 50       #number of time steps
N            = 4000     #number of birds/fishes/particles

#position and velocities of the particles
x = np.random.rand(N,1)*L
y = np.random.rand(N,1)*L
z = np.random.rand(N,1)*L
theta = 2 * np.pi * np.random.rand(N,1)
alpha = 2 * np.pi * np.random.rand(N,1)
vx = v0 * np.cos(alpha)*np.cos(theta)
vy = v0 * np.cos(alpha)*np.sin(theta)
vz = v0 * np.sin(alpha)

#initialize figure
fig = plt.figure(dpi=80)
ax = plt.gca(projection='3d')

#the simulation loop
for i in range(Nt):

	#movement of the particles
	x += vx*dt
	y += vy*dt
	z += vz*dt
	
	#periodic boundary conditions
	x = x % L
	y = y % L
	z = z % L
	
	#mean angle of neighbors within R
	mean_theta = theta
	mean_alpha = alpha
	
	for b in range(N):
		neighbors = (x-x[b])**2+(y-y[b])**2+(z-z[b])**2 < R**2
		sx = np.sum(np.cos(alpha[neighbors])*np.cos(theta[neighbors]))
		sy = np.sum(np.cos(alpha[neighbors])*np.sin(theta[neighbors]))
		sz = np.sum(np.sin(alpha[neighbors]))
		mean_theta[b] = np.arctan2(sy, sx)
		mean_alpha[b] = np.arctan2(sz, np.sqrt((sx)**2 + (sy)**2))
		
	#random deviations
	theta = mean_theta + eta*(np.random.rand(N,1)-0.5)
	alpha = mean_alpha + eta*(np.random.rand(N,1)-0.5)
	
	#update velocities
	vx = v0 * np.cos(alpha)*np.cos(theta)
	vy = v0 * np.cos(alpha)*np.sin(theta)
	vz = v0 * np.sin(alpha)
	
	#plot
	plt.cla()
	plt.quiver(x,y,z, vx,vy, vz, pivot='tip', color ='darkblue', length=0.2, normalize=True)
	ax.set(xlim3d=(0, L), ylim3d=(0, L), zlim3d=(0,L))
	plt.pause(0.001)

plt.savefig("active3d.png")
plt.show()
