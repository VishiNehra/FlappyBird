import random
import pygame
from pygame.rect import Rect

from src.Bird import Bird


class Game:
    _color = (78, 192, 202)
    _size = (1320, 620)
    _fps = 144

    barSpeed = 2
    barWidth = 169
    barHeight = 556
    barVerticalGap = 1.2 * _size[1]
    barHorizontalGap = _size[0] / 3

    groundWidth = 37
    groundHeight = 60

    def __init__(self):
        # init screen
        self.pygame = pygame
        self.screen = self.pygame.display.set_mode(self._size)
        self.background = self.pygame.transform.scale(self.pygame.image.load("..\images\Background.png"),
                                                      (self._size[0], self._size[1] - self.groundHeight))
        # init bird
        self.bird = Bird(self._size[0] / 10, self._size[1] / 3, 8)

        self.initGround()
        self.initBars()

    def initGround(self):
        self.ground = self.pygame.image.load("..\images\Ground.png")
        self.grounds = []
        x = 0
        y = self._size[1] - self.groundHeight
        while x < self._size[0]:
            self.grounds.append([x, y])
            x += self.groundWidth


    def initBars(self):
        self.bar = self.pygame.image.load("..\images\Bar.png")
        self.barFlipped = self.pygame.image.load("..\images\BarFlipped.png")
        self.barsCoordinates = []
        x = self._size[0] / 4
        while x < self._size[0]:
            y = random.randint(200, self._size[1] - 100)  # random height
            self.barsCoordinates.append([x, y])
            x += self.barHorizontalGap

    def run(self):
        self.pygame.init()
        while True:
            self.handleKeys()
            self.bird.update()
            if self.handleCollisions():  # if collision happened
                break
            self.updateScreen()
            self.pygame.time.Clock().tick(self._fps)  # at most 60 fps

    def handleKeys(self):
        for event in self.pygame.event.get():  # read all key events
            if event.type == pygame.QUIT:
                self.pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jumpUp()

    # handles collision and returns True if collision took place
    def handleCollisions(self):
        birdRect = self.bird.getRect()
        buffer = 7
        for bar in self.barsCoordinates:
            barUpRect = Rect(bar[0], bar[1] - self.barVerticalGap - buffer, self.barWidth, self.barHeight)
            barDownRect = Rect(bar[0], bar[1] + buffer, self.barWidth, self.barHeight)
            if barDownRect.colliderect(birdRect) or barUpRect.colliderect(birdRect):
                myfont = pygame.font.SysFont('Comic Sans MS', 30)
                textsurface = myfont.render('Get REKT', False, (255, 255, 255), self.screen)
                self.screen.blit(textsurface, (self._size[0]/2, self._size[1]/2))
                return True
        return False

    def updateScreen(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.bird.getBird(), self.bird.getPosition())
        self.updateBars()
        self.updateGround()
        self.pygame.display.update()

    def updateBars(self):
        for coordinate in self.barsCoordinates:
            coordinate[0] -= self.barSpeed  # move bars left by barSpeed coordinate
            self.screen.blit(self.bar,  (coordinate[0], coordinate[1]))
            self.screen.blit(self.barFlipped, (coordinate[0], coordinate[1] - self.barVerticalGap))
        # add bar if needed
        lastBar = self.barsCoordinates[-1]
        if lastBar[0] < self._size[0]:
            x = lastBar[0] + self.barHorizontalGap
            y = random.randint(200, self._size[1] - 100)
            self.barsCoordinates.append([x, y])
        # remove bar if off screen
        if self.barsCoordinates[0][0] < -self.barWidth:
            self.barsCoordinates.pop(0)

    def updateGround(self):
        for coordinate in self.grounds:
            coordinate[0] -= self.barSpeed  # move ground left by barSpeed coordinate
            self.screen.blit(self.ground, (coordinate[0], coordinate[1]))
        lastGround = self.grounds[-1]
        # add ground if needed
        if lastGround[0] < self._size[0]:
            x = lastGround[0] + self.groundWidth
            y = self._size[1] - self.groundHeight
            self.grounds.append([x, y])
        # remove ground if off screen
        if self.grounds[0][0] < -self.groundWidth:
            self.grounds.pop(0)
