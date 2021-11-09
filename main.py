# public imports
import pygame
import easygui
from math import sin, cos, sqrt
from operator import itemgetter
from copy import deepcopy

# local imports
import objects
from colors import *
from objects import *
from matrix import *
from classes import *
from load_obj import *
from functions import *


# ---- PRE LOOP ----

# pre-register variables
prev_mouse = (0, 0)
right_click = False
left_click = False

# pygame window sizes
window_width = 1000
window_height = 700

pygame.init() # initializes pygame

# pygame window setup
pygame.display.set_caption("Cubo 3D") # title for the pygame window
display = pygame.display.set_mode((window_width, window_height)) # creates the pygame window and the size of it

# pygame clock setup
clock = pygame.time.Clock() # sets the clock variable

# fonts
freesansbold = pygame.font.Font('freesansbold.ttf', 20)
freesansbold_small = pygame.font.Font('freesansbold.ttf', 10)


# -- BUTTONS --
# buttons rect
toggle_verticies_button_rect = pygame.Rect((928, 630), (60, 60))
toggle_edges_button_rect = pygame.Rect((928, 560), (60, 60))
toggle_faces_button_rect = pygame.Rect((928, 490), (60, 60))
toggle_light_button_rect = pygame.Rect((928, 420), (60, 60))

toggle_cube_button_rect = pygame.Rect((928, 30), (60, 60))

# buttons text
settings_text = freesansbold.render('', True, BLACK)
toggle_verticies_button_text = freesansbold_small.render('Mostrar Vertices', True, BLACK)
toggle_edges_button_text = freesansbold_small.render('Mostrar Bordes', True, BLACK)
toggle_faces_button_text = freesansbold_small.render('Mostrar Caras', True, BLACK)
toggle_light_button_text = freesansbold_small.render('Colorear', True, BLACK)

shapes_text = freesansbold.render('Figuras', True, BLACK)
toggle_cube_button_text = freesansbold_small.render('Cubo', True, BLACK)



# buttons
toggle_verticies_button = Toggle_Button(toggle_verticies_button_rect, display, 1, False)
toggle_edges_button = Toggle_Button(toggle_edges_button_rect, display, 1, False)
toggle_faces_button = Toggle_Button(toggle_faces_button_rect, display, 1, False)
toggle_light_button = Toggle_Button(toggle_light_button_rect, display, 1, False)

toggle_cube_button = Toggle_Button(toggle_cube_button_rect, display, 1, False)


# render button texts
def render_button_texts():
    display.blit(settings_text, (916, 390))
    display.blit(toggle_verticies_button_text, (917, 620))
    display.blit(toggle_edges_button_text, (923, 550))
    display.blit(toggle_faces_button_text, (923, 480))
    display.blit(toggle_light_button_text, (938, 410))

    display.blit(shapes_text, (920, 0))
    display.blit(toggle_cube_button_text, (945, 20))

# translation variables
move_x = 0 #Translation on x
move_y = 0 #Translation on y

# graphics variables
rotation_x = 0 # cameras rotation on x axis
rotation_y = 0 # cameras rotation on y axis
rotation_z = 0 # cameras rotation on z axis

