# main.py

import pygame
pygame.init()

# GAME VARIABLES
WINDOW_TITLE = "PySnake by Nolan Freeman"
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 1000
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption(WINDOW_TITLE)

running = True

# Main Game Loop
while running:
    # in milliseconds TODO replace with clock
    pygame.time.delay(100)

    for event in pygame.event_get():
        # Break the game loop if QUIT event arises (eg. hitting 'x' on window)
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

# If loop is broken; quit game and close window
pygame.quit()
