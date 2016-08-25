import numpy as np
import matplotlib.pyplot as plt
import math

data = np.genfromtxt('datos_verificacion_presion.txt', delimiter = ' ') 

x=data[:,0]
y=data[:,1]
vx=data[:,2]
vy=data[:,3]
fx=data[:,4]
fy=data[:,5]
ps=data[:,6]	## Presion social del modulo de LAMMPS


def fsocial(x1,x2,y1,y2):
	delta_x = (x1-x2)
	delta_y = (y1-y2)
	r=math.sqrt(delta_x**2+delta_y**2)
	f=2000*math.exp((0.6-r)/0.08)
	fx=f*delta_x/r
	fy=f*delta_y/r
	return f,fx,fy,r

def fdeseo(x,y,vx,vy):
	vd=4
	tau=0.5
	m=70
	door_up = 10.9
	door_dn = 9.1
	x_target=20
	if (y>door_up):
		y_target=door_up
	elif (y<door_dn):
		y_target=door_dn
	else: 
		y_target=y
	delta_x = x_target-x
	delta_y = y_target-y
	r=math.sqrt(delta_x**2+delta_y**2)
	fdx=m*((vd*delta_x/r)-vx)/tau
	fdy=m*((vd*delta_y/r)-vy)/tau
	fd=math.sqrt(fdx**2+fdy**2)
	return fdx, fdy, fd

##### Calculo de las fuerzas sociales sobre cada individuo #######

def matriz_fuerzas():
	fuerza_social = np.zeros(len(x))
	fuerza_socialx = np.zeros(len(x))
	fuerza_socialy = np.zeros(len(x))
	presion_social = np.zeros(len(x))
	for i in range(0,len(x)):
		j=0
		while j<len(x):
			if j!=i:
				fuerza_social[i] += fsocial(x[i],x[j],y[i],y[j])[0]
				fuerza_socialx[i] += fsocial(x[i],x[j],y[i],y[j])[1]
				fuerza_socialy[i] += fsocial(x[i],x[j],y[i],y[j])[2]

				presion_social[i] += fsocial(x[i],x[j],y[i],y[j])[0]*fsocial(x[i],x[j],y[i],y[j])[3]
			else:
				pass
			j+=1
	return fuerza_social, fuerza_socialx, fuerza_socialy, presion_social

print('Presion calculada con python',matriz_fuerzas()[3])
print('Presion de LAMMPS',ps)
print('Error relativo',(matriz_fuerzas()[3]-ps)/ps)

