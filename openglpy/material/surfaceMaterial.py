from material.basicMaterial import BasicMaterial
from OpenGL.GL import *

class SurfaceMaterial(BasicMaterial):
    def __init__(self, properties={}):
        super().__init__()

        # render vertices as continuous lines by default
        self.settings['drawStyle'] = GL_TRIANGLES
        # render both sides ? default: front side only (verts counter clock)
        self.settings['doubleSide'] = False        
        # wireframe ?
        self.settings['wireframe'] = False
        # line thickness  for wireframe
        self.settings['lineWidth'] = 1

        self.setProperties(properties)

    def updateRenderSettings(self):
        if self.settings['doubleSide']:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings['wireframe']:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings['lineWidth'])


