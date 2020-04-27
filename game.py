# game.py

DEFAULT = 'default'

font = 'Retro.ttf'

themes = {DEFAULT: {'menu_color': (0, 0, 255), 'bg_color': (0, 255, 0), 'gameover_color': (0, 0, 0)}}

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
        self.food_items_array = [1, 2, 3]
        self.map_items_array = [1, 2, 3, 4]

        self.heading_items = [self.mode_items_array, self.speed_items_array, self.wrap_items_array, self.powerup_items_array, self.obstacle_items_array, self.food_items_array, self.map_items_array]

        self.selected_heading = 0
        self.selected_item = 0

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

        print(self.selected_item)

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
                        self.selected_heading = self.selected_heading - 1 if self.selected_heading > 0 else len(self.headings)-1
                        self.selected_item = 0
                    elif event.key == self.window.pygame.K_DOWN:
                        self.selected_heading = self.selected_heading + 1 if self.selected_heading < len(self.headings)-1 else 0
                        self.selected_item = 0
                    if event.key == self.window.pygame.K_LEFT:
                        self.selected_item = self.selected_item - 1 if self.selected_item > 0 else len(self.heading_items[self.selected_heading])-1
                    elif event.key == self.window.pygame.K_RIGHT:
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

        # Alignment variables
        mode_alignment = {'y': 220, 'x_start': self.window.width/8, 'x_end': self.window.width/8*7}

        #title text
        title = self.text_format("PySnake", font, 150, (0,0,0))

        # Mode selection text
        if self.selected_heading == 0:
            mode_selector_title = self.text_format('Mode', font, 75, white)
            if self.selected_item == 0:
                normal_mode_selector = self.text_format('Normal', font, 50, white)
            else:
                normal_mode_selector = self.text_format('Normal', font, 50, black)
            if self.selected_item == 1:
                team_mode_selector = self.text_format('Team', font, 50, white)
            else:
                team_mode_selector = self.text_format('Team', font, 50, black)
            if self.selected_item == 2:
                battle_mode_selector = self.text_format('Battle', font, 50, white)
            else:
                battle_mode_selector = self.text_format('Battle', font, 50, black)
            if self.selected_item == 3:
                zone_mode_selector = self.text_format('Zone', font, 50, white)
            else:
                zone_mode_selector = self.text_format('Zone', font, 50, black)
        if self.selected_heading == 1:
            speed_selector_title = self.text_format(self.headings[1], font, 75, white)
            if self.selected_item == 0:
                speed_1_selector = self.text_format(self.heading_items[1][0], font, 50, white)
            else:
                speed_1_selector = self.text_format(self.heading_items[1][0], font, 50, black)

        #title rect
        title_rect = title.get_rect()

        # Mode selection rect
        mode_selector_title_rect = mode_selector_title.get_rect()
        normal_mode_selector_rect = normal_mode_selector.get_rect()
        team_mode_selector_rect = team_mode_selector.get_rect()
        battle_mode_selector_rect = battle_mode_selector.get_rect()
        zone_mode_selector_rect = zone_mode_selector.get_rect()

        # Speed selection rect
        speed_selector_title_rect = speed_selector_title.get_rect()
        speed_1_selector_rect = speed_1_selector.get_rect()

        #title blit
        self.window.blit(title, (self.window.width/2 - title_rect[2]/2, 40))

        # Mode selection blit
        self.window.blit(mode_selector_title, (mode_alignment['x_start'], 220 - normal_mode_selector_rect.centery))
        self.window.blit(normal_mode_selector, (self.window.width/8*3 - normal_mode_selector_rect.centerx, 225 + mode_selector_title_rect.centery - normal_mode_selector_rect.bottom))
        self.window.blit(team_mode_selector, (self.window.width/8*4.5 - team_mode_selector_rect.centerx, 225 + mode_selector_title_rect.centery - normal_mode_selector_rect.bottom))
        self.window.blit(battle_mode_selector, (self.window.width/8*5.75 - battle_mode_selector_rect.centerx, 225 + mode_selector_title_rect.centery - normal_mode_selector_rect.bottom))
        self.window.blit(zone_mode_selector, (mode_alignment['x_end'] - zone_mode_selector_rect.centerx, 225 + mode_selector_title_rect.centery - normal_mode_selector_rect.bottom))

        #Speed selection blit
        self.window.blit(speed_selector_title, (500, 500))
        self.window.blit(speed_1_selector, (600, 600))


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
