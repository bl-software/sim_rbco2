import numpy
from core.matrix import Matrix

class Object3D(object):
    def __init__(self):
        self.transform= Matrix.makeIdentity()
        self.parent= None
        self.children= []

    def add(self,child):
        self.children.append(child)
        child.parent= self
    def remove(self,child):
        self.children.remove(child)
        child.parent= None

    # calc transformation of this O3D relative to root O3D of the scene graph
    def getWorldMatrix(self):
        if self.parent == None:
            return self.transform
        else:
            return self.parent.getWorldMatrix() @ self.transform

    # return single list containing all descendants
    def getDescendantList(self):
        # master list of all descenddant nodes
        descendants= []
        # nodes to be added to desc list and whose children will be added to this list
        nodesToProcess= [self]
        # continue processing nodes while any are left
        while len(nodesToProcess) > 0:
            # remove first 
            node= nodesToProcess.pop(0)
            # add this node to descendant list
            descendants.append(node)
            # children of this node must also be processed
            nodesToProcess= node.children + nodesToProcess
        return descendants

    # apply geometric transformations
    def applyMatrix(self, matrix, localCoord=True):
        if localCoord:
            self.transform= self.transform @ matrix
        else:
            self.transform= matrix @ self.transform

    def translate(self, x, y, z, localCoord=True):
        m= Matrix.makeTranslation(x,y,z)
        self.applyMatrix(m, localCoord)
    def rotateX(self, angle, localCoord=True):
        m= Matrix.makeRotationX(angle)
        self.applyMatrix(m, localCoord)
    def rotateY(self, angle, localCoord=True):
        m= Matrix.makeRotationY(angle)
        self.applyMatrix(m, localCoord)
    def rotateZ(self, angle, localCoord=True):
        m= Matrix.makeRotationZ(angle)
        self.applyMatrix(m, localCoord)
    def scale(self, s, localCoord=True):
        m= Matrix.makeScale(s)
        self.applyMatrix(m, localCoord)

    # get/set position of components of transform
    def getPosition(self):
        return [ self.transform.item( (0,3) ),
                 self.transform.item( (1,3) ),
                 self.transform.item( (2,3) ) ]
    def getWorldPosition(self): # rel to parent
        worldTransform= self.getWorldMatrix()
        return [ worldTransform.item( (0,3) ),
                 worldTransform.item( (1,3) ),
                 worldTransform.item( (2,3) ) ]
    def setPosition(self, position):
        # numpy 2.0 removed itemsety
        #self.transform.itemset( (0,3), position[0] )
        self.transform[0,3]= position[0]
        #self.transform.itemset( (1,3), position[1] )
        self.transform[1,3]= position[1]
        #self.transform.itemset( (2,3), position[2] )
        self.transform[2,3]= position[2]

    def lookAt(self, targetPosition):
        self.transform= Matrix.makeLookAt( self.getWorldPosition(), targetPosition )

    # returns 3x3 submatrix w/ rotation data
    def getRotationMatrix(self):
        return numpy.array([self.transform[0][0:3],
                            self.transform[1][0:3],
                            self.transform[2][0:3] ])

    def getDirection(self):
        forward= numpy.array([0,0,-1])
        return list( self.getRotationMatrix() @ forward )

    def setDirection(self, direction):
        position= self.getPosition()
        targetPosition= [ position[0] + direction[0],
                          position[1] + direction[1],
                          position[2] + direction[2] ]
        self.lookAt( targetPosition )

