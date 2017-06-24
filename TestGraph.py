# @abrightmoore

from Graph import *
from GraphViewer import *


G = Graph("TestGraph")

N_A = Node("NodeA")
N_B = Node("NodeB")
N_C = Node("NodeC")

G.addNode(N_A)
G.addNode(N_B)
G.addNode(N_C)


#N_A.attach([N_B])
#N_B.attach([N_A])
#N_C.connect([N_A,N_B])

#V_A = N_A.getVertices()
#V_B = N_B.getVertices()
#V_C = N_C.getVertices()

print G.getString()

viewer = GraphViewer(G.getString(),(400,400), G)

while True:
	viewer.update()