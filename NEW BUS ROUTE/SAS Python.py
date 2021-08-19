# Program:  A Privacy Preserving Algorithm to Achieve Vehicle Platooning
# Goal:  To control a set of vehicles near or on the UCD campus so that they all achieve the same average speed, without having to reveal private information about their speed to their neighbours.  Includes real vehicles.
# Programmer:  Wynita Griggs
# Date:  17th June, 2016

# Assumptions:  <To do.>

# To do:
# (a) If the connection to the smartphone is interrupted, remove the real car from the scenario and clean up properly.
# (b) A project for a masters student is to include real car GPS coordinates and map matching.

from multiprocessing import Process, Manager
	# The multiprocessing module provides a way to work with shared objects if they run under the control of a so-called manager.  A manager is a separate subprocess where the
	# real objects exist and which operates as a server.  Other processes access the shared objects through the use of proxies that operate as clients of the manager server.

import socket
	# For TCP servers, the socket object used to receive connections is not the same socket used to perform subsequent communication with the client.  In particular, the accept()
	# system call returns a new socket object that's actually used for the connection.  This allows a server to manage connections from a large number of clients simultaneously.
	
import thread
import time

import os, sys
import subprocess
import traci

import random
import numpy
from cvxpy import *

from xlwt import Workbook, easyxf

# real vehicles:  avatars representing these are added to and removed from the simulation as communications with smartphones are established and terminated
def addRealVehicle(ticket):
	
	priusEdges = ['-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7', '-228955668#6', '-228955668#5', '-228955668#4', '-228955668#3', '-228955668#2', '-228955668#1', '-228955668#0', '97167752', '337793646#0', '337793646#1', '337793645#0', '337793645#1', 
				  '337793645#2', '337793645#3', '337793645#4', '337793645#5', '-7976644#9', '-7976644#8', '-7976644#7', '-7976644#6', '-7976644#5', '-7976644#4', '-7976644#3', '-7976644#2', '-7976644#1', '-7976644#0', 
				  '-32297486#1', '-32297486#0', '32297485#3', '32297485#4', '32297485#0', '32297485#1', '32297485#2', '32297486#0', '32297486#1', '7976644#0', '7976644#1', '7976644#2', '7976644#3', 
				  '7976644#4', '7976644#5', '7976644#6', '7976644#7', '7976644#8', '7976644#9', '-337793645#5', '-337793645#4', '-337793645#3', '-337793645#2', '-337793645#1', '-337793645#0', '-337793646#1', 
				  '-337793646#0', '-97167752', '228955668#0', '228955668#1', '228955668#2', '228955668#3', '228955668#4', '228955668#5', '228955668#6', '228955668#7', '7977687#0', '7977687#1', '7977687#2', '7977689', 
				  '7977688#0', '115099075', '25094818#0', '25094818#1', '-228955668#7'] # 10 return laps
	traci.route.add('routePrius{}'.format(ticket), priusEdges)
	traci.vehicle.addFull('vehPrius{}'.format(ticket), 'routePrius{}'.format(ticket), typeID='vTypePassenger', depart=None, departLane='0', departPos='base', departSpeed='0') # ensure that a vType with id="vTypePassenger"
																																											   # exists in the route file
	traci.vehicle.setColor('vehPrius{}'.format(ticket), (252,252,252,0)) # default colour is light grey
	
def removeRealVehicle(i):

	traci.vehicle.remove('vehPrius{}'.format(i+1), reason=3)
	
