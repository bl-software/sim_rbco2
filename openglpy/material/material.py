from core.openGLUtils import OpenGLUtils
from core.uniform import Uniform
from OpenGL.GL import *

class Material(object):
    def __init__(self, vertexShaderCode, fragmentShaderCode):
        self.programRef= OpenGLUtils.initializeProgram(vertexShaderCode, fragmentShaderCode)

        # store Uniform objecst indexed by name of associated variable in shader
        self.uniforms= {}

        # Each shader typically contains these uniforms
        #   values will be set during render process from Mesh/Camera
        # Additional unifors added by extending classes.
        self.uniforms['modelMatrix'     ]= Uniform('mat4', None)
        self.uniforms['viewMatrix'      ]= Uniform('mat4', None)
        self.uniforms['projectionMatrix']= Uniform('mat4', None)

        # Store OpenGL rendere settings inedexed by var name
        # Additional settings added by extending classes
        self.settings= {}
        self.settings['drawStyle']= GL_TRIANGLES


    def addUniform(self, dataType, variableName, data):
        self.uniforms[variableName]= Uniform(dataType, data)

    # initialize all uniform variable refernces
    def locateUniforms(self):
        for variableName, uniformObject in self.uniforms.items():
            uniformObject.locateVariable( self.programRef, variableName )

    # configure OpenGL with render settings
    def updateRenderSettings(self):
        pass

    # convenience method for setting multiple material "properties"
    # (uniform and render setting) values from a dict
    def setProperties(self, properties):
        for name,data in properties.items():
            # update uniforms
            if name in self.uniforms.keys():
                self.uniforms[name].data= data
            # update render settings
            elif name in self.settings.keys():
                self.settings[name]= data

            else:
                raise Exception('Material has no property named: ' + name)


