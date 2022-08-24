import pygame
from GameManager import *
from obj.CelestialBody import *

running = True
clock = pygame.time.Clock()
gm = GameManager()

gm.AddObject(
        CelestialBody(Vector2(300, 450), 5, 3, (255, 0, 0), Vector2(0, -3))
        )

gm.AddObject(
        CelestialBody(Vector2(450, 550), 5, 3, (0, 255, 0), Vector2(5, 0))
        )

gm.AddObject(
        CelestialBody(Vector2(600, 510), 5, 3, (0, 0, 255), Vector2(0, -4))
        )

gm.AddObject(
        CelestialBody(Vector2(450, 450), 2000, 20, (255, 255, 0))
        )

while running:
        for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                        running = False

        gm.PhysicsUpdate()
        gm.DrawUpdate()
        clock.tick(60)

         