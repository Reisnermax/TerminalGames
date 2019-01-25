#!/usr/bin/env
import socket
import threading
import sys
import time
import copy
import random

test_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
test_ip.connect(("8.8.8.8", 80))
UDP_IP = test_ip.getsockname()[0]
test_ip.close()

UDP_PORT = 5005

message_queue = []
player_list = []



class player:
    def __init__(self, ip, name):
        self.addr = ip
        self.name = name
        self.is_elon = False



def UDP_receiver():
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        message_queue.append(data)

        flag = 0
        for test_player in player_list:
            if test_player.addr == addr[0]:
                flag = 1
        if flag == 0:
            player_list.append(copy.copy(player(addr[0], message_queue[0])))
            print("")
            print("New player with IP " + player_list[len(player_list)-1].addr + " and name " + player_list[len(player_list)-1].name)

def send_message_all(msg):
    for player in player_list:
        sock.sendto(msg, (player.addr, UDP_PORT))

def allocate_elon():
    for player in player_list:
        player.is_elon = False
    player_list[random.randint(0, len(player_list)-1)].is_elon = True

def send_out_question(question):
    for player in player_list:
        if player.is_elon == False:
            sock.sendto(question, (player.addr, UDP_PORT))
        else:
            sock.sendto("You're Elon", (player.addr, UDP_PORT))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

receiving_thread = threading.Thread(name='UDP_receiver', target=UDP_receiver)
receiving_thread.daemon = True
receiving_thread.start()

raw_input("Input to Start")
send_message_all("Waiting for question...")
allocate_elon()
send_out_question(raw_input("What is the question? "))

sys.exit()
