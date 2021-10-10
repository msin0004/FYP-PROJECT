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
#stop = 'stop0'
sending_data = "sample"


# server program:  creates the server, handles incoming calls and subsequent user requests
def server(data,temp,central_authority_broadcast, bus_send, eta_send, pass_send, bus_no, stop, list, bus_info, received, solution):
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
		testing = 1 #for testing purposes
		sent_flag = 0 #for when the user sends the final values
		while True: # infinite loop 2
			incoming = client_socket.recv(buffer).decode('UTF-8') # receive client data into buffer
			print("newthread loop")
			print(incoming)

			#if client finishes the solution
			if (received['sent_flag'] == 1 and sent_flag == 0):
				solution.value = incoming
				sent_flag = 1
				received['end'] = 1
			#if client ends session
			if (incoming == 'quit'):
				print("Ending session with client.")
				client_socket.close() # close the connection with the client
				#central_authority_broadcast[realVehicleIndex] = 'No Advice'
				break # breaks out of infinite loop 2
			if (incoming == 'update'):
				#print("sending Data")
				#central_authority_broadcast[realVehicleIndex] = "hello"
				#client_socket.send(central_authority_broadcast[realVehicleIndex] + '\n') # send the data to the client
				message = "test message \n"
				#central_authority_broadcast[0] = 'testing'
				#print(central_authority_broadcast[0])
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

				if(temp == 'bus_no'):
					message = str(bus_no) + '\n'
					client_socket.send(mesasge.encode())


			#sending bus information code
			if (incoming == 'bus_no'):
				temp.value = ''
				received['operation'] = ''
				print("inside bus_no")
				message = str(bus_no.value) + '\n'
				client_socket.send(message.encode())
				#testing = number of busses (max 3)
				#if testing == 1:
				if bus_no.value == 1:
					#send bus 1 eta
					message = str(bus_info['bus1_eta'])
					client_socket.send(message.encode())
					#send bus 1 passengers
					message = str(bus_info['bus1_pass'])
					client_socket.send(message.encode())
					#send bus 1 seats
					message = str(bus_info['bus1_seat'])
					client_socket.send(message.encode())
				#elif testing == 2:
				elif bus_no.value == 2:
					#send bus 1 eta
					message = str(bus_info['bus1_eta'])
					client_socket.send(message.encode())
					#send bus 1 passengers
					message = str(bus_info['bus1_pass'])
					client_socket.send(message.encode())
					#send bus 1 seats
					message = str(bus_info['bus1_seat'])
					client_socket.send(message.encode())
					#send bus 2 eta
					message = str(bus_info['bus2_eta'])
					client_socket.send(message.encode())
					#send bus 2 passengers
					message = str(bus_info['bus2_pass'])
					client_socket.send(message.encode())
					#send bus 2 seats
					message = str(bus_info['bus2_seat'])
					client_socket.send(message.encode())
				#elif testing == 3:
				elif bus_no.value == 3:
					#send bus 1 eta
					message = str(bus_info['bus1_eta'])
					client_socket.send(message.encode())
					#send bus 1 passengers
					message = str(bus_info['bus1_pass'])
					client_socket.send(message.encode())
					#send bus 1 seats
					message = str(bus_info['bus1_seat'])
					client_socket.send(message.encode())
					#send bus 2 eta
					message = str(bus_info['bus2_eta'])
					client_socket.send(message.encode())
					#send bus 2 passengers
					message = str(bus_info['bus2_pass'])
					client_socket.send(message.encode())
					#send bus 2 seats
					message = str(bus_info['bus2_seat'])
					client_socket.send(message.encode())
					#send bus 3 eta
					message = str(bus_info['bus3_eta'])
					client_socket.send(message.encode())
					#send bus 3 passengers
					message = str(bus_info['bus3_pass'])
					client_socket.send(message.encode())
					#send bus 3 seats
					message = str(bus_info['bus3_seat'])
					client_socket.send(message.encode())


			if (incoming == 'Stop 7'):
				#stop = 'stop7'
				print("inside stop 7")
				stop.value = 7
				temp.value = 'bus_no'
				received['stop'] = 7
				received['operation'] = 'bus_no'
				#data = "capacity"
				#data.value = 1
				#print("data")
				#print(data.value)
