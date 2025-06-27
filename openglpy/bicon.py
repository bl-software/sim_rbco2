import sys
print('NameInBicon.py:', __name__)
print('Package:', __package__)
print('Path:',sys.path)
#sys.path.append('.')
#print('Path2:',sys.path)
#PYOPENGL_PLATFORM=egl python test46.py
#sys.exit()
#from pathlib import Path
oglPath= 'openglpy'#Path(__file__)

from core.baseWX   import Base
from core.renderer import Renderer
from core.scene    import Scene
from core.camera   import Camera
from core.mesh     import Mesh
from core.textureWX  import Texture
from core.matrix   import Matrix

from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
from extras.textTextureWX import TextTexture

from math import pi, cos, sin, atan
#import wx.lib.inspection
#Geometric
from geometry.rectangleGeometry import RectangleGeometry

#Parametric
#from geometry.planeGeometry import PlaneGeometry
from geometry.sphereGeometry import SphereGeometry
from geometry.lineGeometry import LineGeometry
from geometry.biconcavediscGeometry import BiConcaveDiscGeometry

#from material.material import Material
from material.surfaceMaterial import SurfaceMaterial
from material.lineMaterial import LineMaterial
from material.textureMaterial import TextureMaterial

# render basic scene
class BiCon(Base):
#class Test(Base):
    def __init__(self,parent,winwidth,winheight,bicon_kwargs):
        self.parent=parent

        print('\n'*10)
        print('*******************')
        print(f'BiCon: parent={parent}')
        print('*******************')
        self.winwidth=winwidth
        self.winheight=winheight

        self.D= bicon_kwargs['D']
        self.R= bicon_kwargs['R']
        self.r= bicon_kwargs['r']

        self.objlist=[]
        self.rotlist=[]
        self.hudobjlist=[]

        super().__init__(parent,screenSize=(winwidth,winheight))
        self.unitsPerSecond=1
        self.degreesPerSecond=60* (3.1415926 / 180)
        self.dragthisx=0
        self.dragthisy=0

        self.terminalGreen =(65    ,205    ,65    ,250)
        self.terminalGreenN=(65/255,205/255,65/255,0.8)
        self.terminalBlue  =(0x32    ,0xb8    ,0xfd    ,255)
        self.terminalBlueN =(0x32/255,0xb8/255,0xfd/255,0.8)

    def initialize(self):
        print('Initializing program...')
        
        print('RENDERCALL',self.glcanv.GetClientSize())
        self.renderer= Renderer( (self.winwidth,self.winheight) )#self.glcanv.GetClientSize())
        self.scene= Scene()
        self.camera= Camera( aspectRatio= self.winwidth/self.winheight)
        #self.camera.setPosition([0, 0, 4])

        self.rig= MovementRig(unitsPerSecond=5, degreesPerSecond=60)
        self.rig.add( self.camera )
        self.rigZpos=9#10
        self.rig.setPosition( [0, 0, self.rigZpos] )
        #self.rig.rotateX(-3.14/2)
        #self.rig.rotateX(-3.14/2)
        self.scene.add( self.rig )

        self.hudScene= Scene()
        self.hudCamera= Camera()
        self.hudCamera.setOrthographic(0,self.winwidth,0,self.winheight,1,-1)

        #skyMaterial= TextureMaterial(Texture(f'{oglPath}/images/sky.jpg'))
        #sky=Mesh(skyGeometry,skyMaterial)
        #self.scene.add(sky)
        
        #grassGeometry=RectangleGeometry(width=100, height=100)
        #grassMaterial=TextureMaterial(Texture(f'{oglPath}/images/grass.jpg'))
        #grass=Mesh(grassGeometry, grassMaterial)
        #grass.rotateX(-3.14/2)
        #self.scene.add(grass)

        hudkwargs={ 'hudheight': self.winheight//10,
                    'hudtext'  : f'Mouse: C56BL6\Case WT-m\nD_torus = {self.D:0.4} μm' }
        self.makeHUDLabel(hudkwargs, new=False)

        #greenlabelTexture= TextTexture( text=f'12345 {self.D} 67890 μm',
        #greenlabelTexture= TextTexture( text=f'2234567890',
        #        fontFileName=f'{oglPath}/fonts/NotoSansMath-Regular.ttf',
        #        systemFontName='NotoSansMath',
        #        fontSize=64,
        #        fontColor=(200,0,0,255),
        #        transparent=False,
        #        backgroundColor=(50,50,0,255),
        #        imageWidth = None,#800,
        #        imageHeight= None,
        #        #alignHorizontal= 0.25,
        #        #alignVertical  = 0.5,
        #        imageBorderWidth= 0,#4,
        #        imageBorderColor= (0,0,0,255) )

        #print(f'Gimw:{self.winwidth}  imh:{self.winheight}')
        #texiw=greenlabelTexture.imageWidth
        #texih=greenlabelTexture.imageHeight
        #print(f'Gtexiw:{texiw}  texih:{texih}')
        #texscrw= texiw/self.winwidth
        #texscrh= texih/self.winheight
        #print(f'Gtexscrw {texscrw:.3}  texscrh {texscrh:.3}')
        #swcam= texscrw * self.rigZpos *2
        #shcam= texscrh * self.rigZpos *2
        #print(f'Gswcam {swcam:.3}  shcam {shcam:.3}')

        #self.greenlabelMaterial= TextureMaterial( greenlabelTexture )
        #self.greenlabelGeometry= RectangleGeometry( width=500, height=200,
        #        position=[500,1300], alignment=[0.0,1.0])
        #self.greenlabel=Mesh(self.greenlabelGeometry, self.greenlabelMaterial)

        #move_pix_x= (self.winwidth - texiw) / 2
        #move_pix_y= (self.winheight - texih) / 2
        #print(f'Gmove_pix_x:{move_pix_x} move_pix_y:{move_pix_y}')
        #move_cam_x= (move_pix_x/self.winwidth) * self.rigZpos
        #move_cam_y= (move_pix_y/self.winheight) * self.rigZpos
        #print(f'Gmove_cam_x:{move_cam_x:.3} move_cam_y:{move_cam_y:.3}')

        #self.greenlabel.setPosition( [2.00, self.rigZpos/2 *1.05 , 0.0] )
        #WORKSself.greenlabel.setPosition( [-move_cam_x, self.rigZpos/2 *1.05 , 0.0] )
        #self.hudScene.add( self.greenlabel )
        
        self.grid= GridHelper( gridColor=[0.5,0.5,0.5], centerColor=[1,1,1] )
        #self.grid.rotateX( pi/2 )
        self.scene.add(self.grid)

        self.ygrid= GridHelper( gridColor=[0.5,0.1,0.1], centerColor=[1,1,1] )
        self.ygrid.rotateX( -0.9*pi/2 )
        self.scene.add(self.ygrid)
        #material= SurfaceMaterial( {'useVertexColors':True,'doubleSide':True} )
        #GR material= TextureMaterial(grid)
        #GR self.mesh= Mesh( geometry, material )

        #self.lastTime= int(self.time)
        #self.rig.lookAttachment.rotateX( -pi*.20 )#0.81514 )

