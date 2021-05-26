import pygame as pg

vec = pg.math.Vector2


class TextBox():
    def __init__(self, x, y, width, height, font, bg_colour=(124, 124, 124), active_colour=(255, 255, 255),
                 text_size=18, border=False, border_colour=(255, 25, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos = vec(x, y)
        self.size = vec(width, height)
        self.image = pg.Surface((width, height))
        self.bg_colour = bg_colour
        self.active_colour = active_colour
        self.active = False
        self.text = ''
        self.font = font
        self.text_size = text_size
        self.txt_col = (255, 25, 100)
        self.border = border  # int as a thickness
        self.border_colour = border_colour

    def update(self):
        pass

    def draw(self, screen):
        if not self.active:
            if self.border == 0:
                self.image.fill((124, 124, 124))
            else:
                self.image.fill(self.border_colour)
                pg.draw.rect(self.image, self.bg_colour,
                             (self.border, self.border, self.width - self.border * 2, self.height - self.border * 2))

        else:
            if self.border == 0:
                self.image.fill(self.active_colour)
            else:
                self.image.fill(self.border_colour)
                pg.draw.rect(self.image, self.active_colour,
                             (self.border, self.border, self.width - self.border * 2, self.height - self.border * 2))

        # rendering text to image
        text = self.font.render(self.text, False, self.txt_col)
        text_w = text.get_width()
        text_h = text.get_height()
        if text_w < self.width - self.border * 2:
            self.image.blit(text, (self.border * 4, (self.height - text_h) // 2))
        else:  # shifitng text
            self.image.blit(text,
                            ((self.border * 4) + (self.width - text_w - self.border * 8), (self.height - text_h) // 2))
        screen.blit(self.image, self.pos)

    def add_text(self, key):
        caps = self.CAPSLOCK_STATE()
        try:
            text = list(self.text)

            if key == 8:  # backspace
                text.pop()
            elif key == 32:  # space
                text.append(' ')
            else:
                if (caps & 0xffff) == 0:
                    text.append(chr(key))
                else:
                    text.append(chr(key).upper())
            self.text = "".join(text)
        except:
            print(key)

    def check_click(self, pos):

        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                self.active = True
            else:
                self.active = False
        else:
            self.active = False

    def return_input(self):
        return self.text

    def CAPSLOCK_STATE(self):
        import ctypes
        hllDll = ctypes.WinDLL("User32.dll")
        VK_CAPITAL = 0x14
        return hllDll.GetKeyState(VK_CAPITAL)