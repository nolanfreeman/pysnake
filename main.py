
import pygame
import random
import math

class Block:
    def __init__(self, pos, color, canvasdim):
        self.size = BLOCK_SIZE
        self.speedx, self.speedy = 0,0
        self.color = color
        self.canvasdim = canvasdim
        self.posx, self.posy = self.get_random_pos(self.canvasdim) if pos == () else pos

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.posx, self.posy, self.size, self.size))

    def update(self):
        self.posx += self.speedx
        self.posy += self.speedy

    def move(self, xydir):
        self.speedx = xydir[0] * self.size
        self.speedy = xydir[1] * self.size

    def transport(self, coordinates):
        self.posx, self.posy = self.get_random_pos(self.canvasdim) if coordinates == () else coordinates

    def get_random_pos(self, canvasdim):
        x = random.randint(canvasdim[0], canvasdim[2]) // self.size * self.size
        y = random.randint(canvasdim[1], canvasdim[3]) // self.size * self.size
        return x, y

    def distance(self, block):
        bcenter = (block.posx+block.size/2, block.posy+block.size/2)
        self.center = (self.posx+self.size/2, self.posy+self.size/2)
        a = abs(self.center[0] - bcenter[0])
        b = abs(self.center[1] - bcenter[1])
        return math.sqrt(a**2 + b**2)

class Snake:
    def __init__(self, pos, color, canvasdim):
        self.head = Block(pos, color, canvasdim)
        self.body = []
        self.pos = pos
        self.color = color
        self.canvasdim = canvasdim

    def draw(self, window):
        self.head.draw(window)
        for block in self.body:
            block.draw(window)

    def update(self):
        self.move_body()
        self.head.update()
        for block in self.body:
            block.update()

    def move(self, xydir):
        self.head.move(xydir)

    def move_body(self):
        for i in range(len(self.body), 0, -1):
            if i == 1:
                self.body[i-1].posx = self.head.posx
                self.body[i-1].posy = self.head.posy
            else:
                self.body[i-1].posx = self.body[i-2].posx
                self.body[i-1].posy = self.body[i-2].posy

    def add_block(self):
        new_block = Block((self.head.posx, self.head.posy), self.color, self.canvasdim)
        self.body.append(new_block)

    def distance(self, block):
        return self.head.distance(block)

    def body_collision(self):
        for block in self.body:
            if self.head.distance(block) < BLOCK_SIZE:
                 return True
            else:
                return False
        return False

class Food(Block):
    def __init__(self, pos, color, canvasdim):
        super().__init__(pos, color, canvasdim)

class TextBox:
    def __init__(self, text, font, size, color, pos, window):
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.posx, self.posy = pos
        self.window = window

        self.styled = pygame.font.Font(self.font, self.size)
        self.rendered = self.styled.render(self.text, 0, self.color)
        self.rect = self.rendered.get_rect()

        if self.posx == 'center':
            self.posx = self.window.get_width()/2 - self.rect[2]/2
        elif self.posx == 'margin-left':
            self.posx = 50
        elif self.posx == 'margin-right-center':
            self.posx = self.window.get_width() - 50 - self.rect.width

    def draw(self):
        self.blit = self.window.blit(self.rendered, (self.posx, self.posy))

    def update(self):
        pass

    def change_color(self, color):
        self.rendered = self.styled.render(self.text, 0, color)

    def change_text(self, text):
        self.rendered = self.styled.render(text, 0, self.color)

