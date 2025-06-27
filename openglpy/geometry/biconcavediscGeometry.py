from geometry.mirrorParametricGeometry import MirrorParametricGeometry
from math import sin, cos, pi, sqrt, pow

class BiConcaveDiscGeometry(MirrorParametricGeometry):
    def __init__(self, D=7.7, a0=0.02, a1=1.54, a2=2.2, radiusSegments=27, heightSegments=29, **kwargs):
        self.maxZ= 0
        self.maxZ_x= 0
        self.maxZ_y= 0

        def S(r,v,x=1.0,y=1.0,z=1.0):
            #print(f'r:{r}  v:{v}')
            thisZ= z*D * sqrt( 1-(4*pow(r,2)/pow(D,2))) * ( a0 + a1*pow(r,2)/pow(D,2) + a2*pow(r,4)/pow(D,4) )
            thisX= x*r*sin(v)
            thisY= y*r*cos(v)
            if thisZ >= self.maxZ:
                self.maxZ = thisZ
                self.maxZ_x= thisX
                self.maxZ_y= thisY
            v= [ thisX,#x*r*sin(v),
                 thisY,#y*r*cos(v),
                 thisZ#z*D * sqrt( 1-(4*pow(r,2)/pow(D,2))) * ( a0 + a1*pow(r,2)/pow(D,2) + a2*pow(r,4)/pow(D,4) )
            ]
            return v

        super().__init__( 0, D/2.00100, radiusSegments, 0, pi*1.75, heightSegments, S )
        #super().__init__( 0, 2*pi, radiusSegments, -pi/2, pi/2, heightSegments, S )
