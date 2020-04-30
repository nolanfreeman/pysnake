
import pygame
import random

class Block:
    def __init__(self, pos, color, canvasdim):
        self.size = BLOCK_SIZE
        self.speedx, self.speedy = 0,0
        self.color = color
        self.posx, self.posy = self.get_random_pos(canvasdim) if pos == () else pos

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.posx, self.posy, self.size, self.size))

    def update(self):
        self.posx += self.speedx
        self.posy += self.speedy

    def move(self, xydir):
        self.speedx = xydir[0] * self.size
        self.speedy = xydir[1] * self.size

    def transport(self, coordinates):
        pass

    def get_random_pos(self, canvasdim):
        x = random.randint(canvasdim[0], canvasdim[2]) // self.size * self.size
        y = random.randint(canvasdim[1], canvasdim[3]) // self.size * self.size
        return x, y

class Snake:
    def __init__(self, pos, color, canvasdim):
        self.head = Block(pos, color, canvasdim)
        self.body = []

    def draw(self, window):
        self.head.draw(window)
        for block in self.body:
            block.draw(window)
        print(self.head.posx, self.head.posy)

    def update(self):
        self.head.update()
        for block in self.body:
            block.update()

    def move(self, xydir):
        self.head.move(xydir)

    def move_body(self):
        pass

    def add_block(self):
        pass

class Food(Block):
    def __init__(self, pos, color, canvasdim):
        super().__init__(pos, color, canvasdim)

class TextBox:
    def __init__(self, text, font, size, color, pos):
        self.text = format_text(text, font, size, color)
        self.posx, self.posy = pos

    def draw(self):
        pass

    def update(self):
        pass

    def change_color(self):
        pass

class Game:
    def __init__(self):
        self.rows, self.cols = 30, 30
        self.width, self.height = self.cols * BLOCK_SIZE, self.rows * BLOCK_SIZE + HUD_HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))

        self.canvasdim = (0, HUD_HEIGHT, self.width, self.height)

        self.running = True
        self.clock = pygame.time.Clock()

        self.theme = THEMES['default']
        self.state = 'play'

        self.num_foods = 1

        self.players = []
        self.items = []
        self.obstacles = []
        self.play()

    def main(self):
        while self.running:
            pygame.time.delay(100)
            self.clock.tick(10)

            self.update()
            self.draw()

    def draw(self):
        self.window.fill(self.theme[self.state + ' bg'])

        if self.state == 'menu':
            pass
        elif self.state == 'play':
            for player in self.players:
                player.draw(self.window)
            for item in self.items:
                item.draw(self.window)
        elif self.state == 'pause':
            pass
        elif self.state == 'gameover':
            pass

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                if self.state == 'menu':
                    pass
                if self.state == 'play':
                    self.players[0].move((-1,0))
            if keys[pygame.K_RIGHT]:
                if self.state == 'menu':
                    pass
                if self.state == 'play':
                    self.players[0].move((1,0))
            if keys[pygame.K_UP]:
                if self.state == 'menu':
                    pass
                if self.state == 'play':
                    self.players[0].move((0,-1))
            if keys[pygame.K_DOWN]:
                if self.state == 'menu':
                    pass
                if self.state == 'play':
                    self.players[0].move((0,1))
            if keys[pygame.K_SPACE]:
                if self.state == 'menu':
                    pass
                if self.state == 'play':
                    self.pause()
                if self.state == 'pause':
                    self.resume()
                if self.state == 'gameover':
                    self.play()

        for player in self.players:
            if player.head.posx < self.canvasdim[0] or player.head.posx > self.canvasdim[2] or player.head.posy < self.canvasdim[1] or player.head.posy > self.canvasdim[3]:
                self.state = 'gameover'
                self.gameover()
            player.update()
        pygame.display.update()

    def menu(self):
        self.state = 'menu'

    def play(self):
        self.players = []
        self.items = []
        self.state = 'play'
        player1 = Snake((), self.theme['player color'], self.canvasdim)
        self.players.append(player1)
        for i in range(self.num_foods):
            food = Food((), self.theme['food color'], self.canvasdim)
            self.items.append(food)

    def pause(self):
        self.state = 'pause'

    def resume(self):
        self.state = 'play'

    def gameover(self):
        self.state = 'gameover'
        self.window.fill(self.theme['gameover bg'])

# Global Constants
BLOCK_SIZE = 20
HUD_HEIGHT = 100
THEMES = {'default': {'font': 'Retro.ttf', 'player color': (0,0,0), 'food color': (255,0,0), 'play bg': (0,0,255), 'gameover bg': (0,0,0)}}
STATES = ['menu', 'play', 'paused', 'gameover']

game = Game()
game.main()

pygame.quit()
