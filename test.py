import pygame, random, math
from pandas import DataFrame
import webbrowser

# --- constants --- (UPPER_CASE names)
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE = (10, 20, 255)
YELLOW = (255,255,10)
MAGENTA = (255,10,255)
CYAN = (10,255,255)
CHOCOLATE = (210,105,30)
GREY = (119,136,153)
ORCHID = (218,112,214)
GREEN = 	(34,139,34)


FPS = 30

# initialize game
pygame.init()

# screen props
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Psychology Experiment")

# set up rectangle objects
def createRec(x, y):
    return pygame.rect.Rect(176, 134, 17, 18)

# reset function
def moveShapes():
    moveVal = 100
    for i in range(6):
        reclist[i].x = rec_x
        reclist[i].y = moveVal
        moveVal += 100

def chooseImage():
    if len(imageList) == 0:
        submit_pressed = 2
    else:
        randomChoice = random.randrange(len(imageList))
        sImage = imageList[randomChoice]
        sImage_x = image_dic[sImage][0]
        sImage_y = image_dic[sImage][1]
        sImage_w = image_dic[sImage][2]
        sImage_h = image_dic[sImage][3]
        picture_tup = image_dic[sImage][4]
        imageList.remove(sImage)
        return (sImage, sImage_x, sImage_y, sImage_w, sImage_h, picture_tup)

def distance(point1, point2):
    return round(math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2), 2)

def calc_angle(a,b,c):
    b1 = b**2
    c1 = c**2
    a1 = a**2

    lower = 2*b*c
    inner = (b1 + c1 - a1)/lower
    return round(math.degrees(math.acos(inner)), 2)

# path = 'maze.gif'
#
# # Load maze images
# maze_img = pygame.image.load(path)
# maze_w = maze_img.get_width()
# maze_h = maze_img.get_height()
# maze_x = 230
# maze_y = 70

# pathe to pictures
pic1 = 'one.png'
pic2 = 'two.png'
pic3 = 'three.png'
pic4 = 'four.png'
pic5 = 'five.png'
pic6 = 'six.png'

lamp_path = 'lamp_c.png'

# load maze images
# load the image with objects
ob_image = pygame.image.load('withObjects.png')


# part1
part1 = pygame.image.load(pic1)
part1_w = part1.get_width()
part1_h = part1.get_height()
part1_x = 230
part1_y = 20

# part2
part2 = pygame.image.load(pic2)
part2_w = part2.get_width()
part2_h = part2.get_height()
part2_x = part1_x + part1_w
part2_y = part1_y

# part 3
part3 = pygame.image.load(pic3)
part3_w = part3.get_width()
part3_h = part3.get_height()
part3_x = part2_x + part2_w
part3_y = part1_y

# part 4
part4 = pygame.image.load(pic4)
part4_w = part4.get_width()
part4_h = part4.get_height()
part4_x = part1_x
part4_y = part1_y + part1_h

# part 5
part5 = pygame.image.load(pic5)
part5_w = part5.get_width()
part5_h = part5.get_height()
part5_x = part4_x+part4_w
part5_y = part4_y

# part 6
part6 = pygame.image.load(pic6)
part6_w = part6.get_width()
part6_h = part6.get_height()
part6_x = part5_x + part5_w
part6_y = part4_y

# rectangle props
rec_x = 150
rec_side = 20

# decription props
dec_x = rec_x - 120
dec_w = rec_side * 5
dec_h = rec_side

# reset button/submit
reset_w = 80
reset_x = rec_x - reset_w//2
reset_y = 720
reset_h = 30

#submit
sub_x = reset_x - reset_w - 20

# place to move image parts
sImage = None
move_x = SCREEN_WIDTH//2
move_y = SCREEN_HEIGHT//2


# fonts
font1 = pygame.font.SysFont('Arial', 25)

#boolean
rectangle_draging = False
clicked_angle_pointer = False
need_toChoose = True

# lists
points = []
choices = ["allocentric", "egocentric"]
choose_measure = random.random()
if choose_measure > 0.5:
    measure = choices[0]
else:
    measure = choices[1]

submit_pressed = -2

# - objects -
rectangle = pygame.rect.Rect(rec_x, 100, rec_side, rec_side)
rectangle2 = pygame.rect.Rect(rec_x, 200, rec_side, rec_side)
rectangle3 = pygame.rect.Rect(rec_x, 300, rec_side + 6, rec_side)
rectangle4 = pygame.rect.Rect(rec_x, 400, rec_side, rec_side)
rectangle5 = pygame.rect.Rect(rec_x, 500, rec_side + 8, rec_side)
rectangle6 = pygame.rect.Rect(rec_x, 600, rec_side, rec_side)

