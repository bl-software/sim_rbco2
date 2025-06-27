
#! /usr/bin/env python

from OpenGL.GL import *

import wx
import wx.glcanvas as wxgl
if False:
  import ixmwn_glcontext as ixgl
else:
  import wx.glcanvas as ixgl
import numpy as np
import sys

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
    outColor = vec4(0.2, 0.3, 1.0, 1.0);
}
"""

class Frame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, title="Blue triangle on dark green background", size=(640,480))
    canvasAttrs = ixgl.GLAttributes()
    canvasAttrs.PlatformDefaults().MinRGBA(1, 1, 1, 0).DoubleBuffer().Depth(1).EndList()
    self.glcv = ixgl.GLCanvas(self, canvasAttrs)
    contextAttrs = ixgl.GLContextAttrs()
    contextAttrs.CoreProfile().OGLVersion(4, 1).Robust().ResetIsolation().EndList()
    self.glctx = ixgl.GLContext(self.glcv, ctxAttrs=contextAttrs)
    self.Bind(wx.EVT_PAINT, self.on_paint)
    self.Bind(wx.EVT_SIZE, self.on_size)
    self._must_init = True

  def InitGL(self):
    # Vertex Input
    ## Vertex Array Objects
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    ## Vertex Buffer Object
    vbo = glGenBuffers(1) # Generate 1 buffer

    vertices = np.array([0.0,  0.5, 1.0, -0.5, -0.5, -0.5], dtype=np.float32)

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
    glUseProgram(shaderProgram)

    # Making the link between vertex data and attributes
    posAttrib = glGetAttribLocation(shaderProgram, "position")
    glEnableVertexAttribArray(posAttrib)
    glVertexAttribPointer(posAttrib, 2, GL_FLOAT, GL_FALSE, 0, None)

  def actual_on_size(self):
    size = self.glcv.GetClientSize()
    self.glcv.SetCurrent(self.glctx)
    glViewport(0, 0, size[0], size[1])
    self.actual_draw()
  def actual_draw(self):
    self.glcv.SetCurrent(self.glctx)
    glClearColor(0.0, 0.2, 0.0, 1.0)
    #Clear the screen to dark green
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    self.glcv.SwapBuffers()
  def on_size(self, event):
    if self.glctx.IsOK():
      wx.CallAfter(self.actual_on_size)   # CallAfter necessary!
    event.Skip()
  def on_paint(self, event):
    if not self.glctx.IsOK():
      event.Skip()
      return
    if self._must_init:
      self._must_init = False
      self.glcv.SetCurrent(self.glctx)
      self.InitGL()
    self.actual_draw()
    event.Skip()

app = wx.App()
frame = Frame()
frame.Show()
app.MainLoop()