#				while data == 'capacity':
	#				temp = 0
				#message = 'testing\n'
				#client_socket.send(mesasge.encode())

			if (incoming == 'Stop 1'):
				#stop = 'stop1'
				print("inside stop 1")
				stop.value = 1
				temp.value = 'bus_no'
				received['stop'] = 1
				received['operation'] = 'bus_no'
			if (incoming == 'Stop 2'):
				#stop = 'stop2'
				print("inside stop 2")
				stop.value = 2
				temp.value = 'bus_no'
				received['stop'] = 2
				received['operation'] = 'bus_no'
			if (incoming == 'Stop 3'):
				#stop = 'stop3'
				print("inside stop 3")
				stop.value = 3
				temp.value = 'bus_no'
				received['stop'] = 3
				received['operation'] = 'bus_no'
			if (incoming == 'Stop 4'):
				#stop = 'stop4'
				print("inside stop 4")
				stop.value = 4
				temp.value = 'bus_no'
				received['stop'] = 4
				received['operation'] = 'bus_no'
			if (incoming == 'Stop 5'):
				#stop = 'stop5'
				print("inside stop 5")
				stop.value = 5
				temp.value = 'bus_no'
				received['stop'] = 5
				received['operation'] = 'bus_no'
			if (incoming == 'Stop 6'):
				#stop = 'stop6'
				print("inside stop 6")
				stop.value = 6
				temp.value = 'bus_no'
				received['stop'] = 6
				received['operation'] = 'bus_no'
			if (incoming == 'Stop 8'):
				#stop = 'stop8'
				print("inside stop 8")
				stop.value = 8
				temp.value = 'bus_no'
				received['stop'] = 8
				received['operation'] = 'bus_no'

			#FINAL SOLUTION FROM CLIENT
			if (incoming == 'Bus 1'):
				received['sent_flag'] = 1
				received['bus'] = incoming
			if (incoming == 'Bus 2'):
				received['sent_flag'] = 1
				received['bus'] = incoming
			if (incoming == 'Bus 3'):
				received['sent_flag'] = 1
				received['bus'] = incoming
			#if not incoming:
			#	stop = 'no incoming'
			#	print('no incoming')

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
	bus_send = manager.Value(c_wchar_p, "")
	eta_send = manager.Value(c_wchar_p, "")
	pass_send = manager.Value(c_wchar_p, "")
	bus_no = manager.Value('d',0)
	stop = manager.Value('d',0)
	list = manager.list()
	bus_info = manager.dict()  						#stores data obtained from sumo
	received = manager.dict()						#stores data received from client
	solution = manager.Value(c_wchar_p, "") 		#stores the final solution
	received['sent_flag'] = 0						#flag that signals client sending the decision
	received['end'] = 0

	thread = Process(target=server, args=(d, temp, central_authority_broadcast, bus_send, eta_send, pass_send, bus_no, stop, list, bus_info, received, solution)) # represents a task (i.e. the server program) running in a subprocess


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
			#bus_id_all = traci.vehicle.getIDList()
			#print(bus_id_all)
			#print(bus_id_all[0])
			#print(len(bus_id_all))
			#bus_data = traci.vehicle.getStops(bus_id_all[0], 1)
			#next_stop = bus_data[0].stoppingPlaceID
			#print(next_stop)
			#if next_stop == 'r1s2':
				#print("yes")



			##GET NUMBER OF BUSSES FOR THE GIVEN STOP
			#VARIABLES BEING used
			#temp.value, stop.value, bus_no.value
			bus_id_all = traci.vehicle.getIDList()
			stop_num = 0
			count_bus_no = 0
			#check what the device is asking for
			if temp.value == 'bus_no':
				#no_of_bus = len(traci.vehicle.getIDList())
				#loop that runs for each simulated bus
				for num in bus_id_all:
					#getting bus data (next stop data)
					bus_data = traci.vehicle.getStops(num, 1)
					next_stop = bus_data[0].stoppingPlaceID
					#converting next stop to number for comparison
					if next_stop == 'r1s1':
						stop_num = 1
					if next_stop == 'r1s2':
						stop_num = 2
					if next_stop == 'r1s3':
						stop_num = 3
					if next_stop == 'r1s4':
						stop_num = 4
					if next_stop == 'r1s5':
						stop_num = 5
					if next_stop == 'r1s6':
						stop_num = 6
					if next_stop == 'r1s7':
						stop_num = 7
					if next_stop == 'r1s8':
						stop_num = 8
					#comparing simulated bus stop to the device requested stop
					if stop_num <= stop.value and count_bus_no < 4:
						count_bus_no = count_bus_no + 1
						#put code to get data for each bus here
						#USE the following variables
						#bus limit = 64 passengers
						#bus seats = 38 seats

						if count_bus_no == 1:
							bus_info['bus1_eta'] = '10'
							bus_info['bus1_pass'] = str(traci.vehicle.getPersonNumber(bus_id_all)) + '/64'
							bus_info['bus1_seat'] = str(traci.vehicle.getPersonNumber(bus_id_all)) + '/38'
						if count_bus_no == 2:
							bus_info['bus2_eta'] = 10
							bus_info['bus2_pass'] = str(traci.vehicle.getPersonNumber(bus_id_all)) + '/64'
							bus_info['bus2_seat'] = str(traci.vehicle.getPersonNumber(bus_id_all)) + '/38'
						if count_bus_no == 3:
							bus_info['bus3_eta'] = 10
							bus_info['bus3_pass'] = str(traci.vehicle.getPersonNumber(bus_id_all)) + '/64'
							bus_info['bus3_seat'] = str(traci.vehicle.getPersonNumber(bus_id_all)) + '/38'


				#end of for loop
				#send the count to the server variable
				bus_no.value = count_bus_no
				print(bus_no.value)
				bus_info['no_of_bus'] = count_bus_no

			#end of if statement for bus number

			####
			####
			####		MAIN CODE
			####
			####

			if(received['end'] == 1):
				#create excel sheet for storage
				print("Received Solution from user\n")
				print(str(solution.value))
				print("Bus picked by user\n")
				print(str(received['bus']))











			# bus occupancy
			occupied = traci.vehicle.getPersonNumber(bus_id)
			print('Person in vehicle 1: ' + str(occupied))

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
			capacity = traci.vehicle.getPersonCapacity(bus_id)
			print('Capacity of vehicle 1: ' + str(capacity))

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
