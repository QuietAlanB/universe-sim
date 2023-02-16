import pygame
from GameManager import *
from obj.CelestialBody import *

running = True
clock = pygame.time.Clock()
gm = GameManager()

gm.AddObject(
        CelestialBody(
                pos=Vector2(350, 350),
                mass=10,
                radius=3,
                color=(255, 0, 0),
                startVelocity=Vector2(0, 2)
                )
)

gm.AddObject(
        CelestialBody(
                pos=Vector2(450, 450),
                mass=500,
                radius=10,
                color=(255, 255, 0),
                startVelocity=Vector2(0, 0)
                )
)

while running:
        for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                        running = False

        pressed = pygame.key.get_pressed()

        if (pressed[pygame.K_w]): gm.Scroll(Vector2(0, 5))
        if (pressed[pygame.K_s]): gm.Scroll(Vector2(0, -5))
        if (pressed[pygame.K_a]): gm.Scroll(Vector2(5, 0))
        if (pressed[pygame.K_d]): gm.Scroll(Vector2(-5, 0))

        gm.PhysicsUpdate()
        gm.DrawUpdate()
        clock.tick(60)

         