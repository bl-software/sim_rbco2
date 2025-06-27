from OpenGL.GL import *

class OpenGLUtils(object):
    @staticmethod
    def initializeShader(shaderCode, shaderType):
        # specify required OpenGL/GLSL version
        #print(shaderCode.strip()[0:10])
        #shaderCode= '#version 330\n' + shaderCode

        # create empty shader obj and return reference
        shaderRef= glCreateShader(shaderType)

        #store source code in shader
        glShaderSource(shaderRef, shaderCode)

        #compile
        glCompileShader(shaderRef)

        # check
        compileSuccess= glGetShaderiv(shaderRef, GL_COMPILE_STATUS)
        #if not compileSuccess:
        #    errorMessage= glGetShaderInfoLog(shaderRef)
        #    glDeleteShader(shaderRef)
        #    errorMessage= '\n' + errorMessage.decode('utf-8')
        #    raise Exception(errorMessage)
        errorMessage= glGetShaderInfoLog(shaderRef)
        print('ShadercompileInfoLog:',errorMessage)
        if not compileSuccess:
            print('  NOT compileSuccess')
            glDeleteShader(shaderRef)
        #    errorMessage= '\n' + errorMessage.decode('utf-8')
        #    raise Exception(errorMessage)

        return shaderRef

    @staticmethod
    def initializeProgram(vertexShaderCode,fragmentShaderCode):
        print('Init vertexShader...')
        vertexShaderRef=   OpenGLUtils.initializeShader( vertexShaderCode  , GL_VERTEX_SHADER   )
        print('Init fragmentShader...')
        fragmentShaderRef= OpenGLUtils.initializeShader( fragmentShaderCode, GL_FRAGMENT_SHADER )
        
        # create empty program
        print('Create Prog...')
        programRef= glCreateProgram()

        # attach previously compiled shader programs
        print('Attach...')
        glAttachShader(programRef, vertexShaderRef)
        glAttachShader(programRef, fragmentShaderRef)

        # link vertex shader to frag shader
        print('Link...')
        glLinkProgram(programRef)

        linkSuccess= glGetProgramiv(programRef, GL_LINK_STATUS)
        print(f'linkSuccess={linkSuccess}')
        if not linkSuccess:
            errorMessage= glGetProgramInfoLog(programRef)
            print('-- errorMessage', len(errorMessage), errorMessage)
            glDeleteProgram(programRef)
            #errorMessage= '\n' + errorMessage.decode('utf-8')
            raise Exception(errorMessage)

        return programRef

    @staticmethod
    def printSystemInfo():
        print('  Vendor: ' + glGetString(GL_VENDOR).decode('utf-8') )
        print('  Renderer: ' + glGetString(GL_RENDERER).decode('utf-8') )
        print('  OGLVersion: ' + glGetString(GL_VERSION).decode('utf-8') )
        print('  GLSLVersion: ' + glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8') )
