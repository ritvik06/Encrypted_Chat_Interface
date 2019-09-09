
# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
  
random_generator = Random.new().read
key = RSA.generate(1024, random_generator) #generate public and private keys

publickey = key.publickey().exportKey("PEM") # pub key export for exchange
privatekey = key.exportKey("PEM")
# print(publickey)
# print(privatekey)

'''
Socket has a particular type AF_INET which 
identifies a socket by its IP and Port
SOCK_STREAM specifies that data is to be read
in continuous flow
'''
hang=10
server_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_rec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Define correct usage
if len(sys.argv) != 4: 
    print("Correct usage: script, IP address, port number username")
    exit() 

IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
uname = str(sys.argv[3])

'''
Creating two sockets, one for sending, and the other for receiving
'''
server_send.connect((IP_address, Port)) 
server_rec.connect((IP_address,Port))

'''
Sends message to the server for registering the user. Expects an ACK and only then proceeds for 
data forwarding among users
'''
register_msg_send = "REGISTER TOSEND ["+uname+"]\n\n"
register_msg_rec = "REGISTER TORECV ["+uname+"]\n\n"

server_send.send(bytes(register_msg_send,'utf-8'))
# print("waiting")
ack_send = server_send.recv(2048)
ack_send = ack_send.decode('utf-8')
# print(ack_send)
if(ack_send != "REGISTERED TOSEND ["+uname+"]\n\n"):
    print(ack_send)
    print("closed")
    server_send.close()
    exit()

server_rec.send(bytes(register_msg_rec,'utf-8'))

ack_rec = server_rec.recv(2048)
# print(ack_rec)
ack_rec = ack_rec.decode('utf-8')
# print(ack_rec)
if(ack_rec !="REGISTERED TORECV ["+uname+"]\n\n"):
    print(ack_rec)
    print("Here2")
    server_rec.close()
    exit()

server_send.send(bytes("REGISTERKEY" + uname + "-KEY" + str(publickey),'utf-8'))

  
while True: 
	# print("Here")

	# read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
	inputs_list = [sys.stdin, server_rec, server_send]
	read_sockets, write_sockets, error_sockets = select.select(inputs_list,[],[])

	for inp_socket in read_sockets:
		# print(inp_socket)
		if inp_socket == server_rec:

			try:
				# print("caught a message")
				message20 = server_rec.recv(2048)
				# print("recieved")
				message2 = str(message20.decode('utf-8'))
				# print("message2",message2)
				uname = message2[:message2.index(':')]
				rest = message2[message2.index(':')+2 : ]
				#pos = message2.index('\n')
				#uname = message2[7:pos]
				#if (message2[pos+1:pos+15]!="Content-Length"):
				#	server_send.send("ERROR 103 Header Incomplete")
				#else:
				#print(uname)
				server_rec.send(bytes("RECEIVED "+ uname +"\n\n",'utf-8'))
				# print("sent RECEIVED")
				#sub_msg = message2[pos+15:]
				#pos2 = sub_msg.index('\n');
				#length = int(sub_msg[:pos2])		
				#output = sub_msg[pos2+2:pos2+2+length]		

				#sys.stdout.write("#" + uname + ": " + output)
				sys.stdout.write("#" + uname + ": " + rest)



			except:
				hang-=1
				if(hang==0):
					print("Socket crashed")
					exit()
				print("Nothing")
				continue

		elif inp_socket==sys.stdin:

			try:
				message1 = sys.stdin.readline() 
				assert(message1[0]=='@')
				pos = message1.index(':')
				uname_rec = message1[1:pos]
				message = message1[pos+1:]
				server_send.send(bytes("SEND" + uname_rec + "\n"+
						"Content-Length" + str(len(message)) + "\n\n"+ message,'utf-8')) 
				
				sys.stdout.write("<You>: "+message)
			except:
				print("input error")
				continue

		else:
			try:
				ack_rec = server_send.recv(2048)
				ack_rec1 = ack_rec.decode('utf-8')
				#print(ack_rec1)
				if(ack_rec1[:4]!="SENT"):
					print(ack_rec1)	
				elif(ack_rec1[:9]=="ERROR 102"):
					print(ack_rec1)

				# else:
				# 	sys.stdout.write("<You>: " + message) 
			except:
				print("1st continue error")
				continue

	# try:
	# 	message2 = server_rec.recv(2048)
	# 	message2 = message2.decode('utf-8')
	# 	uname = message2[message2.index('<')+1 : message2.index('<')]
	# 	#pos = message2.index('\n')
	# 	#uname = message2[7:pos]
	# 	#if (message2[pos+1:pos+15]!="Content-Length"):
	# 	#	server_send.send("ERROR 103 Header Incomplete")
	# 	#else:
	# 	server_send.send("RECEIVED "+ uname +"\n\n")

	# 	#sub_msg = message2[pos+15:]
	# 	#pos2 = sub_msg.index('\n');
	# 	#length = int(sub_msg[:pos2])		
	# 	#output = sub_msg[pos2+2:pos2+2+length]		

	# 	#sys.stdout.write("#" + uname + ": " + output)
	# 	sys.stdout.write("#" + uname + ": " + message2)
	# except:
	# 	print("Nothing")
	# 	continue
 

	#sys.stdout.write(message) 
	#ack_rec = server_rec.recv(2048)
	#ack_rec = ack_rec.decode('utf-8')

	#if(ack_rec[:4]!=SENT):
	#	print(ack_rec)
	#	server_send.close()
	#	exit()

	#sys.stdout.flush() 
server.close() 
