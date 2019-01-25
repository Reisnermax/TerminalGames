import socket
import threading
import sys

UDP_IP = sys.argv[1]

test_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
test_ip.connect(("8.8.8.8", 80))
personal_ip = test_ip.getsockname()[0]
test_ip.close()

UDP_PORT = 5005
NAME = sys.argv[2]

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "Name:", NAME

def UDP_receiver():
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print(data)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((personal_ip, UDP_PORT))
sock.sendto(NAME, (UDP_IP, UDP_PORT))

receiving_thread = threading.Thread(name='UDP_receiver', target=UDP_receiver)
receiving_thread.daemon = True
receiving_thread.start()

while True:
    pass
