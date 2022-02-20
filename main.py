import pygame
from pygame import gfxdraw
from vector2 import *
import math
import random
import enum

pygame.init()

# ================= celestial body class =================
class CelestialBody:
    def __init__(self, pos, mass, velocity, radius = None, color = (255, 255, 255), showTrail = True):
        self.pos = pos
        self.lastPos = Vector2(self.pos.x, self.pos.y)
        self.mass = mass
        self.velocity = velocity
        self.color = color
        self.showTrail = showTrail
        
        

        if radius != None:
            self.radius = radius
        else:
            self.radius = math.sqrt(mass) * 2


    def drawUpdate(self):
        gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), self.radius, self.color)
        gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), self.radius, self.color)


    def velocityUpdate(self, timeStep):
        for otherBody in bodies:
            if otherBody != self:
                try:
                    sqrDst = (otherBody.pos - self.pos).sqrMagnitude()
                    forceDir = (otherBody.pos - self.pos).normalized()
                    force = forceDir * G * self.mass * otherBody.mass / sqrDst
                    acc = force / self.mass

                    if acc.magnitude() < attractionThreshold:
                        continue

                    self.velocity += acc * timeStep

                except ZeroDivisionError:
                    self.velocity = Vector2(0, 0)

    def positionUpdate(self, timeStep):
        self.lastPos = Vector2(self.pos.x, self.pos.y)
        self.pos += self.velocity * timeStep

    def collisionUpdate(self):
        for otherBody in bodies:
            if otherBody == self:
                continue

            if (abs(otherBody.pos - self.pos)).magnitude() < (otherBody.radius + self.radius):    

                # === low size, low vel ===

                


                self.velocity /= 10


    def fixedUpdate(self):
        self.velocityUpdate(timeStep)
        self.positionUpdate(timeStep)
                

# ================= font class =================
class Font:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.font = pygame.font.Font(name, size)
 
        
# ================= text class =================
class Text:
    def __init__(self, string, pos, color, font, lineSpacing = 10):
        self.string = str(string).split("\n")
        self.lines = len(self.string)
        self.pos = pos
        self.color = color
        self.font = font
        self.lineSpacing = lineSpacing

    def update(self):
        self.lines = len(self.string)

        yPosOffset = 0

        for line in self.string:
            line = self.font.font.render(line, True, self.color)
            screen.blit(line, (self.pos.x, self.pos.y + yPosOffset))

            yPosOffset += self.font.size + self.lineSpacing


# ================= fade rect class =================
class Trail:
    def __init__(self, pos1, pos2, color, fadeAmount):
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = color
        self.fadeAmount = fadeAmount

    def fadeOut(self):
        self.color = [self.color[0], self.color[1], self.color[2], self.color[3] - self.fadeAmount]
        if self.color[3] <= 0:
            self.color[3] = 0
            trails.remove(self)
                
    def update(self):
        gfxdraw.line(trailScreen, int(self.pos1.x), int(self.pos1.y), int(self.pos2.x), int(self.pos2.y), tuple(self.color))


# ================= particle class =================
class Particle:
    def __init__(self, pos, color, size, velocity, lifetime):
        self.pos = pos
        self.color = color
        self.size = size
        self.velocity = velocity
        self.lifetime = lifetime * framerate

        self.loseAmount = self.color[3] / self.lifetime

    def posUpdate(self):
        self.pos += self.velocity

    def lifeUpdate(self):
        self.color[3] -= self.loseAmount
        self.lifetime -= 1

        if self.lifetime <= 0:
            particles.remove(self)

    def drawUpdate(self):
        gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), self.size, self.color)
        gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), self.size, self.color)

    def update(self):
        self.posUpdate()
        self.lifeUpdate()


# ======== functions and other stuff =========
def addParticle(pos, color, size, velocity, lifetime):
    particles.append(Particle(pos, color, size, velocity, lifetime))

def addBody(pos, mass, velocity, radius, color):
    bodies.append(CelestialBody(pos, mass, velocity, radius, color))


# ===== save maps ======
def saveMap(name):
    # file format:
    # BODY
    # <xpos> <ypos>
    # <mass>
    # <xvel> <yvel>
    # <radius>
    # <Rcolor> <Gcolor> <Bcolor>

    try:
        file = open(f"maps/{name}.bm", "x", -1, "utf-8")

        # ===== celestial bodies =====
        for body in bodies:
            file.write("BODY\n")
            file.write(f"{body.pos.x} {body.pos.y}\n")
            file.write(f"{body.mass}\n")
            file.write(f"{body.velocity.x} {body.velocity.y}\n")
            file.write(f"{body.radius}\n")
            file.write(f"{body.color[0]} {body.color[1]} {body.color[2]}\n")
        file.close()

    except FileExistsError:
        raise FileExistsError("The map name already exists")
    

