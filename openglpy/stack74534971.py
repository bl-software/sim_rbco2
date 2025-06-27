
#!/usr/bin/env python

# Python ---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---
import os

# https://github.com/Amulet-Team/Amulet-Map-Editor/issues/247   (see Cebtenzzre)
# The following line addresses a wxPython 4.1.1 issue
os.environ['PYOPENGL_PLATFORM'] = 'egl'

# wxPython -+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---
import wx
from wx import glcanvas

# PyPi -+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---
import numpy    as np
from OpenGL.GL  import *

# My Files -+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---

# Shaders --+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---
vs = """
#version 330 core
layout (location = 0) in vec3 aPos ;

void main () {
    gl_Position = vec4 (aPos.x, aPos.y, aPos.z, 1.0) ;
}
"""

fs = """
#version 330 core
out vec4 FragColor ;

void main () {
    FragColor = vec4 (1.0f, 0.5f, 0.2f, 1.0f) ;
}
"""

#---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---
class View (glcanvas.GLCanvas):
    def __init__ (self, parent):
        cnvsAttr = glcanvas.GLAttributes ()      # Set the canvas attributes
        cnvsAttr.PlatformDefaults ().MinRGBA (8, 8, 8, 8).DoubleBuffer ().Depth (24).Stencil (8).EndList ()
        super ().__init__ (parent, cnvsAttr)
   
        self.context = glcanvas.GLContext (self)

        self.Bind (wx.EVT_SIZE, self.on_size)
        self.Bind (wx.EVT_PAINT, self.on_draw)

    def on_draw (self, event):
        if self.IsShownOnScreen ():
            result = self.SetCurrent (self.context)
            #print ('\n', result, '\n')                                          #x

            vShader = glCreateShader (GL_VERTEX_SHADER)
            glShaderSource (vShader, vs)
            glCompileShader (vShader)
            if glGetShaderiv (vShader, GL_COMPILE_STATUS) != GL_TRUE:
                print (f"SHADER COMPILER ERROR: Shader index {vShader} did not compile")
                print (glGetShaderInfoLog (vShader))


            fShader = glCreateShader (GL_FRAGMENT_SHADER)
            glShaderSource (fShader, fs)
            glCompileShader (fShader)
            if glGetShaderiv (fShader, GL_COMPILE_STATUS) != GL_TRUE:
                print (f"SHADER COMPILER ERROR: Shader index {fShader} did not compile")
                print (glGetShaderInfoLog (fShader))


            program = glCreateProgram ()
            glAttachShader (program, vShader)
            glAttachShader (program, fShader)
            glLinkProgram (program)
            if glGetProgramiv (program, GL_LINK_STATUS) != GL_TRUE:
                print (f"PROGRAM COMPILER ERROR: Program index {program} did not compile")
                print (glGetProgramInfoLog (program))


            glDeleteShader (vShader)
            glDeleteShader (fShader)

            ####################################################################
            VAO = glGenVertexArrays (1)     # This MUST precede VBO creation
            glBindVertexArray (VAO)

            vertices = np.array ([-0.5, -0.5, 0.0,
                                   0.5, -0.5, 0.0,
                                   0.0,  0.5, 0.0], dtype = np.float32)

            VBO = glGenBuffers (1)
            glBindBuffer (GL_ARRAY_BUFFER, VBO)
            glBufferData (GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

            glVertexAttribPointer (0, 3, GL_FLOAT, GL_FALSE, 0, 0)
            glEnableVertexAttribArray (0)

            glClearColor (0.25, 0.25, 0.25, 1.0)
            glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glUseProgram (program)
            glBindVertexArray (VAO)
            glDrawArrays (GL_TRIANGLES, 0, 3)
            glBindVertexArray (0)

            self.SwapBuffers ()
            self.Refresh ()


    def on_size (self, event):
        size = event.GetSize ()
        glViewport (0, 0, size.x, size.y)


#---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---
class stub_5a (wx.Frame):
    def __init__ (self):
        super ().__init__ (None)
        self.SetTitle ("stub_5a ()")
        self.SetClientSize ((400, 300))

        panel = wx.Panel (self)
        sizer = wx.BoxSizer (wx.VERTICAL)

        self.View = View (panel)

        sizer.Add (self.View, 1, wx.ALL | wx.EXPAND)
        panel.SetSizer (sizer)


#---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---
if __name__ == '__main__':
    app = wx.App (False)
    frame = stub_5a ()
    frame.Centre (wx.BOTH)
    frame.Show ()
    app.MainLoop ()

#the environment for the above code is:
#
#        OS: Linux (5.4.0-132-generic)    (Ubuntu 20.04)
#    Python: 3.8.10
#  wxPython: 4.1.1 gtk3 (phoenix) wxWidgets 3.1.5
#  PyOpenGL: 3.1.6
#     Numpy: 1.22.4
#    Pillow: 9.1.1
#   SQLite3: 3.31.1
