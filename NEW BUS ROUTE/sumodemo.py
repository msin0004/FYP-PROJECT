# Program: SUMOPaint
# Goal: Permits the user to connect to the Monash SUMOPaint simulation and subsequently paint the vehicle of interest any desired colour.
# Author: Wynita Griggs
# Editor: Meher Singh
# Date: 20 July, 2021
# Tested and works with SUMO 1.8.0.

import os, sys
import traci
import multiprocessing
from multiprocessing import Process, Value, Manager
from ctypes import c_wchar_p
import socket
import time
import threading
stop = 'stop0'
sending_data = "sample"


# server program:  creates the server, handles incoming calls and subsequent user requests
def server(data,temp,central_authority_broadcast):
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
	realVehicleIndex = 0
	#central_authority_broadcast[realVehicleIndex] = 'hello before loops'

	 # bus stop that the user is at

	def clientHandle(client_socket, address, realVehicleIndex):

		while True: # infinite loop 2
			incoming = client_socket.recv(buffer).decode('UTF-8') # receive client data into buffer
			print("newthread loop")
			print(incoming)
			print(data.value)
			if (incoming == 'quit'):
				print("Ending session with client.")
				client_socket.close() # close the connection with the client
				central_authority_broadcast[realVehicleIndex] = 'No Advice'
				break # breaks out of infinite loop 2
			if (incoming == 'update'):
				#print("sending Data")
				#central_authority_broadcast[realVehicleIndex] = "hello"
				#client_socket.send(central_authority_broadcast[realVehicleIndex] + '\n') # send the data to the client
				message = "test message \n"
				#central_authority_broadcast[0] = 'testing'
				print(central_authority_broadcast[0])
				client_socket.send(message.encode())
			if (incoming == 'get'):
				print("sending get data")
				message = "get data being sent \n"
				client_socket.send(message.encode())
				#print(central_authority_broadcast[realVehicleIndex] + '\n')
			if (incoming == 'send'):
				#global sending_data
				#print("sending data print in incoming\n")
				#print(temp.value)
				#print("sending data print after incoming\n")
				message = str(temp.value)
				#print("darta val")
				#print(data.value)
				#print("data val end")
				print("message being sent")
				print(message)
				#print("message being sent end")
				client_socket.send(message.encode())
				print("data sent")

			if (incoming == 'stop7'):
				stop = 'stop7'
				#data = "capacity"
				data.value = 1
				print("data")
				print(data.value)
#				while data == 'capacity':
	#				temp = 0


				#message = 'testing\n'
				#client_socket.send(mesasge.encode())

			if (incoming == 'stop1'):
				stop = 'stop1'
			if (incoming == 'stop2'):
				stop = 'stop2'
			if (incoming == 'stop3'):
				stop = 'stop3'
			if (incoming == 'stop4'):
				stop = 'stop4'
			if (incoming == 'stop5'):
				stop = 'stop5'
			if (incoming == 'stop6'):
				stop = 'stop6'
			if (incoming == 'stop8'):
				stop = 'stop8'
			if not incoming:
				stop = 'no incoming'
				print('no incoming')

	while True: # infinite loop 1
		client_socket, address = server_socket.accept() # passively accept TCP client connections; the call returns a pair of arguments: client is a new Socket object used to communicate with the client and address is the address of the client

		# record client connection time (as seen from the server)
		start_time = time.strftime('%d %b %Y at %H:%M:%S')
		init_time = str(start_time) # convert connection time to a string
		print('Made a connection with', address, 'on', init_time + '.')

		#threading.newthread(clientHandle, (client_socket, address, realVehicleIndex))
		print("starting thread")
		threading.Thread(target=clientHandle, args=(client_socket, address, realVehicleIndex)).start()



