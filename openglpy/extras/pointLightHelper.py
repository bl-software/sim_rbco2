from geometry.sphereGeometry import SphereGeometry
from material.surfaceMaterial import SurfaceMaterial
from core.mesh import Mesh

class PointLightHelper(Mesh):
    def __init__(self, pointLight, size=0.1, lineWidth=1):
        color= pointLight.color
        geometry= SphereGeometry(radius=size, radiusSegments=4, heightSegments=2)
        material=SurfaceMaterial({
            'baseColor' : color,
            'wireframe' : True,
            'doubleSide':True,
            'lineWidth': lineWidth
        })
        super().__init__(geometry,material)

