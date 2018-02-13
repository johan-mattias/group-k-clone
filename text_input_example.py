__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import pyglet

__WIDTH__ = 800
__HEIGHT__ = 500
__BLACK__ = (0, 0, 0, 255)
__WHITE__ = (255, 255, 255, 255)
__RED__ = (255, 0, 0, 255)

class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch, color=__BLACK__):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', list(color) * 4)
        )

class TextWidget(object):
    def __init__(self, text, x, y, width, batch, color=__BLACK__, bg_color=__WHITE__):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
            dict(color=color)
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
                                   x + width + pad, y + height + pad, batch, color=bg_color)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

class Button(object):
    def __init__(self, x, y, width, batch, text, color=__BLACK__, bg_color=__WHITE__):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.text = text
        pad = 2
        font = self.document.get_font()
        height = font.ascent - font.descent
        self.x1 = x - pad
        self.x2 = x + width + pad
        self.y1 = y - pad
        self.y2 = y + height + pad

        pyglet.text.Label(self.text, x=x, y=y+15, anchor_y='top', anchor_x='left', font_size=10, batch=batch, color=color)

        self.rectangle = Rectangle(self.x1, self.y1,
                                   self.x2, self.y2, batch, color=bg_color)

    def hit_test(self, x, y):
        return (self.x1 <= x <= self.x2 and
                self.y1 <= y <= self.y2)

    def get_value(self):
        return self.text


class RegisterScreen():
    def __init__(self, batch, set_focus):
        self.text_input_labels = [
            pyglet.text.Label('ENTER USERNAME', x=200, y=232, anchor_y='top', font_size=10,
                              color=__WHITE__, batch=batch),
            pyglet.text.Label('ENTER PASSWORD', x=200, y=192, anchor_y='top', font_size=10,
                              color=__WHITE__, batch=batch),
            pyglet.text.Label('ENTER PASSWORD AGAIN', x=200, y=152,
                              anchor_y='top', font_size=10, color=__WHITE__,
                              batch=batch)
        ]
        self.text_inputs = [
            TextWidget(text='', x=200, y=200, width=210, batch=batch),
            TextWidget(text='', x=200, y=160, width=210, batch=batch),
            TextWidget(text='', x=200, y=120, width=210, batch=batch),
        ]

        self.buttons = [
            Button(x=330, y=80, width=80, batch=batch, text='REGISTER'),
            Button(x=200, y=80, width=80, batch=batch, text='BACK')
        ]

        set_focus(self.text_inputs[0])

    def _draw(self):
        self.draw()


class LoginScreen():
    def __init__(self, batch, set_focus):
        print('login screen!')
        self.text_input_labels = [
            pyglet.text.Label('ENTER USERNAME', x=200, y=232, anchor_y='top', font_size=10,
                              color=__WHITE__, batch=batch),
            pyglet.text.Label('ENTER PASSWORD', x=200, y=192, anchor_y='top', font_size=10,
                              color=__WHITE__, batch=batch),
        ]
        self.text_inputs = [
            TextWidget(text='', x=200, y=200, width=210, batch=batch),
            TextWidget(text='', x=200, y=160, width=210, batch=batch),
        ]

        self.buttons = [
            Button(x=330, y=80, width=80, batch=batch, text='LOGIN'),
            Button(x=200, y=80, width=80, batch=batch, text='BACK')
        ]

        set_focus(self.text_inputs[0])



class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(__WIDTH__, __HEIGHT__, caption='Text entry')

        self.batch = pyglet.graphics.Batch()
        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus = None
        self.registerscreen = RegisterScreen(batch=self.batch, set_focus=self.set_focus)
        self.loginscreen = LoginScreen(batch=self.batch, set_focus=self.set_focus)
        self.currentscreen = self.registerscreen

    def on_resize(self, width, height):
        super(Window, self).on_resize(width, height)

    def on_draw(self):
        # pyglet.gl.glClearColor(1, 1, 1, 1)
        # window.clear()
        self.clear()
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.currentscreen.text_inputs:
            if widget.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.currentscreen.text_inputs:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            for button in self.currentscreen.buttons:
                if button.hit_test(x, y):
                    print('button pressed!', button.get_value())
                    window.clear()
                    # self.currentscreen = self.loginscreen
                    # self.currentscreen._draw()
                    # self.batch.draw()
                    # self.on_draw()
                    window.flip()
                    break
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

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

            if self.focus in self.currentscreen.text_inputs:
                i = self.currentscreen.text_inputs.index(self.focus)
            else:
                i = 0
                dir = 0

            self.set_focus(self.currentscreen.text_inputs[(i + dir) % len(self.currentscreen.text_inputs)])

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)

window = Window(resizable=True)
pyglet.app.run()