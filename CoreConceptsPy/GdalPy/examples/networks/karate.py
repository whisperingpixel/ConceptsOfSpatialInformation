#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Abstract: Operations on a social graph as examples for how to use the core concept 'network'
"""

__author__ = "Michel Zimmer"
__copyright__ = "Copyright 2014"
__credits__ = ["Michel Zimmer"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import sys
import itertools
import networkx as nx

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from networks import *

log = _init_log("karate")


print "Analysis of the network of friendships between the 34 members of a karate club at a US university, as described by Wayne Zachary in 1977."
N = NetworkX()
N._G = nx.read_gml('../data/networks/karate.gml')


print "\nPeople who don't maintain a friendship inside the karate club:"
a = []
for b in N.nodes():
    if N.degree(b) == 0:
        a.append(b)
assert len(a) == 0
print " non"


print "\nHow many friendships are there?\n %d" % len(N.edges())


print "\nAnd who maintains the highest number of friendships?"
l = []
m = -1
for n in iter(N.nodes()):
    o = len(N.breadthFirst(n, 1))
    if o > m:
        l = []
        m = o
    if o >= m:
        l.append(n)
for p in l:
    q = N.breadthFirst(p, 1)
    q.remove(p)
    print " %d: %s" % (p, q)


print "\nWe can look for a seperated group by checking if one member is connected to everybody else."
c = N.nodes()[0]
d = iter(N.nodes())
e = next(d)
for f in d:
    assert N.connected(f, c) == True
    e = f
print " All the members are connected."


print "\nSo as a friend of a friend of a friend and so on everyone is connected to everybody else. But what's the highest number of people needed to create a connection between two members?"
g = []
h = -1
for i in itertools.combinations(N.nodes(), 2):
    j = N.distance(i[0], i[1])
    if j > h:
        g = []
        h = j
    if j >= h:
        g.append(i)
assert h > -1
print "It's %d and it's between these connections:" % (h-1)
for k in g:
    print " %s" % N.shortestPath(k[0], k[1])

# QUICK DISPLAY
# import matplotlib.pyplot as plt
# pos=nx.spring_layout(N._G)
# nx.draw_networkx_nodes(N._G,pos)
# nx.draw_networkx_edges(N._G,pos)
# nx.draw_networkx_labels(N._G,pos,dict(N._G.nodes()[i:i+2] for i in range(0, len(N._G.nodes()), 2)))
# plt.axis('off')
# plt.show()
