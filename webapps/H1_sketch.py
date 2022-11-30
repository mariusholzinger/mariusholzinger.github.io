# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math
#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 50
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation            

   #Define Grid
    gridY = 6
    gridX = 6
    gridZ = 6
   
    # Generate Coordinates
    coordinate = []
    for y in range(0,(gridY*2),2):
        for x in range(0,(gridX*2),2):
            for z in range(0,1+(gridZ*2),2):
                coordinate.append((x,y,z))
                #Set Parameter for Sphere
                sphe_params = {
                    "radius":0.15,
                    "wSegments":16,
                    "hSegments":8
                }
                sphe_params = Object.fromEntries(to_js(sphe_params))
                
                
                spheres = []

                geom = THREE.SphereGeometry.new( sphe_params.radius, sphe_params.wSegments, sphe_params.hSegments)
                geom.scale(0.25,0.25,0.25)
                geom.scale(1*z,1*z,1*z)
                color = THREE.Color.new(0,0.02*(y*y),1.0-(0.1*y))
                material = THREE.MeshBasicMaterial.new(color)
                material.color = color
                material.transparent = True
                material.opacity = 0.75
                sphe = THREE.Mesh.new( geom, material )
                spheres.append(sphe)

                line_material = THREE.LineBasicMaterial.new()
                line_material.color = THREE.Color.new(255,255,255)
                edges = THREE.EdgesGeometry.new( sphe.geometry )
                line = THREE.LineSegments.new( edges, line_material)
                scene.add( line )

                # Assign Coordinates
                sphe.position.x = x
                sphe.position.y = y
                sphe.position.z = z

                line.position.x = x
                line.position.y = y
                line.position.z = z
                
                
                scene.add( sphe )

                

                #geom.distanceToPoint()

                #sphe.scale()
    #scene.add(sphe)
    #print(coordinate)

    
    
    

   
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
    # USER INTERFACE
    # Set up GUI
    gui = window.dat.GUI.new()
    gui.add(sphe_params, 'radius', 0.15,5,0.2)
     
    gui.open()
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
def update_spheres():
    global sphe
            
            
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()