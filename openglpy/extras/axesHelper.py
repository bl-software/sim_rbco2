from core.mesh import Mesh
from geometry.geometry import Geometry
from material.lineMaterial import LineMaterial

class AxesHelper(Mesh):
    def __init__(self, axisLength=1, lineWidth=4, axisColors=[[1,0,0], [0,1,0], [0,0,1]]):
        geo=Geometry()
        try:
            axisLengthX,axisLengthY,axisLengthZ=axisLength
        except TypeError:
            axisLengthX,axisLengthY,axisLengthZ=axisLength,axisLength,axisLength

        
        positionData= [ [0,0,0], [axisLengthX,           0,           0 ],
                        [0,0,0], [          0, axisLengthY,           0 ],
                        [0,0,0], [          0,           0, axisLengthZ ]]
        colorData= [axisColors[0],  axisColors[0],
                    axisColors[1],  axisColors[1],
                    axisColors[2],  axisColors[2]]

        geo.addAttribute('vec3', 'vertexPosition', positionData)
        geo.addAttribute('vec3', 'vertexColor',    colorData   )
        geo.countVerticies()

        mat= LineMaterial({
            'useVertexColors': True,
            'lineWidth'      : lineWidth,
            'lineType'       : 'segment' })

        # initialize the mesh
        super().__init__(geo,mat)


