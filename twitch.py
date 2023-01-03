import socket
import logging
from chat_filtering import message_filter
from model import is_question

INPUT = input("streamer name: ")
print(INPUT)
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'learndatasci'
token = 'oauth:rbt4x5otuo0hri7uhwspx4e3d0qm2x'
channel = '#' + INPUT

print(channel)

sock = socket.socket()

sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))


while True:

    resp = sock.recv(2048).decode('utf-8')
    
    analyze = message_filter(resp)

    print(message_filter(resp), " ", is_question(analyze))

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    

sock.close()


