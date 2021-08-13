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

		#input from app
		while True: # infinite loop 2
			input = client_socket.recv(buffer).decode('UTF-8') # receive client data into buffer

			if (input == 'red'):
				print("test from input")
				data.value = 2
			if (input == 'blue'):
				print("blue input")
				data.value = 2
			if (input == 'update'):
				print("Sending data")
				data.value = 10

def bus_eta(bus_id):
	# this function is a hard coded function to get the eta to the next stop for a bus regarding
	# this function is hard coded for the chadstone-monash university bus route defined in bus_route.rou.xml
	curr_lane = traci.vehicle.getLaneID(bus_id)
	#curr_lane = bus_data[0].lane			#get current lane for bus
	curr_edge = curr_lane[:-2]
	#print(str(curr_edge))
	#print(str(bus_id))
	until_s1 = ['-787851477']
	until_s2 = ['787448090#0','787448090#1','807426789','-638398362#2','-638398362#1','-638398362#0', '814105115#0','814105115#1','814105114','198133694#0','198133694#1','198133694#2','198133694#3','198133694#4','198134599#0','198134599#1','198134598#0','198134598#1','198134598#2','198134598#3','782399755','144987843#0','144987843#1','180708618','211260230','180708619','782395452#0','782395452#1','713493692#0','713493692#1','791668582','4419370#0','4419370#1','4419370#2','4419370#3','4419370#4','15475366#0','15475366#1','48718672','167571335','48718680#0','48718680#1','48718680#2','167571359#0','167571359#1','198692245#0','198692245#1','88463238#2','88463238#3','88463238#4','88463238#5','88463238#6','45022884#0','45022884#1','229376392#0']
	until_s3 = ['229376392#1','11588123#0','11588123#1','11588123#2','11588123#3','11588123#4','-229376392#1','-229376392#0','229376385#0','229376385#1','88463238#1','88463238#2','88463238#3','229376387#0','229376387#1','-66793003#1','-66793003#0','-45023071','-23714110#1','-23714110#0','45023005#2','45023005#3','4868063#0','4868063#1','4868063#2','178932596#0','178932596#1','178932594#0','178932594#1']
	until_s4 = ['178931858#0','178931858#1','-178933894#1','-178933894#0','178931861#0','178931861#1','-178933462#1','-178933462#0','178931860#0','178931860#1','-178933463#1','-178933463#0','178931857#0','178931857#1','178933466#0','178933466#1','165171774#0']
	until_s5 = ['165171774#1','165171774#2','165171774#3','165171774#4','165171774#5','165171774#6','165171774#7','165171774#8','165171774#9','165171774#10','165171774#11','165171774#12','165171774#13','48333890','679193453','679193452','679193449','679469626#0']
	until_s6 = ['679469626#1','679469626#2','679193451','679193452','679469629','4612649','791849036','202904759','763416697#0','763416697#1','763416697#2','198691699#0']
	until_s7 = ['198691699#1','198691699#2','198691699#3','792597607#0','792597607#1','794258388','792597606','573676801','794258389#0','794258389#1','794258389#2','198691696']
	until_s8 = ['794269737','792153597','767369896#0','767369896#1','767369896#2','237508424','139327105#0','139327105#1','167571364','44348023#0','44348023#1','139327110','10539028#0','10539028#1','493547206#0','493547206#1','807418425#0','807418425#1']
	stop1 = "-787851477"
	stop2 = "229376392#0"
	stop3 = "178932594#1"
	stop4 = "165171774#0"
	stop5 = "679469626#0"
	stop6 = "198691699#0"
	stop7 = "198691696"
	stop8 = "807418425#1"

	counter = 0  	#counter for time, index of the array that the bus is on
	step = 0 		#step for which section of the route the bus is on (between which stops) 2 = to s2, 3 = to s3, 4 = to s4, 5 = to s5, 6 = to s6, 7 = to s7, 8 = to s8
	#s2 = 55, s3 = 29, s4 = 17, s5 = 18, s6 = 12, s7 = 12, s8 = 18


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

	##	LOCATION OF ALL VARIABLES CREATED
	##
	flag_stops = 1  			#flag to check if code has run before in the get next stop section
	occupied = 1				#current people on the bus
	capacity = 1				#bus Capacity
	#next_stop = "x" 			#next stop for the bus (CREATED IN THE LOOP BELOW)
	bus_id = 'bus_flow.0'		#temporary variable to store bus id for data collection (need to change to allow dynamic readings)


	while step < endSim:
		thread.join(timeout) # implicitly controls the speed of the simulation; blocks the main program either until the server program terminates (if no timeout is defined) or until the timeout occurs

		#print('Time step [s]: {}'.format(step/1000))
		#print('Current value of d: {}'.format(d.value))
		#print(traci.simulation.getLoadedIDList())
		if step > 3000:
			bus_eta(bus_id)
		#if step%10000 == 0 and step > 1000:
			#this shows a list of vehicle ids
			#bus_id_all = print(traci.vehicle.getIDList())

			# bus occupancy
			#occupied = traci.vehicle.getPersonNumber(bus_id)
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
			if(d.value == 2):
				print("INPUT FROM APP")
				d.value = 0

		# go to the next time step
		step += 1000 # in milliseconds
		traci.simulationStep()

	print("Shutting the server down.")
	thread.terminate()
	print("Closing the main program. Goodbye.")
	traci.close() # close the connection to SUMO