descripion = pygame.rect.Rect(dec_x, 100, dec_w, dec_h)
descripion2 = pygame.rect.Rect(dec_x, 200, dec_w, dec_h)
descripion3 = pygame.rect.Rect(dec_x, 300, dec_w, dec_h)
descripion4 = pygame.rect.Rect(dec_x, 400, dec_w, dec_h)
descripion5 = pygame.rect.Rect(dec_x, 500, dec_w, dec_h)
descripion6 = pygame.rect.Rect(dec_x, 600, dec_w, dec_h)

# reset button
reset = pygame.rect.Rect(reset_x, reset_y, reset_w, reset_h)

# submit button
submit = pygame.rect.Rect(sub_x, reset_y, reset_w + 5, reset_h)

# Object Pictures
part1_pic = pygame.image.load(lamp_path)
part1_pic_w = part1_pic.get_width()
part1_pic_h = part1_pic.get_height()
ori_part1_pic_x = 289
ori_part1_pic_y = 100
part1_pic_x = ori_part1_pic_x - (part1_pic_w//2)
part1_pic_y = ori_part1_pic_y - part1_pic_h//2
part1_pic_name = "Lamp"

part2_pic = pygame.image.load('chair_c.png')
part2_pic_w = part2_pic.get_width()
part2_pic_h = part2_pic.get_height()
ori_part2_pic_x = 728
ori_part2_pic_y = 290
part2_pic_x = ori_part2_pic_x - (part2_pic_w//2)
part2_pic_y = ori_part2_pic_y - part2_pic_h//2
part2_pic_name = "Chair"

part3_pic = pygame.image.load('bike_c.png')
part3_pic_w = part3_pic.get_width()
part3_pic_h = part3_pic.get_height()
ori_part3_pic_x = 1347
ori_part3_pic_y = 115
part3_pic_x = ori_part3_pic_x - (part3_pic_w//2)
part3_pic_y = ori_part3_pic_y - part3_pic_h//2
part3_pic_name = "Bike"

part4_pic = pygame.image.load('stove_c.png')
part4_pic_w = part4_pic.get_width()
part4_pic_h = part4_pic.get_height()
ori_part4_pic_x = 441
ori_part4_pic_y = 691
part4_pic_x = ori_part4_pic_x - (part4_pic_w//2)
part4_pic_y = ori_part4_pic_y - part4_pic_h//2
part4_pic_name = "Stove"

part5_pic = pygame.image.load('barrel_c.png')
part5_pic_w = part5_pic.get_width()
part5_pic_h = part5_pic.get_height()
ori_part5_pic_x = 1000
ori_part5_pic_y = 707
part5_pic_x = 1000 - (part5_pic_w//2)
part5_pic_y = 707 - part5_pic_h//2
part5_pic_name = "Barrel"

part6_pic = pygame.image.load('plant_c.png')
part6_pic_w = part6_pic.get_width()
part6_pic_h = part6_pic.get_height()
ori_part6_pic_x = 1370
ori_part6_pic_y = 873
part6_pic_x = ori_part6_pic_x - part6_pic_w//2
part6_pic_y = ori_part6_pic_y - part6_pic_h//2
part6_pic_name = "Plant"

# Man picture
man_pic = pygame.image.load('man.png')
man_pic_w = man_pic.get_width()
man_pic_h = man_pic.get_height()

man_pic_left = pygame.image.load('man_left.png')
man_pic_left_w = man_pic.get_width()
man_pic_left_h = man_pic.get_height()
man_pic_left_x = 0
man_pic_left_y = 0

# INSTRUCTIONS IMAGES
allo_ins = pygame.image.load('Capture_allo_c1.png')
allo_ins_x = SCREEN_WIDTH//2 - allo_ins.get_width()//2
allo_ins_y = SCREEN_HEIGHT//12

ego_ins = pygame.image.load('Capture_ego_c1.png')
ego_ins_x = SCREEN_WIDTH//2 - ego_ins.get_width()//2
ego_ins_y = SCREEN_HEIGHT//12

ego_point_ins = pygame.image.load('ego_point_ins1.png')
ego_point_ins_x = SCREEN_WIDTH//2 - ego_ins.get_width()//2
ego_point_ins_y = SCREEN_HEIGHT//12

allo_point_ins = pygame.image.load('allo_point_ins.png')
allo_point_ins_x = SCREEN_WIDTH//2 - ego_ins.get_width()//2
allo_point_ins_y = SCREEN_HEIGHT//12

# start button
start = pygame.rect.Rect(SCREEN_WIDTH//2 - 240, allo_ins_y + allo_ins.get_height() + 50, 500, 50)

# angle
angle_x = None
angle_y = None

point_x = None
point_y = None

line_endX = None
line_endY = None

pointedValue_x = None
pointedValue_y = None

# Specify the real object x and y
real_obj_points = None


# lists
reclist = [rectangle, rectangle2, rectangle3, rectangle4, rectangle5, rectangle6, reset, submit]
imageList = [part1, part2, part3, part4, part5, part6]
object_list = [(ori_part1_pic_x,ori_part1_pic_y, "Lamp"), (ori_part2_pic_x,ori_part2_pic_y, "Chair"), (ori_part3_pic_x,ori_part3_pic_y, "Bike"), (ori_part4_pic_x,ori_part4_pic_y, "Stove"), (ori_part5_pic_x,ori_part5_pic_y, "Barrel"), (ori_part6_pic_x,ori_part6_pic_y, "Plant")]
image_dic = dict()

image_dic[part1] = (part1_x, part1_y, part1_w, part1_h, (part1_pic, part1_pic_w, part1_pic_h, part1_pic_x, part1_pic_y, ori_part1_pic_x, ori_part1_pic_y, part1_pic_name, "Stove"))
image_dic[part2] = (part2_x, part2_y, part2_w, part2_h, (part2_pic, part2_pic_w, part2_pic_h, part2_pic_x, part2_pic_y, ori_part2_pic_x, ori_part2_pic_y, part2_pic_name, "Lamp"))
image_dic[part3] = (part3_x, part3_y, part3_w, part3_h, (part3_pic, part3_pic_w, part3_pic_h, part3_pic_x, part3_pic_y, ori_part3_pic_x, ori_part3_pic_y, part3_pic_name, "Plant"))
image_dic[part4] = (part4_x, part4_y, part4_w, part4_h, (part4_pic, part4_pic_w, part4_pic_h, part4_pic_x, part4_pic_y, ori_part4_pic_x, ori_part4_pic_y, part4_pic_name, "Barrel"))
image_dic[part5] = (part5_x, part5_y, part5_w, part5_h, (part5_pic, part5_pic_w, part5_pic_h, part5_pic_x, part5_pic_y, ori_part5_pic_x, ori_part5_pic_y, part5_pic_name, "Bike"))
image_dic[part6] = (part6_x, part6_y, part6_w, part6_h, (part6_pic, part6_pic_w, part6_pic_h, part6_pic_x, part6_pic_y, ori_part6_pic_x, ori_part6_pic_y, part6_pic_name, "Chair"))


# Point object dictionary
point_obs = dict()
point_obs[part1_pic_name] = (ori_part1_pic_x, ori_part1_pic_y)
point_obs[part2_pic_name] = (ori_part2_pic_x, ori_part2_pic_y)
point_obs[part3_pic_name] = (ori_part3_pic_x, ori_part3_pic_y)
point_obs[part4_pic_name] = (ori_part4_pic_x, ori_part4_pic_y)
point_obs[part5_pic_name] = (ori_part5_pic_x, ori_part5_pic_y)
point_obs[part6_pic_name] = (ori_part6_pic_x, ori_part6_pic_y)

# - mainloop -

clock = pygame.time.Clock()

# bools
running = True
draw_line = False

selectedShape = None

added = False

submit_without_point = False


# INPUT BOX STUFF
font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()
input_box = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 100, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False
err = False

# PARTICIPANT ID
p_id = None


# Initialize all the columns in the data frame (object placement task)
p_id_col = None
ob_name_col = list()
distance_err = list()
condition = [measure for i in range(6)]

# angular pointing task
point_from = list()
point_to = list()
point_err = list()


while running:

    # - events -
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:


            if event.button == 1:

                # Input ID number
                if submit_pressed == -2:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive

                # if the start button was pressed
                if submit_pressed == -1:
                    if start.collidepoint(event.pos):
                        submit_pressed += 1

                # first phase (drag and drop task)
                if submit_pressed == 0:

                    for shape in reclist:
                        if shape.collidepoint(event.pos):
                            selectedShape = shape

                            if selectedShape == reset:
                                moveShapes()
                                continue

                            elif selectedShape == submit:
                                for i in range (len(reclist)-2):
                                    # print(reclist[i].x, reclist[i].y, end='|')
                                    # print(object_list[i][0], object_list[i][1])
                                    #print(reclist[i].x - rec_side//2)
                                    #print("REC POINTS", (reclist[i].x + rec_side//2, reclist[i].y + rec_side//2), "ORIGINAL OBJECT POINTS", (object_list[i][0], object_list[i][1]) )
                                    d = distance( (reclist[i].x + rec_side//2, reclist[i].y + rec_side//2), (object_list[i][0], object_list[i][1]))
                                    #print(d)
                                    distance_err.append(d)
                                    ob_name_col.append(object_list[i][2])

                                df = DataFrame({'Participant ID': p_id_col, 'Condition': condition, 'Object Name': ob_name_col, 'Error in Distance': distance_err})
                                df.to_excel("participant_"+str(p_id)+'_distant.xlsx', sheet_name='sheet1', index=False)
                                submit_pressed += 1



                            # call get locations function here


                            rectangle_draging = True

                            # mouse_x, mouse_y = event.pos
                            # offset_x = selectedShape.x - mouse_x
                            # offset_y = selectedShape.y - mouse_y


                # Instructions (Angular task)
                elif submit_pressed == 1:
                    if start.collidepoint(event.pos):
                        submit_pressed += 1


                # second phase
                elif submit_pressed == 2:

                    if not submit.collidepoint(event.pos):
                        draw_line = True
                        line_endX, line_endY = event.pos

                    for shape in reclist[-2:]:
                        if start.collidepoint(event.pos):
                            draw_line = False
                        if shape.collidepoint(event.pos):
                            selectedShape = shape
                            # if selectedShape == dot:
                            #     draw_line = True
                            #     angle_x, angle_y = event.pos
                            if selectedShape == reset:
                                draw_line = False
                                continue
                            elif selectedShape == submit:
                                try:
                                    # Now that we have 3 points lets calculate the angle
                                    c = distance((pointing_fromValue_x, pointing_fromValue_y), (real_line_endX, real_line_endY))
                                    b = distance((pointing_fromValue_x, pointing_fromValue_y), (ob2_x, ob2_y))
                                    a = distance((ob2_x, ob2_y), (real_line_endX, real_line_endY))

                                    angle_err = calc_angle(a,b,c)

                                    point_err.append(angle_err)

                                    point_x = None
                                    point_y = None
                                    real_obj_points = None
                                    real_line_endX = None
                                    real_line_endY = None
                                    need_toChoose = True
                                    draw_line = False
                                    submit_without_point = False


                                except:
                                    draw_line = False
                                    submit_without_point = True


                                if len(imageList) == 0:
                                    df1 = DataFrame({'Participant ID': p_id_col, 'Condition': condition, 'Point From': point_from, 'Point To': point_to, 'Angle Error': point_err})
                                    df1.to_excel("participant_" + str(p_id)+ '_pointing.xlsx', sheet_name='sheet1', index=False)
                                    webbrowser.open("https://stlawu.qualtrics.com/jfe/form/SV_3WoQnKtTDSHVpAx")
                                    exit()



        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_draging = False


        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                selectedShape.x = mouse_x - rec_side//2
                selectedShape.y = mouse_y - rec_side//2

        elif event.type == pygame.KEYDOWN:
            if active:
                if submit_pressed == -2:
                    if event.key == pygame.K_RETURN:
                        try:
                            p_id = int(text)
                            p_id_col = [str(p_id) for i in range(6)]
                        except:
                            err = True
                            break
                        submit_pressed += 1
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode



    # - updates (without draws) -
    screen.fill(WHITE)

    # ID Phase
    if submit_pressed == -2:
        # ID INPUT
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (SCREEN_WIDTH//2 - 95, SCREEN_HEIGHT//2 + 10))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        if err:
            screen.blit(font.render('Please enter a valid numeric ID', True, (205, 0, 0)), (SCREEN_WIDTH//4, SCREEN_HEIGHT//3))
        else:
            screen.blit(font.render('Please enter your ID number', True, (0, 150, 0)),
                        (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))


    # INSTRUCTIONS (Object placement)
    if submit_pressed == -1:
        if  measure == 'allocentric':
            screen.blit(allo_ins, (allo_ins_x, allo_ins_y))
            pygame.draw.rect(screen, GREEN, start)
            screen.blit(font.render('START TASK', True, (0, 0, 0)), (start.x + 180, start.y + 10))
        else:
            screen.blit(ego_ins, (ego_ins_x, ego_ins_y))
            pygame.draw.rect(screen, GREEN, start)
            screen.blit(font.render('START TASK', True, (0, 0, 0)), (start.x + 180, start.y + 10))


    # OBJECT PLACEMENT TASK!
    if submit_pressed == 0:
        #blit the images
        screen.blit(part1, (part1_x, part1_y))
        screen.blit(part2, (part2_x, part2_y))
        screen.blit(part3, (part3_x, part3_y))
        screen.blit(part4, (part4_x, part4_y))
        screen.blit(part5, (part5_x, part5_y))
        screen.blit(part6, (part6_x, part6_y))

        if measure == 'egocentric':
            screen.blit(font.render("Imagine you the person at the starting location. Drag and drop the objects to where you think they were located.", True, (0, 0, 0)), (part1_x + 100, -1))
        else:
            screen.blit(font.render("The dot represents the starting location. Drag and drop the objects to where you think they were located.", True, (0, 0, 0)),(part1_x + 100, -1))

        if measure == 'allocentric':
            pygame.draw.circle(screen, BLACK, (312, 896), 7)
        else:
            screen.blit(man_pic, (312 - man_pic_w//2, 896 - man_pic_h//2))

        # - draws (without updates) -
        pygame.draw.rect(screen, CHOCOLATE, rectangle)
        screen.blit(font1.render('L', True, (0, 0, 0)), (rectangle.x + 4, rectangle.y -5))

        pygame.draw.rect(screen, MAGENTA, rectangle2)
        screen.blit(font1.render('C', True, (0, 0, 0)), (rectangle2.x + 4, rectangle2.y - 5))

        pygame.draw.rect(screen, RED, rectangle3)
        screen.blit(font1.render('Bi', True, (0, 0, 0)), (rectangle3.x + 2, rectangle3.y - 5))

        pygame.draw.rect(screen, YELLOW, rectangle4)
        screen.blit(font1.render('S', True, (0, 0, 0)), (rectangle4.x + 4, rectangle4.y - 5))

        pygame.draw.rect(screen, GREY, rectangle5)
        screen.blit(font1.render('Ba', True, (0, 0, 0)), (rectangle5.x + 2, rectangle5.y - 5))

        pygame.draw.rect(screen, GREEN, rectangle6)
        screen.blit(font1.render('P', True, (0, 0, 0)), (rectangle6.x + 4, rectangle6.y - 5))


        # Descriptions
        pygame.draw.rect(screen, CHOCOLATE, descripion)
        screen.blit(font1.render('Lamp', True, (0, 0, 0)), (descripion.x + (descripion.x//2), descripion.y - 5))

        pygame.draw.rect(screen, MAGENTA, descripion2)
        screen.blit(font1.render('Chair', True, (0, 0, 0)), (descripion2.x + (descripion2.x // 2), descripion2.y - 5))

        pygame.draw.rect(screen, RED, descripion3)
        screen.blit(font1.render('Bike', True, (0, 0, 0)), (descripion3.x + (descripion3.x // 2), descripion3.y - 5))

        pygame.draw.rect(screen, YELLOW, descripion4)
        screen.blit(font1.render('Stove', True, (0, 0, 0)), (descripion4.x + (descripion4.x // 2), descripion4.y - 5))

        pygame.draw.rect(screen, GREY, descripion5)
        screen.blit(font1.render('Barrel', True, (0, 0, 0)), (descripion5.x + (descripion5.x // 2), descripion5.y - 5))

        pygame.draw.rect(screen, GREEN, descripion6)
        screen.blit(font1.render('Plant', True, (0, 0, 0)), (descripion6.x + (descripion6.x // 2), descripion6.y - 5))

        pygame.draw.rect(screen, BLUE, reset)
        screen.blit(font1.render('RESET', True, (0, 0, 0)), (reset_x + (reset_w//12),reset_y))

        pygame.draw.rect(screen, RED, submit)
        screen.blit(font1.render('SUBMIT', True, (0, 0, 0)), (sub_x + 5,reset_y))

    # Instructions (Angular pointing)
    if submit_pressed == 1:
        if  measure == 'allocentric':
            screen.blit(allo_point_ins, (allo_point_ins_x, allo_point_ins_y))
            pygame.draw.rect(screen, GREEN, start)
            screen.blit(font.render('START TASK', True, (0, 0, 0)), (start.x + 180, start.y + 10))
        else:
            screen.blit(ego_point_ins, (ego_point_ins_x, ego_point_ins_y))
            pygame.draw.rect(screen, GREEN, start)
            screen.blit(font.render('START TASK', True, (0, 0, 0)), (start.x + 180, start.y + 10))


    # ANGULAR POINTING TASK!
    if submit_pressed == 2:
        if need_toChoose:
            sImage, sImage_x, sImage_y, sImage_w, sImage_h, picture_tuple = chooseImage()
            need_toChoose = False
            added = False

        x = move_x - sImage_w//2
        y = move_y - sImage_h//2

        diff_in_x_vals = sImage_x - picture_tuple[3]
        diff_in_y_vals = sImage_y - picture_tuple[4]

        diff_in_x_vals = -diff_in_x_vals
        diff_in_y_vals = -diff_in_y_vals

        # Specify the dot/man pic x and y values
        man_pic_left_x = x - 20
        man_pic_left_y = y

        # blit the image
        #pygame.draw.line(screen, BLACK, (x, y), (x, y))

        ob1 = picture_tuple[7]

        ob2_name = picture_tuple[8]
        ob2_x, ob2_y = point_obs[ob2_name]

        if not added:
            point_from.append(ob1)
            point_to.append(ob2_name)
            added = True



        # INSTRUCTIONS
        if measure == 'egocentric':
            screen.blit(font.render("Imagine you are the person standing next to the {}. Draw an arrow pointing to the {} relative to yourself.".format(ob1, ob2_name), True, (0, 0, 0)), (SCREEN_WIDTH//5, 80))
        else:
            screen.blit(font.render("Look at the dot next to the {}. Draw an arrow pointing to the {} relative to the dot.".format(ob1, ob2_name), True, (0, 0, 0)),(SCREEN_WIDTH //5, 80))

        if submit_without_point:
            screen.blit(font.render("Cannot press submit without pointing to an object.", True, (200, 0, 0)),
                        (SCREEN_WIDTH // 5, 120))

        screen.blit(sImage, (x, y))

        if measure == 'egocentric':
            point_x = x + diff_in_x_vals + picture_tuple[1] + man_pic_left_w//2

        else:
            point_x = x + diff_in_x_vals + picture_tuple[1] + 20

        point_y = y + diff_in_y_vals + picture_tuple[2] // 2
        # draw line
        if draw_line:
            pygame.draw.line(screen, RED, (point_x, point_y), (line_endX, line_endY))

            # Get the differences
            diff_line_endX = line_endX - x
            diff_line_endY = line_endY - y

            diff_point_x = point_x - x
            diff_point_y = point_y - y

            # Get the real values
            real_line_endX = sImage_x + diff_line_endX
            real_line_endY = sImage_y + diff_line_endY


            pointing_fromValue_x = sImage_x + diff_point_x
            pointing_fromValue_y = sImage_y + diff_point_y

            # Code to test if the above calculations work
            # screen.blit(sImage, (sImage_x, sImage_y))
            # pygame.draw.circle(screen, BLACK, (real_line_endX, real_line_endY), 7)
            # pygame.draw.circle(screen, BLACK, (pointing_fromValue_x, pointing_fromValue_y), 7)
            # pygame.draw.circle(screen, BLACK, (ob2_x, ob2_y), 7)

            clicked_angle_pointer = False

        # reset button
        pygame.draw.rect(screen, BLUE, reset)
        screen.blit(font1.render('RESET', True, (0, 0, 0)), (reset_x + (reset_w//12),reset_y))

        pygame.draw.rect(screen, RED, submit)
        screen.blit(font1.render('SUBMIT', True, (0, 0, 0)), (sub_x + 5,reset_y))

        # Draw the small picture(object)
        screen.blit(picture_tuple[0], (x + diff_in_x_vals, y + diff_in_y_vals))

        # draw the dot/man under object
        if measure == "allocentric":
            pygame.draw.circle(screen, BLACK, (point_x, point_y), 7)
        else:
            screen.blit(man_pic_left, (x + diff_in_x_vals + picture_tuple[1], y + diff_in_y_vals))




    if submit_pressed == 3:
        exit()

    pygame.display.flip()

    # - constant game speed / FPS -
    clock.tick(FPS)

# - end -

pygame.quit()