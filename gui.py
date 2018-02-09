import pyglet
from time import time, sleep
from login_client import Client

__WIDTH__ = 800
__HEIGHT__ = 500
__BUTTON_HEIGHT__ = 40
__BUTTON_WIDTH__ = 150
__BUTTON_WIDTH_SMALL__ = 100
__INPUT_HEIGHT__ = 40
__INPUT_WIDTH__ = 250
__FONTS__ = ('Roboto', 'Calibri', 'Arial')
__SERVER_URL__ = "localhost:5000"


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

        self.intro_text = pyglet.text.Label('Running game', font_size=8, font_name=__FONTS__, x=x, y=y, multiline=False, width=width, height=height, color=(100, 100, 100, 255), anchor_x='center')
        self.has_been_visible_since = time()

    def _draw(self):  # <-- Important, this is the function that is called from the main window.render() function. The built-in rendering function of pyglet is called .draw() so we create a manual one that's called _draw() that in turn does stuff + calls draw(). This is just so we can add on to the functionality of Pyglet.
        self.draw()
        self.intro_text.draw()
        if time() - 2 > self.has_been_visible_since:
            self.intro_text.text = 'foo studios'


class InputField(Spr):
    def __init__(self,
                 text='INPUT',
                 font_size=8,
                 font_name=__FONTS__,
                 texture=None,
                 width=__INPUT_WIDTH__,
                 height = __INPUT_HEIGHT__,
                 x = 300,
                 y = __HEIGHT__//2,
                 bg_color='#C4C4C4',
                 color='#000000'):
        super(InputField, self).__init__(texture, width=int(width), height=int(height), x=x, y=y, color=bg_color)

        self.screen_text = pyglet.text.Label(text,
                                             font_size=font_size,
                                             font_name=font_name,
                                             x=176,
                                             y=y+21,
                                             multiline=False,
                                             width=width,
                                             height=height,
                                             color=convert_hashColor_to_RGBA(color),
                                             anchor_x='left')

    def _draw(self):
        self.draw()
        self.screen_text.draw()


class Button(Spr):
    def __init__(self,
                 func,
                 text='BUTTON',
                 font_size=10,
                 font_name=__FONTS__,
                 texture=None,
                 width=__BUTTON_WIDTH__,
                 height=__BUTTON_HEIGHT__,
                 x=300,
                 y=__HEIGHT__//2,
                 bg_color='#C4C4C4',
                 color='#000000'):
        super(Button, self).__init__(texture, width=width, height=height, x=x, y=y, color=bg_color)

        self.screen_text = pyglet.text.Label(text,
                                             font_size=font_size,
                                             font_name=font_name,
                                             x=x,
                                             y=y+height//2-25,
                                             multiline=False,
                                             width=width,
                                             height=height,
                                             color=convert_hashColor_to_RGBA(color),
                                             anchor_x='center')
        self.func = func
        print(f'button: {self.func} x: {self.x}-{self.x+self.width} y: {self.y}-{self.y+self.height}')

    def _draw(self):
        self.draw()
        self.screen_text.draw()

    def choice(self):
        return self.func