# server program
def server(flag_hello_smartphone, flag_goodbye_smartphone, smartphone_broadcast, central_authority_broadcast):
	
	# initialisation
	realVehicleIndex = 0 # track list indices corresponding to real vehicles
	
	# size of buffer and backlog
	buffer = 2048 # value should be a relatively small power of 2, e.g. 4096
	backlog = 1 # tells the operating system to keep a backlog of 1 connection; this means that you can have at most 1 client waiting while the server is handling the current client;
				# the operating system will typically allow a maximum of 5 waiting connections; to cope with this, busy servers need to generate a new thread to handle each incoming
				# connection so that it can quickly serve the queue of waiting clients

	# create a socket
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4 socket family; SOCK_STREAM = TCP socket type

	# bind the socket to an address and port
	host = '137.43.44.98' # a string containing the hostname of the machine where the Python interpreter is currently executing
	port = 50100 # reserve a port for the service (i.e. a large number less than 2^16); the call will fail if some other application is already using this port number on the same machine
	serverSocket.bind((host, port)) # binds the socket to the hostname and port number

	# listen for incoming connections
	serverSocket.listen(backlog)
	
	def clientHandle(clientSocket, address, realVehicleIndex):
	
		while True: # infinite loop 2
			incoming = clientSocket.recv(buffer) # receive client data into buffer
			if (incoming == 'quit'):
				print 'Ending session with client.'
				clientSocket.close() # close the connection with the client
				smartphone_broadcast[realVehicleIndex] = 0.0
				central_authority_broadcast[realVehicleIndex] = 'No Advice'
				flag_goodbye_smartphone[realVehicleIndex] = True
				break # breaks out of infinite loop 2
			smartphone_broadcast[realVehicleIndex] = float(incoming)*1000/3600 # convert km/h to m/s
			clientSocket.send(central_authority_broadcast[realVehicleIndex] + '\n') # send the data to the client
			
	while True: # infinite loop 1
		clientSocket, address = serverSocket.accept() # passively accept TCP client connections; the call returns a pair of arguments:  clientSocket is a new Socket object used to communicate
													  # with the client and address is the address of the client
	
		# record client connection time (as seen from the server)
		start_time = time.strftime('%d %b %Y at %H:%M:%S')
		init_time = str(start_time) # convert connection time to a string
		print 'Made a connection with', address, 'on', init_time + '.'
		
		flag_hello_smartphone[0] = True
		smartphone_broadcast.append(0.0)
		central_authority_broadcast.append('No Advice')
		flag_goodbye_smartphone.append(False)
		
		# create new thread
		thread.start_new_thread(clientHandle, (clientSocket, address, realVehicleIndex))
		
		realVehicleIndex += 1

