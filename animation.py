import sys, pygame
from game import *

pygame.init()

GREEN = 0, 200, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
BLACK = 50, 50, 50
WHITE = 255, 255, 255
YELLOW = 175, 175, 0

pygame.display.set_caption("Racin Rodney")
clock = pygame.time.Clock()
carImg = pygame.image.load("assets/car.png")
coneImg = pygame.image.load("assets/cone.png")

def getRect(Obj):
    return pygame.Rect(Obj.x, Obj.y, Obj.width, Obj.length)


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


def animate(game):
    screen = pygame.display.set_mode(game.SIZE)
    DIVIDER_WIDTH = game.GRASS_WIDTH * 0.3

    screen.fill(GREEN)
    pygame.draw.rect(screen, BLACK, pygame.Rect(game.GRASS_WIDTH, 0, game.ROAD * game.WIDTH, game.HEIGHT))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(0.5 * (game.WIDTH - DIVIDER_WIDTH), 0, DIVIDER_WIDTH, game.HEIGHT))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(0.5 * (game.WIDTH + DIVIDER_WIDTH), 0, DIVIDER_WIDTH, game.HEIGHT))
    for r in game.rows:
        for o in r:
            # pygame.draw.rect(screen, BLUE, getRect(o))
            screen.blit(coneImg, getRect(o))
    # pygame.draw.rect(screen, RED, getRect(game.car))
    screen.blit(carImg, getRect(game.car))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects("Score: " + str(floor(game.score)), smallText)
    textRect.center = (game.WIDTH * 0.5, game.HEIGHT - 0.03 * game.HEIGHT)
    screen.blit(textSurf, textRect)

    pygame.display.update()
    clock.tick(60)