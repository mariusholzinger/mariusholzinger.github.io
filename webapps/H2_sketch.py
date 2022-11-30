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
    my_axiom_system = system(0, 3, "X")

    console.log(my_axiom_system)

    draw_system((my_axiom_system), THREE.Vector3.new(0,0,0))


    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    """gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'size', 10,100,1)
    param_folder.add(geom1_params, 'x', 2,100,1)
    param_folder.add(geom1_params, 'rotation', 0,180)
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

        material = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
        vis_line = THREE.Line.new( line_geom, material )

        
        global scene
        scene.add(vis_line)


'''# FLIP---Define RULES in a function which takes one SYMBOL and applies rules generation
def generate(fsymbol):
    if fsymbol == "X":
        return "FFF[-X]F[+X]-F[-X]F[+X]-X"
    elif fsymbol == "F":
        return "FF"
    elif fsymbol == "+":
        return "+"
    elif fsymbol == "-":
        return "-"
    elif fsymbol == "[":
        return "["
    elif fsymbol == "]":
        return "]"
# A recursive fundtion, which taken an AXIOM as an inout and runs the generate function for each symbol
def system(current_iterationf, max_iterationsf, axiomf):
    current_iterationf += 1
    new_axiomf = ""
    for fsymbol in axiomf:
        new_axiomf += generate(fsymbol)
    if current_iterationf >= max_iterationsf:
        return new_axiomf
    else:
        return system(current_iterationf, max_iterationsf, new_axiomf)

def draw_system(axiomf, start_ptf):
    move_vecf = THREE.Vector3.new(0,5,0)
    old_statesf = []
    old_move_vecsf = []
    linesf = []

    for fsymbol in axiomf:
        if fsymbol == "F" or fsymbol == "X":
            oldf = THREE.Vector3.new(start_ptf.x, start_ptf.y, start_ptf.z)
            new_ptf = THREE.Vector3.new(start_ptf.x, start_ptf.y, start_ptf.z)
            new_ptf = new_ptf.add(move_vecf)
            linef = []
            linef.append(oldf)
            linef.append(new_ptf)
            linesf.append(linef)

            start_ptf = new_ptf

        elif fsymbol == "+": 
            move_vecf.applyAxisAngle(THREE.Vector3.new(0,1,0), -math.pi/6)
            move_vecf.applyAxisAngle(THREE.Vector3.new(0,1,-1), -math.pi/9)

        elif fsymbol == "-":
            move_vecf.applyAxisAngle(THREE.Vector3.new(1,0,1), math.pi/6)
        
        elif fsymbol == "[":
            old_statef = THREE.Vector3.new(start_ptf.x, start_ptf.y, start_ptf.z)
            old_move_vecf = THREE.Vector3.new(move_vecf.x, move_vecf.y, move_vecf.z)
            old_statesf.append(old_statef)
            old_move_vecsf.append(old_move_vecf)

        elif fsymbol == "]":
            start_ptf = THREE.Vector3.new(old_statesf[-1].x, old_statesf[-1].y, old_statesf[-1].z)
            move_vecf = THREE.Vector3.new(old_move_vecsf[-1].x, old_move_vecsf[-1].y, old_move_vecsf[-1].z)
            old_statesf.pop(-1)
            old_move_vecsf.pop(-1)



    for fpoints in linesf:
        fline_geom = THREE.BufferGeometry.new()
        fpoints = to_js(fpoints)
        
        console.log(fpoints)

        fline_geom.setFromPoints( fpoints )

        fmaterial = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
        fvis_line = THREE.Line.new( fline_geom, fmaterial )

        
        global scene
        scene.add(fvis_line)'''

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