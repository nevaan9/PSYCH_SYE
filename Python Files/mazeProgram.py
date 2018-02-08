import intrographicsFork

width = 1500
height = 1000

window = intrographicsFork.window(width,height)
window.fill("maroon")



#Load the images
mazeImage = window.image(width//5-70, 35, "maze.gif")

imageTab = window.rectangle(15, 30, 200, 700)
imageTab.fill("grey")

flag = window.image(width//20, 50, "flag.gif")
lamp = window.image(width//20 - 10, 150, "lamppost.gif")
clock = window.image(width//20 + 5, 250, "gfclock.gif")
art = window.image(width//20 - 7, 350, "art.gif")
bike = window.image(width//20, 450, "bike.gif")
chair = window.image(width//20, 520, "chair.gif")
fountain = window.image(width//20 - 15, 610, "fountain.gif")


#Button to submit
button = window.button(width//5-40, 750, "Submit")


# variable to track what's been selected
selectedShape = None

imageArray = [flag, lamp, clock, art, bike, chair, fountain]

# define the click function
def click(x, y):
    global selectedShape, flag, lamp, clock, art, bike, chair, fountain

    # create a small temporary rectangle
    tempRectangle = window.rectangle(x, y, 1, 1)

    # see if the temporary rectangle overlaps with mario
    for image in imageArray:
        if tempRectangle.overlaps(image):
            # mario needs to be the selected shape
            selectedShape = image
            break
        else:
            selectedShape = None

    # remove the temporary rectangle
    window.remove(tempRectangle)

# link the click function to the left click event
window.onLeftClick(click)

# define the drag function
def drag(x, y):
    global selectedShape

    # move the selected shape to the drag destination (x, y)
    if selectedShape != None:
        selectedShape.relocate(x-selectedShape.width//2, y-selectedShape.height//2)


# link the drag function to the left drag event
window.onLeftDrag(drag)

def buttonClick():
    print("Flag Coordinates: ", getCoordinates(flag))
    print("Lamp Coordinates: ", getCoordinates(lamp))
    print("Clock Coordinates: ", getCoordinates(clock))
    print("Art Coordinates: ", getCoordinates(art))
    print("Bike Coordinates: ", getCoordinates(bike))
    print("Chair Coordinates: ", getCoordinates(chair))
    print("Fountain Coordinates: ", getCoordinates(fountain))

button.onActivate(buttonClick)

def getCoordinates(anImage):
    return (anImage.left + anImage.width//2, anImage.top + anImage.height//2)

window.open("Object Placement Task")