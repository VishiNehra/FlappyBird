import pygame
from pygame.rect import Rect


class Bird:
    jumpDuration = 10
    maxFlyingDuration = 15
    maxFallingDuration = 13
    width = 58
    height = 46

    # creates a bird with x, y coordinates and speed
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

        self.bird = pygame.image.load("..\images\Bird.png")
        self.direction = "down"
        self.fallingDuration = 0
        self.flyingDuration = 0
        self.previousRotation = 0

    def update(self):
        if self.direction == "up":
            self.y -= self.speed
            self._handleFlyingDuration()
        else:  # direction down
            self.y += self.speed
            self._handleFallingDuration()

    def _handleFlyingDuration(self):
        if self.flyingDuration < self.maxFlyingDuration:
            self.flyingDuration += 1
        if self.flyingDuration == self.jumpDuration:
            self.direction = "down"
            self.flyingDuration = 0

    def _handleFallingDuration(self):
        if self.fallingDuration < self.maxFallingDuration:
            self.fallingDuration += 1

    def jumpUp(self):
        self.direction = "up"
        self.flyingDuration = 0
        self.fallingDuration = 0

    def getPosition(self):
        return (self.x, self.y)

    def getRect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def getBird(self):
        # rotate bird according to how much it has fallen
        return pygame.transform.rotate(self.bird, self._calculateRotation())

    def _calculateRotation(self):
        if self.direction == "down" and self.fallingDuration >= 8:
            if self.previousRotation > -90:
                self.previousRotation -= 2 * (self.fallingDuration - 8)
            return self.previousRotation
        if self.direction == "up":
            if self.previousRotation < 0:
                self.previousRotation += 5*(self.flyingDuration)
            return self.previousRotation
        self.previousRotation = 0
        return self.previousRotation