# BCD Stuff
        #a0 = 0.002 +  int(self.time)/100
        #a1 = 0.24 +  int(self.time)/100 # Max width at torus
        #a2 = 031 +  int(self.time)/10
#            print(f'time:{self.time:0.3f}  a0={a0}  a1={a1}  a2={a2}')
        self.bcdkwargs={
            'D'  : self.D,
            'a0' : 0.050,
            'a1' : 0.9,
            'a2' : 1.3,
            'radiusSegments':47,
            'heightSegments':39,
        }
        self.makeBCD()#**self.bcdkwargs)# a0=a0, a1=a1, a2=a2, radiusSegments=47, heightSegments=39 )


    def updateScenes(self,combokwargs):
        self.D= combokwargs['D']
        self.R= combokwargs['R']
        self.r= combokwargs['r']
        self.bcdkwargs.update({'D':self.D})
        self.makeBCD(new=True)#,**combokwargs)
        hudkwargs={ 'hudheight': self.winheight//10,
                    'hudtext'  : f'Mouse: C56BL6\Case WT-m\nD_torus = {self.D:0.4} μm' }
        #hl1=
        #self.makeHUDLabel(new=True)#,**combokwargs)

    def makeHUDLabel(self, hudkwargs, new=False):#, **kwargs):
        if new: # new params
            for obj in [ self.hudlabel, self.dlsrlabel_t ]:
                try:
                    self.hudScene.remove(obj)
                except Exception as e:
                    print(f'EXC:{e}')

        hudtext= hudkwargs['hudtext']
        hudheight= hudkwargs['hudheight']
        hudlabelTexture= TextTexture( text=f'{hudtext}',
                #fontFileName='fonts/InputSerifNarrow-BoldItalic.ttf',
                #fontFileName='fonts/NotoSansMath-Regular.ttf',
                fontFileName=f'{oglPath}/fonts/NotoSansMath-Regular.ttf',
                systemFontName='NotoSansMath',
                fontSize=64,
                fontColor=self.terminalGreen,
                transparent=False,
                #backgroundColor=(140,40,40,200),
                backgroundColor=(0,0,0,255),
                imageWidth = None,#400,#self.winwidth,
                imageHeight= None,#200,#hudheight,
                #alignHorizontal= 0.25,
                #alignVertical  = 0.5,
                imageBorderWidth= 0,#4,
                imageBorderColor= (0,0,0,255) )

        self.hudlabelMaterial= TextureMaterial( hudlabelTexture )
        
        self.hudlabelGeometry= RectangleGeometry(width=hudlabelTexture.imageWidth,height=hudlabelTexture.imageHeight,
                position=[10,self.winheight-10], alignment=[0.0,1.0])# width=0.5, height=0.5)
        self.hudlabel=Mesh(self.hudlabelGeometry, self.hudlabelMaterial)

        self.hudScene.add(self.hudlabel)
        print(f'HUD UPDATED with hudtext={hudtext}')


    def floatlabel_t(self,flttext,**kwargs):
        fltlabelTexture= TextTexture(\
                text=f'{flttext}',
                fontFileName=f'{oglPath}/fonts/NotoSansMath-Regular.ttf',
                systemFontName='NotoSansMath',
                fontSize=kwargs.get('fontSize',64),
                fontColor=kwargs.get('fltcolor',(255,255,255,255)),
                transparent=False,
                backgroundColor=kwargs.get('bgc',(0,0,0,255)),
                imageWidth = kwargs.get('iw',None),
                imageHeight= kwargs.get('ih',None),
                #alignHorizontal= kwargs.get('ah',0.25),
                #alignVertical  = kwargs.get('av',0.5),
                imageBorderWidth= kwargs.get('ibw',0),
                imageBorderColor= kwargs.get('ibc',(0,0,0,255)),
        )
        fltlabelMaterial= TextureMaterial( fltlabelTexture )
        return fltlabelTexture, fltlabelMaterial

    def floatlabel(self,px,py,fltlabelTexture,fltlabelMaterial,ax=0.0,ay=1.0):
        fltlabelGeometry= RectangleGeometry(width=fltlabelTexture.imageWidth,height=fltlabelTexture.imageHeight,
                position=[px,py], alignment=[ax,ay])
        return Mesh(fltlabelGeometry, fltlabelMaterial)


    def makeBCD(self, new=False):#, **bcdkwargs):#D=7.7, a0=0.02, a1=1.54, a2=2.2, radiusSegments=27, heightSegments=29 ):
        print('makeBCD')
        if new: # new params
            for m in self.objlist:
                    self.scene.remove(m)
            self.objlist=[]
            self.rotlist=[]
        #if new: # new params
        #    #meshes=[self.bluesphere, self.greensphere, self.bcd, self.dls_r, self.dls_D, self.torusN]#,self.dimN]
        #    #for m in meshes:
        #    for m in self.objlist:
        #        try:
        #            self.scene.remove(m)
        #        except:
        #            pass
