# ui_text.py

class ui_text:
    def __init__(self, title, font, size, color, posx, posy):
        self.text = self.text_format(title, font, size, color)
        self.rect = self.text.get_rect()
        self.blit = window.blit(self.text, (posx, posy))

    def set_color(self, color):


    def text_format(self, message, textFont, textSize, textColor):
        newFont=self.window.pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText
