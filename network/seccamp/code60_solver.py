import socket
import re


HOST = "188.166.133.53"
PORT = 11059


def sock(remoteip, remoteport):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteip, remoteport))
    return s, s.makefile('rw')


def read_until(f, delim='\n'):
    data = ""
    while not data.endswith(delim):
        data += f.read(1)
    return data


def prime_table(n):
    lis = [True for _ in range(n+1)]
    i = 2
    while i * i <= n:
        if lis[i]:
            j = i + i
            while j <= n:
                lis[j] = False
                j += i
        i += 1

    table = [i for i in range(n + 1) if lis[i] and i >= 2]
    return table


prime_table = prime_table(100000)  # 100000でのテーブルを予め作成しておく


s, f = sock(HOST, PORT)
m = re.compile(r"Level (\d+).: Find the next prime number after (\d+):")

print(read_until(f))
while True:
    exp = read_until(f)
    print("<< : " + exp)
    exp = m.match(exp)
    y = int(exp.group(2))
    n = list(filter(lambda x: x > y, prime_table))[0]
    print(">> : " + str(n))
    s.send(str(n).encode())
    print(read_until(f))