class LoginRegisterScreen(Spr):
    def __init__(self,
                 font_size=20,
                 font_name=__FONTS__,
                 texture=None,
                 width=300,
                 width_offset=225,
                 height=235,
                 height_offset=60,
                 x=300,
                 y=__HEIGHT__//2,
                 bg_color='#FFFFFF',
                 color='#FFFFFF',
                 header_text='HEADER TEXT',
                 inputs=[],
                 buttons=[]):
        super(LoginRegisterScreen, self).__init__(texture, width=width, height=height, x=x, y=y, color=bg_color)

        self.screen_text = pyglet.text.Label(header_text,
                                             font_size=font_size,
                                             font_name=font_name,
                                             x=x-152,
                                             y=y+height//2+1,
                                             multiline=False,
                                             width=width,
                                             height=height,
                                             color=convert_hashColor_to_RGBA(color),
                                             anchor_x='left')

        self.height_offset = height_offset
        self.inputs = []
        for input_field in inputs:
            self.inputs.append(InputField(text=input_field["text"], y=__HEIGHT__//2 + self.height_offset))
            self.height_offset += - __BUTTON_HEIGHT__ - __BUTTON_HEIGHT__//2

        self.width_offset = width_offset
        self.buttons = []
        for button in buttons:
            self.buttons.append(Button(text=button["text"], func=button["func"], width=__BUTTON_WIDTH_SMALL__, x = self.width_offset, y=__HEIGHT__//2 + self.height_offset))
            self.width_offset += __BUTTON_WIDTH__

    def _draw(self):
        self.draw()
        self.screen_text.draw()
        for input_field in self.inputs:
            input_field._draw()
        for button in self.buttons:
            button._draw()


class MenuScreen(Spr):
    def __init__(self,
                 font_size=20,
                 font_name=__FONTS__,
                 texture=None,
                 width=300,
                 height = 235,
                 x=300,
                 y=__HEIGHT__//2,
                 bg_color='#FFFFFF',
                 color='#FFFFFF',
                 header_text='HEADER TEXT',
                 buttons=[]):
        super(MenuScreen, self).__init__(texture, width=width, height=height, x=x, y=y, color=bg_color)

        self.screen_text = pyglet.text.Label(header_text,
                                             font_size=font_size,
                                             font_name=font_name,
                                             x=x-152,
                                             y=y+height//2+1,
                                             multiline=False,
                                             width=width,
                                             height=height,
                                             color=convert_hashColor_to_RGBA(color),
                                             anchor_x='left')

        button__offset = 60

        self.buttons = []
        for button in buttons:
            self.buttons.append(Button(func=button["func"], text=button["text"], y=__HEIGHT__//2 + button__offset))
            button__offset += - __BUTTON_HEIGHT__ - __BUTTON_HEIGHT__//2

    def _draw(self):
        self.draw()
        self.screen_text.draw()
        for button in self.buttons:
            button._draw()


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

        self.batch = pyglet.graphics.Batch()

        self.currentScreen = MenuScreen(header_text='GAME MENU',
                                        buttons=[{'text': 'LOG IN', 'func': 'login_menu'},
                                                 {'text': 'REGISTER', 'func': 'register_menu'},
                                                 {'text': 'QUIT', 'func': 'quit'}])

        # self.currentScreen = LoginRegisterScreen(height=235, height_offset=60, header_text='LOG IN',
        #                                 inputs=[{'text': 'ENTER USERNAME'}, {'text': 'ENTER PASSWORD'}],
        #                                 buttons=[{'text': 'BACK'}, {'text': 'LOG IN'}])

        # self.currentScreen = LoginRegisterScreen(height=300, height_offset=90, header_text='REGISTER USER',
        #                                 inputs=[{'text': 'ENTER USERNAME'}, {'text': 'ENTER PASSWORD'}, {'text': 'RE-ENTER PASSWORD'}],
        #                                 buttons=[{'text': 'BACK'}, {'text': 'REGISTER'}])
        self.screen_has_been_shown_since = time()

        self.login_client = Client(__SERVER_URL__)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_down(self, symbol, mod):
        print('Keyboard down:', symbol)  # <-- Important

    def on_mouse_press(self, x, y, button, modifiers):
        print("x: ", x, " y: ", y)
        if button == pyglet.window.mouse.LEFT:
            for menu_button in self.currentScreen.buttons:
                if x > (menu_button.x - menu_button.width//2) and x < (menu_button.x + menu_button.width//2):
                    if y > (menu_button.y - menu_button.height//2) and y < (menu_button.y + menu_button.height//2):
                        response = menu_button.choice()
                        print(response)
                        if response == "login_menu":
                            self._login_menu()
                        elif response == "login":
                            self._login()
                        elif response == "register_menu":
                            self._register_menu()
                        elif response == "register":
                            self._register()
                        elif response == "main_menu":
                            self._main_menu()
                        elif response == "quit":
                            self._quit()

    def _login_menu(self):
        login_response = self.login_client.login()
        if login_response == "ok":
            print("Log in with token successful")
        else:
            print(login_response)
            self.currentScreen = LoginRegisterScreen(height=235,
                                                     height_offset=60,
                                                     header_text='LOG IN',
                                                     inputs=[{'text': 'ENTER USERNAME'},
                                                             {'text': 'ENTER PASSWORD'}],
                                                     buttons=[{'text': 'BACK', 'func': 'main_menu'},
                                                              {'text': 'LOG IN', 'func': 'login'}])

    def _login(self):
        username = "anton"
        password = "carlsson"
        login_response = self.login_client.login_with_password(username, password)
        if login_response == "ok":
            print("Log in with password successful")
        else:
            print(login_response)

    def _register_menu(self):
        self.currentScreen = LoginRegisterScreen(height=300,
                                                 height_offset=90,
                                                 header_text='REGISTER USER',
                                                 inputs=[{'text': 'ENTER USERNAME'},
                                                         {'text': 'ENTER PASSWORD'},
                                                         {'text': 'RE-ENTER PASSWORD'}],
                                                 buttons=[{'text': 'BACK', 'func': 'main_menu'},
                                                          {'text': 'REGISTER', 'func': 'register'}])

    def _register(self):
        username = "anton"
        password = "carlsson"
        register_response = self.login_client.register(username, password)
        if register_response == "ok":
            self._login()
        else:
            print(register_response)


    def _main_menu(self):
        self.currentScreen = MenuScreen(header_text='GAME MENU',
                                        buttons=[{'text': 'LOG IN', 'func': 'login_menu'},
                                                 {'text': 'REGISTER', 'func': 'register_menu'},
                                                 {'text': 'QUIT', 'func': 'quit'}])

    def _quit(self):
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
