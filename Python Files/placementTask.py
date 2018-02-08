# Top Left Corner: (231, 37)
# Top Right Corner: (1408, 37)
# Bottom Left Corner: (231, 725)
# Bottom Right Corner: (1408, 725)

import intrographicsFork, pygame

width = 1500
height = 1000

window = intrographicsFork.window(width,height)
window.fill("maroon")



#Load the images
mazeImage = window.image(width//5-70, 35, "maze.gif")

imageTab = window.rectangle(15, 30, 200, 700)
imageTab.fill("grey")


#Button to submit
Submitbutton = window.button(width//5-40, 750, "Submit")

Resetbutton = window.button(width//5+100, 750, "Reset Circles")


# variable to track what's been selected
selectedShape = None

flagCircle = window.oval(150, 60, 15, 15)
flagRec = window.rectangle(33, 52, 100, 30)
flagRec.fill("green")
flagtext = window.text(60,58,"Flag")
flagCircle.fill("green")

fountainCircle = window.oval(150, 160, 15, 15)
fountainRec = window.rectangle(30, 152, 100, 30)
fountainRec.fill("OrangeRed2")
fountaintext = window.text(55,158,"Fountain")
fountainCircle.fill("OrangeRed2")

bikeCircle = window.oval(150, 260, 15, 15)
bikeRec = window.rectangle(33, 252, 100, 30)
bikeRec.fill("medium purple")
biketext = window.text(60,258,"Bike")
bikeCircle.fill("medium purple")

artCircle = window.oval(150, 360, 15, 15)
artRec = window.rectangle(33, 352, 100, 30)
artRec.fill("yellow")
arttext = window.text(69,358,"Art")
artCircle.fill("yellow")

lampCircle = window.oval(150, 460, 15, 15)
lampRec = window.rectangle(33, 452, 100, 30)
lampRec.fill("WhiteSmoke")
lamptext = window.text(60,458,"Lamp")
lampCircle.fill("WhiteSmoke")

chairCircle = window.oval(150, 560, 15, 15)
chairRec = window.rectangle(30, 552, 100, 30)
chairRec.fill("hot pink")
chairtext = window.text(60,558,"Chair")
chairCircle.fill("hot pink")

clockCircle = window.oval(150, 660, 15, 15)
clockRec = window.rectangle(30, 652, 100, 30)
clockRec.fill("turquoise")
clocktext = window.text(60,658,"Clock")
clockCircle.fill("turquoise")

Circle = window.oval(150, 760, 15, 15)
Circle.fill("turquoise")


selectedShape = None

circleArray = [flagCircle,fountainCircle,bikeCircle,artCircle,lampCircle,chairCircle,clockCircle]

# define the click function
def click(x, y):
    global selectedShape,flagCircle,fountainCircle,bikeCircle,artCircle,lampCircle,chairCircle,clockCircle

    # create a small temporary rectangle
    tempRectangle = window.rectangle(x, y, 1, 1)

    for circle in circleArray:
        if tempRectangle.overlaps(circle):
            # mario needs to be the selected shape
            selectedShape = circle
            break
        else:
            selectedShape = None

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

# click button
def submitClick():
    print("Flag Coordinates", getCoordinates(flagCircle))
    print("Fountain Coordinates", getCoordinates(fountainCircle))
    print("Bike Coordinates", getCoordinates(bikeCircle))
    print("Art Coordinates", getCoordinates(artCircle))
    print("Lamp Coordinates", getCoordinates(lampCircle))
    print("Chair Coordinates", getCoordinates(chairCircle))
    print("Clock Coordinates", getCoordinates(clockCircle))
    return

#run the function when clicked
Submitbutton.onActivate(submitClick)





# reset button
def resetCircles():
    y = 60
    for aCircle in circleArray:
        aCircle.relocate(150, y)
        y += 100

Resetbutton.onActivate(resetCircles)

def getCoordinates(aShape):
    return (aShape.left + aShape.width // 2, aShape.top + aShape.height // 2)

window.open("Object Placement Task")