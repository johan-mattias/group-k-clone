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
        c = max(6-len(c),0)*"0" + c
        r = int(c[:2], 16)
        g = int(c[2:4], 16)
        b = int(c[4:], 16)
        color = (r,g,b,255)
    return color

class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )

    def delete(self):
        self.vertex_list.delete()

class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
            dict(color=(0, 0, 0, 255))
        )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

    def delete(self):
        self.rectangle.delete()
        self.layout.delete()

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

    def _draw(self):
        self.draw()
        self.screen_text.draw()

    def choice(self):
        return self.func

class LoginRegisterScreen(Spr):
    def __init__(self,
                 batch,
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
        super(LoginRegisterScreen, self).__init__(texture, width=5, height=5, x=x, y=y, color=bg_color)

        self.labels = [
            pyglet.text.Label('Name', x=10, y=100, anchor_y='bottom',
                              color=(255, 255, 255, 255), batch=batch),
            pyglet.text.Label('Species', x=10, y=60, anchor_y='bottom',
                              color=(255, 255, 255, 255), batch=batch),
            pyglet.text.Label('Special abilities', x=10, y=20,
                              anchor_y='bottom', color=(255, 255, 255, 255),
                              batch=batch)
        ]
        self.height_offset = height_offset
        # self.text_inputs = [
        #     TextWidget('', 300, 100, self.width - 210, batch),
        #     TextWidget('', 300, 60, self.width - 210, batch),
        #     TextWidget('', 300, 20, self.width - 210, batch)
        # ]
        self.text_inputs = []
        for input_field in inputs:
            self.text_inputs.append(TextWidget('', 300, __HEIGHT__//2 + self.height_offset, self.width + __INPUT_WIDTH__, batch))
            self.height_offset += - __BUTTON_HEIGHT__ - __BUTTON_HEIGHT__//2

        self.width_offset = width_offset
        self.buttons = []
        for button in buttons:
            self.buttons.append(Button(text=button["text"], func=button["func"], width=__BUTTON_WIDTH_SMALL__, x = self.width_offset, y=__HEIGHT__//2 + self.height_offset))
            self.width_offset += __BUTTON_WIDTH__

    def _draw(self):
        self.draw()
        for button in self.buttons:
            button._draw()

class Window(pyglet.window.Window):
    def __init__(self, refreshrate):
        super(Window, self).__init__(__WIDTH__, __HEIGHT__, caption='Text entry', vsync = False)
        self.alive = 1
        self.refreshrate = refreshrate
        self.screen_has_been_shown_since = time()

        self.batch = pyglet.graphics.Batch()
        self.current_screen = LoginRegisterScreen(batch=self.batch,
                                                    height=235,
                                                    height_offset=60,
                                                    header_text='LOG IN',
                                                    inputs=[{'text': 'ENTER USERNAME'},
                                                            {'text': 'ENTER PASSWORD'}],
                                                    buttons=[{'text': 'BACK', 'func': 'main_menu'},
                                                            {'text': 'LOG IN', 'func': 'login'}])
        # self.labels = [
        #     pyglet.text.Label('Name', x=10, y=100, anchor_y='bottom',
        #                       color=(0, 0, 0, 255), batch=self.batch),
        #     pyglet.text.Label('Species', x=10, y=60, anchor_y='bottom',
        #                       color=(0, 0, 0, 255), batch=self.batch),
        #     pyglet.text.Label('Special abilities', x=10, y=20,
        #                       anchor_y='bottom', color=(0, 0, 0, 255),
        #                       batch=self.batch)
        # ]
        # self.text_inputs = [
        #     TextWidget('', 200, 100, self.width - 210, self.batch),
        #     TextWidget('', 200, 60, self.width - 210, self.batch),
        #     TextWidget('', 200, 20, self.width - 210, self.batch)
        # ]
        self.text_cursor = self.get_system_mouse_cursor('text')

        self.focus = None
        # self.set_focus(self.text_inputs[0])
        self.clear()
        self.batch.draw()

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.current_screen.text_inputs:
            if widget.hit_test(x, y):
                # self.set_focus(widget)
                try:
                    widget.delete()
                except Exception:
                    pass
                del widget
                self.clear()
                self.batch.draw()
                break
        else:
            self.set_focus(None)

        # if self.focus:
            # self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                dir = -1
            else:
                dir = 1

            if self.focus in self.text_inputs:
                i = self.text_inputs.index(self.focus)
            else:
                i = 0
                dir = 0

            self.set_focus(self.text_inputs[(i + dir) % len(self.text_inputs)])

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

    def on_key_down(self, symbol, mod):
        print('Keyboard down:', symbol) # <-- Important

    def render(self):
        self.clear()
        self.batch.draw()
        self.current_screen._draw() # <-- Important, draws the current screen
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