from material.material import Material
from OpenGL.GL import *
class LambertMaterial(Material):
    def __init__(self, texture=None, properties={}, bumpTexture=None):

        vertexShaderCode='''
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        in vec3 vertexNormal;
        out vec3 position;
        out vec2 UV;
        out vec3 normal;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
            position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            UV= vertexUV;
            normal = normalize( mat3(modelMatrix) * vertexNormal );
        }
        '''
        fragmentShaderCode='''
        struct Light
        {
            // 1=ABIENT, 2=DIRECTIONAL, 3=POINT
            int lightType;
            // used by all lights
            vec3 color;
            // used by directional lights
            vec3 direction;
            // used by point lights
            vec3 position;
            vec3 attenuation;
        };
        uniform Light light0;
        uniform Light light1;
        uniform Light light2;
        uniform Light light3;

        vec3 lightCalc(Light light, vec3 pointPosition, vec3 pointNormal)
        {
            float ambient = 0;
            float diffuse = 0;
            float specular = 0;
            float attenuation = 1;
            vec3 lightDirection = vec3(0,0,0);

            if (light.lightType == 1) // ambient light
            {
                ambient = 1;
            }
            else if (light.lightType == 2) // directional light
            {
                lightDirection = normalize(light.direction);
            }
            else if (light.lightType == 3) // point light
            {
                lightDirection = normalize(pointPosition - light.position);
                float distance = length(light.position - pointPosition);
                attenuation = 1.0 / ( light.attenuation[0] +
                                      light.attenuation[1] * distance +
                                      light.attenuation[2] * distance * distance);
            }
            if ( light.lightType > 1) // directional or point light
            {
                pointNormal = normalize(pointNormal);
                diffuse = max( dot(pointNormal, -lightDirection), 0.0 );
                diffuse *= attenuation;
            }
            return light.color * (ambient + diffuse + specular);
        }

        uniform bool useBumpTexture;
        uniform sampler2D bumpTexture;
        uniform float bumpStrength;


        uniform vec3 baseColor;
        uniform bool useTexture;
        uniform sampler2D texture;
        in vec3 position;
        in vec2 UV;
        in vec3 normal;
        out vec4 fragColor;
        void main()
        {
            vec4 color = vec4(baseColor, 1.0);
            if ( useTexture )
                color *= texture2D( texture, UV );
            // calculate total effect of lights on color
            vec3 bNormal = normal;
            if (useBumpTexture)
                bNormal += bumpStrength * vec3( texture2D(bumpTexture, UV));
            vec3 total = vec3(0,0,0);
            total += lightCalc( light0, position, bNormal );
            total += lightCalc( light1, position, bNormal );
            total += lightCalc( light2, position, bNormal );
            total += lightCalc( light3, position, bNormal );
            color *= vec4( total, 1 );
            fragColor = color;
        }
        '''

        super().__init__(vertexShaderCode, fragmentShaderCode)

        self.addUniform('vec3' ,  'baseColor', [1.0,1.0,1.0] )
        self.addUniform('Light',     'light0', None          )
        self.addUniform('Light',     'light1', None          )
        self.addUniform('Light',     'light2', None          )
        self.addUniform('Light',     'light3', None          )
        self.addUniform('bool' , 'useTexture', 0             )

        if texture == None:
            self.addUniform('bool'     , 'useTexture', False                  )
        else:
            self.addUniform('bool'     , 'useTexture', True                   )
            self.addUniform('sampler2D', 'texture'   , [texture.textureRef,1] )

        if bumpTexture == None:
            self.addUniform('bool'     , 'useBumpTexture', False)
        else:
            self.addUniform('bool'     , 'useBumpTexture', True                        )
            self.addUniform('sampler2D', 'bumpTexture'   , [bumpTexture.textureRef, 2] )
            self.addUniform('float'    , 'bumpStrength'  , 1.0                         )

        # uniforms to be added
        self.locateUniforms()

        # render both sides?
        self.settings['doubleside'] = True
        # render triangles as wireframe
        self.settings['wireframe'] = False
        # line thickness for wireframe rendering
        self.settings['lineWidth'] = 1

        self.setProperties(properties)

    def updateRenderSettings(self):
        if self.settings['doubleside']:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings['wireframe']:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings['lineWidth'])

