from OpenGL.GL import *
from core.mesh import Mesh
from light.light import Light

class Renderer(object):
    def __init__(self, windowSize=(512,512), clearColor= [0,0,0]):
        #print('windowsize=',windowSize)
        glEnable( GL_DEPTH_TEST )
        # requiared for antialiasing
        glEnable( GL_MULTISAMPLE )
        glClearColor( clearColor[0], clearColor[1], clearColor[2], 1 )

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def render(self, scene, camera, windowSize, clearColor=True, clearDepth=True, renderTarget=None):
        #print('windowsize=',windowSize)
        if( renderTarget == None ):
            glBindFramebuffer( GL_FRAMEBUFFER, 0 )
            glViewport( 0, 0, windowSize[0], windowSize[1] )
        else:
            glBindFramebuffer( GL_FRAMEBUFFER, renderTarget.framebufferRef )
            glViewport( 0, 0, renderTarget.width, renderTarget.height )

        #clear color and depth buffers
        if clearColor:
            glClear(GL_COLOR_BUFFER_BIT)
        if clearDepth:
            glClear(GL_DEPTH_BUFFER_BIT)

        #update camera view (calc inverse)
        camera.updateViewMatrix()

        # extrace list of all Mesh objects in scene
        descendantList = scene.getDescendantList()
        meshFilter= lambda x : isinstance(x,Mesh)
        meshList= list( filter(meshFilter, descendantList) )
        lightFilter = lambda x: isinstance(x,Light)
        lightList = list( filter(lightFilter, descendantList) )
        while len(lightList) < 4:
            lightList.append(Light())

        for mesh in meshList:
            # if this object is not visible continue to next object in list
            if not mesh.visible:
                continue
            
            glUseProgram( mesh.material.programRef )

            # bind VAO
            glBindVertexArray( mesh.vaoRef )

            # update uniform values stored outside of material
            mesh.material.uniforms['modelMatrix'     ].data= mesh.getWorldMatrix()
            mesh.material.uniforms['viewMatrix'      ].data= camera.viewMatrix
            mesh.material.uniforms['projectionMatrix'].data= camera.projectionMatrix

            # if material uses light data, add light from list
            if 'light0' in mesh.material.uniforms.keys():
                for lightNumber in range(4):
                    lightName= f'light{lightNumber}'
                    lightObject= lightList[lightNumber]
                    mesh.material.uniforms[lightName].data = lightObject

            # add camera position if needed (specular lighting)
            if 'viewPosition' in mesh.material.uniforms.keys():
                mesh.material.uniforms['viewPosition'].data = camera.getWorldPosition()

            # update uniforms stored in material
            for varibleName, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()

            # update render settings
            mesh.material.updateRenderSettings()

            glDrawArrays( mesh.material.settings['drawStyle'], 0, mesh.geometry.vertexCount )

