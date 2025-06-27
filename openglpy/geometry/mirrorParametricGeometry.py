import numpy
from geometry.geometry import Geometry
import pprint
pp=pprint.PrettyPrinter(indent=2)

class MirrorParametricGeometry(Geometry):
    ''' Currently only for biConcave Disc like - stitch triangles at max radius '''
    def __init__(self, uStart, uEnd, uResolution,
            vStart, vEnd, vResolution, surfaceFunction, mirrorZ=True):
        super().__init__()

        def calcNormal(P0,P1,P2):
            v1= numpy.array(P1) - numpy.array(P0)
            v2= numpy.array(P2) - numpy.array(P0)
            normal= numpy.cross(v1,v2)
            #print('normal=',normal, f' cN point: {P0}, {P1}, {P2}')
            n= numpy.linalg.norm(normal)
            #print('n=',n)
            #if n != 0:
            normal= normal / n#umpy.linalg.norm(normal)
            return normal

        # gen set of points on function
        deltaU= (uEnd - uStart) / uResolution
        deltaV= (vEnd - vStart) / vResolution
        positions= []
        uvs   = []
        uvData= []
        vertexNormals = []
        for uIndex in range(uResolution+1):
            pArray= []
            vArray= []
            nArray= []
            for vIndex in range(vResolution+1):
                u= uStart + uIndex * deltaU
                v= vStart + vIndex * deltaV
                pArray.append( surfaceFunction(u,v) )
                #print('pArray', pArray)

                u= uIndex / uResolution 
                v= vIndex / vResolution 
                vArray.append( [u, v] )

                u= uStart + uIndex * deltaU
                v= vStart + vIndex * deltaV
                h= 0.0001
                P0= surfaceFunction(u  ,v  )
                P1= surfaceFunction(u+h,v  )
                P2= surfaceFunction(u  ,v+h)
                normalVector= calcNormal(P0,P1,P2)
                nArray.append( normalVector )

            positions.append(pArray)
            uvs.append(vArray)
            vertexNormals.append(nArray)

        for uIndex in range(uResolution,-1,-1):
            pArray= []
            vArray= []
            nArray= []
            for vIndex in range(vResolution+1):
                u= uStart + uIndex * deltaU
                v= vStart + vIndex * deltaV
                pArray.append( surfaceFunction(u,v,z=-1.0) )
                #print('pArray', pArray)

                u= uIndex / uResolution 
                v= vIndex / vResolution 
                vArray.append( [u, v] )

                u= uStart + uIndex * deltaU
                v= vStart + vIndex * deltaV
                h= 0.0001
                P0= surfaceFunction(u  ,v  ,z=-1.0)
                P1= surfaceFunction(u+h,v  ,z=-1.0)
                P2= surfaceFunction(u  ,v+h,z=-1.0)
                normalVector= calcNormal(P0,P1,P2)
                nArray.append( normalVector )

            positions.append(pArray)
            uvs.append(vArray)
            vertexNormals.append(nArray)

        #if mirrorZ == True:
        #    mirZ_positions=[]
        #    for rect6p in positions:
        #        print('r6')
        #        va= []
        #        for p in rect6p:
        #            print('r6:p=',p)
        #            va.append( [p[0], p[1], -p[2]] )
        #        mirZ_positions.append(va)
        #    positions.extend(mirZ_positions)
#
#        print('\nPPPPP:\n')
#        pp.pprint(positions)
#        print('\n')

        #store vertex data
        positionData= []
        colorData= []

        C1, C2, C3 = [1,0,0], [0,1,0], [0,0,1]
        C4, C5, C6 = [0,1,1], [1,0,1], [1,1,0]

        vertexNormalData= []
        faceNormalData  = []

        # group vertex data into triangles
        # note: .copy() is necessary to aviod storing references.
        for xIndex in range(uResolution):
            for yIndex in range(vResolution):
                # pos data
                pA= positions[xIndex+0][yIndex+0]
                pB= positions[xIndex+1][yIndex+0]
                pD= positions[xIndex+0][yIndex+1]
                pC= positions[xIndex+1][yIndex+1]
                positionData += [ pA.copy(), pB.copy(), pC.copy(), pA.copy(), pC.copy(), pD.copy() ]

                # color data
                colorData += [ C1, C2, C3, C4, C5, C6 ]

                # uv coords
                uvA= uvs[xIndex+0][yIndex+0]
                uvB= uvs[xIndex+1][yIndex+0]
                uvD= uvs[xIndex+0][yIndex+1]
                uvC= uvs[xIndex+1][yIndex+1]
                uvData += [uvA,uvB,uvC,  uvA,uvC,uvD]

                # vertex normal vectors
                nA= vertexNormals[xIndex+0][yIndex+0]
                nB= vertexNormals[xIndex+1][yIndex+0]
                nD= vertexNormals[xIndex+0][yIndex+1]
                nC= vertexNormals[xIndex+1][yIndex+1]
                vertexNormalData += [nA,nB,nC, nA,nC,nD]
                
                # face normal vectors
                fn0= calcNormal(pA,pB,pC)
                fn1= calcNormal(pA,pC,pD)
                faceNormalData += [fn0,fn0,fn0, fn1,fn1,fn1]

        for xIndex in range(uResolution, 2*uResolution):
            for yIndex in range(vResolution):
                # pos data
                pA= positions[xIndex+0][yIndex+0]
                pB= positions[xIndex+1][yIndex+0]
                pD= positions[xIndex+0][yIndex+1]
                pC= positions[xIndex+1][yIndex+1]
                positionData += [ pA.copy(), pB.copy(), pC.copy(), pA.copy(), pC.copy(), pD.copy() ]

                # color data
                colorData += [ C1, C2, C3, C4, C5, C6 ]

                # uv coords
                uvA= uvs[xIndex+0][yIndex+0]
                uvB= uvs[xIndex+1][yIndex+0]
                uvD= uvs[xIndex+0][yIndex+1]
                uvC= uvs[xIndex+1][yIndex+1]
                uvData += [uvA,uvB,uvC,  uvA,uvC,uvD]

                # vertex normal vectors
                nA= vertexNormals[xIndex+0][yIndex+0]
                nB= vertexNormals[xIndex+1][yIndex+0]
                nD= vertexNormals[xIndex+0][yIndex+1]
                nC= vertexNormals[xIndex+1][yIndex+1]
                vertexNormalData += [nA,nB,nC, nA,nC,nD]
                
                # face normal vectors
                fn0= calcNormal(pA,pB,pC)
                fn1= calcNormal(pA,pC,pD)
                faceNormalData += [fn0,fn0,fn0, fn1,fn1,fn1]


        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor"   , colorData   )
        self.addAttribute("vec2", "vertexUV"      , uvData      )
        self.addAttribute("vec3", "vertexNormal"  , vertexNormalData  )
        self.addAttribute("vec3", "faceNormal"    , faceNormalData  )
        self.countVerticies()

