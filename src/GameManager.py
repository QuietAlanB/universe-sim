import pygame
from obj.CelestialBody import CelestialBody
from obj.Trail import Trail

class GameManager:
        def __init__(self):
                self.screen = pygame.display.set_mode((900, 900))
                self.objects = []
                self.options = {
                        "GravConst": 1, # gravitational constant. used for increasing/decreasing gravitational force
                        "AttractionThreshold": 0.01 # makes it so that attraction isn't applied on objects which are far
                }


        def AddObject(self, object):
                self.objects.append(object)


        def RemoveObject(self, object):
                self.objects.remove(object)


        def PhysicsUpdate(self):
                for object in self.objects:
                        if (type(object) == CelestialBody):
                                self.AddObject(Trail(object.pos, object.prevPos, object.color))

                                bodiesToRemove = object.PhysicsUpdate(self.objects, self.options)

                                # removes bodies which have collided in PhysicsUpdate
                                if (len(bodiesToRemove) > 0):
                                        for body in bodiesToRemove:
                                                self.RemoveObject(body)

                        if (type(object) == Trail):
                                removeTrail = object.PhysicsUpdate()
                                
                                if (removeTrail):
                                        self.RemoveObject(object)


        def DrawUpdate(self):
                self.screen.fill((0, 0, 0))
                
                for object in self.objects:
                        object.DrawUpdate(self.screen)

                pygame.display.update()