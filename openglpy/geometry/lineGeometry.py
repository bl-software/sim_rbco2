from geometry.geometry import Geometry

class LineGeometry(Geometry):
    def __init__(self, plist, clist=([1,1,1,1],[1,1,1,1])):
        super().__init__()
        positionData=[]
        colorData=[]
        #breakpoint()
#        (Pdb) print(list(zip(plist,clist)))
#[
#    ( [-3.478, 3.825, 0.0], (0.254, 0.803, 0.254) ),
#    ( [ 3.478, 3.825, 0.0], (0.254, 0.803, 0.254) )
#]
        for P,C in zip(plist,clist):
            positionData.append( P )#0,P1 )
            colorData.append( C )#0,C1 )

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec4", "vertexColor"   , colorData   )
        self.countVerticies()