# control algorithms	
def controlAlgorithmLeaderless(vehicleSet):

	vehicleSetSubset = []
	
	# noise calculation
	mu = 0 ; sigma = 0.5
	noise = random.gauss(mu, sigma)
	# print 'Noise generated by Base Station 1 this time step: {}'.format(noise)

	for i in range(len(vehicleSet)):

		print 'Speed for Vehicle {} this time step [m/s]: {}'.format(vehicleSet[i], traci.vehicle.getSpeed(vehicleSet[i]))
		
		if traci.vehicle.getSpeed(vehicleSet[i]) > 5.56: # 5.56m/s = approx. 20km/h
			vehicleSetSubset.append(vehicleSet[i])
		else:
			indexIdentifierControl = participants.index(vehicleSet[i])
			newSpeed[indexIdentifierControl] = -1
			controlHistory[indexIdentifierControl] = 0
			if 'vehPrius' not in vehicleSet[i]:
				traci.vehicle.setSpeed(vehicleSet[i], -1)
		
	for i in range(len(vehicleSetSubset)):
		
		if len(vehicleSetSubset) > 1: # i.e. if there is more than one vehicle in the set of vehicles to be controlled...
	
			# first term calculation; "link to neighbours"
			if i - 1 < 0:
				firstTerm = traci.vehicle.getSpeed(vehicleSetSubset[i+1]) - traci.vehicle.getSpeed(vehicleSetSubset[i])
			elif i + 1 >= len(vehicleSetSubset):
				firstTerm = traci.vehicle.getSpeed(vehicleSetSubset[i-1]) - traci.vehicle.getSpeed(vehicleSetSubset[i])
			else:
				firstTerm = traci.vehicle.getSpeed(vehicleSetSubset[i-1]) - traci.vehicle.getSpeed(vehicleSetSubset[i]) + traci.vehicle.getSpeed(vehicleSetSubset[i+1]) - traci.vehicle.getSpeed(vehicleSetSubset[i])
			# print 'First term for {}: {}'.format(vehicleSetSubset[i], firstTerm)
			
			# second term calculation; "link to everybody"
			sum = 0
			for j in range(len(vehicleSetSubset)):
				if j != i:
					sum = sum + (traci.vehicle.getSpeed(vehicleSetSubset[j]) - traci.vehicle.getSpeed(vehicleSetSubset[i])) * noise
			secondTerm = sum
			# print 'Second term for {}: {}'.format(vehicleSetSubset[i], secondTerm)
				
			# control output; the effect is seen next time step
			control = firstTerm + secondTerm # acceleration [m/s^2]
			indexIdentifierControl = participants.index(vehicleSetSubset[i])
			integral = numpy.trapz([controlHistory[indexIdentifierControl], control], dx=0.1) # integrate to get speed [m/s]
			newSpeed[indexIdentifierControl] = traci.vehicle.getSpeed(vehicleSetSubset[i]) + integral
		
		else:
			control = 0
			indexIdentifierControl = participants.index(vehicleSetSubset[i])
			newSpeed[indexIdentifierControl] = -1
		
		controlHistory[indexIdentifierControl] = control
	
	for i in range(len(vehicleSetSubset)):
		if len(vehicleSetSubset) > 1:
			indexIdentifierControl = participants.index(vehicleSetSubset[i])
			if 'vehPrius' not in vehicleSetSubset[i]:
				traci.vehicle.setSpeed(vehicleSetSubset[i], newSpeed[indexIdentifierControl])
		else:
			if 'vehPrius' not in vehicleSetSubset[i]:
				traci.vehicle.setSpeed(vehicleSetSubset[i], -1)

def controlAlgorithmExternalReference(vehicleSet):

	vehicleSetSubset = []
	
	# noise calculation
	mu = 0 ; sigma = 0.5
	noise = random.gauss(mu, sigma)
	# print 'Noise generated by Base Station 1 this time step: {}'.format(noise)

	for i in range(len(vehicleSet)):

		print 'Speed for Vehicle {} this time step [m/s]: {}'.format(vehicleSet[i], traci.vehicle.getSpeed(vehicleSet[i]))
		
		if traci.vehicle.getSpeed(vehicleSet[i]) > 5.56: # 5.56m/s = approx. 20km/h
			vehicleSetSubset.append(vehicleSet[i])
		else:
			indexIdentifierControl = participants.index(vehicleSet[i])
			newSpeed[indexIdentifierControl] = -1
			controlHistory[indexIdentifierControl] = 0
			if 'vehPrius' not in vehicleSet[i]:
				traci.vehicle.setSpeed(vehicleSet[i], -1)
		
	for i in range(len(vehicleSetSubset)):
		
		if len(vehicleSetSubset) > 1: # i.e. if there is more than one vehicle in the set of vehicles to be controlled...
	
			# first term calculation; "link to neighbours"
			if i == 0:
				firstTerm = externalReference - traci.vehicle.getSpeed(vehicleSetSubset[i])
			else:
				firstTerm = 0
			# print 'First term for {}: {}'.format(vehicleSetSubset[i], firstTerm)
			
			# second term calculation; "link to everybody"
			sum = 0
			for j in range(len(vehicleSetSubset)):
				if j != i:
					sum = sum + (traci.vehicle.getSpeed(vehicleSetSubset[j]) - traci.vehicle.getSpeed(vehicleSetSubset[i])) * noise
			secondTerm = sum
			# print 'Second term for {}: {}'.format(vehicleSetSubset[i], secondTerm)
				
			# control output; the effect is seen next time step
			control = firstTerm + secondTerm # acceleration [m/s^2]
			indexIdentifierControl = participants.index(vehicleSetSubset[i])
			integral = numpy.trapz([controlHistory[indexIdentifierControl], control], dx=0.1) # integrate to get speed [m/s]
			newSpeed[indexIdentifierControl] = traci.vehicle.getSpeed(vehicleSetSubset[i]) + integral
		
		else:
			control = 0
			indexIdentifierControl = participants.index(vehicleSetSubset[i])
			newSpeed[indexIdentifierControl] = -1
		
		controlHistory[indexIdentifierControl] = control
	
	for i in range(len(vehicleSetSubset)):
		if len(vehicleSetSubset) > 1:
			indexIdentifierControl = participants.index(vehicleSetSubset[i])
			if 'vehPrius' not in vehicleSetSubset[i]:
				traci.vehicle.setSpeed(vehicleSetSubset[i], newSpeed[indexIdentifierControl])
		else:
			if 'vehPrius' not in vehicleSetSubset[i]:
				traci.vehicle.setSpeed(vehicleSetSubset[i], -1)

