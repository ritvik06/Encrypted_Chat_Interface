
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
# print(ack_send)
if(ack_send != "REGISTERED TOSEND ["+uname+"]\n\n"):
    print(ack_send)
    print("closed")
    server_send.close()
    exit()

server_rec.send(bytes(register_msg_rec,'utf-8'))
ack_rec = server_rec.recv(2048)
print(ack_rec)
ack_rec = ack_rec.decode('utf-8')
print(ack_rec)
if(ack_rec !="REGISTERED TORECV ["+uname+"]\n\n"):
    print(ack_rec)
    print("Here2")
    server_rec.close()
    exit()
  
while True: 
	# print("Here")
	message = sys.stdin.readline() 
	server_send.send(bytes("SEND" + "12201\n"+
    	"Content-length5\n\n"+message,'utf-8')) 
	sys.stdout.write("<You>") 
	sys.stdout.write(message) 
	sys.stdout.flush() 
server.close() 
