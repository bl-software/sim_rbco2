from core.object3D import Object3D
from core.matrix import Matrix
class MovementRig(Object3D):
    def __init__(self,unitsPerSecond=1, degreesPerSecond=60):
        # initialize base Object3D; controls movement and turn left/right
        super().__init__()

        # initialize attached Object3D; controls "look" up/down
        self.lookAttachment= Object3D()
        self.children= [self.lookAttachment]
        self.lookAttachment.parent= self

        # control rate of movement
        self.unitsPerSecond= unitsPerSecond
        self.degreesPerSecond= degreesPerSecond * (3.1415926 / 180)

        # customizable key mappings
        #  defaults: WASDRF (move), QE (turn), TG (look)
        # NOTE - ord upper is for wx.EVT_KEY_[UP|DOWN] events
        self.KEY_MOVE_FORWARDS     = ord("w".upper()) # 87
        self.KEY_MOVE_BACKWARDS    = ord("s".upper()) # 83
        self.KEY_MOVE_LEFT         = ord("a".upper()) # 65
        self.KEY_MOVE_RIGHT        = ord("d".upper()) # 68
        self.KEY_MOVE_UP           = ord("r".upper()) # 82
        self.KEY_MOVE_DOWN         = ord("f".upper()) # 70

        self.KEY_TURN_LEFT         = ord("q".upper()) # 81
        self.KEY_TURN_RIGHT        = ord("e".upper()) # 69

        self.KEY_LOOK_UP           = ord("i".upper()) # 84
        self.KEY_LOOK_DOWN         = ord("k".upper()) # 71
        self.KEY_LOOK_LEFT         = ord("j".upper()) # 74
        self.KEY_LOOK_RIGHT        = ord("l".upper()) # 76

        self.stdmv={
            self.KEY_MOVE_FORWARDS : self.moveupG,
            self.KEY_MOVE_BACKWARDS: self.movedownG,
            self.KEY_MOVE_LEFT     : self.moveleftG,
            self.KEY_MOVE_RIGHT    : self.moverightG,
            self.KEY_MOVE_UP       : self.moveZG,
            self.KEY_MOVE_DOWN     : self.moveXG,
            self.KEY_TURN_LEFT     : self.rotleftG,
            self.KEY_TURN_RIGHT    : self.rotrightG,

            self.KEY_LOOK_UP       : self.rotupL,
            self.KEY_LOOK_DOWN     : self.rotdownL,
            self.KEY_LOOK_LEFT     : self.rotleftL,
            self.KEY_LOOK_RIGHT    : self.rotrightL,
        }
    # adding and removing objects applies to look attachment
    #  override functions from Object3D class
    def add(self,child):
        self.lookAttachment.add(child)

    def remove(self, child):
        self.lookAttachment.remove(child)

    def do_keys(self, io, moveAmount, rotateAmount):
        keyCode,another= io.consume_pressed_key()
        #print(f'moveRig:do_keys: handling key {keyCode}')
        try:
            self.stdmv[keyCode](moveAmount,rotateAmount)
            #print(f'        {self.stdmv[keyCode]}')
        except KeyError:
            pass
        if another:
            self.do_keys(io,moveAmount,rotateAmount)

    def update(self, inputObject, deltaTime=0, moveAmount=0, rotateAmount=0):
        #print(f'moveRigUpdate deltaTime:{deltaTime}')
        if deltaTime:
            moveAmount  = self.unitsPerSecond   * deltaTime
            rotateAmount= self.degreesPerSecond * deltaTime
        

        self.do_keys(inputObject,moveAmount,rotateAmount)

    # GLOBAL
    def moveupG(self,moveAmount,rotateAmount):
        self.translate( 0,  moveAmount, 0 )
        #m=Matrix.makeTranslation( 0,  moveAmount, 0 )
        #self.modelMatrix.data = m @ self.modelMatrix.data
    def movedownG(self,moveAmount,rotateAmount):
        #print( f'movedownG {moveAmount}, {rotateAmount}' )
        self.translate( 0, -moveAmount, 0 )
        #m=Matrix.makeTranslation( 0, -moveAmount, 0 )
        #self.modelMatrix.data = m @ self.modelMatrix.data
    def moveleftG(self,moveAmount,rotateAmount):
        self.translate( -moveAmount, 0, 0 )
        #m=Matrix.makeTranslation( -moveAmount, 0, 0 )
        #self.modelMatrix.data = m @ self.modelMatrix.data
    def moverightG(self,moveAmount,rotateAmount):
        self.translate(  moveAmount, 0, 0 )
        #m=Matrix.makeTranslation(  moveAmount, 0, 0 )
        #self.modelMatrix.data = m @ self.modelMatrix.data
    def moveZG(self,moveAmount,rotateAmount):
        self.translate( 0, 0, -moveAmount )
        #m=Matrix.makeTranslation( 0, 0, -moveAmount )
        #self.modelMatrix.data = m @ self.modelMatrix.data
    def moveXG(self,moveAmount,rotateAmount):
        self.translate( 0, 0,  moveAmount )
        #m=Matrix.makeTranslation( 0, 0,  moveAmount )
        #self.modelMatrix.data = m @ self.modelMatrix.data

    def rotleftG(self,moveAmount,rotateAmount):
        self.rotateY( -rotateAmount )
        #m=Matrix.makeRotationZ( rotateAmount )
        #self.modelMatrix.data = m @ self.modelMatrix.data
    def rotrightG(self,moveAmount,rotateAmount):
        self.rotateY( rotateAmount )
        #m=Matrix.makeRotationZ( -rotateAmount )
        #self.modelMatrix.data = m @ self.modelMatrix.data
    def rotupG(self,moveAmount,rotateAmount):
        self.rotateX( -rotateAmount )
        #m=Matrix.makeRotationZ( rotateAmount )
        #self.modelMatrix.data = m @ self.modelMatrix.data
    def rotdownG(self,moveAmount,rotateAmount):
        self.rotateX( rotateAmount )
        #m=Matrix.makeRotationZ( -rotateAmount )
        #self.modelMatrix.data = m @ self.modelMatrix.data


        # LOCAL
    def moveupL(self,moveAmount,rotateAmount):
        self.lookAttachment.translate( 0, 0, -moveAmount )
        #m=Matrix.makeTranslation( 0,  moveAmount, 0 )
        #self.modelMatrix.data = self.modelMatrix.data @ m
    def movedownL(self,moveAmount,rotateAmount):
        self.lookAttachment.translate( 0, 0, moveAmount )
        #m=Matrix.makeTranslation( 0, -moveAmount, 0 )
        #self.modelMatrix.data = self.modelMatrix.data @ m
    def moveleftL(self,moveAmount,rotateAmount):
        self.lookAttachment.translate( 0, -moveAmount, 0 )
        #m=Matrix.makeTranslation( -moveAmount, 0, 0 )
        #self.modelMatrix.data = self.modelMatrix.data @ m
    def moverightL(self,moveAmount,rotateAmount):
        self.lookAttachment.translate( 0, moveAmount, 0 )
        #m=Matrix.makeTranslation(  moveAmount, 0, 0 )
        #self.modelMatrix.data = self.modelMatrix.data @ m

    def rotleftL(self,moveAmount,rotateAmount):
        self.lookAttachment.rotateY( -rotateAmount )
        #m=Matrix.makeRotationY( rotateAmount )
        #self.modelMatrix.data = self.modelMatrix.data @ m
    def rotrightL(self,moveAmount,rotateAmount):
        self.lookAttachment.rotateY( rotateAmount )
        #m=Matrix.makeRotationY( -rotateAmount )
        #self.modelMatrix.data = self.modelMatrix.data @ m
    def rotupL(self,moveAmount,rotateAmount):
        self.lookAttachment.rotateX( rotateAmount )
        #m=Matrix.makeRotationX( rotateAmount )
        #self.modelMatrix.data = self.modelMatrix.data @ m
    def rotdownL(self,moveAmount,rotateAmount):
        self.lookAttachment.rotateX( -rotateAmount )
        #m=Matrix.makeRotationX( -rotateAmount )
        #self.modelMatrix.data = self.modelMatrix.data @ m




