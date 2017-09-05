# coding=utf-8
from hashring import HashRing


memcache_servers = [
    '192.168.100.50',
    '192.168.100.51',
    '192.168.100.52'
]
ring = HashRing(memcache_servers)
ring.add_node('192.168.100.53')
ring.remove_node('192.168.100.53')
server = ring.get_proper_node('my_key')

print server
