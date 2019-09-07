
# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
  
'''
Socket has a particular type AF_INET which 
identifies a socket by its IP and Port
SOCK_STREAM specifies that data is to be read
in continuous flow
'''
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
ack_send = server_send.recv(2048)
ack_send = ack_send.decode('utf-8')
print(ack_send)
if(ack_send != "REGISTERED TOSEND ["+uname+"]\n\n"):
    print(ack_send)
    print("closed")
    server_send.close()
    exit()

server_rec.send(bytes(register_msg_rec,'utf-8'))
ack_rec = server_rec.recv(2048)
# print(ack_rec)
ack_rec = ack_rec.decode('utf-8')
print(ack_rec)
if(ack_rec !="REGISTERED TORECV ["+uname+"]\n\n"):
    print(ack_rec)
    print("Here2")
    server_rec.close()
    exit()
  
while True: 
	# print("Here")

	# read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
	try:
		message1 = sys.stdin.readline() 
		server_send.send(bytes("SEND" + "jay123\n"+
   			"Content-Length5\n\n"+message1,'utf-8')) 
		sys.stdout.write("<You> " + message1) 
	except:
		continue

	try:
		server_rec.recv(2048)
		message2 = message2.decode('utf-8')
		print("Message 1 " + message2)
	except:
		print("Nothing")
		continue
 

	# sys.stdout.write(message) 
	# ack_rec = server_send.recv(2048)
	# ack_rec = ack_rec.decode('utf-8')

	# if(ack_rec[:4]!=SENT):
	# 	print(ack_rec)
	# 	server_send.close()
	# 	exit()

	sys.stdout.flush() 
server.close() 