#
        print('\nB\nB\nB\nB\nB\nbcdkwargs:',self.bcdkwargs)
        #print(sys.path)
        #    D=7.7, a0=0.02, a1=1.54, a2=2.2, radiusSegments=27, heightSegments=29)
        self.bcdGeometry= BiConcaveDiscGeometry(**self.bcdkwargs )
        self.bcdTexture = Texture('blood_tex.png')
        self.bcdMaterial= TextureMaterial(self.bcdTexture, {'transparency':0.53})
        self.bcd= Mesh( self.bcdGeometry, self.bcdMaterial)
        self.objlist.append(self.bcd)
        self.rotlist.append(self.bcd)

        print('maxZ',self.bcdGeometry.maxZ)
        print('maxZ_x',self.bcdGeometry.maxZ_x)
        print('maxZ_y',self.bcdGeometry.maxZ_y)
        torus_small_r= self.bcdGeometry.maxZ
        torus_big_R= abs(self.bcdGeometry.maxZ_x)

        # blue sphere
        self.bluesphereGeometry= SphereGeometry(radius=torus_small_r, radiusSegments=15, heightSegments=15)
        self.bluesphereMaterial= SurfaceMaterial( {'baseColor':self.terminalBlueN,#[1.0,0.0,1.0],
                                                   'useVertexColors':False,
                                                   'doubleSide':False} )
        self.bluesphere=Mesh( self.bluesphereGeometry, self.bluesphereMaterial )
        self.objlist.insert(self.objlist.index(self.bcd),self.bluesphere)
        self.rotlist.append(self.bluesphere)

        #dim lines
        bsx,bsy,bsz= torus_big_R*cos(pi*3/8), torus_big_R*sin(pi*3/8), 0.0
        dls_mat=LineMaterial({'useVertexColors':True, 'lineWidth':3, 'lineType':'segment'})

        self.dimlines_D= LineGeometry(\
            [ [-self.D/2, -0.2, 0.0], [-self.D/2,  0.0, 0.0],
              [-self.D/2,  0.0, 0.0], [ self.D/2,  0.0, 0.0],
              [ self.D/2,  0.0, 0.0], [ self.D/2, -0.2, 0.0]
            ],
            [ self.terminalGreenN ]*6,
            #[[1.0,0.0,0.0,1.0], [0.0,0.0,1.0,1.0]],
        )
        self.dls_D= Mesh( self.dimlines_D, dls_mat )
        self.objlist.append(self.dls_D)
        
        DIMNORM=False
        if DIMNORM:
            dim_normal_end=dne= self.dls_D.getDirection()
            dim_normal_end=[dne[0],dne[1],dne[2]*10]#self.dls_D.getDirection()
            self.dim_norm= LineGeometry(\
                [[0.0, 0.0, 0.0], dim_normal_end],
                [[1.0,1.0,0.0,1.0], [1.0,0.0,1.0,1.0]],
            )
            self.dimlines_D.merge(self.dim_norm)
            #self.dimN= Mesh( self.dim_norm, dls_mat )
        self.dls_D.setPosition([0.20,self.D/2*1.1,0.0])
        self.dls_D.rotateZ(pi/2, localCoord=True)
        #self.dls_D.lookAt([0.1,0.1,0.0])
        
        TORUSNORMAL=False
        if TORUSNORMAL:
            torus_normal_end=self.bcd.getDirection()
            print('torus_normal_end',torus_normal_end)
            self.torus_norm= LineGeometry(\
                [[0.0, 0.0, 0.0]     , torus_normal_end],
                 [self.terminalGreenN, self.terminalGreenN]
            )
            self.torusN= Mesh( self.torus_norm, dls_mat )
            self.objlist.insert(self.objlist.index(self.bcd),self.torusN)
            self.rotlist.append(self.torusN)

        
        whitealphagreen=[1,1,1,0.1]#v/10 for v in self.terminalGreenN]
        redalphagreen =[1,0,0,0.1]#  for v in self.terminalGreenN]

        self.dimlines_r= LineGeometry(\
            #[ [r-0.2,   0.0, 0.0], [r    ,   0.0, 0.0],
            #  [r    ,   0.0, 0.0], [r    , bsy/2, 0.0],
            #  [r    , bsy/2, 0.0], [r-0.2, bsy/2, 0.0],
            [ [0.0-0.2,   0.0, 0.0], [0.0    ,   0.0, 0.0],
              [0.0    ,   0.0, 0.0], [0.0    , bsy/2, 0.0],
              [0.0    , bsy/2, 0.0], [0.0-0.2, bsy/2, 0.0],
            ],
            [ self.terminalBlueN ]*6,
            )
        self.dls_r= Mesh( self.dimlines_r, dls_mat )
        self.objlist.append(self.dls_r)
        #self.dlsrlabel=self.floatlabel( self.r*1.1, bsy+0, '{self.r:0.4} μm',self.terminalBlue, new=new )
        dlsr_t,dlsr_m=self.floatlabel_t( f'r_torus= {self.r:0.4} μm', fltcolor=self.terminalBlue )
        px=self.winwidth -10# - dlsr_t.imageWidth
        py=self.winheight -10 - 67# - 64
        self.dlsrlabel_t=self.floatlabel( px, py, dlsr_t, dlsr_m, ax=1.0, ay=0.0 )
        #self.dlsrlabel_t.setDirection([0.0,0.0,-1.0])
