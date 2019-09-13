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
			if(message):
				# A registration request for receiving data
				if(message_string[:15]=="REGISTER TORECV" and message_string[-2:]=='\n\n'):

					uname = message_string[17:-3]

					#Username should be alpha numeric
					if(not uname.isalnum()):
						conn.send(bytes("ERROR 100 MALFORMED USERNAME\n\n",'utf-8'))
						return
					try:
						li = clients[uname]
						li += ["recv_socket",conn]
						clients[uname]=li
						conn.send(bytes("REGISTERED TORECV ["+uname+"]\n\n",'utf-8')) 
					
						# DO EXCEPTION HANDLING FOR KEY ERROR if different usernames come up for send and receive sockets
					except:
						conn.send(bytes("USERNAME MISMATCH",'utf-8'))
						return
					
					
				# A registration request for sending data
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
					continue

				#Register the public key of the user
				elif(message_string[:11]=="REGISTERKEY"):

					pos = message_string.index('-')
					uname = message_string[11:pos]

					li = clients[uname]
					public_key = message_string[pos+4:]
					li += [public_key]
					clients[uname] = li

					conn.send(bytes("NEW KEY REGISTERED",'utf-8'))

				elif (message_string[:8]=="FETCHKEY"):
					uname_rec = message_string[8:]
					public_key = clients[uname_rec][5]

					conn.send(bytes(public_key,'utf-8'))


					'''
					MAKE THE FORWARDING PART
					'''

				elif(message_string[:4]=="SEND"):
					pos = message_string.index('\n')
					#extract the username
					uname_rec = message_string[4:pos]
					#throw error if header does not have content length
					if ("Content-Length" not in message_string):
						conn.send(bytes("ERROR 103 Header incomplete\n\n", 'utf-8'))
						clients.pop(uname)
						return

					else:
						#extract various parts from the message
						pos2 = message_string[(pos+1):].index('\n')
						pos3 = message_string[(pos+pos2+2):].index('\n')
						sub_msg = message_string[pos+pos2+16:]
						sign_send = message[pos+5:pos+pos2]
						length = int(sub_msg[:sub_msg.index('\n')])
						# msg = message_string[pos+pos2+pos3+4:]
						msg = message_string[pos+pos2+pos3+4:pos+pos2+pos3+4+length]

						#retrieve the recipient's key 
						for key in clients:
							if(clients[key][2]==addr):
								uname = key

						if(uname_rec not in list(clients.keys())):
							print("Error")
							conn.send(bytes("ERROR 102 Unable to send\n",'utf-8'))
							continue
						else:
							try:
								#extract the recipient's receiver socket
								conn_forward = clients[uname_rec][4]
								#forward data to recipient
								conn_forward.send(bytes(""+uname+"\n "+msg+"\n ", 'utf-8')+sign_send)

								#wait for ACK from recipient
								msent = conn_forward.recv(2048)
								msent_str = str(msent.decode('utf-8'))
								if(msent_str[:8]=="RECEIVED"):
									conn.send(bytes('SENT'+uname_rec,'utf-8'))
								else:
									conn.send(bytes("ERROR 102 Unable to send","utf-8"))
							except:
								print("Failure to Forward -- " , sys.exc_info()[0])
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
