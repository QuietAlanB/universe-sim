from pygame import gfxdraw

class Particle:
        def __init__(self, pos, radius, color, vel):
                self.pos = pos
                self.radius = radius
                self.color = color
                self.vel = vel

                self.lifetime = 180
                self.colorSubtract = 255 / self.lifetime

        
        def PhysicsUpdate(self):
                self.pos += self.vel
                self.lifetime -= 1

                self.color = [
                        self.color[0] - self.colorSubtract,
                        self.color[1] - self.colorSubtract,
                        self.color[2] - self.colorSubtract
                ]

                # check if any RGB values are below 0 and correct it
                for i in range(len(self.color)):
                        if (self.color[i] < 0):
                                self.color[i] = 0

                # check if particle is invisible, and return True so the gamemanager can remove it
                if (self.lifetime == 0):
                        return True
                return False


        def DrawUpdate(self, screen):
                gfxdraw.circle(
                        screen, 
                        int(self.pos.x), int(self.pos.y), 
                        int(self.radius), 
                        (int(self.color[0]), int(self.color[1]), int(self.color[2]))
                )