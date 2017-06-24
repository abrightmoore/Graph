# @abrightmoore
# 2017-06-18 Visualise a graph

import sys
from random import randint, random, Random

import pygame
from pygame.locals import *

from Graph import *

class GraphViewer:
	
	def __init__(self, label, size, graph):
		self.size = size
		(cx,cy) = size
		self.centre = (cx>>1,cy>>1)
		self.label = label
		self.COL_CANVAS = (0,0,0,0)
		self.FPS = 10
		self.iterationCount = 0
		self.graph = graph
		pygame.init()
		pygame.display.set_caption(self.label)
		self.surface = pygame.display.set_mode(size)
		fpsClock = pygame.time.Clock()
		fpsClock.tick(self.FPS)
		self.font = pygame.font.SysFont("monospace", 15)
		self.mousex = -1
		self.mousey = -1
		
		nodes = graph.getNodes()
		for node in nodes:
			node.pos = (randint(-(cx>>1),cx>>1),randint(-(cy>>1),cy>>1),0)
			node.selected = False
			node.selectedsource = False
			node.selectedtarget = False
			node.nodelabel = None
			node.markedfordelete = False
	
	def update(self):	
		self.surface.fill(self.COL_CANVAS)
		self.iterationCount += 1
		
		self.renderGraph()
		
		self.doInputs()
		pygame.display.update()
		
	def doInputs(self):

		px, py = (-1,-1)
		for event in pygame.event.get():
			#print event
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == MOUSEMOTION:
 				mousex, mousey = event.pos
				self.mousex = mousex
				self.mousey = mousey
				for node in self.graph.getNodes():
					if node.selected == True:
						node.pos = (mousex - self.centre[0]-(node.nodelabel.get_width()>>1), mousey - self.centre[1]-(node.nodelabel.get_height()>>1), 0)
						break; # Only select one
 			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1: # LEFT
					(px,py) = event.pos
					#Check to see which nodes were selected
					selected = []
					for node in self.graph.getNodes():
						nox, noy, noz = node.pos
						qx = px - nox-self.centre[0]
						qy = py - noy-self.centre[1]
						if node.nodelabel != None:
							if qx >= 0 and qx < node.nodelabel.get_width() and qy >= 0 and qy < node.nodelabel.get_height():
								print "Clicked node "+node.label
								node.selected = True
								break;
							else:
								node.selected = False
				if event.button == 3: # RIGHT
					(px,py) = event.pos
					#Check to see which nodes were selected
					selected = []
					for node in self.graph.getNodes():
						nox, noy, noz = node.pos
						qx = px - nox-self.centre[0]
						qy = py - noy-self.centre[1]
						if node.nodelabel != None:
							node.selectedtarget = False
							if qx >= 0 and qx < node.nodelabel.get_width() and qy >= 0 and qy < node.nodelabel.get_height():
								print "Clicked node "+node.label
								node.selectedsource = True
							else:
								node.selectedsource = False
 			elif event.type == MOUSEBUTTONUP:					
					
				if event.button == 3: # RIGHT
					(px,py) = event.pos
					#Check to see which nodes were selected
					selected = []
					for node in self.graph.getNodes():
						nox, noy, noz = node.pos
						qx = px - nox-self.centre[0]
						qy = py - noy-self.centre[1]
						if node.nodelabel != None:
							if qx >= 0 and qx < node.nodelabel.get_width() and qy >= 0 and qy < node.nodelabel.get_height():
								print "Unclicked node "+node.label
								node.selectedtarget = True
							else:
								node.selectedtarget = False
				source = None
				target = None
				for node in self.graph.getNodes(): # Clear any left clicks
					if node.selectedsource == True:
						source = node
					if node.selectedtarget == True:
						target = node

				if source != target and source != None and target != None:
					# If present, remove
#					print source,target
#					for i in xrange(0,len(source.vertices)):
#						print source.vertices[i]
#						i = i + 1
					
					removed = False
					for v in source.vertices:
						if target in v.nodes:
							v.nodes.remove(target)
							removed = True
					if removed == False: # Otherwise Add
						source.attach([target])
				elif source == target and source != None:
					if source.markedfordelete == False:
						source.markedfordelete = True
						source = None
						target = None
					elif source.markedfordelete == True:
						source.markedfordelete = False
						source = None
						target = None
						
				for node in self.graph.getNodes():
					node.selected = False
					node.selectedsource = False
					node.selectedtarget = False
					
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					cx,cy = self.centre
					node = Node(str(randint(100000000,999999999)))
					node.pos = (self.mousex-cx,self.mousey-cy,0)
					node.selected = False
					node.selectedsource = False
					node.selectedtarget = False
					node.markedfordelete = False
					node.nodelabel = None
					self.graph.addNode(node)
				elif event.key == K_DELETE:
					for node in self.graph.nodes:
						if node.markedfordelete == True:
							self.graph.removeNode(node)
#							self.graph.nodes.remove(node) # ToDo: Move this back into GRAPH class
#							for n1 in self.graph.nodes: # Check through the remaining vertex lists for instances of the node to be removed
#								for v in n1.vertices:
#									for n in v.nodes:
#										if n == node:
#											v.nodes.remove(node)
#											n1.vertices.remove(v)
								
				print self.graph.getString()
	def renderGraph(self):
		cx,cy = self.centre
		nodes = self.graph.getNodes()
		for node in nodes:
			(x,y,z) = node.pos
			if node.nodelabel == None:
				node.nodelabel = self.font.render(node.label , 1, (128,190,255)) # Save this for later
			for v in node.getVertices():
				for n in v.nodes:
					qx,qy,qz = n.pos
					pygame.draw.line(self.surface, (255,255,255,255), (x+cx+(node.nodelabel.get_width()>>1)+2,y+cy+(node.nodelabel.get_height()>>1)+2),(qx+cx+(n.nodelabel.get_width()>>1),qy+cy+(n.nodelabel.get_height()>>1)), 1)
		
		for node in nodes:
			(x,y,z) = node.pos
			
			pygame.draw.rect(self.surface,(20,20,20,255),(cx+x,cy+y,node.nodelabel.get_width(),node.nodelabel.get_height()))
			
			if node.selected == True:
				pygame.draw.rect(self.surface,(80,80,80,255),(cx+x,cy+y,node.nodelabel.get_width(),node.nodelabel.get_height()))
			if node.selectedsource == True:
				pygame.draw.rect(self.surface,(0,80,0,255),(cx+x,cy+y,node.nodelabel.get_width(),node.nodelabel.get_height()))
			if node.selectedtarget == True:
				pygame.draw.rect(self.surface,(80,0,0,255),(cx+x,cy+y,node.nodelabel.get_width(),node.nodelabel.get_height()))
			if node.markedfordelete == True:
				pygame.draw.rect(self.surface,(255,0,0,255),(cx+x,cy+y,node.nodelabel.get_width(),node.nodelabel.get_height()))
			self.surface.blit(node.nodelabel, (cx+x, cy+y))
				