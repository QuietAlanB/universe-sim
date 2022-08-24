import pygame
from GameManager import *
from obj.CelestialBody import *

running = True
clock = pygame.time.Clock()
gm = GameManager()



while running:
        for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                        running = False

        pressed = pygame.key.get_pressed()

        if (pressed[pygame.K_w]): gm.Scroll(Vector2(0, 1))
        if (pressed[pygame.K_s]): gm.Scroll(Vector2(0, -1))
        if (pressed[pygame.K_a]): gm.Scroll(Vector2(1, 0))
        if (pressed[pygame.K_d]): gm.Scroll(Vector2(-1, 0))

        gm.PhysicsUpdate()
        gm.DrawUpdate()
        clock.tick(60)

         