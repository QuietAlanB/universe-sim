import pygame
from GameManager import *
from obj.CelestialBody import *

running = True
clock = pygame.time.Clock()
gm = GameManager()

gm.AddObject(
        CelestialBody(Vector2(400, 400), 5, 3, (255, 0, 0), Vector2(0, 0))
        )

gm.AddObject(
        CelestialBody(Vector2(450, 450), 8, 4, (0, 255, 0), Vector2(0, 0))
        )

gm.AddObject(
        CelestialBody(Vector2(350, 450), 12, 5, (0, 0, 255), Vector2(0, 0))
        )

gm.AddObject(
        CelestialBody(Vector2(400, 350), 5, 3, (255, 0, 255), Vector2(0, 0))
        )

#gm.AddObject(
#        CelestialBody(Vector2(450, 450), 2000, 20, (255, 255, 0))
#        )

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

         