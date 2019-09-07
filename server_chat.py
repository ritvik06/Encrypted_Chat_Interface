import socket
import select
import sys
from _thread import *


def clientthread(conn,addr):
	'''
	Looks at the header of a client message and takes actions for acking and
	forwarding
	Inputs: conn - the socket connection of the client
			addr - IP of the client 
	'''

	#global dictionary of registered clients on the server
	global clients
	#print(clients)

	while True:
		try:
			message = conn.recv(2048)
			message_string = str(message.decode('utf-8'))
			# print(message_string)
			if(message):
				# print("Entered")
				# A registration request for receiving data
				if(message_string[:15]=="REGISTER TORECV" and message_string[-2:]=='\n\n'):

					uname = message_string[17:-3]
					print(uname)

					#Username should be alpha numeric
					if(not uname.isalnum()):
						conn.send(bytes("ERROR 100 MALFORMED USERNAME\n\n",'utf-8'))
						return
					try:
						li = clients[uname]
						li += ["recv_socket",conn]
						clients[uname]=li
						#print(clients)
						conn.send(bytes("REGISTERED TORECV ["+uname+"]\n\n",'utf-8')) 
					
						# DO EXCEPTION HANDLING FOR KEY ERROR if different usernames come up for send and receive sockets
					except:
						conn.send(bytes("USERNAME MISMATCH",'utf-8'))
						return
					
					
				# A registration request for receiving data
				elif(message_string[:15]=="REGISTER TOSEND" and message_string[-2:]=="\n\n"):
					
					uname = message_string[17:-3]
					
					#Username should be alphanumeric
					if(not uname.isalnum()):
						conn.send(bytes("ERROR 100 MALFORMED USERNAME\n\n",'utf-8'))
						return

					#Username should be unique
					if(uname in list(clients.keys())):
						conn.send(bytes("EXISTING USERNAME. TRY ANOTHER ONE. CLOSING SOCKET\n",'utf-8'))
						return
					
					li = ["send_socket",conn,addr]
					clients[uname] = li
					conn.send(bytes("REGISTERED TOSEND ["+uname+"]\n\n",'utf-8')) 
						
					'''
					MAKE THE FORWARDING PART
					'''

				elif(message_string[:4]=="SEND"):
					# print("Reached Here")
					pos = message_string.index('\n')
					# print("Pos" + str(pos))
					uname_rec = message_string[4:pos]
					# print("Receiver " + uname_rec)
					if (message_string[pos+1:pos+15]!="Content-Length"):
						conn.send(bytes("ERROR 103 Header incomplete\n\n"))
						clients.pop(uname)
						return

					else:
						# print("Reached Here")
						sub_msg = message_string[pos+15:]
						# print(sub_msg)
						pos2 = sub_msg.index('\n');
						# print("pos2 is " + str(pos2))
						length = int(sub_msg[:pos2])
						# print("Length is " + str(length))		
						msg = sub_msg[pos2+2:pos2+2+length]	
						# print(msg)

						for key in clients:
							if(clients[key][2]==addr):
								uname = key

						if(uname_rec not in list(clients.keys())):
							# print("Error")
							conn.send(bytes("ERROR 102 Unable to send\n"))
							return
						else:
							# print("No error")
							print("Forwarded message to " + uname_rec + " is <" + msg + ">")
							try:
								# conn.send(bytes("SENT ["+uname_rec+"]\n\n"))
								conn_forward = clients[uname_rec][4] 
								conn_forward.send(bytes("FORWARD " + uname + "\n"+
   													"Content-Length" + len(message) +
   													 "\n\n"+ message,'utf-8'))
							except:
								print("Failure to forward")
								# print(clients[uname_rec][4])
								continue

		except:
			continue


'''
Socket has a particular type AF_INET which 
identifies a socket by its IP and Port
SOCK_STREAM specifies that data is to be read
in continuous flow
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#No clue what the above line means

if(len(sys.argv)!=3):
	print("Correct usage: name_of_file IP Port")
	exit()

IP = str(sys.argv[1])
Port = int(sys.argv[2])

'''
Bind the server to the above specified IP and Port.
Will be used by client to connect to server
'''
server.bind((IP,Port))

#Listen for set number of active connections
active_conns = 50
server.listen(active_conns)

# global clients 
clients={}

'''
Continuously keep a socket for connecting to client. For every client, make a 
new thread to process the message according to registration request and general message
'''
while True:
	#print(clients)
	conn, addr = server.accept()
	start_new_thread(clientthread,(conn,addr))
		

conn.close()
server.close()
