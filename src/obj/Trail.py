from pygame import gfxdraw

class Trail:
        def __init__(self, pointA, pointB, color):
                self.color = color
                self.pointA = pointA
                self.pointB = pointB

                self.lifetime = 60
                self.colorSubtract = 255 / self.lifetime


        def PhysicsUpdate(self):
                self.lifetime += 1

                self.color = [
                        self.color[0] - self.colorSubtract,
                        self.color[1] - self.colorSubtract,
                        self.color[2] - self.colorSubtract
                ]

                # check if any RGB values are below 0 and correct it
                for i in range(len(self.color)):
                        if (self.color[i] < 0):
                                self.color[i] = 0

                # check if trail is invisible, and return True so the gamemanager can remove it
                if (self.color == [0, 0, 0]):
                        return True
                return False




        def DrawUpdate(self, screen):
                gfxdraw.line(
                        screen, 
                        int(self.pointA.x), int(self.pointA.y), 
                        int(self.pointB.x), int(self.pointB.y), 
                        (int(self.color[0]), int(self.color[1]), int(self.color[2]))
                )