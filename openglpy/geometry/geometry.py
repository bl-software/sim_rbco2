import numpy
from core.attribute import Attribute

class Geometry(object):
    def __init__(self):
        # Store attrib objects indexed by name of associated var in shader
        # Shader var associations setup later and stored in vertex array object in Mesh
        self.attributes= {}
        # num of verts
        self.vertexCount= None

    def addAttribute(self, dataType, variableName, data):
        #print(f'addAttribute: {dataType} :: {variableName} :: {data}')
        self.attributes[variableName]= Attribute(dataType, data)

    def countVerticies(self):
        # num of verts may be calced from length of any Attribute objecst array of data
        attrib= list( self.attributes.values() )[0]
        self.vertexCount= len( attrib.data )

    # transform data in an attribute using a matrix
    def applyMatrix( self, matrix, variableName= 'vertexPosition'):
        oldPositionData= self.attributes[variableName].data
        newPositionData= []

        for oldPos in oldPositionData:
            # avoid changing list references
            newPos= oldPos.copy()
            # add homogeneous fourth coord
            newPos.append(1)
            # multiply by matrix
            newPos = matrix @ newPos
            # remove homogeneous coord
            newPos= list( newPos[0:3] )
            # add to new data list
            newPositionData.append(newPos)

        self.attributes[variableName].data = newPositionData

        # extract the rotation submatrix
        rotationMatrix= numpy.array( [ matrix[0][0:3],
                                       matrix[1][0:3],
                                       matrix[2][0:3] ] )
        oldVertexNormalData = self.attributes['vertexNormal'].data
        newVertexNormalData = []
        for oldNormal in oldVertexNormalData:
            newNormal= oldNormal.copy()
            newNormal= rotationMatrix @ newNormal
            newVertexNormalData.append( newNormal )
        self.attributes['vertexNormal'].data = newVertexNormalData

        oldFaceNormalData = self.attributes['faceNormal'].data
        newFaceNormalData = []
        for oldNormal in oldFaceNormalData:
            newNormal= oldNormal.copy()
            newNormal= rotationMatrix @ newNormal
            newFaceNormalData.append( newNormal )
        self.attributes['faceNormal'].data = newFaceNormalData



        # new data must be uploaded
        self.attributes[variableName].uploadData()


    def print_tris(self,geom_obj):
        #print('geom_obj:',geom_obj.data)
        for vn,vert in enumerate(geom_obj.data):#[0:-1:3]: # vert number
            if vn % 3 == 0:
                print('')
            print(f'P{vn: >3}:  {vert[0]: >6.3f}  {vert[1]: >6.3f}  {vert[2]: >6.3f}' )

    # mrege data from attributes of other geometry into this object
    # requires both geometries to have attributes with same names
    def merge(self, otherGeometry):
        for variableName, attributeObject in self.attributes.items():
            #self.print_tris(attributeObject)
            #self.print_tris(otherGeometry.attributes[variableName])
            attributeObject.data += otherGeometry.attributes[variableName].data
            #self.print_tris(attributeObject)

            # new data must be uploadwd
            # TODO page 161 had indent error in text- I think indent error - maybe not
            self.attributes[variableName].uploadData()

            # update number of verticies
        self.countVerticies()
