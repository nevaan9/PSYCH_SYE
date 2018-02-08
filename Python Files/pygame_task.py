import pygame, random
pygame.init()


img_path = "/Users/nevaanperera/Desktop/Psych SYE/Python/maze.gif"
maze_img = pygame.image.load(img_path)
maze_w = maze_img.get_width()
maze_h = maze_img.get_height()

# maze propeerties
maze_x = 200
maze_y = 50

# rectangle properties
rect_x = 20
rect_y = 50
rect_h = maze_h
rect_w = maze_w//8

def make_dragCircle(x, y):
     pygame.draw.circle(window, (random.randrange(256), random.randrange(256), random.randrange(256)), (x, y), 15)


# make window
window = pygame.display.set_mode((1500, 1500))

# add maze image
window.blit(maze_img, (maze_x,maze_y))

# draw side bar
pygame.draw.rect(window, (150, 150, 150), (rect_x, rect_y, rect_w, rect_h))

# specify starting points for the circles
x = rect_x + 3*rect_w // 4
y = rect_y + 40

# draw circles
for i in range(7):
    make_dragCircle(x, y)
    y = y + 100

pygame.display.update()

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y

