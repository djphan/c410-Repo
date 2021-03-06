import socket
import sys
import thread

def makeSocket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ('Socket Created')
        return s

    except socket.error as msg:
        print ('Failed to make socket. Error code: ' + str(msg[0]) + ' , Error Message: ' + str(msg[1]))
        sys.exit();


def connectHost(s, host='www.google.com', port=80):
    try:
        remote_ip = socket.gethostbyname(host)
        print ('IP address of ' + host + ' is: ' + remote_ip)

    except socket.gaierror:
        print ('Host name could not be resolved')
        sys.exit()

    s.connect((remote_ip, port))
    print ('Socket connected to ' + host + ' on IP: ' + remote_ip)

def sendSocketMessage(s, message = 'GET / HTTP/1.1\r\n\r\n'):
    try:
        s.sendall(message.encode("UTF8"))
        print("SEND SUCCESS")

    except:
        print("SEND FAIL")
        sys.exit()

def recieveSocketMessage(s):
    reply = s.recv(4096)
    print(reply)
	return reply

if __name__ == "__main__":

    s = makeSocket()
    connectHost(s, '', 8889)
	while 1:
		data = recieveSocketMessage(s)
		

    # Adjust sending and recieving socket message.
    #sendSocketMessage(s, 'hi')
    #
