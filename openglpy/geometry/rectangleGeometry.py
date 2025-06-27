from geometry.geometry import Geometry

class RectangleGeometry(Geometry):
    def __init__(self, width=1, height=1, position=[0,0], alignment=[0.5, 0.5]):
        super().__init__()
        posx, posy= position
        alx, aly= alignment
        P0= [posx +  (-alx) * width/2, posy +  (-aly) * height/2, 0]
        #P0=    [posx +  (-alx  ) * width/2, posy +  (-aly  ) * height/2, 0]
        #defP0= [0 +  (-0.5) *    1 /2, 0 +  (-0.5) *      1/2, 0]
        #defP0= [ -0.25, -0.25 , 0]
        P1= [posx + (1-alx) * width/2, posy +  (-aly) * height/2, 0]
        #defP1= [ 0.25, -0.25 , 0]
        P2= [posx +  (-alx) * width/2, posy + (1-aly) * height/2, 0]
        #defP2= [ -0.25, 0.25 , 0]
        P3= [posx + (1-alx) * width/2, posy + (1-aly) * height/2, 0]
        #defP2= [ 0.25, 0.25 , 0]
        C0,C1,C2,C3= [ 1,1,1 ], [1,0,0], [0,1,0], [0,0,1]
        T0,T1,T2,T3=    [ 0,0],   [1,0],   [0,1],   [1,1]
        print('PPPP', P0, P1, P2, P3)
        positionData= [ P0,P1,P3, P0,P3,P2 ]
        colorData   = [ C0,C1,C3, C0,C3,C2 ]
        uvData      = [ T0,T1,T3, T0,T3,T2 ]

        normalVector= [0,0,1]
        normalData  = [normalVector] * 6

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor"   , colorData   )
        self.addAttribute("vec2", "vertexUV"      , uvData      )
        self.addAttribute("vec3", "vertexNormal"  , normalData  )
        self.addAttribute("vec3", "faceNormal"    , normalData  )
        self.countVerticies()
