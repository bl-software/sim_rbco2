from geometry.parametricGeometry import ParametricGeometry
from geometry.polygonGeometry import PolygonGeometry
from core.matrix import Matrix
from math import sin, cos, pi

class CylindricalGeometry(ParametricGeometry):
    def __init__(self, radiusTop=1, radiusBottom=1, height=1,
            radialSegments=32, heightSegments=4,
            closedTop=True, closedBottom=True):

        #print(f'Clyindrical: rT:{radiusTop} rB:{radiusBottom} h:{height}\n\
        #    radSed:{radialSegments}  heightSeg:{heightSegments}\n\
        #    cT:{closedTop} cB:{closedBottom}')

        def S(u,v):
            return [ (v*radiusTop + (1-v)*radiusBottom) * sin(u),
                     height * (v-0.5),
                     (v*radiusTop + (1-v)*radiusBottom) * cos(u) ]

        super().__init__( 0, 2*pi, radialSegments, 0, 1, heightSegments, S)

        #self.print_tris(self.attributes['vertexPosition'])

        if closedTop:
            #print(f'CLOSED TOP rS:{radialSegments}, rT:{radiusTop}')
            topGeometry= PolygonGeometry(radialSegments, radiusTop)
            #self.print_tris(topGeometry.attributes['vertexPosition'])
            transform= Matrix.makeTranslation( 0, height/2, 0) @  Matrix.makeRotationY(-pi/2) @  Matrix.makeRotationX(-pi/2)
            topGeometry.applyMatrix(transform)
            #self.print_tris(topGeometry.attributes['vertexPosition'])
            self.merge(topGeometry)

        if closedBottom:
            #print(f'CLOSED BOTTOM rS:{radialSegments}, rT:{radiusTop}')
            bottomGeometry= PolygonGeometry(radialSegments, radiusBottom)
            transform= Matrix.makeTranslation( 0, -height/2, 0) @ Matrix.makeRotationY(-pi/2) @ Matrix.makeRotationX(pi/2)
            bottomGeometry.applyMatrix(transform)
            self.merge(bottomGeometry)
