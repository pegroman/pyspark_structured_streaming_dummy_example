import socket
import time
import random

s = socket.socket()

port = 9999

s.bind(('127.0.0.1', port))

s.listen(5)
i = 0
while True:
    c, addr = s.accept()
    while True:    
        c.send((str(random.randint(0, 40)) + "\r").encode())
        time.sleep(1)
        print("pasa")
    c.close()
    