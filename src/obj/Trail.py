from pygame import gfxdraw

class Trail:
        def __init__(self, pointA, pointB, color):
                self.color = color
                self.alpha = 255
                self.pointA = pointA
                self.pointB = pointB

                self.lifetime = 60
                self.alphaSubtract = 255 / self.lifetime


        def PhysicsUpdate(self):
                self.lifetime -= 1

                self.alpha -= self.alphaSubtract

                # check if trail is invisible, and return True so the gamemanager can remove it
                if (self.alpha <= 0):
                        return True
                return False


        def DrawUpdate(self, screen):
                gfxdraw.line(
                        screen, 
                        int(self.pointA.x), int(self.pointA.y), 
                        int(self.pointB.x), int(self.pointB.y), 
                        (*self.color, int(self.alpha))
                )