def controlAlgorithmCostFunctions(vehicleSet):

	vehicleSetSubset = []
	
	# noise calculation
	mu = 0 ; sigma = 0.5
	noise = random.gauss(mu, sigma)
	# print 'Noise generated by Base Station 1 this time step: {}'.format(noise)

	for i in range(len(vehicleSet)):

		print 'Speed for Vehicle {} this time step [m/s]: {}'.format(vehicleSet[i], traci.vehicle.getSpeed(vehicleSet[i]))
		
		if traci.vehicle.getSpeed(vehicleSet[i]) > 5.56: # 5.56m/s = approx. 20km/h
			vehicleSetSubset.append(vehicleSet[i])
		else:
			indexIdentifierControl = participants.index(vehicleSet[i])
			newSpeed[indexIdentifierControl] = -1
			controlHistory[indexIdentifierControl] = 0
			if 'vehPrius' not in vehicleSet[i]:
				traci.vehicle.setSpeed(vehicleSet[i], -1)
	
	# compute optimisationSolution; minimise the sum of all cost functions w.r.t. speed s.t. all speeds are equal to each other
	if len(vehicleSetSubset) > 1:
		indexIdentifierControl = participants.index(vehicleSetSubset[0])
		constraints = [costFunctionVariables[indexIdentifierControl] <= 30] # set the maximum speed limit of 30km/h
		inUseVariables = []
		for i in range(len(vehicleSetSubset)):
			if i != 0:
				indexIdentifierControlA = participants.index(vehicleSetSubset[i-1])
				indexIdentifierControlB = participants.index(vehicleSetSubset[i])
				constraints.append(costFunctionVariables[indexIdentifierControlA] == costFunctionVariables[indexIdentifierControlB])	
		indexIdentifierControl = participants.index(vehicleSetSubset[0])
		inUseVariables.append(costFunctionVariables[indexIdentifierControl])
		if costFunctionTags[indexIdentifierControl] == 1:
			sumCostFunctions = costFunction_1(costFunctionVariables[indexIdentifierControl])
		elif costFunctionTags[indexIdentifierControl] == 2:
			sumCostFunctions = costFunction_2(costFunctionVariables[indexIdentifierControl])
		else:
			sumCostFunctions = costFunction_3(costFunctionVariables[indexIdentifierControl])
		for i in range(len(vehicleSetSubset)):
			if i != 0:
				indexIdentifierControl = participants.index(vehicleSetSubset[i])
				inUseVariables.append(costFunctionVariables[indexIdentifierControl])
				if costFunctionTags[indexIdentifierControl] == 1:
					sumCostFunctions = sumCostFunctions + costFunction_1(costFunctionVariables[indexIdentifierControl])
				elif costFunctionTags[indexIdentifierControl] == 2:
					sumCostFunctions = sumCostFunctions + costFunction_2(costFunctionVariables[indexIdentifierControl])
				else:
					sumCostFunctions = sumCostFunctions + costFunction_3(costFunctionVariables[indexIdentifierControl])
		objective = Minimize(sumCostFunctions)
		prob = Problem(objective, constraints) # form the optimisation problem
		prob.solve()
		print "Solution status:", prob.status
		print "Optimal value:", prob.value
		print "Optimal speed:", inUseVariables[0].value, inUseVariables[1].value
		optimisationSolution = (inUseVariables[0].value)/3.6 # convert km/h to m/s
		print optimisationSolution
	
	for i in range(len(vehicleSetSubset)):
		
		if len(vehicleSetSubset) > 1: # i.e. if there is more than one vehicle in the set of vehicles to be controlled...
	
			# first term calculation; "link to neighbours"
			if i == 0:
				firstTerm = optimisationSolution - traci.vehicle.getSpeed(vehicleSetSubset[i])
			else:
				firstTerm = 0
			# print 'First term for {}: {}'.format(vehicleSetSubset[i], firstTerm)
			
			# second term calculation; "link to everybody"
			sum = 0
			for j in range(len(vehicleSetSubset)):
				if j != i:
					sum = sum + (traci.vehicle.getSpeed(vehicleSetSubset[j]) - traci.vehicle.getSpeed(vehicleSetSubset[i])) * noise
			secondTerm = sum
			# print 'Second term for {}: {}'.format(vehicleSetSubset[i], secondTerm)
				
			# control output; the effect is seen next time step
			control = firstTerm + secondTerm # acceleration [m/s^2]
			indexIdentifierControl = participants.index(vehicleSetSubset[i])
			integral = numpy.trapz([controlHistory[indexIdentifierControl], control], dx=0.1) # integrate to get speed [m/s]
			newSpeed[indexIdentifierControl] = traci.vehicle.getSpeed(vehicleSetSubset[i]) + integral
		
		else:
			control = 0
			indexIdentifierControl = participants.index(vehicleSetSubset[i])
			newSpeed[indexIdentifierControl] = -1
		
		controlHistory[indexIdentifierControl] = control
	
	for i in range(len(vehicleSetSubset)):
		if len(vehicleSetSubset) > 1:
			indexIdentifierControl = participants.index(vehicleSetSubset[i])
			if 'vehPrius' not in vehicleSetSubset[i]:
				traci.vehicle.setSpeed(vehicleSetSubset[i], newSpeed[indexIdentifierControl])
		else:
			if 'vehPrius' not in vehicleSetSubset[i]:
				traci.vehicle.setSpeed(vehicleSetSubset[i], -1)

