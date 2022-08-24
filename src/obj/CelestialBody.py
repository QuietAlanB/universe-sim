from pygame import gfxdraw
from vector2 import *

class CelestialBody:
        def __init__(self, pos, mass, radius, color, startVelocity = Vector2(0, 0)):
                self.pos = pos
                self.mass = mass
                self.radius = radius
                self.color = color
                self.velocity = startVelocity

                self.prevPos = self.pos


        def PhysicsUpdate(self, objects, options):
                self.prevPos = self.pos
                G = options["GravConst"]
                attractionThreshold = options["AttractionThreshold"]
                bodiesToRemove = []

                for otherBody in objects:
                        if (otherBody != self and type(otherBody) == CelestialBody):
                                self.Attract(otherBody, G, attractionThreshold)

                                # when a collision is detected, the body is added to a "bodies to remove list" *
                                collision = self.Collide(otherBody)
                                if (collision):
                                        bodiesToRemove.append(otherBody)

                self.pos += self.velocity

                # * the list is returned and sent to the gamemanager to remove the bodies
                if (len(bodiesToRemove) != 0):
                        bodiesToRemove.append(self)

                return bodiesToRemove


        def Attract(self, body, G, attractionThreshold):
                try:
                        sqrDst = sqrMagnitude(body.pos - self.pos)
                        forceDir = normalized(body.pos - self.pos)
                        force = forceDir * G * self.mass * body.mass / sqrDst
                        acc = force / self.mass

                        if magnitude(acc) < attractionThreshold:
                                return

                        self.velocity += acc

                except ZeroDivisionError:
                        self.velocity = Vector2(0, 0)    


        def Collide(self, body):
                distance = magnitude(body.pos - self.pos)
                if (distance < self.radius + body.radius):
                        return True
                return False


        def DrawUpdate(self, screen):
                gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.color)
                gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.color)