import socket
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


HOST = "188.166.133.53"
PORT = 11027

def sock(remoteip, remoteport):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteip, remoteport))
    return s, s.makefile('rw')



def read_until(f, delim='\n'):
    data = ""
    while not data.endswith(delim):
        data += f.read(1)
    return data


s, f = sock(HOST, PORT)

var("x")  # x を変数として扱う
print(read_until(f))

while True:
    exp = read_until(f)
    print("<< : " + exp)
    # exp = "Level 1.: x - 17 = 13"
    exp = exp.split(".: ")[1].split(" = ")
    ans = solve(Eq(parse_expr(exp[0]), int(exp[1])))
    print(">> : " + str(ans))
    s.send(str(ans[0]).encode())
    print(read_until(f))
