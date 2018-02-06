#########################################################################
# A simple module for Python graphical displays.
# Documentation: http://myslu.stlawu.edu/~ltorrey/intrographics
#########################################################################

import tkinter
import traceback
import inspect
import math
import wave
import os.path

VERSION = 1.4

# Window manager
class system:
    def __init__(self):
        self.toplevel = tkinter.Tk()
        self.toplevel.withdraw()
        self.root = None
        self.toplevels = []
        self.pyglet = False
        self.pillow = False

    # Create a tkinter frame.
    def create(self, win):
        if not self.root:
#            self.root = tkinter.Tk()
            self.root = tkinter.Toplevel(self.toplevel)
            self.root.withdraw()
            return self.root
        else:
            frame = tkinter.Toplevel(self.root)
            self.toplevels.append(win)
            frame.withdraw()
            return frame

    # Show a tkinter frame.
    def show(self, win):
        win.frame.update()
        win.frame.deiconify()
        if win.frame == self.root:
            self.root.mainloop()

    # Destroy a tkinter frame.
    def destroy(self, win):
        if win.frame == self.root:
            for window in self.toplevels:
                window.close()
            self.toplevels = []
            self.root.destroy()
            self.root.quit()
            self.root = None
        else:
            self.toplevels.remove(win)
            win.frame.destroy()

    # Convert a color from string or (r,g,b) to hex.
    def hex(self, color):
        try:
            return "#%02x%02x%02x" % self.tuple(color)
        except:
            system.invalid("color", color)

    # Convert a color from string or (r,g,b) to (r,g,b).
    def tuple(self, color):
        try:
            if not system.rgb(color):
                color = tuple(map(lambda x: x // 256, self.root.winfo_rgb(color)))
            return color
        except:
            system.invalid("color", color)

    # Check for a valid RBG color.
    @staticmethod
    def rgb(color):
        if type(color) != tuple:
            return False
        if len(color) != 3:
            return False
        for c in color:
            if c < 0 or c > 255:
                return False
        return True

    @staticmethod
    def extra(command):
        system.error("Call to " + command + " has too many arguments.")

    @staticmethod
    def missing(command):
        system.error("Call to " + command + " doesn't have enough arguments.")

    @staticmethod
    def invalid(argument, value):
        system.error("Invalid " + argument + ": " + str(value))

    @staticmethod
    def immutable(attribute, item):
        system.error("The " + attribute + " of the " + item + " is read-only.")

    @staticmethod
    def error(message):
        print("An error occurred here:")
        for location in reversed(traceback.format_stack()):
            if "intrographics.py" not in location and "tkinter.py" not in location:
                print(location, message)
                quit()

sys = system()  # Singleton

try:
    import pyglet
    sys.pyglet = True
except ImportError:
    print("SoundFX will be disabled. Install pyglet to enable SoundFX.")
#    system.error("The intrographics module requires the Pyglet module")

try:
    from PIL import Image, ImageTk
    sys.pillow = True
except ImportError:
    print("Only GIF images will work, and image rotation will be disabled. Install pillow to enable these features.")
#    system.error("The intrographics module requires the PIL module")

class window:
    """Simple graphical display."""

    def __init__(self, width=None, height=None, *extra):
        command = "intrographics.window(width,height)"

        # Argument existence
        if len(extra) > 0:
            system.extra(command)
            return
        if width is None or height is None:
            system.missing(command)
            return

        # Argument types
        try:
            width,height = int(width),int(height)
            if width < 1 or height < 1:
                raise ValueError
        except ValueError:
            system.invalid("window dimensions", (width,height))
            return

        # Room for edges
        #width = width + 1
        #height = height + 1

        # Custom setup
        self.x = 0
        self.y = 0
        self.shapes = []
        self.timers = []
        self.opened = False
        self.closed = False
        self.keyPressHandlers = []
        self.leftClickHandlers = []
        self.leftDragHandlers = []
        self.rightClickHandlers = []
        self.rightDragHandlers = []

        # Tkinter setup
        self.frame = sys.create(self)
        self.canvas = tkinter.Canvas(self.frame)
        self.configure(self.x, self.y, width, height)
        self.fill("white")

        # Audio setup
        self.music = None
        self.musicPlayer = None

        if sys.pyglet:
            self.musicPlayer = pyglet.media.Player()
            self.musicPlayer.volume = 0.5
#        self.musicPlayer.eos_action = pyglet.media.SourceGroup.loop

        # Bindings
        self.frame.protocol("WM_DELETE_WINDOW", lambda: self.close(""))
        self.frame.bind("<KeyPress>", lambda event: self.keyPress(event))
        self.frame.bind("<Button-1>", lambda event: self.leftClick(event))
        self.frame.bind("<B1-Motion>", lambda event: self.leftDrag(event))
        self.frame.bind("<Button-3>", lambda event: self.rightClick(event))
        self.frame.bind("<B3-Motion>", lambda event: self.rightDrag(event))
        self.canvas.bind("<Configure>", lambda event: self.configure(self.x, self.y,
                                                                     self.frame.winfo_width(),
                                                                     self.frame.winfo_height()))

    # Update the window location and/or size.
    def configure(self, x, y, width, height):
        self.x, self.y = x, y
        self.__dict__["width"] = width - 1
        self.__dict__["height"] = height - 1
        self.frame.wm_geometry(str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y))
        self.canvas.configure(width=width, height=height, highlightthickness=0)

    # Disallow direct changes to some attributes.
    def __setattr__(self, attribute, value):
        if attribute in ["width", "height"]:
            return system.immutable(attribute, "window")
        self.__dict__[attribute] = value

    def fill(self, color=None, *extra):
        """Give the window a background color."""
        command = "window.fill(color)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if color is None:
            return system.missing(command)

        if not self.closed:
            self.canvas.configure(background=sys.hex(color))

    def relocate(self, x=None, y=None, *extra):
        """Change the location of the window."""
        command = "window.relocate(x,y)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("window location", (x,y))

        if not self.closed:
            self.configure(x, y, self.__dict__["width"], self.__dict__["height"])

    def resize(self, width=None, height=None, *extra):
        """Change the size of the window."""
        command = "window.resize(width,height)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if width is None or height is None:
            return system.missing(command)

        # Argument types
        try:
            width = int(width)
            height = int(height)
            if width < 1 or height < 1:
                raise ValueError
        except ValueError:
            return system.invalid("window dimensions", (width,height))

        if not self.closed:
            self.configure(self.x, self.y, width + 1, height + 1)

    def rectangle(self, x=None, y=None, width=None, height=None, *extra):
        """Draw and return a rectangle shape."""
        command = "window.rectangle(x,y,width,height)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None or width is None or height is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("rectangle location", (x,y))

        try:
            width,height = int(width),int(height)
            if width < 1 or height < 1:
                raise ValueError
        except ValueError:
            return system.invalid("rectangle dimensions", (width,height))

        if not self.closed:
            shape = rectangle(self.canvas, x, y, width, height)
            self.shapes.append(shape)
            return shape

    def oval(self, x=None, y=None, width=None, height=None, *extra):
        """Draw and return an oval shape."""
        command = "window.oval(x,y,width,height)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None or width is None or height is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("oval location", (x,y))

        try:
            width = int(width)
            height = int(height)
            if width < 1 or height < 1:
                raise ValueError
        except ValueError:
            return system.invalid("oval dimensions", (width,height))

        if not self.closed:
            shape = oval(self.canvas, x, y, width, height)
            self.shapes.append(shape)
            return shape

    def arc(self, x=None, y=None, width=None, height=None, beginAngle=None, arcAngle=None, *extra):
        """Draw and return an arc shape."""
        command = "window.arc(x,y,width,height, beginAngle, arcAngle)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None or width is None or height is None or beginAngle is None or arcAngle is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("arc location", (x,y))

        try:
            width = int(width)
            height = int(height)
            if width < 1 or height < 1:
                raise ValueError
        except ValueError:
            return system.invalid("arc dimensions", (width,height))

        try:
            beginAngle = int(beginAngle) % 360
            arcAngle = int(arcAngle) % 360


        except ValueError:
            return system.invalid("arc dimensions", (width,height))

        if not self.closed:
            shape = arc(self.canvas, x, y, width, height, beginAngle, arcAngle)
            self.shapes.append(shape)
            return shape

    def polygon(self, *points):
        """Draw and return a polygon shape."""
        command = "window.polygon( (x1,y1), (x2,y2), (x3,y3), ...)"

        # Argument existence
        if len(points) < 3:
            return system.missing(command)

        # Argument types
        pointlist = []
        for point in points:
            try:
                (x,y) = tuple(point)
                x = int(x)
                y = int(y)
                pointlist.append((x,y))
            except:
                return system.invalid("(x,y) point", point)

        if not self.closed:
            shape = polygon(self.canvas, tuple(pointlist))
            self.shapes.append(shape)
            return shape

    def line(self, *points):
        """Draw and return a line shape."""
        command = "window.line( (x1,y1), (x2,y2), ...)"

        # Argument existence
        if len(points) < 2:
            return system.missing(command)

        # Argument types
        pointlist = []
        for point in points:
            try:
                (x,y) = tuple(point)
                x = int(x)
                y = int(y)
                pointlist.append((x,y))
            except:
                return system.invalid("(x,y) point", point)

        if not self.closed:
            shape = line(self.canvas, tuple(pointlist))
            self.shapes.append(shape)
            return shape

    def text(self, x=None, y=None, message=None, *extra):
        """Draw and return a text shape."""
        command = "window.text(x,y,message)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None or message is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("text location", (x,y))

        if not self.closed:
            shape = text(self.canvas, x, y, str(message))
            self.shapes.append(shape)
            return shape

    def button(self, x=None, y=None, message=None, *extra):
        """Draw and return a button shape."""
        command = "window.button(x,y,message)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None or message is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("button location", (x,y))

        if not self.closed:
            shape = button(self.canvas, x, y, str(message))
            self.shapes.append(shape)
            return shape

    def field(self, x=None, y=None, message="", *extra):
        """Draw and return a field shape."""
        command = "window.field(x,y,message?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("field location", (x,y))

        if not self.closed:
            shape = field(self.canvas, x, y, str(message))
            self.shapes.append(shape)
            return shape

    def image(self, x=None, y=None, filename=None, *extra):
        """Draw and return an image shape."""
        command = "window.image(x,y,filename)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None or filename is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("image location", (x,y))

        if not self.closed:
            shape = image(self.canvas, x, y, str(filename))
            self.shapes.append(shape)
            return shape

    def emptyimage(self, x=None, y=None, width=None, height=None, *extra):
        """Draw and return an empty image shape."""
        command = "window.emptyimage(x,y,width,height)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None or width is None or height is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("image location", (x,y))

        try:
            width = int(width)
            height = int(height)
        except ValueError:
            return system.invalid("image width and height", (width,height))

        if not self.closed:
            shape = emptyimage(self.canvas, x, y, width, height)
            self.shapes.append(shape)
            return shape

    def queueMusic(self, filename=None, *extra):
        """Queue the audio object."""
        if not sys.pyglet:
            system.error("Music feature is disabled due to a missing module. Please install pyglet to use this feature.")
    		
        command = "window.queueMusic(filename)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if filename is None:
            return system.missing(command)

        # Argument types
        filename = filename.strip()

        if not os.path.isfile(filename):
            return system.invalid("file not found", filename)

        if not self.closed:
            try:
                audioObject = pyglet.media.load(filename, streaming=False)
                self.musicPlayer.queue(audioObject)
            except:
                return system.invalid("Invalid audio file", filename)

    def playMusic(self, *extra):
        """Queue the audio object."""
        if not sys.pyglet:
            system.error("Music feature is disabled due to a missing module. Please install pyglet to use this feature.")

        command = "window.playMusic()"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        if not self.closed:
            self.musicPlayer.play()

    def playNextMusic(self, *extra):
        """Queue the audio object."""
        if not sys.pyglet:
            system.error("Music feature is disabled due to a missing module. Please install pyglet to use this feature.")
    		
        command = "window.playNextMusic()"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        if not self.closed:
            self.musicPlayer.next_source()
            self.playMusic()

    def pauseMusic(self, *extra):
        """Queue the audio object."""
        if not sys.pyglet:
            system.error("Music feature is disabled due to a missing module. Please install pyglet to use this feature.")

        command = "window.pauseMusic()"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        if not self.closed:
            self.musicPlayer.pause()

    def isMusicPlaying(self, *extra):
        """Return boolean whether music is playing."""
        if not sys.pyglet:
            system.error("Music feature is disabled due to a missing module. Please install pyglet to use this feature.")
    		
        command = "window.isMusicPlaying()"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        if not self.closed:
            return self.musicPlayer.playing

    def setMusicVolume(self, volume, *extra):
        """Set the music volume."""
        if not sys.pyglet:
            system.error("Music feature is disabled due to a missing module. Please install pyglet to use this feature.")
    		
        command = "window.setMusicVolume(volume)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if volume is None:
            return system.missing(command)

        if (type(volume) is not float and type(volume) is not int) or volume < 0 or volume > 1:
            return system.invalid("Volume must be between 0.0 and 1.0", volume)

        if not self.closed:
            self.musicPlayer.volume = volume

    def getMusicVolume(self, *extra):
        """Return the current volume as float."""
        if not sys.pyglet:
            system.error("Music feature is disabled due to a missing module. Please install pyglet to use this feature.")
    		
        command = "window.getMusicVolume()"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        if not self.closed:
            return self.musicPlayer.volume

    def soundfx(self, filename=None, *extra):
        """Set and return the audio object."""
        if not sys.pyglet:
            system.error("Music feature is disabled due to a missing module. Please install pyglet to use this feature.")
    		
        command = "window.soundfx(filename)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if filename is None:
            return system.missing(command)

        # Argument types
        filename = filename.strip()

        if not os.path.isfile(filename):
            return system.invalid("file not found", filename)

        if not self.closed:
            audioObject = soundfx(filename)
            return audioObject

    def all(self, group=None, *extra):
        """Get a list of shapes in the window."""
        command = "window.getAll(group?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        shapes = []
        for shape in self.shapes:
            if group is None or group in shape.groups:
                shapes.append(shape)
        return shapes

    def remove(self, shape=None):
        """Remove a shape from the window."""
        command = "window.remove(shape)"

        # Argument existence
        if shape is None:
            return system.missing(command)
        if not isinstance(shape, windowshape):
            return system.invalid("shape", shape)

        if not self.closed and shape in self.shapes:
            self.shapes.remove(shape)
            shape.delete()

    def onTimer(self, milliseconds=None, function=None, *extra):
        """Assign a function to handle timer ticks."""
        command = "window.onTimer(milliseconds,function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if milliseconds is None or function is None:
            return system.missing(command)

        # Argument types
        try:
            milliseconds = int(milliseconds)
            if milliseconds < 1:
                raise ValueError
        except ValueError:
            return system.invalid("timer interval", milliseconds)

        if not hasattr(function, "__call__"):
            return system.invalid("timer function", function)
        if len(inspect.getargspec(function)[0]) > 0:
            return sys.error("Timer function '" + function.__name__ + "' should expect no arguments.")

        if not self.closed and function not in self.timers:
            self.timers.append(function)
            self.canvas.after(milliseconds, self.tick, milliseconds, function)

    # Call a function periodically.
    def tick(self, milliseconds, function):
        if not self.closed and function in self.timers:
            if self.opened:
                function()
            self.canvas.after(milliseconds, self.tick, milliseconds, function)

    def offTimer(self, function=None, *extra):
        """Unassign a timer function."""
        command = "window.offTimer(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("timer function", function)
        if len(inspect.getargspec(function)[0]) > 0:
            return system.invalid("timer function", function.__name__)

        if function in self.timers:
            self.timers.remove(function)

    def onKeyPress(self, function=None, *extra):
        """Assign a function to handle key presses."""
        command = "window.onKeyPress(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("key function", function)
        if inspect.getargspec(function)[0] != ["key"]:
            return sys.error("Key function '" + function.__name__ + "' should expect one argument (key).")

        if not self.closed and function not in self.keyPressHandlers:
            self.keyPressHandlers.append(function)

    def offKeyPress(self, function=None, *extra):
        """Unassign a key-press function."""
        command = "window.offKeyPress(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("key function", function)
        if inspect.getargspec(function)[0] != ["key"]:
            return system.invalid("key function", function.__name__)

        if function in self.keyPressHandlers:
            self.keyPressHandlers.remove(function)

    def onLeftClick(self, function=None, *extra):
        """Assign a function to handle left clicks."""
        command = "window.onLeftClick(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("click function", function)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return sys.error("Click function '" + function.__name__ + "' should expect two arguments (x,y).")

        if not self.closed and function not in self.leftClickHandlers:
            self.leftClickHandlers.append(function)

    def offLeftClick(self, function=None, *extra):
        """Unassign a left-click function."""
        command = "window.offLeftClick(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("click function", function)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return system.invalid("click function", function.__name__)

        if function in self.leftClickHandlers:
            self.leftClickHandlers.remove(function)

    def onLeftDrag(self, function=None, *extra):
        """Assign a function to handle left drags."""
        command = "window.onLeftDrag(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("drag function", function)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return sys.error("Drag function '" + function.__name__ + "' should expect two arguments (x,y).")

        if not self.closed and function not in self.leftDragHandlers:
            self.leftDragHandlers.append(function)

    def offLeftDrag(self, function=None, *extra):
        """Unassign a left-drag function."""
        command = "window.offLeftDrag(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("drag function", function)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return system.invalid("drag function", function.__name__)

        if function in self.leftDragHandlers:
            self.leftDragHandlers.remove(function)

    def onRightClick(self, function=None, *extra):
        """Assign a function to handle right clicks."""
        command = "window.onRightClick(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("click function", function)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return sys.error("Click function '" + function.__name__ + "' should expect two arguments (x,y).")

        if not self.closed and function not in self.rightClickHandlers:
            self.rightClickHandlers.append(function)

    def offRightClick(self, function=None, *extra):
        """Unassign a right-click function."""
        command = "window.offRightClick(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("click function", function)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return system.invalid("click function", function.__name__)

        if function in self.rightClickHandlers:
            self.rightClickHandlers.remove(function)

    def onRightDrag(self, function=None, *extra):
        """Assign a function to handle right drags."""
        command = "window.onRightDrag(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("drag function", function)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return sys.error("Drag function '" + function.__name__ + "' should expect two arguments (x,y).")

        if not self.closed and function not in self.rightDragHandlers:
            self.rightDragHandlers.append(function)

    def offRightDrag(self, function=None, *extra):
        """Unassign a right-drag function."""
        command = "window.offRightDrag(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("drag function", function)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return system.invalid("drag function", function.__name__)

        if function in self.rightDragHandlers:
            self.rightDragHandlers.remove(function)

    def keyPress(self, event):
        for function in self.keyPressHandlers:
            function(event.keysym)

    def leftClick(self, event):
        for function in self.leftClickHandlers:
            function(event.x, event.y)

    def leftDrag(self, event):
        for function in self.leftDragHandlers:
            function(event.x, event.y)

    def rightClick(self, event):
        for function in self.rightClickHandlers:
            function(event.x, event.y)

    def rightDrag(self, event):
        for function in self.rightDragHandlers:
            function(event.x, event.y)

    def open(self, title="intrographics", *extra):
        """Make the window visible."""
        command = "window.open(title?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        if not self.opened and not self.closed:
            self.frame.wm_title(str(title))
            self.canvas.pack()
            self.opened = True
            sys.show(self)

    def close(self, output="", *extra):
        """Close the window."""
        command = "window.close(output?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        if self.opened and not self.closed:
            for obj in self.shapes[:]:
                self.remove(obj)
            self.timers = []
            self.keyPressHandlers = []
            self.leftClickHandlers = []
            self.leftDragHandlers = []
            self.rightClickHandlers = []
            self.rightDragHandlers = []
            self.closed = True
            sys.destroy(self)
            print(str(output))

# Any shape displayed in a window.
class windowshape:
    def __init__(self, canvas):
        self.canvas = canvas
        self.deleted = False
        self.groups = set()

    # Disallow direct changes to some attributes.
    def __setattr__(self, attribute, value):
        if attribute in ["left", "top", "right", "bottom", "width", "height"]:
            return system.immutable(attribute, self.__class__.__name__)
        super().__setattr__(attribute, value)

    # Take this shape off the canvas.
    def delete(self):
        self.deleted = True
        self.canvas.delete(self.id)

    def group(self, name=None, *extra):
        """Put this shape in a named group."""
        command = self.__class__.__name__ + ".group(name)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if name is None:
            return system.missing(command)

        if not self.deleted:
            self.groups.add(name)

    def ungroup(self, name=None, *extra):
        """Take this shape out of a named group."""
        command = self.__class__.__name__ + ".ungroup(name)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if name is None:
            return system.missing(command)

        if name in self.groups:
            self.groups.remove(name)

    def overlaps(self, shape=None, *extra):
        """Check if this shape overlaps another."""
        command = self.__class__.__name__ + ".overlaps(shape)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if shape is None:
            return system.missing(command)

        # Argument types
        if not isinstance(shape, windowshape):
            return system.invalid("shape", shape)

        if self.deleted or shape.deleted or self == shape:
            return False
        else:
            return self.id in self.canvas.find_overlapping(shape.left, shape.top, shape.right, shape.bottom)

# A shape specified by a list of points.
class listshape(windowshape):
    def __init__(self, canvas, points):
        super().__init__(canvas)
        self.configure(points)

    # Update the shape location.
    def configure(self, points):
        self.points = points
        self.__dict__["left"] = min(x for (x,y) in points)
        self.__dict__["top"] = min(y for (x,y) in points)
        self.__dict__["right"] = max(x for (x,y) in points)
        self.__dict__["bottom"] = max(y for (x,y) in points)
        self.__dict__["width"] = self.__dict__["right"] - self.__dict__["left"]
        self.__dict__["height"] = self.__dict__["bottom"] - self.__dict__["top"]
        self.canvas.coords(self.id, tuple([c for p in points for c in p]))

    def rotate(self, angle):
        angle = math.radians(angle)

        cx = self.__dict__["left"] + self.__dict__["width"] / 2
        cy = self.__dict__["top"] + self.__dict__["height"] / 2

        newPoints = []
        for index in range(len(self.points)):
            x, y = self.points[index]
            dx = x - cx
            dy = y - cy
            newx = dx * math.cos(angle) - dy * math.sin(angle)
            newy = dy * math.cos(angle) + dx * math.sin(angle)

            newx += cx
            newy += cy
            newPoints.append((newx, newy))
        self.configure(newPoints)

    def fill(self, color=None, *extra):
        """Change the color of this shape."""
        command = self.__class__.__name__ + ".fill(color)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if color is None:
            return system.missing(command)

        if not self.deleted:
            self.canvas.itemconfig(self.id, fill=sys.hex(color))

    def move(self, dx=None, dy=None, *extra):
        """Move this shape."""
        command = self.__class__.__name__ + ".move(dx,dy)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if dx is None or dy is None:
            return system.missing(command)

        # Argument types
        try:
            dx = int(dx)
            dy = int(dy)
        except ValueError:
            return system.invalid("movement vector", (dx,dy))

        if not self.deleted:
            self.configure(tuple(map(lambda p: (p[0] + dx,p[1] + dy), self.points)))

    def relocate(self, x=None, y=None, *extra):
        """Change the location of this shape."""
        command = self.__class__.__name__ + ".relocate(x,y)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None:
            return system.missing(command)

        # Argument types
        try:
            sx, sy = self.__dict__["left"], self.__dict__["top"]
            dx = int(x) - sx
            dy = int(y) - sy
        except ValueError:
            return system.invalid("new location", (x,y))

        if not self.deleted:
            self.move(dx, dy)

class polygon(listshape):
    """A polygon shape."""
    def __init__(self, canvas, points):
        self.id = canvas.create_polygon(0,0,0,0,0,0, fill="", width=1, outline=sys.hex("black"))
        super().__init__(canvas, points)

    def border(self, width=None, color="black", *extra):
        """Change the border around this polygon."""
        command = "polygon.border(width,color?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if width is None:
            return system.missing(command)

        # Argument types
        try:
            width = int(width)
            if width < 0:
                raise ValueError
        except ValueError:
            return system.invalid("border width", width)

        if not self.deleted:
            if width == 0:
                self.canvas.itemconfig(self.id, width=1, outline="")
            else:
                self.canvas.itemconfig(self.id, width=width, outline=sys.hex(color))

class line(listshape):
    """A line shape."""
    def __init__(self, canvas, points):
        self.id = canvas.create_line(0,0,0,0, width=1)
        super().__init__(canvas, points)

    def border(self, width=None, *extra):
        """Change the width of this line."""
        command = "line.border(width)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if width is None:
            return system.missing(command)

        # Argument types
        try:
            width = int(width)
            if width < 1:
                raise ValueError
        except ValueError:
            return system.invalid("line width", width)

        if not self.deleted:
            self.canvas.itemconfig(self.id, width=width)

class rectangle(polygon):
    """A rectangle shape."""

    def __init__(self, canvas, x, y, width, height):
        points = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        super().__init__(canvas, points)

class arc(polygon):
    """An oval shape."""

    def __init__(self, canvas, x, y, width, height, beginAngle, arcAngle):
#        self.id = canvas.create_oval(0, 0, 0, 0, width=1)
        points = []

        arcAngle %= 360

        if arcAngle == 0:
            arcAngle = 360
        else:
            points.append((0, 0))

        a = width / 2
        b = height / 2

        t = math.radians(1)

        for i in range(beginAngle, beginAngle + arcAngle + 1):
            points.append((math.cos(i * t) * a, math.sin(i * t) * b))

        points = [(v + x + a, w + y + b) for (v, w) in points]

        super().__init__(canvas, points)



class oval(arc):
    """An oval shape."""
    def __init__(self, canvas, x, y, width, height):
        super().__init__(canvas, x, y, width, height, 0, 360)


# A shape specified by a single point.
class pointshape(windowshape):
    def __init__(self, canvas, x, y):
        super().__init__(canvas)
        self.configure(x, y)

    # Update the shape location.
    def configure(self, x, y):
        self.x = x
        self.y = y
        self.__dict__["left"] = x
        self.__dict__["top"] = y
        self.__dict__["right"] = self.canvas.bbox(self.id)[2]
        self.__dict__["bottom"] = self.canvas.bbox(self.id)[3]
        self.__dict__["width"] = self.__dict__["right"] - self.__dict__["left"]
        self.__dict__["height"] = self.__dict__["bottom"] - self.__dict__["top"]

        self.canvas.coords(self.id, (x, y))

    def move(self, dx=None, dy=None, *extra):
        """Move this shape."""
        command = self.__class__.__name__ + ".move(dx,dy)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if dx is None or dy is None:
            return system.missing(command)

        # Argument types
        try:
            dx = int(dx)
            dy = int(dy)
        except ValueError:
            return system.invalid("movement vector", (dx,dy))

        if not self.deleted:
            self.configure(self.x + dx, self.y + dy)

    def relocate(self, x=None, y=None, *extra):
        """Change the location of this shape."""
        command = self.__class__.__name__ + ".relocate(x,y)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return system.invalid("new location", (x,y))

        if not self.deleted:
            self.configure(x, y)

class text(pointshape):
    """A text label."""
    def __init__(self, canvas, x, y, message):
        self.id = canvas.create_text(0,0, text=message, font=("Helvetica",16), fill="black", anchor="nw")
        super().__init__(canvas, x, y)
        super().configure(x, y)

    def read(self, datatype=str, *extra):
        """Read the current message."""
        command = "text.read(datatype?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        # Argument types
        if datatype not in [str, int, float]:
            return system.invalid("datatype", datatype)

        try:
            return datatype(self.canvas.itemcget(self.id, "text"))
        except ValueError:
            return sys.error("Couldn't interpret '" + self.canvas.itemcget(self.id, "text") + "' as a float.")

    def rewrite(self, message=None, *extra):
        """Change the message of this text."""
        command = "text.rewrite(message)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if message is None:
            return system.missing(command)

        if not self.deleted:
            self.canvas.itemconfig(self.id, text=str(message))

    def format(self, font=None, size=None, color="black", *extra):
        """Change the text style of this text."""
        command = "text.format(font,size,color)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if font is None or size is None:
            return system.missing(command)

        # Argument types
        try:
            size = int(size)
            if size < 1:
                raise ValueError
        except ValueError:
            return system.invalid("font size", size)

        if not self.deleted:
            self.canvas.itemconfig(self.id, font=(str(font),size), fill=sys.hex(color))
            self.configure(self.x, self.y)

class button(pointshape):
    """A clickable button."""
    def __init__(self, canvas, x, y, message):
        self.handlers = []
        self.button = tkinter.Button(canvas.master, text=message)
        self.button.config(command=self.activate)
        self.id = canvas.create_window(x, y, anchor="nw", window=self.button)
        super().__init__(canvas, x, y)

    def read(self, datatype=str, *extra):
        """Read the current message."""
        command = "button.read(datatype?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        # Argument types
        if datatype not in [str, int, float]:
            return system.invalid("datatype", datatype)

        try:
            return datatype(self.button.cget("text"))
        except ValueError:
            return sys.error("Couldn't interpret '" + self.button.cget("text") + "' as a float.")

    def rewrite(self, message=None, *extra):
        """Change the message of this button."""
        command = "button.rewrite(message)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if message is None:
            return system.missing(command)

        if not self.deleted:
            self.button.config(text=str(message))

    def onActivate(self, function=None, *extra):
        """Assign a function to call when this button is activated."""
        command = "button.onActivate(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("button function", function)
        if len(inspect.getargspec(function)[0]) > 1:
            return sys.error("Button function '" + function.__name__ + "' should expect  no arguments or one (source).")

        if not self.deleted and function not in self.handlers:
            self.handlers.append(function)

    def offActivate(self, function=None, *extra):
        """Unassign a function for this button."""
        command = "button.offActivate(function)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if function is None:
            return system.missing(command)

        # Argument types
        if not hasattr(function, "__call__"):
            return system.invalid("button function", function)
        if len(inspect.getargspec(function)[0]) > 1:
            return system.invalid("button function", function.__name__)

        if not self.deleted and function in self.handlers:
            self.handlers.remove(function)

    # Activate the button.
    def activate(self):
        for function in self.handlers:
            if len(inspect.getargspec(function)[0]) > 0:
                function(self)
            else:
                function()

class field(pointshape):
    """An input field."""
    def __init__(self, canvas, x, y, message):
        self.message = tkinter.StringVar(value=message)
        self.entry = tkinter.Entry(canvas.master, textvariable=self.message, relief="sunken", background="gray99")
        self.id = canvas.create_window(x, y, anchor="nw", window=self.entry)
        self.entry.bind("<FocusIn>", lambda event: self.message.set(""))
        super().__init__(canvas, x, y)

    def read(self, datatype=str, *extra):
        """Read the current message."""
        command = "field.read(datatype?)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)

        # Argument types
        if datatype not in [str, int, float]:
            return system.invalid("datatype", datatype)

        try:
            return datatype(self.message.get())
        except ValueError:
            return sys.error("Couldn't interpret '" + self.message.get() + "' as a float.")

    def rewrite(self, message=None, *extra):
        """Change the message of this field."""
        command = "field.rewrite(message)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if message is None:
            return system.missing(command)

        if not self.deleted:
            self.message.set(str(message))

class image(pointshape):
    """A GIF image."""
    def __init__(self, canvas, x, y, filename=None):
        self.angle = 0
        if filename is not None:
            if sys.pillow:
                self.imageObj = Image.open(filename).convert('RGBA')
                self.img = ImageTk.PhotoImage(self.imageObj)
            else:
                self.img = tkinter.PhotoImage(master=canvas.master, file=filename)
        self.id = canvas.create_image(x, y, anchor="nw", image=self.img)

        super().__init__(canvas, x, y)

    # Update the shape location.
    def configure(self, x, y):
        self.x = x
        self.y = y
        self.__dict__["left"] = x
        self.__dict__["top"] = y
        self.__dict__["width"] = self.img.width()
        self.__dict__["height"] = self.img.height()
        self.__dict__["right"] = x + self.img.width()
        self.__dict__["bottom"] = y + self.img.height()

        self.canvas.coords(self.id, (x, y))

    def rotate(self, angle):
        if not sys.pillow:
            system.error("Image rotation is disabled. Please install pillow to use this feature")
    		
        self.angle = int(self.angle - angle) % 360
        imageObj = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        rotatedImage = self.imageObj.rotate(self.angle, resample=Image.BILINEAR).resize((self.width, self.height))
        imageObj.paste(rotatedImage, (0, 0), rotatedImage)
        self.img = ImageTk.PhotoImage(rotatedImage)
        self.canvas.itemconfig(self.id, image = self.img)
        self.configure(self.x, self.y)

    def resetRotation(self):
        self.angle = 0
        self.rotate(0)

    def getPixel(self, x, y):
        if sys.pillow:
            r, g, b, a = self.imageObj.getpixel((x, y))
            return (r, g, b)
        else:
            returnColor = self.img.get(x,y)
            if type(returnColor) is tuple:
                return returnColor
            else:
                r, g, b = [int(intensity) for intensity in returnColor.split()]
                return (r, g, b)
#            return system.rgb(self.img.get(x,y))

    def getColor(self, x=None, y=None, *extra):
        """Retrieve the (r,g,b) color at pixel x,y of the image."""
        command = "image.getColor(x,y)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
            if x < 0 or x >= self.img.width():
                raise ValueError
            if y < 0 or y >= self.img.height():
                raise ValueError
        except ValueError:
            return system.invalid("image pixel", (x,y))

        if self.deleted:
            return system.error("Can't get colors from a deleted image.")
        else:
            return self.getPixel(x, y)


    def setPixel(self, x, y, color):
        if sys.pillow:
            self.imageObj.putpixel((x, y), sys.tuple(color))
            del self.img
            self.img = ImageTk.PhotoImage(self.imageObj)
        else:
            self.img.put(sys.hex(color), (x, y))

    def setColor(self, x=None, y=None, color=None, *extra):
        """Change the (r,g,b) color at pixel x,y of the image."""
        command = "image.setColor(x,y,color)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if x is None or y is None or color is None:
            return system.missing(command)

        # Argument types
        try:
            x = int(x)
            y = int(y)
            if x < 0 or x >= self.img.width():
                raise ValueError
            if y < 0 or y >= self.img.height():
                raise ValueError
        except ValueError:
            return system.invalid("image pixel", (x,y))

        if not self.deleted:
            self.setPixel(x, y, color)
            self.canvas.itemconfig(self.id, image=self.img)

    def saveAs(self, filename=None, *extra):
        """Save this image to a file."""
        command = "image.saveAs(filename)"

        # Argument existence
        if len(extra) > 0:
            return system.extra(command)
        if filename is None:
            return system.missing(command)

        if self.deleted:
            system.error("Can't save a deleted image.")
        else:
            if sys.pillow:
                self.imageObj.save(str(filename))
            else:
                self.img.write(str(filename), format="GIF")

class emptyimage(image):
    """An empty image."""
    def __init__(self, canvas, x, y, width, height):
        if sys.pillow:
            self.imageObj = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        self.img = tkinter.PhotoImage(master=canvas.master, width=width, height=height)
        super().__init__(canvas, x, y)

    def getPixel(self, x, y):
        returnColor = self.img.get(x, y)
        if type(returnColor) is tuple:
            return returnColor
        else:
            r, g, b = [int(intensity) for intensity in returnColor.split()]
            return (r, g, b)
#        returnColor = self.img.get(x, y)

    def setPixel(self, x, y, color):
        self.img.put(sys.hex(color), (x, y))
        if sys.pillow:
            self.imageObj.putpixel((x, y), sys.tuple(color))
#            print(x, y, sys.tuple(color))
#        super().setPixel(x, y, color)

class soundfx():
    """An Sound FX object"""
    def __init__(self, filename):
        self.soundfx = pyglet.media.load(filename, streaming=False)

    def play(self):
        self.soundfx.play()

