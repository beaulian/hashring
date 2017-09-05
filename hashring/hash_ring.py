# coding=utf-8
import math
from .node_policy import defaultNodePolicy

DEFAULT_FACTOR = 50
DEFAULT_WEIGHT = 1


class HashRing(object):
    def __init__(self, nodes=None, weights=None, node_policy=defaultNodePolicy):
        self._node_policy = node_policy
        self.nodes = nodes or []
        self.weights = weights or {}
        self._total_weight = 0

        self._init_ring()

    def _init_ring(self):
        for node in self.nodes:
            self._total_weight += self.weights.get(node, DEFAULT_WEIGHT)
        average_weight = self._total_weight / len(self.nodes)

        for node in self.nodes:
            weight = self.weights.get(node, DEFAULT_WEIGHT)
            vnode_count = self._gen_vnode_count(weight, average_weight)
            self._node_policy.add_node(node, vnode_count)

    def get_proper_node(self, key):
        return self._node_policy.get_proper_node(key)

    def add_node(self, node, weight=DEFAULT_WEIGHT):
        average_weight = (self._total_weight + weight) / (len(self.nodes) + 1)
        vnode_count = self._gen_vnode_count(weight, average_weight)
        self._node_policy.add_node(node, vnode_count)

    def remove_node(self, node):
        self._node_policy.remove_node(node)

    @staticmethod
    def _gen_vnode_count(weight, average_weight):
        return math.floor(DEFAULT_FACTOR * (weight / average_weight))


