import random
import pygame
from pygame.rect import Rect


class Background:

    barSpeed = 2
    barWidth = 169
    barHeight = 556

    groundWidth = 37
    groundHeight = 60

    # creates a background with ground and bars
    def __init__(self, pygame, size):
        self.size = size
        self.pygame = pygame
        self.background = pygame.transform.scale(pygame.image.load("../images/Background.png"),
                                                 (size[0], size[1] - self.groundHeight))
        self.initGround()
        self.initBars()

    def initGround(self):
        # init ground fields
        self.ground = pygame.image.load("../images/Ground.png")
        self.grounds = []
        x = 0
        y = self.size[1] - self.groundHeight
        # create ground
        while x < self.size[0]:
            self.grounds.append([x, y])
            x += self.groundWidth

    def initBars(self):
        # init bar fields
        self.barVerticalGap = 1.2 * self.size[1]
        self.barHorizontalGap = self.size[0] / 3
        self.bar = pygame.image.load("../images/Bar.png")
        self.barFlipped = pygame.image.load("../images/BarFlipped.png")
        self.barsCoordinates = []
        # create bars
        x = self.size[0] / 4
        while x < self.size[0]:
            y = random.randint(200, self.size[1] - 100)  # random height
            self.barsCoordinates.append([x, y])
            x += self.barHorizontalGap

    # updates bars and ground
    def update(self, screen):
        screen.blit(self.background, (0, 0))
        self.updateBars(screen)
        self.updateGround(screen)

    def isCollided(self, rect):
        buffer = 7
        # check if collided with bars
        for bar in self.barsCoordinates:
            barUpRect = Rect(bar[0], bar[1] - self.barVerticalGap - buffer, self.barWidth, self.barHeight)
            barDownRect = Rect(bar[0], bar[1] + buffer, self.barWidth, self.barHeight)
            if barDownRect.colliderect(rect) or barUpRect.colliderect(rect):
                return True
        # check if collided with ground
        if rect.bottom >= self.size[1] - self.groundHeight:
            return True
        return False

    # moves bars
    # removes bars that are no longer on screen
    # adds bars about to come on screen
    def updateBars(self, screen):
        for coordinate in self.barsCoordinates:
            coordinate[0] -= self.barSpeed  # move bars left by barSpeed coordinate
            screen.blit(self.bar,  (coordinate[0], coordinate[1]))
            screen.blit(self.barFlipped, (coordinate[0], coordinate[1] - self.barVerticalGap))
        # add bar if needed
        lastBar = self.barsCoordinates[-1]
        if lastBar[0] < self.size[0]:
            x = lastBar[0] + self.barHorizontalGap
            y = random.randint(200, self.size[1] - 100)
            self.barsCoordinates.append([x, y])
        # remove bar if off screen
        if self.barsCoordinates[0][0] < -self.barWidth:
            self.barsCoordinates.pop(0)

    # moves ground
    # removes ground that is no longer on screen
    # adds ground about to come on screen
    def updateGround(self, screen):
        for coordinate in self.grounds:
            coordinate[0] -= self.barSpeed  # move ground left by barSpeed coordinate
            screen.blit(self.ground, (coordinate[0], coordinate[1]))
        lastGround = self.grounds[-1]
        # add ground if needed
        if lastGround[0] < self.size[0]:
            x = lastGround[0] + self.groundWidth
            y = self.size[1] - self.groundHeight
            self.grounds.append([x, y])
        # remove ground if off screen
        if self.grounds[0][0] < -self.groundWidth:
            self.grounds.pop(0)

    def getBarCoordinates(self):
        return self.barsCoordinates
