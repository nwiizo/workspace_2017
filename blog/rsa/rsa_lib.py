# -*- coding: utf-8 -*-

import Crypto.PublicKey.RSA
import Crypto.Util.randpool
import sys

pool = Crypto.Util.randpool.RandomPool()

# RSAオブジェクトをランダムな鍵で生成する
# 40bit(5文字)までを暗号化できるようにする
rsa = Crypto.PublicKey.RSA.generate(2048, pool.get_bytes)

# 公開鍵を取得する
pub_rsa = rsa.publickey()

# RSAオブジェクトをタプルから生成する
# rsa.nが公開鍵、rsa.dが秘密鍵と思う
priv_rsa = Crypto.PublicKey.RSA.construct((rsa.n, rsa.e, rsa.d))

message = "Hello @nwiizo"

message = message.encode('utf-8')


# 暗号化する
enc = pub_rsa.encrypt(message, "")

# 復号する
dec = priv_rsa.decrypt(enc)

print ("private: n=%d, e=%d, d=%d, p=%d, q=%d, u=%d" % \
      (rsa.n, rsa.e, rsa.d, rsa.p, rsa.q, rsa.u))
print ("public: n=%d, e=%d" % (pub_rsa.n, pub_rsa.e))
print ("encrypt:", enc)
print ("decrypt:", dec)

# 署名する
text = (message)
signature = priv_rsa.sign(message, "")
# 文字列が変わってないか調べる
print (pub_rsa.verify(text, signature))
