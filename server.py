from multiprocessing import Process, Queue, Pipe

subwidgets_list = {'A':['Apple', 'Aardvark', 'Astronaut'], 'B':['Bear', 'Bobcat', 'Beaver']}
widgetfile = open('./widgetfile.txt', 'a')

def subwidgets(server_conn):
	while(True):
		clientrequest = server_conn.recv()

		if clientrequest == 'subwidgets':
			server_conn.send(subwidgets_list)
		else:
			temp=''.join(e+' ' for e in clientrequest)
			widgetfile.write(temp)
			widgetfile.write('\n')
			widgetfile.flush()
			server_conn.send('written')
