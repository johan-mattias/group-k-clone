import pyglet
from time import time, sleep

__WIDTH__ = 800
__HEIGHT__ = 600
__WHITE__ = (255, 0, 0, 255)

def convert_hashColor_to_RGBA(color):
    if '#' in color:
        c = color.lstrip("#")
        c = max(6-len(c),0)*"0" + c
        r = int(c[:2], 16)
        g = int(c[2:4], 16)
        b = int(c[4:], 16)
        color = (r,g,b,255)
    return color

class Spr(pyglet.sprite.Sprite):
    def __init__(self, texture=None, width=__WIDTH__, height=__HEIGHT__, color='#000000', x=0, y=0):
        if texture is None:
            self.texture = pyglet.image.SolidColorImagePattern(convert_hashColor_to_RGBA(color)).create_image(width,height)
        else:
            self.texture = texture
        super(Spr, self).__init__(self.texture)

        ## Normally, objects in graphics have their anchor in the bottom left corner.
        ## This means that all X and Y cordinates relate to the bottom left corner of
        ## your object as positioned from the bottom left corner of your application-screen.
        ##
        ## We can override this and move the anchor to the WIDTH/2 (aka center of the image).
        ## And since Spr is a class only ment for generating a background-image to your "intro screen" etc
        ## This only affects this class aka the background, so the background gets positioned by it's center.
        self.image.anchor_x = self.image.width / 2
        self.image.anchor_y = self.image.height / 2

        ## And this sets the position.
        self.x = x
        self.y = y

    def _draw(self):
        self.draw()

## IntoScreen is a class that inherits a background, the background is Spr (our custom background-image class)
## IntoScreen contains 1 label, and it will change it's text after 2 seconds of being shown.
## That's all it does.
class IntroScreen(Spr):
    def __init__(self, texture=None, width=300, height = 150, x = 10, y = 10, color='#000000'):
        super(IntroScreen, self).__init__(texture, width=width, height=height, x=x, y=y, color=color)

        self.intro_text = pyglet.text.Label('Running game', font_size=8, font_name=('Verdana', 'Calibri', 'Arial'), x=x, y=y, multiline=False, width=width, height=height, color=(100, 100, 100, 255), anchor_x='center')
        self.has_been_visible_since = time()

    def _draw(self): # <-- Important, this is the function that is called from the main window.render() function. The built-in rendering function of pyglet is called .draw() so we create a manual one that's called _draw() that in turn does stuff + calls draw(). This is just so we can add on to the functionality of Pyglet.
        self.draw()
        self.intro_text.draw()
        if time() - 2 > self.has_been_visible_since:
            self.intro_text.text = 'foo studios'

## Then we have a MenuScreen (with a red background)
## Note that the RED color comes not from this class because the default is black #000000
## the color is set when calling/instanciating this class further down.
##
## But all this does, is show a "menu" (aka a text saying it's the menu..)
class MenuScreen(Spr):
    def __init__(self, texture=None, width=300, height = 150, x = 10, y = 10, color='#000000'):
        super(MenuScreen, self).__init__(texture, width=width, height=height, x=x, y=y, color=color)



    def _draw(self):
        self.draw()

class Window(pyglet.window.Window):
    def __init__(self, refreshrate):
        super(Window, self).__init__(vsync = False)
        self.alive = 1
        self.refreshrate = refreshrate

        self.screen_has_been_shown_since = time()

    def update_batch(self, batch, group):
        self.caret.delete()
        self.layout.delete()

        ### workaround for pyglet issue 408
        self.layout.batch = None
        if self.layout._document:
            self.layout._document.remove_handlers(self.layout)
        self.layout._document = None
        ### end workaround

        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, self.layout.width, self.layout.height, multiline=False, batch=batch, group=group)
        self.caret = pyglet.text.caret.Caret(self.layout)
        self.caret.visible = False

    def on_draw(self):
        self.render()

    def on_key_down(self, symbol, mod):
        print('Keyboard down:', symbol) # <-- Important

    def render(self):
        self.clear()
        # self.currentScreen._draw() # <-- Important, draws the current screen
        self.flip()

    def on_close(self):
        self.alive = 0

    def run(self):
        while self.alive:
            self.render()
            event = self.dispatch_events()
            sleep(1.0/self.refreshrate)

win = Window(23) # set the fps
win.run()