# main program
if __name__ == '__main__':

	# constants
	endSim = 3600000 # the simulation will be permitted to run for a total of endSim milliseconds; 1800000 = 30 minutes, 3600000 = 1hr
	timeout = 1 #controls the speed of the simulation with 1 = 1 second, 2 = 0.5 seconds, 0.5 = 2 seconds, 0.1

	# initialisations
	step = 0 # time step
	d = Value('d', 0.0) # 'd' is a string containing a type code as used by the array module (where 'd' is a floating point number implemented in double in C) and 0.0 is an initial value for 'd'
	#d = 'temp'

	manager = Manager()
	central_authority_broadcast = manager.list()
	temp = manager.Value(c_wchar_p, "")
	thread = Process(target=server, args=(d, temp, central_authority_broadcast)) # represents a task (i.e. the server program) running in a subprocess


	#manager = Manager()
	#central_authority_broadcast = manager.list()
	#thread = Process(target=server, args=(d,central_authority_broadcast)) # represents a task (i.e. the server program) running in a subprocess


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


	print("Launching the server.")
	thread.start()
	print("The server has been launched.")

	##	LOCATION OF ALL VARIABLES CREATED
	##
	flag_stops = 1  			#flag to check if code has run before in the get next stop section
	occupied = 1				#current people on the bus
	capacity = 1				#bus Capacity
	#next_stop = "x" 			#next stop for the bus (CREATED IN THE LOOP BELOW)
	bus_id = 'bus_flow.0'		#temporary variable to store bus id for data collection (need to change to allow dynamic readings)
	t = 0

	while step < endSim:
		thread.join(timeout) # implicitly controls the speed of the simulation; blocks the main program either until the server program terminates (if no timeout is defined) or until the timeout occurs

		#print('Time step [s]: {}'.format(step/1000))
		#print('Current value of d: {}'.format(d.value))
		#print(traci.simulation.getLoadedIDList())
		if step > 3000:
			#print(temp.value)
			#central_authority_broadcast.append = 'test'
			#print(central_authority_broadcast[0])

			#bus_eta(bus_id)
		#if step%10000 == 0 and step > 1000:
			#this shows a list of vehicle ids
			#bus_id_all = print(traci.vehicle.getIDList())

			# bus occupancy
			occupied = traci.vehicle.getPersonNumber(bus_id)
			#print('Person in vehicle 1: ' + str(occupied))

			# the following code provides the next bus stop the bus is going to
			# test1 is a string value and stores the next bus stop
			# getstops provides detials of the next stop for the bus like stop, lane etc.

			#bus_data = traci.vehicle.getStops(bus_id, 1)
			# getting the initial stop
			#if flag_stops == 1:
			# 	next_stop = bus_data[0].stoppingPlaceID
			# 	flag_stops = flag_stops + 1
			 	#print(next_stop)

			#if bus_data[0].stoppingPlaceID == next_stop:
			# 	next_stop = bus_data[0].stoppingPlaceID
			#else:
			 	#next_stop = bus_data[0].stoppingPlaceID
			 	#print(next_stop)

			#eta code (HARD CODED REQUIRED)
			# will need to have a seperate function to calculate eta
			# need to check bus at every edge
			#not working yet (ETA TO STOP)
			# test = traci.vehicle.getStops(bus_id, 1)
			# print(test[0])
			# print('\n')
			# print(test[0].intendedArrival)
			# print('\n')
			#
			# call eta function
			#bus_eta(bus_id)


			# bus capacity
			#capacity = traci.vehicle.getPersonCapacity(bus_id)
			#print('Capacity of vehicle 1: ' + str(capacity))

			#inputs from app
			#print(d)
			if(d.value == 2):
				print("INPUT FROM APP")
				#d = 0
			#if(d == 'capacity'):
			#	bus_id = 'bus_flow.0'
			#	print("bus_flow_0")
			#	d = traci.vehicle.getPersonCapacity(bus_id)
			#	print(d)
			#print(d.value)
			if(d.value == 1):
				#print("sending data printing")
				#print(sending_data)
				#print("sending data printed now message")
				message = "passengers = " + str(occupied) + '\n'
				sending_data = message
				if t == 0:
					temp.value = message
					t = t+1
				elif t == 1:
					message = "nononono\n"
					temp.value = message
					t = t+1
				elif t == 2:
					message = 23
					temp.value = str(message) + '\n'
					print("printing message as a number into string")
					print(temp.value)
					print("end print")
					t = 0
				#print()
				#temp.value = occupied
				#print(occupied)
				#print(temp.value)
				print("end of main")
				d.value = 9

		# go to the next time step
		step += 1000 # in milliseconds
		traci.simulationStep()

	print("Shutting the server down.")
	thread.terminate()
	print("Closing the main program. Goodbye.")
	traci.close() # close the connection to SUMO
