import pygame
import random
import copy
from vector2 import *
from obj.CelestialBody import CelestialBody
from obj.Particle import Particle
from obj.Trail import Trail

class GameManager:
        def __init__(self):
                self.screen = pygame.display.set_mode((900, 900))
                self.objects = []
                self.cameraPos = Vector2(0, 0)
                self.options = {
                        "GravConst": 1, # gravitational constant. used for increasing/decreasing gravitational force
                        "AttractionThreshold": 0.001, # makes it so that attraction isn't applied on objects which are far
                        "ScrollSpeed": 5 # how fast you can scroll using movement keys (WASD)
                }


        def AddObject(self, object):
                self.objects.append(object)


        def RemoveObject(self, object):
                self.objects.remove(object)


        def Explode(self, body):
                randVector = Vector2(random.uniform(-4.1, 4.1), random.uniform(-4.1, 4.1))
                self.AddObject(Particle(body.pos, 3, body.color, randVector))


        def Scroll(self, dir):
                self.cameraPos += dir


        def PhysicsUpdate(self):
                for object in self.objects:
                        if (type(object) == CelestialBody):
                                self.AddObject(Trail(object.pos, object.prevPos, object.color))

                                bodiesToRemove = object.PhysicsUpdate(self.objects, self.options)

                                # removes bodies which have collided in PhysicsUpdate
                                if (len(bodiesToRemove) > 0):
                                        for body in bodiesToRemove:
                                                self.RemoveObject(body)

                                                for i in range(10):
                                                        self.Explode(body)


                        if (type(object) == Trail or type(object) == Particle):
                                removeObj = object.PhysicsUpdate()
                                if (removeObj):
                                        self.RemoveObject(object)


        def DrawUpdate(self):
                self.screen.fill((0, 0, 0))
                
                for object in self.objects:
                        objectCopy = copy.deepcopy(object)
                        
                        if (type(object) != Trail):
                                objectCopy.pos += self.cameraPos
                        else:
                                objectCopy.pointA += self.cameraPos
                                objectCopy.pointB += self.cameraPos

                        objectCopy.DrawUpdate(self.screen)

                pygame.display.update()