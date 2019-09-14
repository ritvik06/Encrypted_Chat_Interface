# Encrypted_Chat_Interface

Implemented a chat application that allows users to do an encrypted chat with one another ,which cannot be decrypted by the chat server.

## Details
This is a course assignment for the graduate-level Computer Networks course taught by [**Prof. Aditeshwar Seth**]  
The assignment documentation can be found [here](http://www.cse.iitd.ac.in/~mausam/courses/col333/autumn2019/A2/A2.pdf)

## Dependencies
+ Python3.5

`pip3 install -r requirements.txt`

## Main Files
+ `client_chat.py` - This is an implementation of the client that sends data to other clients from stdin via the central server and recieves data from other clients as well. 
+ `server.py` - This is an implementation of a random bot.
+ `client.py` - This will encapsulate your process and help it connect to the game server.
  > `ip` (mandatory) - The IP address.  
  > `port` (mandatory) - The Server Port.  
  > `username` (mandatory) - The username of the client  
+ `server_chat.py` - This connects the clients and manages the transfer of information. 
  > `ip` (mandatory) - The IP address.
  > `port` (mandatory) - The Server Port.  

## Run Instructions
Here are the sample instructions used to connect and send messages between two clients connected to the server.Use TMUX to run these three scripts on the terminal together while opening 3 windows
### Setup Server
`python3 server_chat.py "0.0.0.0" 9000`
### Setup Client 1
`python client_chat.py "0.0.0.0" 9000 ritvik` 
### Setup Client 2
`python client_chat.py "0.0.0.0" 9000 jay`

## Sending Messages
To direct messages to a user type `@username_recipient: message`
While Receiving messages, client receives `#username_sender: message`

