# coding=utf-8
import hashlib
from .compat import range_


class Hash(object):
    @classmethod
    def get_hashval(cls, key):
        raise NotImplementedError

    def __str__(self):
        if self.__class__ in Hash.__subclasses__():
            return 'Hash method with %s' % \
                   self.__class__.__name__.rstrip('Hash')
        else:
            return 'Abstract hash method'


class MD5Hash(Hash):
    @classmethod
    def get_hashval(cls, key):
        m = hashlib.md5()
        m.update(key)
        init = [ord(v) for v in m.digest()]
        # 每四个字节构成一个32位整数
        # 将四个32位整数相加得到最终的hash值
        hash_ = 0
        for i in range_(4):
            hash_ += (
                # i << 2 等价于 i * 4
                ((init[(i << 2) + 3] & 0xff) << 24) |
                ((init[(i << 2) + 2] & 0xff) << 16) |
                ((init[(i << 2) + 1] & 0xff) << 8) |
                (init[i << 2] & 0xff)
            )

        return hash_


defaultHashClass = MD5Hash
