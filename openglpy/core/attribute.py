from OpenGL.GL import *
import numpy

class Attribute(object):
    def __init__(self,dataType,data):
        # type of elements
        # int | float | vec2 | vec3 | vec4
        self.dataType= dataType

        # array of data to be stored in buffer
        self.data= data

        # ref to avail buffer from GPU
        self.bufferRef= glGenBuffers(1)

        # upload data immediately
        self.uploadData()

    # upload this data to GPU Buffer
    def uploadData(self):
        # convert data to numpy array format
        #   convert numbers to 32 bit floats
        data= numpy.array(self.data).astype( numpy.float32 )

        # select buffer used by following funcs
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)

        # store data in cur bound buffer
        glBufferData( GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    # assoc variable in program with this buffer
    def associateVariable(self, programRef, variableName):
        # get ref
        variableRef= glGetAttribLocation(programRef,variableName)
        if variableRef == -1: # exit
            return

        # select buff
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)

        # spec how data will be read
        if self.dataType == "int":
            glVertexAttribPointer( variableRef, 1, GL_INT, False, 0, None)
        elif self.dataType == "float":
            glVertexAttribPointer( variableRef, 1, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec2":
            glVertexAttribPointer( variableRef, 2, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec3":
            glVertexAttribPointer( variableRef, 3, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec4":
            glVertexAttribPointer( variableRef, 4, GL_FLOAT, False, 0, None)
        else:
            raise Exception('(attribute.py) Attribute ' + variableName + ' has unknown type ' + self.dataType )

        # indicate data will be streamed to this var
        glEnableVertexAttribArray( variableRef )