class Game:
    def __init__(self):
        self.selected_map = MAPS[0]
        self.rows, self.cols = self.selected_map
        self.width, self.height = self.cols * BLOCK_SIZE, self.rows * BLOCK_SIZE + HUD_HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))

        self.canvasdim = (0, HUD_HEIGHT, self.width, self.height)

        self.running = True
        self.clock = pygame.time.Clock()

        self.theme = THEMES['default']
        self.state = 'play'
        self.score = 0
        self.highscore = 0

        self.num_foods = 1
        self.speed = 1

        self.players = []
        self.items = []
        self.obstacles = []

        self.menu_headers = []
        self.menu_items = []

        self.menu()

    def main(self):
        while self.running:
            pygame.time.delay(math.floor(60 / self.speed))
            self.clock.tick(10)

            self.update()
            self.draw()

    def draw(self):
        self.window.fill(self.theme[self.state + ' bg'])

        if self.state == 'menu':
            for header in self.menu_headers:
                if self.headings[self.selected_header] == header.text:
                    header.change_color(self.theme['menu item selected'])
                else:
                    header.change_color(self.theme['menu title color'])
                header.draw()
            for i, item in enumerate(self.menu_items):
                item[self.selected_items[i]].draw()
        elif self.state == 'play':
            # draw HUD
            pygame.draw.rect(self.window, self.theme['hud bg color'], (0, 0, self.width, self.canvasdim[1]))
            self.score_text.change_text("Score: " + str(self.score))
            self.score_text.draw()
            self.highscore_text.change_text("Highscore: " + str(self.highscore))
            self.highscore_text.draw()

            for item in self.items:
                item.draw(self.window)
            for player in self.players:
                player.draw(self.window)
        elif self.state == 'pause':
            pass
        elif self.state == 'gameover':
            self.gameover_text.draw()
            self.finalscore_text.draw()
            self.gameover_press_space_text.draw()
            self.gameover_press_M_text.draw()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_a]:
                if self.state == 'menu':
                    self.selected_items[self.selected_header] = self.selected_items[self.selected_header] + 1 if self.selected_items[self.selected_header] < len(self.menu_items[self.selected_header])-1 else 0
                if self.state == 'play':
                    self.players[0].move((-1,0))
            if keys[pygame.K_d]:
                if self.state == 'menu':
                    self.selected_items[self.selected_header] = self.selected_items[self.selected_header] - 1 if self.selected_items[self.selected_header] > 0 else len(self.menu_items[self.selected_header])-1
                if self.state == 'play':
                    self.players[0].move((1,0))
            if keys[pygame.K_w]:
                if self.state == 'menu':
                    self.selected_header = self.selected_header - 1 if self.selected_header > 0 else len(self.headings)-1
                if self.state == 'play':
                    self.players[0].move((0,-1))
            if keys[pygame.K_s]:
                if self.state == 'menu':
                    self.selected_header = self.selected_header + 1 if self.selected_header < len(self.headings)-1 else 0
                if self.state == 'play':
                    self.players[0].move((0,1))
            if keys[pygame.K_SPACE]:
                if self.state == 'menu':
                    self.mode = self.selected_items[0]
                    if self.selected_items[1] == 0:
                        self.speed = 0.5
                    if self.selected_items[1] == 1:
                        self.speed = 1
                    if self.selected_items[1] == 2:
                        self.speed = 1.5
                    if self.selected_items[1] == 3:
                        self.speed = 2
                    self.wraparound_on = self.selected_items[2]
                    self.powerups_on = self.selected_items[3]
                    self.obstacles_on = self.selected_items[4]
                    self.num_foods = self.selected_items[5] + 1
                    self.selected_map = MAPS[self.selected_items[6]]
                    self.rows, self.cols = self.selected_map
                    self.width, self.height = self.cols * BLOCK_SIZE, self.rows * BLOCK_SIZE + HUD_HEIGHT
                    self.window = pygame.display.set_mode((self.width, self.height))
                    self.canvasdim = (0, HUD_HEIGHT, self.width, self.height)
                    self.play()
                if self.state == 'play':
                    self.pause()
                if self.state == 'pause':
                    self.resume()
                if self.state == 'gameover':
                    self.play()
            if keys[pygame.K_m]:
                if self.state == 'gameover':
                    self.menu()

        if self.state == 'play':
            for player in self.players:
                if player.head.posx < self.canvasdim[0] or player.head.posx > self.canvasdim[2] or player.head.posy < self.canvasdim[1] or player.head.posy > self.canvasdim[3]:
                    self.gameover()
                if player.body_collision():
                    self.gameover()
                for item in self.items:
                    if player.distance(item) < BLOCK_SIZE:
                        item.transport(())
                        if isinstance(item, Food):
                            player.add_block()
                            self.score += int(10 * self.speed)
                            if self.score > self.highscore:
                                self.highscore = self.score

            player.update()
        pygame.display.update()

    def menu(self):
        self.state = 'menu'
        self.selected_items = [0,1,0,0,0,1,0]
        self.selected_header = 0
        self.menu_items = []

        title = TextBox(MENU_TEXT['title'], self.theme['font'], 150, self.theme['menu title color'], ('center', 10), self.window)
        self.headings = ['Mode', 'Speed', 'Wraparound', 'Power Ups', 'Obstacles', 'Num Food', 'Map']
        ypos = 10+150+10
        for heading_i, heading in enumerate(self.headings):
            heading_box = TextBox(heading, self.theme['font'], 75, self.theme['menu title color'], ('margin-left', ypos), self.window)
            self.menu_headers.append(heading_box)
            array_of_menu_items = []
            for item in MENU_TEXT[heading]:
                item_box = TextBox(item, self.theme['font'], 75, self.theme['menu title color'], ('margin-right-center', ypos), self.window)
                array_of_menu_items.append(item_box)

            self.menu_items.append(array_of_menu_items)
            ypos += 75

        self.menu_headers.append(title)

    def play(self):
        self.players = []
        self.items = []
        self.state = 'play'
        player1 = Snake((), self.theme['player color'], self.canvasdim)
        self.players.append(player1)
        for i in range(self.num_foods):
            food = Food((), self.theme['food color'], self.canvasdim)
            self.items.append(food)
        self.highscore_text = TextBox("Highscore: " + str(self.highscore), self.theme['font'], 50, (0,0,0), ('margin-right-center', 5), self.window)
        self.score_text = TextBox("Score: " + str(self.score), self.theme['font'], 50, (0,0,0), ('margin-right-center', 50), self.window)

    def pause(self):
        self.state = 'pause'



    def resume(self):
        self.state = 'play'

    def gameover(self):
        self.state = 'gameover'
        self.window.fill(self.theme['gameover bg'])
        print(self.score)
        self.gameover_text = TextBox("Game Over", self.theme['font'], 150, (255,255,255), ('center', self.height/2 - 75), self.window)
        self.finalscore_text = TextBox("Final Score: " + str(self.score), self.theme['font'], 50, (255,255,255), ('center', self.height/2 + 75), self.window)
        self.gameover_press_space_text = TextBox("Press SPACE to play again", self.theme['font'], 40, (255,255,255), ('center', self.height/2 + 180), self.window)
        self.gameover_press_M_text = TextBox("Press M for Menu", self.theme['font'], 40, (255,255,255), ('center', self.height/2 + 225), self.window)
        self.gameover_text.draw()
        self.finalscore_text.draw()
        self.gameover_press_space_text.draw()
        self.gameover_press_M_text.draw()

        self.score = 0

# Global Constants
BLOCK_SIZE = 20
HUD_HEIGHT = 100
THEMES = {'default': {'font': 'Retro.ttf', 'player color': (0,0,0), 'food color': (255,0,0), 'menu title color': (0,0,0), 'menu bg': (100,100,100), 'play bg': (0,0,255), 'gameover bg': (0,0,0), 'hud bg color': (0,0,150), 'menu item selected': (255,255,255)}}
STATES = ['menu', 'play', 'paused', 'gameover']

MENU_TEXT = {'title': 'PySnake', 'Mode': ['Normal', 'Team', 'Battle', 'Zone'], 'Speed': ['0.5x', '1x', '1.5x', '2x'], 'Wraparound': ['off', 'on'], 'Power Ups': ['off', 'on'], 'Obstacles': ['off', 'on'], 'Num Food': ['1', '2', '3'], 'Map': ['1', '2', '3', '4']}
MAPS = [(30, 30), (50, 50), (50, 25), (80, 80)]

pygame.init()
game = Game()
game.main()

pygame.quit()
