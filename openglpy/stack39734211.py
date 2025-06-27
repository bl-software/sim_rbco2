import wx
from wx import glcanvas
from OpenGL.GL import *
#from OpenGL.GLU import *
#from OpenGL.GLUT import *
from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.fragment_shader import *
from OpenGL.GL.ARB.vertex_shader import *
import numpy as np

vertexSource = """
#version 410
in vec2 position;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""
fragmentSource = """
#version 410
out vec4 outColor;
void main()
{
    outColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        #glcanvas.GLCanvas.__init__(self, parent)#, -1, size=(640, 480))
        glcanvas.GLCanvas.__init__(self, parent, id=wx.ID_ANY, size=(640, 480))
        self.init = False
        # Dale added
        ctxAttrs = wx.glcanvas.GLContextAttrs()
        ctxAttrs.CoreProfile().OGLVersion(4, 1).Robust().ResetIsolation().EndList()
        self.context = glcanvas.GLContext(self,ctxAttrs=ctxAttrs) 
        #print('OK: ', self.context.IsOK() )
        #print('OK: ', glGetString(GL_VERSION))#self.context.IsOK() )


        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
 
    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.
    def OnSize(self, event):
        #print('\nE OnSize')
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        #print('DoSetViewport')
        size = self.size = self.GetClientSize() * self.GetContentScaleFactor()
        #print('VERSION DSV1: ', glGetString(GL_VERSION))#self.context.IsOK() )
        if self.IsShownOnScreen():
            self.SetCurrent(self.context)
            glViewport(0, 0, size.width, size.height)
            #print('VERSION DSV2: ', glGetString(GL_VERSION))#self.context.IsOK() )



    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        #print('VERSION OP1: ', glGetString(GL_VERSION))#self.context.IsOK() )
        if self.IsShownOnScreen():
            #print('VERSION OP2: ', glGetString(GL_VERSION))#self.context.IsOK() )
            self.SetCurrent(self.context)
            if not self.init:
                self.InitGL()
                self.init = True
            self.OnDraw()

    def InitGL(self):

        # Vertex Input
        ## Vertex Array Objects
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        ## Vertex Buffer Object
        vbo = glGenBuffers(1) # Generate 1 buffer

        vertices = np.array([0.0,  0.5, 0.5, -0.5, -0.5, -0.5], dtype=np.float32)

        ## Upload data to GPU
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Compile shaders and combining them into a program
        ## Create and compile the vertex shader
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, vertexSource)
        glCompileShader(vertexShader)

        ## Create and compile the fragment shader
        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, fragmentSource)
        glCompileShader(fragmentShader)

        ## Link the vertex and fragment shader into a shader program
        shaderProgram = glCreateProgram()
        glAttachShader(shaderProgram, vertexShader)
        glAttachShader(shaderProgram, fragmentShader)
        glBindFragDataLocation(shaderProgram, 0, "outColor")
        glLinkProgram(shaderProgram)
        
        linkSuccess= glGetProgramiv(shaderProgram, GL_LINK_STATUS)
        print(f'linkSuccess={linkSuccess}')
        if not linkSuccess:
            errorMessage= glGetProgramInfoLog(shaderProgram)
            print('eeror', errorMessage)
            glDeleteProgram(shaderProgram)
            #errorMessage= '\n' + errorMessage.decode('utf-8')
            raise Exception(errorMessage)

        glUseProgram(shaderProgram)

        # Making the link between vertex data and attributes
        posAttrib = glGetAttribLocation(shaderProgram, "position")
        glEnableVertexAttribArray(posAttrib)
        glVertexAttribPointer(posAttrib, 2, GL_FLOAT, GL_FALSE, 0, None)

    def OnDraw(self):
        # Set clear color
        glClearColor(0.0, 0.0, 0.0, 1.0)
#Clear the screen to black
        glClear(GL_COLOR_BUFFER_BIT)

        # draw six faces of a cube
        glDrawArrays(GL_TRIANGLES, 0, 3)

        self.SwapBuffers()

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Hello World", size=(640,480))
        canvas = OpenGLCanvas(self)

app = wx.App()
frame = Frame()
frame.Show()
app.MainLoop()