#        self.dlsrlabel_t.rotateZ(-pi/2, localCoord=True)
        #self.dlsrlabel_t.translate ( self.D/2*1.1,bsy,bsz )
#        self.dlsrlabel_t.translate( self.D/2*1.1 +0.2,bsy,bsz,localCoord=False )
#        self.dlsrlabel_t.scale(0.10)
        #self.objlist.append(self.dlsrlabel_t)
        self.hudScene.add(self.dlsrlabel_t)

        self.bluesphere.translate( bsx,bsy,bsz )
        self.dls_r.translate      ( self.D/2*1.1,bsy,bsz )

        GREENSPHERE=False
        if GREENSPHERE:
            self.greensphereGeometry= SphereGeometry(radius=torus_small_r/10, radiusSegments=15, heightSegments=15)
            self.greensphereMaterial= SurfaceMaterial( {'baseColor':[0.0,1.0,0.0],'useVertexColors':False,'doubleSide':False} )
            self.greensphere=Mesh( self.greensphereGeometry, self.greensphereMaterial )
            self.objlist.insert(self.objlist.index(self.bcd),self.greensphere)
            self.rotlist.append(self.greensphere)
            self.greensphere.translate( 0.0, 1.1*self.D/2, 0.0 )

        self.rotTogether( [self.bcd,self.bluesphere], #, self.greensphere],self.dls],
            [\
                ('x',pi*0.5),
                ('z',pi*0.15),
                ('y',pi*0.1),
                ('x',pi*0.1),
            ])

        bspos=self.bluesphere.getPosition()
        print('Obspos',self.prettypos(bspos))

        for obj in self.objlist:
            self.scene.add( obj )

    def rotTogether(self, meshes, axsrads):
        rots=['']
        for a,rads in axsrads:
            for m in meshes:
                {'x': m.rotateX,
                 'y': m.rotateY,
                 'z': m.rotateZ,
                 }[a](rads, localCoord=False)

    def update(self):
        #if self.setQUIT:
        #    print('update: got setQUIT!')
        #    self.Destroy()
        #    self.parent.Close()

        moveAmount  = self.unitsPerSecond   * self.deltaTime
        rotateAmount= self.degreesPerSecond * self.deltaTime

        self.rig.update(self.input, moveAmount= moveAmount, rotateAmount=rotateAmount )
        self.do_mouse(self.input,moveAmount,rotateAmount)

        size= self.glcanv.GetClientSize()
        #print('size=',size)
        self.renderer.render( self.scene, self.camera, size )
        self.renderer.render( self.hudScene, self.hudCamera, size, clearColor=False )

        #print(f'{dir(self.bcd)}')
        #print(f'{self.bcd.getWorldPosition()}')

    def prettypos(self,p):
        return [ f'{v:0.3f}' for v in p ]

    lastθ=0
    def do_mouse(self, io,moveAmount, rotateAmount):
        #(mmx,mmy),another= io.consume_mouse_movement()
        mmx,mmy= io.mmot()
        mx= mmx - self.dragthisx
        my= mmy - self.dragthisy
        #print('mmx=',mmx, '      dragx',self.dragthisx)
        if mmx > 1000:
            print('Drag >1000 in X dir == quit')
            self.running=False

        speed=6.28/900 # lower is faster
        if mmx==0 and mmy==0:
            self.dragthisx=0
            self.dragthisy=0
        else:
            self.dragthisx = mmx
            self.dragthisy = mmy
        #print(f'test46:do_mouse: handling {mmx,mmy}')
        yrot= mx * speed
        xrot= my * speed
        if mmx:
            for obj in self.rotlist:
                obj.rotateY(yrot, localCoord=False)
        if mmy:
            for obj in self.rotlist:
                obj.rotateX(xrot, localCoord=False)

        bdir=self.bcd.getDirection()
        brot=self.bcd.getRotationMatrix()
        bspos=self.bluesphere.getPosition()
        bsx,bsy,bsz=self.bluesphere.getPosition()
        #print( 'bsx,bsy,bsz', bsx,bsy,bsz)
        #print('bspos',self.prettypos(bspos))
        #dpos=self.dls_r.getPosition()
        dsx,dsy,dsz=self.dls_r.getPosition()
        #print( 'dsx,dsy,dsz', dsx,dsy,dsz)
        #wpos=self.dls_r.getWorldPosition()
        #print('dlpos',self.prettypos(dpos))#,'\n')
        #print('dwpos',self.prettypos(wpos),'\n')
        #self.dls_r.setPosition([dpos[0], bspos[1], bspos[2]])
        #dsx=#min(dsx,2.0)
        self.dls_r.setPosition([dsx,bsy,bsz])
        
        nx,ny,nz= torus_normal=self.bcd.getDirection()
        #print('torus_normal',torus_normal)
        '''
        |\
        | \
        |  \
        |   \
        |____\tanθ= ny/nx
        '''
        if abs(nx) > 0.001:
            θ= atan( ny/nx)
        else:
            θ= 0

        dDx=self.D/2*cos(θ)
        dDy=self.D/2*sin(θ)
        if dDx > 0.0:
            dDy=-dDy  # if pointing to right neg q
        dDx=-abs(dDx) # keep it on the left

        self.dls_D.setPosition([dDx,dDy,0.0])
        dsx,dsy,dsz=self.dls_r.getDirection()
        #print( 'dsx,dsy,dsz', dsx,dsy,dsz)
        if abs(dsx) > 0.001:
            θ2= atan( dsy/dsx)
        else:
            θ2= 0

        #dθ=(pi/2-θ)-self.lastθ
        dθ=θ-self.lastθ
        #print(f'θ {θ:8.5f} dθ {dθ:8.5f}  lastθ {self.lastθ:8.5f}  dDx {dDx:8.5f}  dDy {dDy:8.5f}')
        self.dls_D.rotateZ(dθ, localCoord=True)
        self.lastθ+=dθ#self.lastθ+dθ