# cost functions
def costFunction_1(s):
	f = aR007*inv_pos(s) + bR007 + cR007*s + dR007*(s**2) # grams per kilometre
	return f
	
def costFunction_2(s):
	f = aR014*inv_pos(s) + bR014 + cR014*s + dR014*(s**2) # grams per kilometre
	return f
	
def costFunction_3(s):
	f = aR021*inv_pos(s) + bR021 + cR021*s + dR021*(s**2) # grams per kilometre
	return f
				
# main program
if __name__ == '__main__':

	# constants
	endSim = 1200000 # the simulation will be permitted to run for a total of endSim milliseconds
	timeout = 0.1 # a floating point number [s]
	FLAGHELLOSMARTPHONEDATA = False
	p = 1 # proportion of vehicles participating in the service; between 0 and 1, inclusive
	externalReference = 6.8 # 6.8m/s = 24.48km/h
	
	# cost function constants:  each function quantifies a vehicle's CO_2 emissions given the speed that it's travelling at
	aR007 = 2260.6 # vehicle type R007
	bR007 = 31.583 # vehicle type R007
	cR007 = 0.29263 # vehicle type R007
	dR007 = 0.0030199 # vehicle type R007
	aR014 = 2532.4 # vehicle type R014
	bR014 = 68.842 # vehicle type R014
	cR014 = -0.43167 # vehicle type R014
	dR014 = 0.0066776 # vehicle type R014
	aR021 = 3747.3 # vehicle type R021
	bR021 = 105.71 # vehicle type R021
	cR021 = -0.8527 # vehicle type R021
	dR021 = 0.012264 # vehicle type R021
	
	# cost function variable and tag initialisation
	costFunctionVariables = []
	costFunctionTags = []
	
	# initialisations
	step = 0 # time step
	ticket = 1 # used to provide unique IDs to real vehicles
	
	manager = Manager() # create a running manager server in a separate process
	flag_hello_smartphone = manager.list() # create a shared list instance on the manager server
	flag_hello_smartphone.append(FLAGHELLOSMARTPHONEDATA) # add an element to the list
	flag_goodbye_smartphone = manager.list() # create a shared list instance on the manager server
	smartphone_broadcast = manager.list() # create a shared list instance on the manager server
	central_authority_broadcast = manager.list() # create a shared list instance on the manager server
	serverThread = Process(target=server, args=(flag_hello_smartphone, flag_goodbye_smartphone, smartphone_broadcast, central_authority_broadcast)) # represents a task (i.e. the server program) running in a subprocess
	
	participants = [] # a list of vehicles participating in the service
	newSpeed = []
	controlHistory = []
	removedParticipants = []
	realVehicles = []
	
	# set up an Excel Workbook
	rowCounter = 1
	vehiclesHistoryExcel = []
	book = Workbook()
	sheet1 = book.add_sheet('Current Speed')
	style1 = easyxf('font: bold true')
	style2 = easyxf('font: bold true;' 'alignment: horizontal centre')
	
	# additional sheets
	sheet2 = book.add_sheet('Carbon Dioxide')
	sheet3 = book.add_sheet('Advised Speed')

	print
	
	print "Starting the main program."
	print "Connecting to SUMO via TraCI."
	
	# import TraCI (to use the library, the <SUMO_HOME>/tools directory must be on the python load path)
	if 'SUMO_HOME' in os.environ:
		tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
		sys.path.append(tools)
	else:   
		sys.exit("Please declare environment variable 'SUMO_HOME'.")
		
	# interface with SUMO from Python:  (i) begin by starting SUMO-GUI from within the python script;...
	PORT = 8813
	sumoBinary = "/Program Files (x86)/DLR/Sumo/bin/sumo-gui"
	sumoProcess = subprocess.Popen([sumoBinary, "-c", "ucdhil_nosegments.sumo.cfg", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)
		
	# ...then (ii) connect to the (waiting) simulation
	traci.init(PORT)
	
	print "Launching the server."
	serverThread.start()
	print "The server has been launched."
	
	print
	
	# begin the simulation
	traci.simulationStep(54000100) # perform the simulation until the time in the day indicated (in milliseconds) is reached; use for time steps of 0.1s
	
	while step < endSim:
	
		print 'Time step [ms]: {}'.format(step)
		# print 'Current simulation time [ms]: {}'.format(traci.simulation.getCurrentTime())
		vehicles = traci.vehicle.getIDList() # a list of vehicles currently running in the scenario
		# print 'No. of vehicles currently running in the scenario: {}'.format(len(vehicles)) # number of vehicles currently running in the scenario
		print 'Vehicles currently running in the scenario: {}'.format(vehicles)
		
		departed = traci.simulation.getDepartedIDList() # a list of vehicles which departed (were inserted into the road network) in this time step		
		# print 'Newly inserted vehicles: {}'.format(departed)
		for i in range(len(departed)):
			vehiclesHistoryExcel.append(departed[i]) # a history of vehicles is kept for the Excel Workbook
			if 'vehPrius' in departed[i]:
				participants.append(departed[i]) # i.e. real vehicles are assumed to be always participating in the service
				newSpeed.append(-1)
				controlHistory.append(0)
				costFunctionVariables.append(Variable()) # append a scalar optimization variable
				costFunctionTags.append(random.randint(1,3))
			else:
				coin = random.uniform(0,1) # determine what vehicles are participating in the service; flip a weighted coin; returns a random floating point number r such that 0 <= r < 1
				if coin < p:
					participants.append(departed[i])
					newSpeed.append(-1)
					controlHistory.append(0)
					costFunctionVariables.append(Variable()) # append a scalar optimization variable
					costFunctionTags.append(random.randint(1,3))
		
		# arrived = traci.simulation.getArrivedIDList() # a list of vehicles which arrived (have reached their destination and are removed from the road network) in this time step
		# print 'Arrived vehicles: {}'.format(arrived)
		
		# clean the participants list
		for i in range(len(participants)):
			if participants[i] not in vehicles:
				removedParticipants.append(participants[i])
		for i in range(len(removedParticipants)):
			indexIdentifier = participants.index(removedParticipants[i])
			newSpeed.pop(indexIdentifier)
			controlHistory.pop(indexIdentifier)
			costFunctionVariables.pop(indexIdentifier)
			costFunctionTags.pop(indexIdentifier)
			participants.remove(removedParticipants[i])
		# print 'Vehicles ejected from the participants list: {}'.format(removedParticipants) # includes arrived, real and 'vanished' vehicles
		removedParticipants = []
		
		# print 'Vehicles currently running in the scenario and participating in the service: {}'.format(participants)
		
		# write to Excel Workbook
		sheet1.write(rowCounter,0,step/1000.0) # convert milliseconds to seconds
		sheet2.write(rowCounter,0,step/1000.0) # convert milliseconds to seconds
		sheet3.write(rowCounter,0,step/1000.0) # convert milliseconds to seconds
		for i in range(len(vehiclesHistoryExcel)):
			if vehiclesHistoryExcel[i] in vehicles:
				sheet1.write(rowCounter,i+1,traci.vehicle.getSpeed(vehiclesHistoryExcel[i]))
				# sheet2.write(rowCounter,i+1,traci.vehicle.getCO2Emission(vehiclesHistoryExcel[i]))
				if vehiclesHistoryExcel[i] in participants:	
					if traci.vehicle.getSpeed(vehiclesHistoryExcel[i]) >= 1.39: # i.e. 5km/h
						indexIdentifier = participants.index(vehiclesHistoryExcel[i])
						if costFunctionTags[indexIdentifier] == 1:
							g = aR007/traci.vehicle.getSpeed(vehiclesHistoryExcel[i]) + bR007 + cR007*traci.vehicle.getSpeed(vehiclesHistoryExcel[i]) + dR007*(traci.vehicle.getSpeed(vehiclesHistoryExcel[i])**2) # grams per kilometre
							sheet2.write(rowCounter,i+1,g*traci.vehicle.getSpeed(vehiclesHistoryExcel[i])*0.0001) # grams = grams per kilometre * no. of kilometres, where no. of kilometres = speed (km/h) * hours
						elif costFunctionTags[indexIdentifier] == 2:
							g = aR014/traci.vehicle.getSpeed(vehiclesHistoryExcel[i]) + bR014 + cR014*traci.vehicle.getSpeed(vehiclesHistoryExcel[i]) + dR014*(traci.vehicle.getSpeed(vehiclesHistoryExcel[i])**2) # grams per kilometre
							sheet2.write(rowCounter,i+1,g*traci.vehicle.getSpeed(vehiclesHistoryExcel[i])*0.0001) # grams = grams per kilometre * no. of kilometres, where no. of kilometres = speed (km/h) * hours)
						else:
							g = aR021/traci.vehicle.getSpeed(vehiclesHistoryExcel[i]) + bR021 + cR021*traci.vehicle.getSpeed(vehiclesHistoryExcel[i]) + dR021*(traci.vehicle.getSpeed(vehiclesHistoryExcel[i])**2) # grams per kilometre
							sheet2.write(rowCounter,i+1,g*traci.vehicle.getSpeed(vehiclesHistoryExcel[i])*0.0001) # grams = grams per kilometre * no. of kilometres, where no. of kilometres = speed (km/h) * hours)				
				if vehiclesHistoryExcel[i] in participants:
					indexIdentifier = participants.index(vehiclesHistoryExcel[i])
					if newSpeed[indexIdentifier] >= 0:
						sheet3.write(rowCounter,i+1,newSpeed[indexIdentifier])
		
		# chose which control algorithm to apply
		# controlAlgorithmLeaderless(participants)
		# controlAlgorithmExternalReference(participants)
		controlAlgorithmCostFunctions(participants)
		
		print
		
		# check that all participating vehicles have a newSpeed registered each time step:  YEP! (DONE)
		
		# prepare the information to send to the real vehicles
		for i in range(len(participants)):
			if 'vehPrius' in participants[i]:
				indexIdentifier = realVehicles.index(participants[i])
				if newSpeed[i] == -1:
					central_authority_broadcast[indexIdentifier] = 'No Advice'
				else:
					central_authority_broadcast[indexIdentifier] = str(newSpeed[i] * 3.6) # convert m/s to km/h
		print 'Advised speeds sent to the real vehicles:', central_authority_broadcast
		
		# communicate with the real vehicles
		serverThread.join(timeout) # implicitly controls the speed of the simulation; blocks the main program either until the server program terminates (if no timeout is defined) or until the timeout occurs
		
		# process the information received from the real vehicles
		if flag_hello_smartphone[0] == True:
			addRealVehicle(ticket)
			realVehicles.append('vehPrius{}'.format(ticket))
			flag_hello_smartphone[0] = False
			ticket += 1
		for i in range(len(smartphone_broadcast)):
			if 'vehPrius{}'.format(i+1) in vehicles:
				traci.vehicle.setSpeed('vehPrius{}'.format(i+1), smartphone_broadcast[i])
		for i in range(len(flag_goodbye_smartphone)):		
			if flag_goodbye_smartphone[i] == True:
				removeRealVehicle(i)
				flag_goodbye_smartphone[i] = False
		
		print
		
		# goto the next time step
		rowCounter += 1
		step += 100 # in milliseconds
		traci.simulationStep(54000100+step) # perform the simulation until the time in the day indicated (in milliseconds) is reached; use for time steps of 0.1s
	
	print "Shutting the server down."
	serverThread.terminate()
	print "Writing to the Excel Workbook."
	
	sheet1.write(0,0,'Time Step [s]',style1)
	sheet1.col(0).width = 3200
	sheet2.write(0,0,'Time Step [s]',style1)
	sheet2.col(0).width = 3200
	sheet3.write(0,0,'Time Step [s]',style1)
	sheet3.col(0).width = 3200
	for i in range(len(vehiclesHistoryExcel)):
		sheet1.write(0,i+1,vehiclesHistoryExcel[i] + ' ' + '[m/s]',style2)
		sheet1.col(i+1).width = 3200
		# sheet2.write(0,i+1,vehiclesHistoryExcel[i] + ' ' + '[mg]',style2) # select this option if recording CO2 via traci
		sheet2.write(0,i+1,vehiclesHistoryExcel[i] + ' ' + '[g]',style2) # select this option if recording CO2 via formulae
		sheet2.col(i+1).width = 3200
		sheet3.write(0,i+1,vehiclesHistoryExcel[i] + ' ' + '[m/s]',style2)
		sheet3.col(i+1).width = 3200

	print "Saving the Excel Workbook."
	book.save('ucdhil_nosegments.xls')
	print "Closing the main program.  Goodbye."
	traci.close() # close the connection to SUMO