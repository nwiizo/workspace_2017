# -*- coding: utf-8 -*-

message = "NEET".encode("utf-8")
message_int = int.from_bytes(message, byteorder='big')

print("文章:{}".format(message))
print("平文:{}".format(message_int))

# メッセージは、modulusより小さい値でなければならない。 
modulus = 3243485389
publicExponent = 65537
privateExponent = 2834145457

# 暗号化
# pow(x,y,m) で x^y mod m が計算できる
ciphertext = pow(message_int, publicExponent, modulus)
print("暗号化:{}".format(ciphertext))
# 復号
# pow(x,y,m) で x^y mod m が計算できる
message2 = pow(ciphertext, privateExponent, modulus)
print("復号:{}".format(message2))
