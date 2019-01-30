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
responce_counter = [0]


class player:
    def __init__(self, ip, name):
        self.addr = ip
        self.name = name
        self.is_elon = False
        self.question = ""
        self.responce = ""



def UDP_receiver():
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        message_queue.append([data, addr])

        ip = addr[0]
        command = message_queue[0][0][:4]
        text = message_queue[0][0][5:]

        if command == "JOIN":
            flag = 0
            for test_player in player_list:
                if test_player.addr == addr[0]:
                    flag = 1
            if flag == 0:
                player_list.append(copy.copy(player(ip, text)))
                print("")
                print("New player with IP " + player_list[len(player_list)-1].addr + " and name " + player_list[len(player_list)-1].name)
        elif command == "RSPN":
                player_list[find_ip_index(ip)].responce = text
                print(text)
                responce_counter[0] = responce_counter[0] + 1

        del message_queue[0]

def find_ip_index(ip):
    for index in range(0, len(player_list)):
        if player_list[index].addr == ip:
            return index

def send_message_all(msg):
    for player in player_list:
        sock.sendto(msg, (player.addr, UDP_PORT))

def allocate_elon():
    for player in player_list:
        player.is_elon = False
    player_list[random.randint(0, len(player_list)-1)].is_elon = True

def send_out_question():
    for player in player_list:
        player.is_elon = False

    question_picker = random.randint(0, len(player_list)-1)

    wait = True
    while wait == True:
        elon_num = random.randint(0, len(player_list)-1)
        print("stuck here")
        if elon_num != question_picker:
            wait = False

    player_list[elon_num].is_elon = True
    question = player_list[question_picker].responce
    print("question is " + question)

    for player in player_list:
        if player.is_elon == False:
            sock.sendto("PRNT|" + question, (player.addr, UDP_PORT))
        else:
            sock.sendto("PRNT| You're Elon", (player.addr, UDP_PORT))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

receiving_thread = threading.Thread(name='UDP_receiver', target=UDP_receiver)
receiving_thread.daemon = True
receiving_thread.start()


raw_input("Waiting for <ENTER> to continue...")
send_message_all("ASKQ|Submit a Question")
print("""
Waiting for Responces...""")
while responce_counter[0] != len(player_list):
    pass
responce_counter[0] = 0
print("all responces found")
send_out_question()
while True:
    pass

"""
while True:
    send_message_all("ASKQ|Submit a Question")
    pick_question_elon()
    send_out_question()
    send_message_all("ASKQ|Hit <ENTER> when ready for the next round")
"""
sys.exit()
