# Program: SUMOPaint
# Goal: Permits the user to connect to the Monash SUMOPaint simulation and subsequently paint the vehicle of interest any desired colour.
# Author: Wynita Griggs
# Editor: Meher Singh
# Date: 20 July, 2021
# Tested and works with SUMO 1.8.0.

import os, sys
import traci
import multiprocessing
from multiprocessing import Process, Value
import socket
import time

# server program:  creates the server, handles incoming calls and subsequent user requests
def server(data):
	# size of buffer and backlog
	buffer = 2048 # value should be a relatively small power of 2, e.g. 4096
	backlog = 1 # tells the operating system to keep a backlog of 1 connection; this means that you can have at most 1 client waiting while the server is handling the current client; the operating system will typically allow a maximum of 5 waiting connections; to cope with this, busy servers need to generate a new thread to handle each incoming connection so that it can quickly serve the queue of waiting clients

	# create a socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4 socket family; SOCK_STREAM = TCP socket type

	# bind the socket to an address and port
	host = '127.0.0.1' # localhost
	port = 8080 # reserve a port for the service (i.e. a large number less than 2^16); the call will fail if some other application is already using this port number on the same machine
	server_socket.bind((host, port)) # binds the socket to the hostname and port number

	# listen for incoming connections
	server_socket.listen(backlog)

	while True: # infinite loop 1
		client_socket, address = server_socket.accept() # passively accept TCP client connections; the call returns a pair of arguments: client is a new Socket object used to communicate with the client and address is the address of the client

		# record client connection time (as seen from the server)
		start_time = time.strftime('%d %b %Y at %H:%M:%S')
		init_time = str(start_time) # convert connection time to a string
		print('Made a connection with', address, 'on', init_time + '.')

# main program
if __name__ == '__main__':

	# constants
	endSim = 3600000 # the simulation will be permitted to run for a total of endSim milliseconds; 1800000 = 30 minutes, 3600000 = 1hr
	timeout = 1 #controls the speed of the simulation with 1 = 1 second, 2 = 0.5 seconds, 0.5 = 2 seconds, 0.1

	# initialisations
	step = 0 # time step
	d = Value('d', 0.0) # 'd' is a string containing a type code as used by the array module (where 'd' is a floating point number implemented in double in C) and 0.0 is an initial value for 'd'

	print()
	print('===========================')
	print('Beginning the main program.')
	print('===========================')
	print()
	print("Connecting to SUMO via TraCI.")
	print()

	# import TraCI (to use the library, the <SUMO_HOME>/tools directory must be on the python load path)
	if 'SUMO_HOME' in os.environ:
		tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
		sys.path.append(tools)
	else:
		sys.exit("Please declare environment variable 'SUMO_HOME'.")

	# compose the command line to start SUMO-GUI
	sumoBinary = "/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui"
	sumoCmd = [sumoBinary, "-S", "-c", "bus_route.sumocfg"]
	# start the simulation and connect to it with the python script
	traci.start(sumoCmd)

	thread = Process(target=server, args=(d,)) # represents a task (i.e. the server program) running in a subprocess
	print("Launching the server.")
	thread.start()
	print("The server has been launched.")

	flag1 = 1

	while step < endSim:
		thread.join(timeout) # implicitly controls the speed of the simulation; blocks the main program either until the server program terminates (if no timeout is defined) or until the timeout occurs

		#print('Time step [s]: {}'.format(step/1000))
		#print('Current value of d: {}'.format(d.value))
		#print(traci.simulation.getLoadedIDList())


		if step%10000 == 0 and step > 1000:
			#this shows a list of vehicle ids
			#print(traci.vehicle.getIDList())

			#need to convert to string to print, but actual value is a integer
			#print('Person in vehicle 1: ' + str(traci.vehicle.getPersonNumber('bus_flow.0')))

			# the following code provides the next bus stop the bus is going to
			# test1 is a string value and stores the next bus stop
			# getstops provides detials of the next stop for the bus like stop, lane etc.

			# test = traci.vehicle.getStops('bus_flow.0', 1)
			# if flag1 == 1:
			# 	test1 = test[0].stoppingPlaceID
			# 	flag1 = flag1 + 1
			# 	print(test1)
			#
			# if test[0].stoppingPlaceID == test1:
			# 	test1 = test[0].stoppingPlaceID
			# else:
			# 	test1 = test[0].stoppingPlaceID
			# 	print(test1)

			#not working yet (ETA TO STOP)
			test = traci.vehicle.getStops('bus_flow.0', 1)
			print(test[0])
			print('\n')
			print(test[0].intendedArrival)
			print('\n')

		# go to the next time step
		step += 1000 # in milliseconds
		traci.simulationStep()

	print("Shutting the server down.")
	thread.terminate()
	print("Closing the main program. Goodbye.")
	traci.close() # close the connection to SUMO