# ===== load maps ======
def loadMap(name):
    try:
        file = open(f"maps/{name}.bm", "r", -1, "utf-8")
        lines = file.readlines()
        continueAmount = 0

        for i in range(len(lines)):
            if continueAmount > 0:
                continueAmount -= 1
                continue

            lines[i] = lines[i].strip("\n")

            # ===== celestial bodies =====
            if lines[i] == "BODY":
                pos = Vector2(int(lines[i + 1].split(" ")[0]), int(lines[i + 1].split(" ")[1]))
                mass = int(lines[i + 2])
                velocity = Vector2(int(lines[i + 3].split(" ")[0]), int(lines[i + 3].split(" ")[1]))
                radius = int(lines[i + 4])
                color = ( int(lines[i + 5].split(" ")[0]), int(lines[i + 5].split(" ")[1]), int(lines[i + 5].split(" ")[2]) )
                addBody(pos, mass, velocity, radius, color)
                continueAmount = 5

    except FileNotFoundError:
        raise FileNotFoundError("That map name does not exist")


# ======== pygame variables ========
running = True
framerate = 60
clock = pygame.time.Clock()
screenSize = Vector2(1900, 1000)
screen = pygame.display.set_mode((screenSize.x, screenSize.y))
trailScreen = pygame.Surface((screenSize.x, screenSize.y), pygame.SRCALPHA)


# ======== other variables ========
# === universe variables ===
dt = 0
bodies = []
G = 1
timeStep = 1
maxDistance = 1000000

# === fade ===
fadeAmount = 1
trails = []

# === scroll ===
scrollSpeed = 10
defaultScrollSpeed = scrollSpeed

# === threshold ===
attractionThreshold = 0.0015

# === particles ===
particles = []

# === size related vars ===
sizeThresholds = {
    "small": 0,
    "medium": 0,
    "large": 0,
    "very large": 0
}

velThresholds = {
    "small": 0,
    "medium": 0,
    "large": 0,
    "very large": 0
}

# solar system 1
addBody(Vector2(600, 600), 20000, Vector2(0, 0), 20, (255, 0, 0))
addBody(Vector2(1000, 600), 20, Vector2(0, 7), 5, (0, 200, 125))

# solar system 2
addBody(Vector2(4000, 600), 20000, Vector2(-0.5, 0), 20, (255, 0, 255))
addBody(Vector2(3600, 600), 15, Vector2(0, -5), 5, (255, 125, 0))

# ======== main loop ========
while running:
    pressed = pygame.key.get_pressed()
    mousePos = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    initialPos = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pressed[pygame.K_LSHIFT]: scrollSpeed = defaultScrollSpeed * 2.5
    else: scrollSpeed = defaultScrollSpeed

    trailScreen.fill((0, 0, 0, 0))
    screen.fill((0, 0, 0))


    # ======= trail updates =======
    for trail in trails:
        if pressed[pygame.K_w]: 
            trail.pos1.y += scrollSpeed
            trail.pos2.y += scrollSpeed
        if pressed[pygame.K_a]: 
            trail.pos1.x += scrollSpeed
            trail.pos2.x += scrollSpeed
        if pressed[pygame.K_s]: 
            trail.pos1.y -= scrollSpeed
            trail.pos2.y -= scrollSpeed
        if pressed[pygame.K_d]: 
            trail.pos1.x -= scrollSpeed
            trail.pos2.x -= scrollSpeed

        trail.fadeOut()
        trail.update()


    # ======= body updates =======
    for body in bodies:
        if body.pos.x > maxDistance or body.pos.y > maxDistance or body.pos.x < -maxDistance or body.pos.y < -maxDistance:
            bodies.remove(body)
            continue

        if pressed[pygame.K_w]:
            body.pos.y += scrollSpeed
            body.lastPos.y += scrollSpeed
        if pressed[pygame.K_a]: 
            body.pos.x += scrollSpeed
            body.lastPos.x += scrollSpeed
        if pressed[pygame.K_s]: 
            body.pos.y -= scrollSpeed
            body.lastPos.y -= scrollSpeed
        if pressed[pygame.K_d]: 
            body.pos.x -= scrollSpeed
            body.lastPos.x -= scrollSpeed

        if body.showTrail:
            trails.append(Trail(Vector2(body.pos.x, body.pos.y), Vector2(body.lastPos.x, body.lastPos.y), [body.color[0], body.color[1], body.color[2], 255], fadeAmount))

        body.fixedUpdate()
        body.collisionUpdate()
        body.drawUpdate()


    # ======= particle updates =======
    for particle in particles:
        if pressed[pygame.K_w]: particle.pos.y += scrollSpeed
        if pressed[pygame.K_a]: particle.pos.x += scrollSpeed
        if pressed[pygame.K_s]: particle.pos.y -= scrollSpeed
        if pressed[pygame.K_d]: particle.pos.x -= scrollSpeed

        particle.update()
        particle.drawUpdate()

    screen.blit(trailScreen, (0, 0))

    pygame.display.update()
    clock.tick(framerate)