objPos = [window_width//2, window_height//2] # where the object should be pointed on the screen
fov = 500 # field of view (I think)
distance_from_object = 10 # cameras distance from the objects

light_enabled = True

points = 'placeholder'
edges = 'placeholder'
original_faces = 'placeholder'
current_shape = 'placeholder'
current_obj_file = 'placeholder'

# objects to render
def change_shape(shape, file=None, reset_camera=True):
    global points
    global edges
    global original_faces

    global current_shape
    global current_obj_file

    global distance_from_object
    global rotation_x
    global rotation_y
    global rotation_z

#########################################################

    if shape == 0:
        points = cube()[0] # gets the points that will be rendered
        edges = cube()[1] # gets the edges that will be rendered
        original_faces = cube()[2] # gets the faces that will be rendered
        current_shape = 0

    for face in original_faces:
        tuple_exists = False
        for item in face:
            if type(item) is tuple:
                tuple_exists = True
        if tuple_exists == False:
            if light_enabled == True:
                face.append(GRAY)
            else:
                face.append(random_color())

    auto_zoom_list = []
    for point in points:
        for item in point:
            auto_zoom_list.append(item[0])

    if reset_camera == True:
        distance_from_object = max(auto_zoom_list) + 2 * 3
        rotation_x = 0
        rotation_y = 0
        rotation_z = 0

change_shape(0)

# in-engine toggleable variables
do_render_faces = True
do_render_edges = True
do_render_verticies = True

# adjustable variables
sensitivity = 0.0002 # how sensitive the movement is
scroll_sensitivity = 0.5 # how sensitive the camera is
max_fps = 60 # sets the frames per second (based on my monitors hertz)
max_distance = 250 # max distance the user can go away from the objects
min_distance = 2 # minimum distance the user can go close to the objects

# ---- MAIN LOOP ----
run = True
while run:
    # clock things
    clock.tick(max_fps)
    fps = clock.get_fps() # sets the fps variable to the current fps

    display.fill(WHITE) # fills the screen with white

    mouse_buttons = pygame.mouse.get_pressed() # gets the mouse buttons pressed
    if mouse_buttons[2]: # if that mouse button is pressed
        right_click = True # sets right_click to True
    else:
        right_click = False # sets right_click to False

    if mouse_buttons[0]:
        left_click = True
    else:
        left_click = False

    # pygame event detections
    for event in pygame.event.get(): # detects if theres an event in the frame

        if event.type == pygame.QUIT: # if the event is exitting out of pygame
            run = False # exits out of the loop

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_x -= move_amount[1] * sensitivity
                print(move_x);

            if event.key == pygame.K_RIGHT:
                move_x += move_amount[1] * sensitivity
                print(move_x);

            if event.key == pygame.K_DOWN:
                move_y += move_amount[0] * sensitivity
                print(move_y);

            if event.key == pygame.K_UP:
                move_y -= move_amount[0] * sensitivity
                print(move_y);

        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            move_amount = (prev_mouse[0] - pos[0], prev_mouse[1] - pos[1])

            if right_click: # if right click is being held down
                rotation_x += move_amount[1] * sensitivity
                rotation_y += move_amount[0] * sensitivity

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                holding_light_intensity_slider = False
                holding_light_radius_slider = False
                holding_light_x_slider = False
                holding_light_y_slider = False
                holding_light_z_slider = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos() # gets the position of the mouse

            if event.button == 4: # scroll up
                if distance_from_object >= min_distance:
                    distance_from_object -= scroll_sensitivity # go towards object
            if event.button == 5: # scroll down
                if distance_from_object <= max_distance:
                    distance_from_object += scroll_sensitivity # go away from the object

            if event.button == 1: # left click

                if toggle_verticies_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if toggle_verticies_button.disabled == False:
                        if toggle_verticies_button.clicked():
                            do_render_verticies = True
                        else:
                            do_render_verticies = False
                
                if toggle_edges_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if toggle_edges_button.disabled == False:
                        if toggle_edges_button.clicked():
                            do_render_edges = True
                        else:
                            do_render_edges = False

                if toggle_faces_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if toggle_faces_button.disabled == False:
                        if toggle_faces_button.clicked():
                            do_render_faces = True
                        else:
                            do_render_faces = False

                if toggle_light_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if toggle_light_button.disabled == False:
                        if toggle_light_button.clicked():
                            light_enabled = True
                            change_shape(current_shape, current_obj_file, False)
                        else:
                            light_enabled = False
                            change_shape(current_shape, current_obj_file, False)

                if toggle_cube_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if toggle_cube_button.disabled == False:
                        if toggle_cube_button.toggle == 0:
                            toggle_cube_button.clicked()
                            change_shape(0)

    faces = deepcopy(original_faces)

    # -- VERTEX MATHS --
    # Obtiene la lista de identificadores de los puntos
    projected_points = [p for p in range(len(points))]

    # matrices that we will be multiplying for 3d rotation math
    rotation_x_matrix = [[1, 0, 0], [0, cos(rotation_x), -sin(rotation_x)], [0, sin(rotation_x), cos(rotation_x)]]
    rotation_y_matrix = [[cos(rotation_y), 0, -sin(rotation_y)], [0, 1, 0], [sin(rotation_y), 0, cos(rotation_y)]]
    rotation_z_matrix = [[cos(rotation_z), -sin(rotation_z), 0], [sin(rotation_z), cos(rotation_z), 0], [0, 0, 1]]

    pointsZ = [] # list of the points distance from the camera
    for index, point in enumerate(points): # loops through the list of points

        # rotation math
        rotated = multiply_matrix(rotation_x_matrix, point)
        rotated = multiply_matrix(rotation_y_matrix, rotated)
        rotated = multiply_matrix(rotation_z_matrix, rotated)

        # projection math
        if distance_from_object != 0:
            z = 1/(distance_from_object - rotated[2][0])
        else:
            z = 0
        projection = [[z, 0, 0], [0, z, 0]]

        projected = multiply_matrix(projection, rotated)

        x = projected[0][0] * fov + objPos[0]
        y = projected[1][0] * fov + objPos[1]

        projected_points[index] = [x, y]

        pointsZ.append(z) # appends the points distance from the camera

    # -- SPRITE MATHS --
    rotated = multiply_matrix(rotation_y_matrix, rotated)
    rotated = multiply_matrix(rotation_z_matrix, rotated)

    if distance_from_object != 0:
        z = 1/(distance_from_object - rotated[2][0])
    else:
        z = 0
    projection = [[z, 0, 0], [0, z, 0]]
    projected = multiply_matrix(projection, rotated)
    light_bulb_x = projected[0][0] * fov + objPos[0]
    light_bulb_y = projected[1][0] * fov + objPos[1]

    for face in faces: # for every face that needs to be rendered (this one gets the avg z value of the face)
        faceZ = []
        for value in face:
            if isinstance(value, int) == True:
                faceZ.append(pointsZ[value])
        face.append(faceZ)
        if len(face) == 6:
            face.append(sum([face[5][0], face[5][1], face[5][2], face[5][3]]) / 4)
        elif len(face) == 5:
            face.append("placeholder")
            face.append(sum([face[4][0], face[4][1], face[4][2]]) / 3)
    faces.sort(key=itemgetter(6)) # sorts our list of faces by the average z value

    for index, face in enumerate(faces):
        if "placeholder" in face:
            face.remove("placeholder")

        if light_enabled == True:
            face_point_list = []
            for point in face:
                if type(point) == int:
                    face_point_list.append(points[point])

            x_list = []
            y_list = []
            z_list = []
            for point in face_point_list:
                x_list.append(point[0][0])
                y_list.append(point[1][0])
                z_list.append(point[2][0])

            if len(x_list) == 4:
                face_point_average = [[(x_list[0] + x_list[1] + x_list[2] + x_list[3]) / 4], [(y_list[0] + y_list[1] + y_list[2] + y_list[3]) / 4], [(z_list[0] + z_list[1] + z_list[2] + z_list[3]) / 4]]
            elif len(x_list) == 3:
                face_point_average = [[(x_list[0] + x_list[1] + x_list[2]) / 3], [(y_list[0] + y_list[1] + y_list[2]) / 3], [(z_list[0] + z_list[1] + z_list[2]) / 3]]

            if len(x_list) == 4:
                if faces[index][4][0] > 255:
                    faces[index][4] = (255, 255, 255)
                elif faces[index][4][0] < 0:
                    faces[index][4] = (0, 0, 0)
            elif len(x_list) == 3:
                if faces[index][3][0] > 255:
                    faces[index][3] = (255, 255, 255)
                elif faces[index][3][0] < 0:
                    faces[index][3] = (0, 0, 0)


    # DRAWING TO THE PYGAME WINDOW
    def render_faces():
        for index, face in enumerate(faces): # for every face that needs to be rendered (this one renders the face based on teh average z value)
            a = (projected_points[face[0]][0], projected_points[face[0]][1])
            b = (projected_points[face[1]][0], projected_points[face[1]][1])
            c = (projected_points[face[2]][0], projected_points[face[2]][1])
            if len(face) == 7:
                d = (projected_points[face[3]][0], projected_points[face[3]][1])
                e = face[4]
                pygame.draw.polygon(display, e, (a, b, c, d))
            else:
                e = face[3]
                pygame.draw.polygon(display, e, (a, b, c))

    def render_edges():
        for edge in edges: # for every edge that needs to be rendered
            a = (projected_points[edge[0]][0], projected_points[edge[0]][1])
            b = (projected_points[edge[1]][0], projected_points[edge[1]][1])

            pygame.draw.line(display, BLACK, a, b, 2) # renders the edge

    def render_verticies():
        for point in projected_points:
            pygame.draw.circle(display, RED, (int(point[0]), int(point[1])), 4)

    if do_render_faces:
        render_faces()
    if do_render_edges:
        render_edges()
    if do_render_verticies:
        render_verticies()

    if edges == []:
        toggle_edges_button.disabled = True
    else:
        toggle_edges_button.disabled = False

    # BUTTON RENDERING
    toggle_verticies_button.draw()
    toggle_edges_button.draw()
    toggle_faces_button.draw()
    toggle_light_button.draw()
    
    toggle_cube_button.draw()

    # TEXT REGISTERING
    fps_text = freesansbold.render('FPS: ' + str(round(fps, 2)), True, BLACK)
    hint_text = freesansbold_small.render('(Mantenga presionado el click derecho para rotar)', True, BLACK)
    authors = freesansbold_small.render('Victor Carreon - Andrea Mejia', True, BLACK)

    # TEXT RENDERING
    display.blit(fps_text, (0, 0))
    display.blit(hint_text, (400, 0))
    display.blit(authors, (450,10))

    render_button_texts()

    pygame.display.update() # updates the pygame display

# ---- POST LOOP ----
pygame.quit() # quits out of the pygame window