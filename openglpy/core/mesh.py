from core.object3D import Object3D
from OpenGL.GL import *

class Mesh(Object3D):
    def __init__(self, geometry, material): 
        super().__init__()
        self.geometry= geometry
        self.material= material
        self.visible= True

        # setup assoc between atributes stored in geometry and
        # shader prog stored in material
        self.vaoRef= glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)
        for variableName, attributeObject in geometry.attributes.items():
            attributeObject.associateVariable( material.programRef, variableName)
        # unbind this VAO
        glBindVertexArray(0)

 
