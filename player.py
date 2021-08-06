import sys, pygame
from game import *
import animation


game = Game()
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
    failCondition = game.update()

    animation.animate(game)


pygame.quit()
quit()
