#!/usr/bin/env python
import os
import sys
from math import pi, sin, cos

import wx
from wx import glcanvas

# The Python OpenGL package can be found at
# http://PyOpenGL.sourceforge.net/
from OpenGL.GL import *
from OpenGL.GLU import *


class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        print(f'MyCanvasBase: parent={parent}')
        glcanvas.GLCanvas.__init__(self, parent, -1, size=[640,640])
        self.init = False
        self.context = glcanvas.GLContext(self)

        # Initial mouse position.
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.Bind(wx.EVT_SIZE , self.OnSize )
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown  )
        self.Bind(wx.EVT_LEFT_UP  , self.OnMouseUp    )
        self.Bind(wx.EVT_MOTION   , self.OnMouseMotion)


    def OnEraseBackground(self, event):
        pass  # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize() * self.GetContentScaleFactor()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        print('OP')
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, event):
        print('Down')
        if self.HasCapture():
            self.ReleaseMouse()
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = event.GetPosition()
        print('DownXY:',self.x, self.y)

    def OnMouseUp(self, event):
        print('Up')
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMouseMotion(self, event):
        print('Mot',end='')
        dr= event.Dragging()
        lid= event.LeftIsDown()
        print(f'Mot Drag>{dr}<  LIsDown:{lid}  E:{event} C:{self}')
        if dr and lid:
        #if event.Dragging() and event.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = event.GetPosition()
            print(f'  x,y:{self.x:0.2f},{self.y:0.2f}')
            self.Refresh(False)

class ConeCanvas(MyCanvasBase):
    def InitGL( self ):
        glMatrixMode(GL_PROJECTION)
        # Camera frustrum setup.
        glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)
        glMaterial(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterial(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterial(GL_FRONT, GL_SPECULAR, [1.0, 0.0, 1.0, 1.0])
        glMaterial(GL_FRONT, GL_SHININESS, 50.0)
        glLight(GL_LIGHT0, GL_AMBIENT, [0.0, 1.0, 0.0, 1.0])
        glLight(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLight(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glLight(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Position viewer.
        glMatrixMode(GL_MODELVIEW)
        # Position viewer.
        glTranslatef(0.0, 0.0, -2.0);


    def OnDraw(self):
        # Clear color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Use a fresh transformation matrix.
        glPushMatrix()
        # Position object.
        ## glTranslate(0.0, 0.0, -2.0)
        glRotate(30.0, 1.0, 0.0, 0.0)
        glRotate(30.0, 0.0, 1.0, 0.0)

        glTranslate(0, -1, 0)
        glRotate(250, 1, 0, 0)

        glEnable(GL_BLEND)
        glEnable(GL_POLYGON_SMOOTH)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0.5, 0.5, 1.0, 0.5))
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 1.0)
        glShadeModel(GL_FLAT)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        quad = gluNewQuadric()
        base = .5
        top = 0.0
        height = 1.0
        slices = 16
        stacks = 16
        # stacks = 0
        if stacks:
            # This is the premade way to make a cone.
            gluCylinder(quad, base, top, height, slices, stacks)
        else:
            # Draw cone open ended without glu.
            tau = pi * 2
            glBegin(GL_TRIANGLE_FAN)
            centerX, centerY, centerZ = 0.0, 0.0, height
            glVertex3f(centerX, centerY, centerZ)  # Center of circle.
            centerX, centerY, centerZ = 0.0, 0.0, 0.0
            for i in range(slices + 1):
                theta = tau * float(i) / float(slices)  # Get the current angle.
                x = base * cos(theta)  # Calculate the x component.
                y = base * sin(theta)  # Calculate the y component.
                glVertex3f(x + centerX, y + centerY, centerZ)  # Output vertex.
            glEnd()

        glPopMatrix()
        glRotatef((self.y - self.lasty), 0.0, 0.0, 1.0);
        glRotatef((self.x - self.lastx), 1.0, 0.0, 0.0);
        # Push into visible buffer.
        self.SwapBuffers()

if __name__ == '__main__':
    print('in __main__')
    #from wxTestConeOnly import ConeCanvas
    #from testfiles.test3 import Test
    #from test3 import Test
    #from testfiles.test46 import Test
    app = wx.App()
    frame = wx.Frame( None, title="WORKS", size=(640,640))
    #canvas = ConeCanvas(frame)
    panel= wx.Panel(frame, wx.ID_ANY, size=(640,640))
    panel.SetAutoLayout(True)

    canvas = ConeCanvas(panel)
    #canvas = Test( panel ).run()
    #canvas = BiCon( frame ).run()
    frame.Show()
    #print('INSP\n'*10)
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


