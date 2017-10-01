# Erich McMillan 28 September 2017
# A program for VerticalAIT
# Will do the following
# Prompt user for the Widget type (A,B,1,2)
# Dynamically load the subwidgets from the server side which is using a simple HTTP server
# Submit choice to server and store it
# command line argument should be the server ip

import sys
import time
import datetime
from multiprocessing import Process, Queue, Pipe
from server import subwidgets

widgets = {'A', 'B', '1', '2'}

client_conn, server_conn = Pipe()
server = Process(target=subwidgets, args=(server_conn,))
server.start()

while(True):
	# request widget name
	name = input('What is the Widget name: ')
	# check for termination request
	if name == 'exit':
		print('Exiting program')
		exit()
	# request widget type
	type = input('Select your Widget type A, B, 1, 2: ')
	#check if valid widget
	if (type in widgets) is False:
		print('Not a valid widget type, start over')
		continue

	# get the time widget created
	ts = time.time()
	formattime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	# prompt server for subwidgets
	client_conn.send('subwidgets')

  	# read subwidgets from server
	subwidgets_list = client_conn.recv()
	print(subwidgets_list)

	# display subwidgets to user
	print('Choose a subwidget for ', name)
	subtype = input(subwidgets_list[type])

	# pass information back to server
	client_conn.send([str(name), str(type), str(formattime), str(subtype)])

	# wait for writeback
	client_conn.recv()
