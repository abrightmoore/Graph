# @abrightmoore
# 2017-06-18 Clean up implementation and unit testing. Visualiser
# 2017-06-01 Initial - flight SYD-->MEL

class Graph:

    def __init__(self,label):
        self.label = label
        self.nodes = []

    def addNode(self,node):
        self.nodes.append(node)

    def removeNode(self,node):
		for n in self.nodes:
			if n == node:
				self.nodes.remove(node) # ToDo: Move this back into GRAPH class
				for n1 in self.nodes: # Check through the remaining vertex lists for instances of the node to be removed
					for v in n1.vertices:
						for n in v.nodes:
							if n == node:
								v.nodes.remove(node)
								n1.vertices.remove(v)

		
    def getNodes(self):
        return self.nodes

    def getString(self):
        result = self.label
        for n in self.nodes:
            result = result+",\nN:"+n.getString()
        return result

class Node:

    def __init__(self,label):
        self.label = label
        self.vertices = []

    def makeVertexLabel(self,nodes): # Creates a label for a vertex
        result = self.label
        if len(nodes) > 0:
            iter = 0
            result = result+"--"
            while iter < len(nodes):
                result = result+">"+nodes[iter].label
                iter = iter+1
        return "["+result+"]"

    def attach(self,nodes): # Directional attachment
        #vlabel = self.makeVertexLabel(nodes)
        for node in nodes:
			if node.label != self.label:
			    vlabel = self.makeVertexLabel([node])
			    self.vertices.append(Vertex(vlabel,[self,node]))

    def connect(self,nodes): # Bidirectional attachment
        self.attach(nodes)
        for node in nodes:
            if node.label != self.label:
                node.attach([self])
         
    def getVertices(self):
        return self.vertices

    def getString(self):
        result = self.label
        for v in self.vertices:
            result = result+",V:"+v.label
        return result

class Vertex:

    def __init__(self, label, nodes): # Note: supports more than two nodes
        self.label = label
        self.nodes = []
        for node in nodes:
            self.nodes.append(node)

    def getString(self):
        return self.label
    
