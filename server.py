from multiprocessing import Process, Queue, Pipe

subwidgetfile = open('./subwidgetfile.txt', 'r')
subwidgets_lines = subwidgetfile.readlines()
lines = []
for line in subwidgets_lines:
	lines.append(line.split())

subwidgets_list = {'A':lines[0], 'B':lines[1], '1':lines[2], '2':lines[3]}
widgetfile = open('./widgetfile.txt', 'a')

def subwidgets(server_conn):
	# continue communications
	while(True):
		# get request from client block until recieved
		clientrequest = server_conn.recv()

		# if requests subwidgets send list
		if clientrequest == 'subwidgets':
			server_conn.send(subwidgets_list)
		# otherwise read input and write the widget info to file
		else:
			temp=''.join(e+' ' for e in clientrequest)
			widgetfile.write(temp)
			widgetfile.write('\n')
			widgetfile.flush()
			server_conn.send('written')
