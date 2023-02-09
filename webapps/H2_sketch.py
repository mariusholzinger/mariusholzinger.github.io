# Import javascript modules
from js import THREE, window, document, Object, console
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
    back_color = THREE.Color.new(0.9,0.9,0.9)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 3000)
    camera.position.z = 800
    camera.position.y = 1000
    camera.position.x = 0
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 

    global def_params
    def_params = {

        "size": 5,
    }

    def_params = Object.fromEntries(to_js(def_params))
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
    my_axiom_system = system(0, def_params.size, "X")

    console.log(my_axiom_system)

    draw_system((my_axiom_system), THREE.Vector3.new(0,0,0))


    my_axiom_system2 = system2(0, def_params.size, "X")

    

    console.log(my_axiom_system2)

    draw_system2((my_axiom_system2), THREE.Vector3.new(0,0,0))

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    """ gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(def_params, 'size', 2,10,1)
    param_folder.open()"""
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Define RULES in a function which takes one SYMBOL and applies rules generation
def generate(symbol):
    if symbol == "X":
        return "FFF[+X]F[-X]+F[+X]F[-X]+X"
    elif symbol == "F":
        return "FF"
    elif symbol == "+":
        return "+"
    elif symbol == "-":
        return "-"
    elif symbol == "[":
        return "["
    elif symbol == "]":
        return "]"
# A recursive fundtion, which taken an AXIOM as an inout and runs the generate function for each symbol

def system(current_iteration, max_iterations, axiom):
    current_iteration += 1
    new_axiom = ""
    for symbol in axiom:
        new_axiom += generate(symbol)
    if current_iteration >= max_iterations:
        return new_axiom
    else:
        return system(current_iteration, max_iterations, new_axiom)

def draw_system(axiom, start_pt):
    move_vec = THREE.Vector3.new(0,5,0)
    old_states = []
    old_move_vecs = []
    lines = []

    for symbol in axiom:
        if symbol == "F" or symbol == "X":
            old = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = new_pt.add(move_vec)
            line = []
            line.append(old)
            line.append(new_pt)
            lines.append(line)

            start_pt = new_pt

        elif symbol == "+": 
            move_vec.applyAxisAngle(THREE.Vector3.new(0,1,0), math.pi/6)
            move_vec.applyAxisAngle(THREE.Vector3.new(0,1,-1), math.pi/9)

        elif symbol == "-":
            move_vec.applyAxisAngle(THREE.Vector3.new(1,0,1), -math.pi/6)
        
        elif symbol == "[":
            old_state = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            old_move_vec = THREE.Vector3.new(move_vec.x, move_vec.y, move_vec.z)
            old_states.append(old_state)
            old_move_vecs.append(old_move_vec)

        elif symbol == "]":
            start_pt = THREE.Vector3.new(old_states[-1].x, old_states[-1].y, old_states[-1].z)
            move_vec = THREE.Vector3.new(old_move_vecs[-1].x, old_move_vecs[-1].y, old_move_vecs[-1].z)
            old_states.pop(-1)
            old_move_vecs.pop(-1)



    for points in lines:
        line_geom = THREE.BufferGeometry.new()
        points = to_js(points)
        
        console.log(points)

        line_geom.setFromPoints( points )
        color = THREE.Color.new(255,0,0)
        material = THREE.LineBasicMaterial.new(color)
        material.color = color
        vis_line = THREE.Line.new( line_geom, material )

        
        global scene
        scene.add(vis_line)

#-------------------------------------------------------------------------------------------------------------

def system2(current_iteration, max_iterations, axiom):
    current_iteration += 1
    new_axiom = ""
    for symbol in axiom:
        new_axiom += generate(symbol)
    if current_iteration >= max_iterations:
        return new_axiom
    else:
        return system2(current_iteration, max_iterations, new_axiom)

def draw_system2(axiom, start_pt):
    move_vec = THREE.Vector3.new(0,5,0)
    old_states = []
    old_move_vecs = []
    lines = []

    for symbol in axiom:
        if symbol == "F" or symbol == "X":
            old = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = new_pt.add(move_vec)
            line = []
            line.append(old)
            line.append(new_pt)
            lines.append(line)

            start_pt = new_pt

        elif symbol == "+": 
            move_vec.applyAxisAngle(THREE.Vector3.new(0,1,0), -math.pi/6)
            move_vec.applyAxisAngle(THREE.Vector3.new(0,1,-1), -math.pi/9)

        elif symbol == "-":
            move_vec.applyAxisAngle(THREE.Vector3.new(1,0,1), math.pi/6)
           

        
        elif symbol == "[":
            old_state = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            old_move_vec = THREE.Vector3.new(move_vec.x, move_vec.y, move_vec.z)
            old_states.append(old_state)
            old_move_vecs.append(old_move_vec)

        elif symbol == "]":
            start_pt = THREE.Vector3.new(old_states[-1].x, old_states[-1].y, old_states[-1].z)
            move_vec = THREE.Vector3.new(old_move_vecs[-1].x, old_move_vecs[-1].y, old_move_vecs[-1].z)
            old_states.pop(-1)
            old_move_vecs.pop(-1)



    for points in lines:
        line_geom = THREE.BufferGeometry.new()
        points = to_js(points)
        
        console.log(points)
        global vis_line
        line_geom.setFromPoints( points )
        color = THREE.Color.new(255,0,0)
        material = THREE.LineBasicMaterial.new(color)
        material.color = color
        vis_line = THREE.Line.new( line_geom, material )

        
        global scene
        scene.add(vis_line)

def onSliderChange():
    global max_iterations
    max_iterations = def_params.size
    render()
    

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    #controls.update()
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