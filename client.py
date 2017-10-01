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
valid = 0

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
	while(valid == 0):
		type = input('Select your Widget type A, B, 1, 2: ')
		#check if valid widget
		if (type in widgets) is False:
			print('Not a valid widget type, reselect:')
		else:
			valid = 1

	# reset check
	valid = 0

	# get the time widget created
	ts = time.time()
	formattime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	# prompt server for subwidgets
	client_conn.send('subwidgets')

  	# read subwidgets from server
	subwidgets_list = client_conn.recv()

	# request subwidget type
	while(valid == 0):
		print('Choose a subwidget for ', name)
		subtype = input(subwidgets_list[type])
		# check if valid subtype
		if(subtype in subwidgets_list[type]) is False:
			print('Not a valid subwidget type, reselect:')
		else:
			valid = 1

	# reset check
	valid = 0

	# pass information back to server
	client_conn.send([str(name), str(type), str(formattime), str(subtype)])

	# wait for writeback
	client_conn.recv()
