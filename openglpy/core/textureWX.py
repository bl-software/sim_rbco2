import sys
import os
import numpy as np
from OpenGL.GL import *
from PIL import Image


class Error(Exception): pass

def _find(pathname, matchFunc=os.path.isfile):
    for dirname in sys.path:
        candidate = os.path.join(dirname, pathname)
        if matchFunc(candidate):
            return candidate
    raise Error("Can't find file %s" % pathname)

def findFile(pathname):
    return _find(pathname)

def findDir(path):
    return _find(path, matchFunc=os.path.isdir)




class Texture(object):
    def __init__(self, fileName=None, properties={}):
        print('Texture WX')
        # reference of available texture from GPU
        self.textureRef= glGenTextures(1)

        # default property values
        self.properties= {
            'magFilter' : GL_LINEAR,
            'minFilter' : GL_LINEAR_MIPMAP_LINEAR,
            'wrap'      : GL_REPEAT
        }

        # overwrite default proerty values
        self.setProperties(properties)

        if fileName is not None:
            #print('syslpaht',sys.path)
            #print('fname=',fileName)
            self.loadImage(fileName)
            self.uploadData()

    # load image file
    def loadImage(self, fileName):
        #print('LI')
        #print(sys.path)
        #print(os.getcwd())
        foundFileName=findFile(fileName)
        #print('found=',foundFileName)
        #breakpoint()
#HERE:
#    https://importlib-resources.readthedocs.io/en/latest/using.html
#https://docs.python.org/3/library/pathlib.html
#https://stackoverflow.com/questions/10174211

        self.img= Image.open(foundFileName).convert('RGBA') # OpenGL reqs RGBA for texture below
        self.imageWidth= self.img.width
        self.imageHeight= self.img.height

    # set property values
    def setProperties(self, props):
        #print('setProperties')
        for name, data in props.items():
            if name in self.properties.keys():
                self.properties[name] = data
                #print(f'  {name}: {data}')
            else: # unknown property type
                raise Exception( f'Texture has not property with name: {name}' )


    # upload pixel data to GPU
    def uploadData(self):
        #print('textureWX: uploadData')
        #print(self.img)

        #seems numpy (or opengl) and pillow disagree about up and down
        self.img= self.img.transpose(Image.FLIP_TOP_BOTTOM)
        # store image dimensions
        width, height= self.img.size
        #print(f'  wid:{width} height:{height}')

        # convert image data to string buffer
        pixelData= np.array(list(self.img.getdata()), np.uint8)
#        pixelData=np.fliplr(pixelData)
#        pixelData=np.flipud(pixelData)
        #print('  pixData.size',pixelData.size)
        #print('  UD2')
        #breakpoint()

        # specify texture used by the following functions
        glBindTexture(GL_TEXTURE_2D, self.textureRef)
        #print('  UD3')

        # send pixel data to texture buffer
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA,
                width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixelData.tostring() )

        # generate mipmap image from uploaded pixel data
        glGenerateMipmap(GL_TEXTURE_2D)

        # specify technique for magnifying/minifying textrues.
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.properties['magFilter'] )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.properties['minFilter'] )
        # specify what happens to texture coordinates outside range [0,1]
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S    , self.properties['wrap']      )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T    , self.properties['wrap']      )

        # set default border color to white, important for rendering shadows
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1,1,1,1])


