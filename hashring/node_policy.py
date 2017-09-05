# coding=utf-8
from sortedcontainers import SortedDict
from .hash_func import defaultHashClass
from .compat import range_


class BaseNodePolicy(object):
    def __init__(self, hash_class=defaultHashClass):
        """ The initial function for this class.

        :param hash_class: The class to calculate hash key for hash ring.
        """
        self._hash_class = hash_class

    def add_node(self, node=None, vnode_count=None):
        """ Add node to hash ring.

        :param node: The node address, format as '<ip>:<port>'
        :param vnode_count: The virtual node count.
        :return: None
        """
        raise NotImplementedError

    def remove_node(self, node=None):
        """ Remove node from hash ring

        :param node: The node address, format as '<ip>:<port>'
        :return: None
        """
        raise NotImplementedError

    def get_proper_node(self, key):
        """ Get a proper node to store object.

        :param key: The object key
        :return: The node: string
        """
        raise NotImplementedError

    def _find_proper_pos(self, key):
        """ Find a proper position to store object.

        :param key: The object key
        :return: The position: int
        """
        raise NotImplementedError

    def _gen_key(self, *args):
        args = [str(arg) for arg in args]
        return self._hash_class.get_hashval('#'.join(args))


class BisectNodePolicy(BaseNodePolicy):
    def __init__(self, hash_class=defaultHashClass):
        self.ring = SortedDict()
        super(BisectNodePolicy, self).__init__(hash_class=hash_class)

    def add_node(self, node=None, vnode_count=None):
        for i in range_(int(vnode_count)):
            self.ring[self._gen_key(node, i)] = node

    def remove_node(self, node=None):
        keys = list(self.ring.keys())
        for key in keys:
            if self.ring[key] == node:
                self.ring.pop(key)

    def get_proper_node(self, key):
        key, _ = self.ring.peekitem(self._find_proper_pos(key))
        return self.ring[key]

    def _find_proper_pos(self, key):
        key = self._gen_key(key)
        pos = self.ring.bisect(key)
        # if object_hash == node_hash, return node index
        if key in self.ring:
            return pos - 1
        # embodies the concept of the ring.
        if pos == len(self.ring):
            return 0
        return pos


defaultNodePolicy = BisectNodePolicy()

