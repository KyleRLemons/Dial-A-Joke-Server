import socket

PORT = 1234
HEADER_LEN = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", PORT))
string = " "



while string != "X   0   ":
    msg = s.recv(1024) #recieves first message
    print(msg.decode("utf-8")) #prints first message
    string = input("input: ")
    s.send(string.encode("utf-8"))









print("Connection terminated")
s.close()