#Original author Daimones. Modified from original from the Python Rogue-like.
#from constants import *

def gt(point, mapy):
    try:
        f = mapy[point][0]
        if f is True:
            return False
        else:
            return True
    except Exception, e:
        print e
        return True

class AStar: 
    def findPath(self, start, goal, mapy):
        
        self.goal = goal
        self.start = start
        pathFound = False 
        
        self.closedSet = {}        
        self.openSet = {start:Node(self.start)}
        
        hScore = self.findH(self.openSet[self.start].pos)
        self.openSet[start].fScore = hScore + self.openSet[self.start].gScore
           
        while pathFound != True:      
            currentNode = self.lowestF()
            if currentNode == None:
                break
            x, y = self.openSet[currentNode].pos
            remove = []
            
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            
            for newx, newy in neighbors:
                if (newx, newy) not in mapy.keys(): #If its not in hitmap, it's probablly outside the map range
                    remove.append((newx, newy))
                
                elif gt((newx-1, newy-1), mapy): #Can the AI go there?
                    remove.append((newx, newy))
                    
                elif self.closedSet.__contains__((newx, newy)): #Did we already know we could go there?
                    remove.append((newx, newy))
                    
            for node in remove:
                neighbors.remove(node)
    
            if len(neighbors) > 0:        
                for node in neighbors:
                    
                    h = self.findH(node)
                    g = self.openSet[currentNode].gScore + 1
                    f = g + h
                
                    exists = self.openSet.__contains__(node)
                    if exists:
                        if self.openSet[node].fScore > f:
                            self.openSet[node].fScore = f
                            self.openSet[node].gScore = g
                            self.openSet[node].parent = currentNode
                        else:
                            neighbors.remove(node)
                    else:
                        self.openSet[node] = Node(node, currentNode, f, g)
    
            self.closedSet[currentNode] = self.openSet[currentNode]
            self.openSet.pop(currentNode)
             
            if currentNode == self.goal:
                pathFound = True
        
        self.path = []
        if currentNode == None:
            for node in self.closedSet:
                self.path.append(node)
           
        else: 
            for i in range(self.closedSet.__len__()):
                
                if i == 0:
                    self.path.append(self.closedSet[self.goal].pos)
                elif self.closedSet[self.path[i - 1]].parent == None:
                    return
                else:
                    self.path.append(self.closedSet[self.path[i - 1]].parent)
              
    def findH(self, pos):
        posx, posy = pos
        goalx, goaly = self.goal
        
        x = abs(goalx - posx)
        y = abs(goaly - posy)
        
        return x + y
        
    def lowestF(self):
        minF = 255
        for node in self.openSet:
            fScore = self.openSet[node].fScore
            if fScore < minF:
                minF = fScore
                currentNode = node
        try:
            return currentNode
        except UnboundLocalError:
            return None

class Node:
    def __init__(self, pos, parent = None, fScore = 0, gScore = 0):
        self.pos = pos
        self.parent = parent
        self.fScore = fScore
        self.gScore = gScore