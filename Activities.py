import pygame
pygame.init()

import MusicUtils
from enum import Enum


class ProgramState(Enum):
    MENU = 0
    VISUALIZER = 1
    GAMES = 2

class GameState(Enum):
    MENU = 0
    NOTEPICKER = 1
    ARPEGGIO = 2

def setup():
    global WIDTH, HEIGHT, SCREEN_SIZE, FONT
    global CURRENT_STATE, GAME_STATE
    global CLICK_RECTS

    pygame.init()

    WIDTH, HEIGHT = SCREEN_SIZE = (1600,900)
    CURRENT_STATE = ProgramState.MENU
    GAME_STATE = GameState.MENU
    FONT = pygame.font.SysFont(None, 24)

    # My weird way of doing callbacks. At first it was going to map rects -> funcs but rects are unhashable, so now it's the other way around.
    # Still takes O(N) to find the match, so two lists could do the same thing.
    CLICK_RECTS = {
        ProgramState.MENU: {},
        ProgramState.VISUALIZER: {},
        ProgramState.GAMES: {}
    }

def lerp(a, b, t):
    return (1 - t) * a + t * b

def draw_bass(screen):
    """
    docstring
    """
    left_h = 165
    right_h = 140
    tl = (0, (HEIGHT / 2) - (left_h / 2))
    tr = (WIDTH, (HEIGHT / 2) - (right_h / 2))
    br = (WIDTH, (HEIGHT / 2) + (right_h / 2))
    bl = (0, (HEIGHT / 2) + (left_h / 2))
    fretboard_col = (205, 179, 139)

    pygame.draw.polygon(screen, fretboard_col, (tl, tr, br, bl))

    string_interval = 1 / 5
    g_string = (0, tl[1] + left_h * (string_interval * 1)), (WIDTH, tr[1] + right_h * (string_interval * 1))
    d_string = (0, tl[1] + left_h * (string_interval * 2)), (WIDTH, tr[1] + right_h * (string_interval * 2))
    a_string = (0, tl[1] + left_h * (string_interval * 3)), (WIDTH, tr[1] + right_h * (string_interval * 3))
    e_string = (0, tl[1] + left_h * (string_interval * 4)), (WIDTH, tr[1] + right_h * (string_interval * 4))

    string_col = (60,60,60)
    string_back_col = (40,40,40)
    pygame.draw.line(screen, string_back_col, g_string[0], g_string[1], 4)
    pygame.draw.line(screen, string_col, g_string[0], g_string[1], 2)
    pygame.draw.line(screen, string_back_col, d_string[0], d_string[1], 6)
    pygame.draw.line(screen, string_col, d_string[0], d_string[1], 4)
    pygame.draw.line(screen, string_back_col, a_string[0], a_string[1], 8)
    pygame.draw.line(screen, string_col, a_string[0], a_string[1], 6)
    pygame.draw.line(screen, string_back_col, e_string[0], e_string[1], 10)
    pygame.draw.line(screen, string_col, e_string[0], e_string[1], 8)


def draw_button(surface, rect, text, onclick, state):
    """
    Draw a button with a text caption overlaid, along with a click handler

    surface -- Surface on which to draw the button
    rect -- The position and size of the button
    text -- Caption of the button, displayed in the center
    onclick -- Callback function, invoked when button is clicked
    state -- The state the application needs to be in to invoke the handler.

    Globals:
    CLICK_RECTS -- Maps rects to callback functions
    """

    # Button Rect
    pygame.draw.rect(surface, pygame.Color('white'), rect)

    # Text
    rendered_text = FONT.render(text, True, pygame.Color('black'))
    rendered_text_rect = rendered_text.get_rect(center=rect.center)
    surface.blit(rendered_text, rendered_text_rect)

    # Click handler
    CLICK_RECTS[state][onclick] = rect

def switch_to_games():
    """Change the program state to GAMES"""
    global CURRENT_STATE
    CURRENT_STATE = ProgramState.GAMES

def note_finder():
    global GAME_STATE
    GAME_STATE = GameState.NOTEPICKER

def draw_menu(surface):
    draw_button(surface, pygame.Rect(20, 20, 200, 75), "Games", switch_to_games, ProgramState.MENU)

def draw_game(surface):
    if GAME_STATE == GameState.MENU:
        draw_button(surface, pygame.Rect(20, 20, 200, 75), "Note Finder", note_finder, ProgramState.GAMES)

    elif GAME_STATE == GameState.NOTEPICKER:
        pass

def run():
    setup()

    screen = pygame.display.set_mode(SCREEN_SIZE)

    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                for func in CLICK_RECTS[CURRENT_STATE]:
                    if CLICK_RECTS[CURRENT_STATE][func].collidepoint(event.pos):
                        func()

        screen.fill((0, 0, 0))
        if CURRENT_STATE == ProgramState.MENU:
            draw_menu(screen)
        elif CURRENT_STATE == ProgramState.VISUALIZER:
            draw_bass(screen)
        elif CURRENT_STATE == ProgramState.GAMES:
            draw_game(screen)

        pygame.display.update()

if __name__ == "__main__":
    run()