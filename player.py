import sys, pygame
from game import *

pygame.init()

GREEN = 0, 200, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
BLACK = 0, 0, 0
WHITE = 255, 255, 255

game = Game()
screen = pygame.display.set_mode(game.SIZE)
pygame.display.set_caption("Racin Rodney")
clock = pygame.time.Clock()


def getRect(Obj):
    return pygame.Rect(Obj.x, Obj.y, Obj.width, Obj.length)


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        game.car.left()
    elif pressed[pygame.K_RIGHT]:
        game.car.right()
    else:
        game.car.stop()
    game.update()

    screen.fill(GREEN)
    pygame.draw.rect(screen, BLACK, pygame.Rect(game.GRASS_WIDTH, 0, game.ROAD * game.WIDTH, game.HEIGHT))
    for o in game.obstacles:
        pygame.draw.rect(screen, BLUE, getRect(o))
    pygame.draw.rect(screen, RED, getRect(game.car))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects("Score: "+str(floor(game.score)), smallText)
    textRect.center = (game.WIDTH*0.5, game.HEIGHT - 0.03 * game.HEIGHT)
    screen.blit(textSurf, textRect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
