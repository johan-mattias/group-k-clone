import pyglet
from time import time, sleep
from login_client import Client

__WIDTH__ = 800
__HEIGHT__ = 500
__BUTTON_HEIGHT__ = 40
__BUTTON_WIDTH__ = 150


def convert_hashColor_to_RGBA(color):
    if '#' in color:
        c = color.lstrip("#")
        c = max(6-len(c), 0)*"0" + c
        r = int(c[:2], 16)
        g = int(c[2:4], 16)
        b = int(c[4:], 16)
        color = (r, g, b, 255)
    return color


class Spr(pyglet.sprite.Sprite):
    def __init__(self, texture=None, width=__WIDTH__, height=__HEIGHT__, color='#000000', x=0, y=0):
        if texture is None:
            self.texture = pyglet.image.SolidColorImagePattern(convert_hashColor_to_RGBA(color)).create_image(width,height)
        else:
            self.texture = texture
        super(Spr, self).__init__(self.texture)

        # Normally, objects in graphics have their anchor in the bottom left corner.
        # This means that all X and Y cordinates relate to the bottom left corner of
        # your object as positioned from the bottom left corner of your application-screen.
        #
        # We can override this and move the anchor to the WIDTH/2 (aka center of the image).
        # And since Spr is a class only ment for generating a background-image to your "intro screen" etc
        # This only affects this class aka the background, so the background gets positioned by it's center.
        self.image.anchor_x = self.image.width / 2
        self.image.anchor_y = self.image.height / 2

        # And this sets the position.
        self.x = x
        self.y = y

    def _draw(self):
        self.draw()


# IntoScreen is a class that inherits a background, the background is Spr (our custom background-image class)
# IntoScreen contains 1 label, and it will change it's text after 2 seconds of being shown.
# That's all it does.
class IntroScreen(Spr):
    def __init__(self, texture=None, width=300, height = 150, x = 10, y = 10, color='#000000'):
        super(IntroScreen, self).__init__(texture, width=width, height=height, x=x, y=y, color=color)

        self.intro_text = pyglet.text.Label('Running game', font_size=8, font_name=('Verdana', 'Calibri', 'Arial'), x=x, y=y, multiline=False, width=width, height=height, color=(100, 100, 100, 255), anchor_x='center')
        self.has_been_visible_since = time()

    def _draw(self):  # <-- Important, this is the function that is called from the main window.render() function. The built-in rendering function of pyglet is called .draw() so we create a manual one that's called _draw() that in turn does stuff + calls draw(). This is just so we can add on to the functionality of Pyglet.
        self.draw()
        self.intro_text.draw()
        if time() - 2 > self.has_been_visible_since:
            self.intro_text.text = 'foo studios'


class Button(Spr):
    def __init__(self,
                 func,
                 text='BUTTON',
                 font_size=10,
                 font_name=('Roboto', 'Calibri', 'Arial'),
                 texture=None,
                 width=__BUTTON_WIDTH__,
                 height=__BUTTON_HEIGHT__,
                 x=300,
                 y=__HEIGHT__ // 2,
                 bg_color='#C4C4C4',
                 color='#000000'):
        super(Button, self).__init__(texture, width=width, height=height, x=x, y=y, color=bg_color)

        self.screen_text = pyglet.text.Label(text,
                                             font_size=font_size,
                                             font_name=font_name,
                                             x=x,
                                             y=y+height/2-20,
                                             multiline=False,
                                             width=width,
                                             height=height,
                                             color=convert_hashColor_to_RGBA(color),
                                             anchor_x='center')
        self.func = func

    def _draw(self):
        self.draw()
        self.screen_text.draw()


# Then we have a MenuScreen (with a red background)
# Note that the RED color comes not from this class because the default is black #000000
# the color is set when calling/instanciating this class further down.
#
# But all this does, is show a "menu" (aka a text saying it's the menu..)
class MenuScreen(Spr):
    def __init__(self,
                 font_size=20,
                 font_name=('Roboto', 'Calibri', 'Arial'),
                 texture=None,
                 width=300,
                 height = 235,
                 x = 300,
                 y = __HEIGHT__/2,
                 bg_color='#FFFFFF',
                 color='#FFFFFF'):
        super(MenuScreen, self).__init__(texture, width=width, height=height, x=x, y=y, color=bg_color)

        self.screen_text = pyglet.text.Label('GAME IN DISGUISE',
                                             font_size=font_size,
                                             font_name=font_name,
                                             x=x,
                                             y=y+height/2+20,
                                             multiline=False,
                                             width=width,
                                             height=height,
                                             color=convert_hashColor_to_RGBA(color),
                                             anchor_x='center')
        self.client = Client("antoncarlsson.se:5000")

        BUTTON_OFFSET = 60
        self.buttons = [
            Button(func=lambda: print("log in"), text='LOG IN', y=__HEIGHT__ // 2 + BUTTON_OFFSET),
            Button(func=lambda: print("register"), text='REGISTER', y=(__HEIGHT__ // 2 + BUTTON_OFFSET - __BUTTON_HEIGHT__ - __BUTTON_HEIGHT__ // 2)),
            Button(func=self.quit, text='QUIT', y=(__HEIGHT__ // 2 + BUTTON_OFFSET - (__BUTTON_HEIGHT__*2) - __BUTTON_HEIGHT__))
        ]

    def _draw(self):
        self.draw()
        self.screen_text.draw()
        for button in self.buttons:
            button._draw()

    @staticmethod
    def quit():
        return "QUIT"


# This is the actual window, the game, the glory universe that is graphics.
# It will be blank, so you need to set up what should be visible when and where.
#
# I've creates two classes which can act as "screens" (intro, game, menu etc)
# And we'll initate the Window class with the IntroScreen() and show that for a
# total of 5 seconds, after 5 seconds we will swap it out for a MenuScreeen().
#
# All this magic is done in __init__() and render(). All the other functions are basically
# just "there" and executes black magic for your convencience.
class Window(pyglet.window.Window):
    def __init__(self, refresh_rate):
        super(Window, self).__init__(vsync = False)
        self.alive = 1
        self.refresh_rate = refresh_rate

        self.currentScreen = MenuScreen()  # <-- Important
        self.screen_has_been_shown_since = time()

    def on_draw(self):
        self.render()

    def on_key_down(self, symbol, mod):
        print('Keyboard down:', symbol)  # <-- Important

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            for menu_button in self.currentScreen.buttons:
                if x > menu_button.x and x < (menu_button.x + menu_button.width):
                    if y > menu_button.y and y < (menu_button.y + menu_button.height):
                        response = menu_button.func()
                        if response == "QUIT":
                            self.close()
                            self.on_close()

    def render(self):
        self.clear()

        # if time() - 5 > self.screen_has_been_shown_since and type(self.currentScreen) is not MenuScreen:  # <-- Important
        #     self.currentScreen = MenuScreen(x=320, y=__HEIGHT__-210, color='#FF0000') # <-- Important, here we switch screen (after 5 seconds)

        self.currentScreen._draw()  # <-- Important, draws the current screen
        self.flip()

    def on_close(self):
        self.alive = 0

    def run(self):
        while self.alive:
            self.render()
            event = self.dispatch_events()
            sleep(1.0/self.refresh_rate)


window = Window(30)  # set the fps
window.run()
