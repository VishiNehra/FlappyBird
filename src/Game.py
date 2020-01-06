import pygame

from src.Background import Background
from src.Bird import Bird


class Game:
    _fps = 144
    _size = (1320, 620)

    def __init__(self):
        self.pygame = pygame
        self.screen = self.pygame.display.set_mode(self._size)
        self.score = 0

        self.background = Background(self.pygame, self._size)
        self.bird = Bird(self._size[0] / 10, self._size[1] / 3, 8)

    def run(self):
        self.pygame.init()
        while True:
            self.handleKeys()
            self.bird.update()
            if self.background.isCollided(self.bird.getRect()):  # if collision happened
                break
            self.updateScreen()
            self.pygame.time.Clock().tick(self._fps)
        self.endScreen()

    def endScreen(self):
        print('lel  ')

    # handles bird jumping and game quitting
    def handleKeys(self):
        for event in self.pygame.event.get():  # read all key events
            if event.type == pygame.QUIT:
                self.pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jumpUp()

    # updates position of background and bird, and updates score
    def updateScreen(self):
        self.background.update(self.screen)
        self.screen.blit(self.bird.getBird(), self.bird.getPosition())
        self.updateAndDisplayScore()
        self.pygame.display.update()

    def updateAndDisplayScore(self):
        bird = self.bird.getPosition()
        buffer = 2
        for bar in self.background.getBarCoordinates():
            barX = bar[0] + self.background.barWidth
            # if bar's x coordinate is same as bird's
            if barX < bird[0] < barX + buffer:
                self.score += 1
        # display font
        font = self.pygame.font.SysFont('tlwgtypo', 80)
        text = font.render(str(self.score), True, (0, 35, 122), self.screen)
        self.screen.blit(text, (self._size[0] / 2, self._size[1] / 10))
