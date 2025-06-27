from core.textureWX import Texture
import wx
from PIL import Image, ImageDraw, ImageFont

class TextTexture(Texture):
    def __init__(self,text=u'Hello, World!',
            systemFontName='Arial', fontFileName=None,
            fontSize=24,
            fontColor=(255,0,0,255),
            #backgroundColor=(55,55,55,55),
            backgroundColor=(0,0,0,0),
            transparent=False,
            imageWidth=None, imageHeight=None,
            alignHorizontal=0.0, alignVertical=0.0,
            imageBorderWidth=0, imageBorderColor=(0,0,0,255)):
        print('\n'*5,'TextTexture WX\n'*8)
        print(f'    fontSize={fontSize}')
        super().__init__()

#        f=ImageFont.truetype('fonts/InputSerifNarrow-BoldItalic.ttf', fontSize)
        # can override by loading font file
        if fontFileName is not None:
            print(f'    trying font {fontFileName}')
            f= ImageFont.truetype(fontFileName, fontSize)
        else:
            print(f'    FAILED getting default font')
            f=ImageFont.load_default(size=fontSize)

        print('text=',text)
        print(f'    argIW:{imageWidth},  argIH:{imageHeight}')

        # This is a bit crazy just to get the size of multiline, but ...
        # This doesn't work for multiline : left,top,right,bottom= f.getbbox(text)
        # Wrote loop, that didn't get spacing - 
        iJunk=Image.new('RGB',(0,0))
        dJunk=ImageDraw.Draw(iJunk)
        left,top,right,bottom= dJunk.multiline_textbbox((0,0),text,font=f)
        
        self.imageWidth= imageWidth
        self.imageHeight= imageHeight
        if not self.imageWidth:
            print(    'Calc r-l')
            self.imageWidth = right-left
        if not self.imageHeight:
            print(    'Calc b-t')
            self.imageHeight = bottom-top

        #self.imageHeight= self.imageHeight * 2
        print(f'textTextureWX: imageWidth {self.imageWidth}  imageHeight {self.imageHeight}') 

        # create surface to store image of text (with transparency channel by default)
#        self.surface= pygame.Surface( (self.imageWidth, self.imageHeight), pygame.SRCALPHA )
        #self.img= Image.new('RGBA', (self.imageWidth,self.imageHeight), backgroundColor)#(255,220,200,75))
        print('    backgroundColor',backgroundColor)
        self.img= Image.new('RGBA', (self.imageWidth,self.imageHeight), backgroundColor)#(255,220,200,75))

#        self.img= self.img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        midimgx= self.imageWidth//2
        midimgy= self.imageHeight//2
        d= ImageDraw.Draw( self.img, 'RGBA' )
        #d.text((0,0), text, font=f, fill=fontColor)#(0,255,0,250))#,font=myfont)
        print(f'    MIDS {midimgx}, {midimgy}')

        #lwid=5
        #red=(255,0,0)
        #yloc=1#midimgy
        #d.line((10,yloc, 100,yloc),fill=red  ,width=lwid)
        ##d.line((10,yloc, 100,yloc),fill=red  ,width=1)#lwid)
        ##yloc=1#midimgy
        ##d.line((100,yloc, 200,yloc),fill=red  ,width=lwid)
        ##yloc=2#midimgy
        ##d.line((200,yloc, 300,yloc),fill=red  ,width=lwid)
        ##yloc=3#midimgy
        ##d.line((300,yloc, 400,yloc),fill=red  ,width=lwid)
        ##yloc=4#midimgy
        ##d.line((400,yloc, 500,yloc),fill=red  ,width=lwid)

        #white=(255,255,255)
        #yloc=22#midimgy+20
        #d.line((10,yloc, 100,yloc),fill=white,width=lwid)

        #green=(5,255,5)
        #yloc=70#midimgy+20
        #d.line((10,yloc, 100,yloc),fill=green,width=lwid)

        d.text((midimgx,midimgy)   , text, anchor='mm', font=f, fill=fontColor)
        #d.text((midimgx,midimgy+10), text, anchor='mm', font=f, fill=fontColor)
        #d.text((5,5), text, anchor='mm', font=f, fill=fontColor)#(0,255,0,250))#,font=myfont)
#        d.text((0,0), text, font=f, fill=fontColor)#(0,255,0,250))#,font=myfont)
        #d.line( [(5,5), (100,100)], fill=(255,240,240,150), width=10)
        print("    POS",self.img.size)
        #self.img.show()
        # background color used when not transparent
#        if not transparent:
#            self.surface.fill( backgroundColor )
        # alignHorizontal, alignVertical are percentages measured from top-left
    #    cornerPoint= ( alignHorizontal * (self.imageWidth  - textWidth ),
    #                   alignVertical   * (self.imageHeight - textHeight) )

    #    destinationRectangle= fontSurface.get_rect( topleft=cornerPoint)

        # optional: add border
    #    if imageBorderWidth > 0:
    #        pygame.draw.rect( self.surface, imageBorderColor,
    #            [0,0, self.imageWidth, self.imageHeight], imageBorderWidth )
        
        # apply fontSurface to correct position on final surface
    #    self.surface.blit( fontSurface, destinationRectangle )
        self.uploadData()


