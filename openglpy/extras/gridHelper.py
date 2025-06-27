from core.mesh import Mesh
from geometry.geometry import Geometry
from material.lineMaterial import LineMaterial

class GridHelper(Mesh):
    def __init__(self, size=10, divisions=10,
            gridColor=[0,0,0], centerColor=[0.5, 0.5, 0.5], lineWidth=1):
        geo=Geometry()

        positionData=[]
        colorData=[]

        # create a range of values
        values= []
        deltaSize= size/divisions
        for n in range(divisions+1):
            values.append( -size/2 + n * deltaSize )
        #values=[-3.0,3.0]
        #values=[1.0]

        #print('values:\n', values)
        for x in values:
            positionData.append( [x, -size/2, 0 ] )
            positionData.append( [x,  size/2, 0 ] )
            #print(f'x {x}')
            if x == 0:
                #print(f'x {x} centerColor')
                colorData.append(centerColor)
                colorData.append(centerColor)
            else:
                colorData.append(gridColor)
                colorData.append(gridColor)
        #print('posData:\n', positionData)
        #print('colorData:\n', colorData)

        # add horiz lines
        for y in values:
            positionData.append( [ -size/2, y, 0] )
            positionData.append( [  size/2, y, 0] )
            #print(f'y {y}')
            if y == 0:
                #print(f'y {y} centerColor')
                colorData.append(centerColor)
                colorData.append(centerColor)
            else:
                colorData.append(gridColor)
                colorData.append(gridColor)
        #s=6.95
        #s=4.95
        #positionData.append( [ -s/2, 4.0, 0] )
        #positionData.append( [  s/2, 4.0, 0] )
        #colorData.append(gridColor)
        #colorData.append(gridColor)
        #print('posData:\n', positionData)
        #print('colData:\n', colorData)
        #for i,(p,c) in enumerate(zip(positionData,colorData)):
        #    print(f'{i:3} {[f"{v:5.1f}" for v in p]} {[f"{v:5.1f}" for v in c]}')

        geo.addAttribute('vec3', 'vertexPosition', positionData)
        geo.addAttribute('vec3', 'vertexColor', colorData)
        geo.countVerticies()

        mat= LineMaterial({
            'useVertexColors': True,
            'lineWidth'      : lineWidth,
            'lineType'       : 'segment' })

        super().__init__(geo, mat)
        #super().rotateZ(0.1)
        
        #print('GVCs:',geo.vertexCount)
