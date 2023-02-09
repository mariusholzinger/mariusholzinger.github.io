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
    back_color = THREE.Color.new("rgb(75,75,75)")
    scene.background = back_color
    fog_color = THREE.Color.new("rgb(0,0,0)")
    scene.fog = THREE.Fog.new(fog_color, 50,400)
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 1, 500)
    camera.position.set(-10,15,-15)
    scene.add(camera)

    #Set up Studio Scene
    groundGeo = THREE.PlaneGeometry.new(5000,5000)
    groundMat = THREE.MeshBasicMaterial.new ()
    groundMat.color = THREE.Color.new("rgb(50,50,50)")

    ground = THREE.Mesh.new(groundGeo, groundMat)
    ground.position.y = - 33
    ground.rotation.x = - math.pi / 2
    ground.receiveShadow = True
    scene.add( ground )

    
    #Lighting
    hemiLight = THREE.HemisphereLight.new( 0xffffff, 0x444444 )
    hemiLight.position.set( 0, 100, 0 )
    scene.add( hemiLight )

    dirLight = THREE.DirectionalLight.new( 0xffffff )
    dirLight.position.set( - 0, 40, 50 )
    dirLight.castShadow = True
    dirLight.shadow.camera.top = 50
    dirLight.shadow.camera.bottom = - 25
    dirLight.shadow.camera.left = - 25
    dirLight.shadow.camera.right = 25
    dirLight.shadow.camera.near = 0.1
    dirLight.shadow.camera.far = 200
    dirLight.shadow.mapSize.set( 1024, 1024 )
    scene.add( dirLight )

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
    global grid_params, gridX, gridY, gridZ, space

    grid_params = {
        "size" : 4,
        "space": 4,
    }
    grid_params = Object.fromEntries(to_js(grid_params))

    gridY = grid_params.size
    gridX = grid_params.size
    gridZ = grid_params.size

    space = grid_params.space
    spaceX = grid_params.space
    spaceZ = grid_params.space


    #Set Parameter for Sphere
    global sphe_params, spheres, sphe_lines

    spheres = []
    sphe_lines = []

    sphe_params = {
        "radius":0.15,
        "wSegments":16,
        "hSegments":8,
        "space": 3,
                }
    sphe_params = Object.fromEntries(to_js(sphe_params))
   

    
    # Generate Coordinates
    coordinate = []
    for y in range(0,(gridY),4):
        for x in range(0,(gridX),4):
            for z in range(0,1+(gridZ),4):
                coordinate.append((x,y,z))
                
                global material, line_material

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
                sphe_lines.append(line)
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

    
    
    

   
    
    
    #------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)
   
    # Set up GUI
    gui = window.dat.GUI.new()
    gui.add(sphe_params, 'radius', 0.15,5,0.2)
    #gui.add(grid_params, 'size', 2,8,1)
    #gui.add(grid_params, 'size', 6,10,1)
     
    gui.open()
   

    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
def update_spheres():
    global spheres, sphe_lines, material, line_material


    if len(spheres) != 0:
        if len(spheres) != sphe_params.radius:
            for sphe in spheres: scene.remove(sphe)
            for line in sphe_lines: scene.remove(line)

            spheres = []
            sphe_lines = []
    
            coordinate = []
            for y in range(0,(gridY*2),2):
                for x in range(0,(gridX*2),2):
                    for z in range(0,1+(gridZ*2),2):
                        coordinate.append((x,y,z))
                                        
                        

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
                        sphe_lines.append(line)
                        scene.add( line )

                        # Assign Coordinates
                        sphe.position.x = x
                        sphe.position.y = y
                        sphe.position.z = z

                        line.position.x = x
                        line.position.y = y
                        line.position.z = z
                        
                        
                        scene.add( sphe )

    
            
            
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_spheres()
    controls.update

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