#        self.dls_D.setPosition([3.0,3.0,0.0])
#        self.dls_D.rotateZ(θ, localCoord=False)
        #self.dls_D.rotateZ(0.3, localCoord=False)
    #    m1= dDy/dDx
    #    try:
    #        m2=-1/m1 # look at is perp towards x axis
    #    except ZeroDivisionError:
    #        m2=-0.000000001
    #    b=dDy-m2*dDx
    #    print('b=',b)

#        self.dls_D.setDirection([yrot,xrot,-1])
#        self.dls_D.setDirection([1,-1,0.0])
#        self.dls_D.lookAt([0.1,0.1,0.0])
        #print('D\n'*4, self.dls_D.getPosition())
        #print(self.dls_D.getDirection())
        
        
        #if another:
        #    self.do_mouse(moveAmount,rotateAmount)


if __name__ == '__main__':
    print('in bicon:__main__')
    import wx
    #from wxTestConeOnly import ConeCanvas
    #from testfiles.test3 import Test
    #from test3 import Test
    #from testfiles.test46 import Test
    ww=1200
    wh=1200
    app = wx.App()
    frame = wx.Frame( None, title="BiCon", size=(ww,wh))
    #canvas = ConeCanvas(frame)
    #panel= wx.Panel(frame, wx.ID_ANY, size=(ww,wh))
    #panel.SetAutoLayout(True)
    d=6.28
    BiCon( frame, ww, wh, {'D':d,'R':d/2,'r':1.1} ).run()
#    canvas = Test( panel ).run()
    #canvas = BiCon( frame ).run()
    frame.Show()
    #print('INSP\n'*10)
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


