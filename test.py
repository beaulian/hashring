# coding=utf-8
from hashring import HashRing


memcache_servers = [
    '192.168.100.50',
    '192.168.100.51',
    '192.168.100.52'
]
ring = HashRing(memcache_servers)
server = ring.get_proper_node('my_key')

print server