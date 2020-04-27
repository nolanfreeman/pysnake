# game.py

DEFAULT = 'default'

font = 'Retro.ttf'

themes = {DEFAULT: {'menu_color': (0, 0, 255), 'bg_color': (0, 255, 0), 'gameover_color': (0, 0, 0), 'menu_item_selected':(255,255,255), 'menu_item_unselected':(0,0,0)}}

# states
MENU = 'menu'
PLAY = 'play'
PAUSED = 'paused'
GAMEOVER = 'gameover'

white = (255,255,255)
black = (0,0,0)

items_array_template = [
    ['normal', 'team', 'battle', 'zone'], # mode
]

from ui_text import UIText

class Game:
    def __init__(self, window):
        self.theme = themes[DEFAULT]
        self.window = window
        self.canvas_size = (800, 800)
        self.state = MENU

        self.headings = ['Mode', 'Speed', 'Wraparound', 'PowerUps', 'Obstacles', '# Food', 'Map']

        self.mode_items_array = ['normal', 'team', 'battle', 'zone']
        self.speed_items_array = ['0.75x', '1x', '1.5x', '2x']
        self.wrap_items_array =    ['on', 'off']
        self.powerup_items_array = ['on', 'off']
        self.obstacle_items_array = ['on', 'off']
        self.food_items_array = ['1', '2', '3']
        self.map_items_array = ['1', '2', '3', '4']

        self.heading_items = [self.mode_items_array, self.speed_items_array, self.wrap_items_array, self.powerup_items_array, self.obstacle_items_array, self.food_items_array, self.map_items_array]

        self.selected_heading = 0
        self.selected_item = 0
        self.prev_selected_heading = 1
        self.prev_selected_item = 1

        self.menu_headers, self.menu_items, self.menu_title = self.build_menu()

    # redraws any changes made in update
    def draw(self):
        if self.state == MENU:
            self.display_menu()
        if self.state == PLAY:
            self.display_play()
        if self.state == PAUSED:
            self.display_pause()
        if self.state == GAMEOVER:
            self.display_gameover()

    # updates logic like player location
    def update(self):
        for event in self.window.pygame.event.get():
            # Break the game loop if QUIT event arises (eg. hitting 'x' on window)
            if event.type == self.window.pygame.QUIT:
                running = False
                self.window.pygame.quit()
                break

            if self.state == MENU:
                if event.type == self.window.pygame.KEYDOWN:
                    if event.key == self.window.pygame.K_UP:
                        self.prev_selected_heading = self.selected_heading
                        self.selected_heading = self.selected_heading - 1 if self.selected_heading > 0 else len(self.headings)-1
                        self.selected_item = 0
                        self.prev_selected_item = 1
                    elif event.key == self.window.pygame.K_DOWN:
                        self.prev_selected_heading = self.selected_heading
                        self.selected_heading = self.selected_heading + 1 if self.selected_heading < len(self.headings)-1 else 0
                        self.selected_item = 0
                        self.prev_selected_item = 1
                    if event.key == self.window.pygame.K_LEFT:
                        self.prev_selected_item = self.selected_item
                        self.selected_item = self.selected_item - 1 if self.selected_item > 0 else len(self.heading_items[self.selected_heading])-1
                    elif event.key == self.window.pygame.K_RIGHT:
                        self.prev_selected_item = self.selected_item
                        self.selected_item = self.selected_item + 1 if self.selected_item < len(self.heading_items[self.selected_heading])-1 else 0
                    if event.key == self.window.pygame.K_RETURN:
                        pass
            if self.state == PLAY:
                if event.type == self.window.pygame.KEYDOWN:
                    if event.key == self.window.pygame.K_UP:
                        pass
                    elif event.key == self.window.pygame.K_DOWN:
                        pass
                    if event.key == self.window.pygame.K_LEFT:
                        pass
                    elif event.key == self.window.pygame.K_RIGHT:
                        pass
                    if event.key == self.window.pygame.K_RETURN:
                        pass
            if self.state == PAUSED:
                if event.type == self.window.pygame.KEYDOWN:
                    if event.key == self.window.pygame.K_UP:
                        pass
                    elif event.key == self.window.pygame.K_DOWN:
                        pass
                    if event.key == self.window.pygame.K_LEFT:
                        pass
                    elif event.key == self.window.pygame.K_RIGHT:
                        pass
                    if event.key == self.window.pygame.K_RETURN:
                        pass
            if self.state == GAMEOVER:
                if event.type == self.window.pygame.KEYDOWN:
                    if event.key == self.window.pygame.K_UP:
                        pass
                    elif event.key == self.window.pygame.K_DOWN:
                        pass
                    if event.key == self.window.pygame.K_LEFT:
                        pass
                    elif event.key == self.window.pygame.K_RIGHT:
                        pass
                    if event.key == self.window.pygame.K_RETURN:
                        pass

    def set_canvas_size(self, size):
        self.canvas_size = size

    def display_menu(self):
        self.window.fill(self.theme['menu_color'])

        for header in self.menu_headers:
            header.change_color(self.theme['menu_item_unselected'])
        for item in self.menu_items:
            header.change_color(self.theme['menu_item_unselected'])

        self.menu_headers[self.selected_heading].change_color(self.theme['menu_item_selected'])
        self.menu_items[self.selected_heading][self.selected_item].change_color(self.theme['menu_item_selected'])


    def display_pause(self):
        self.window.fill(self.theme['menu_color'])

    def display_play(self):
        self.window.fill(self.theme['bg_color'])

    def display_gameover(self):
        self.window.fill(self.theme['gamover_color'])

    def text_format(self, message, textFont, textSize, textColor):
        newFont=self.window.pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

    def build_menu(self):
        menu_headers = []
        menu_header_items = []

        title = UIText('PySnake', font, 150, black, 'centerx', 40, self.window)

        for header_i, header in enumerate(self.heading_items):
            new_header = UIText(self.headings[header_i], font, 75, black, self.window.width/8, 220 + (75 * header_i) + 10, self.window)
            menu_headers.append(new_header)
            menu_items = []
            for item_i, item in enumerate(header):
                new_item = UIText(self.heading_items[header_i][item_i], font, 50, black, self.window.width/8*5, 220 + (75 * header_i) + 10, self.window)
                menu_items.append(new_item)

            menu_header_items.append(menu_items)
        return (menu_headers, menu_header_items, title)
