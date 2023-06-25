import threading
import time
import pygame
import inputviewer

pygame.init()

NESClockFPS = 39375000 / 655171
clock = pygame.time.Clock()

size = (0, 0)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
size = screen.get_size()

iv = inputviewer.InputViewer(screen)

class PeriodicSleeper(threading.Thread):
    def __init__(self, task_function, period):
        super().__init__()
        self.task_function = task_function
        self.period = period
        self.i = 0
        self.t0 = time.time()
        self.start()

    def sleep(self):
        self.i += 1
        delta = self.t0 + self.period * self.i - time.time()
        if delta > 0:
            time.sleep(delta)

    def run(self):
        while 1:
            self.task_function()
            self.sleep()

generic_sleeper = PeriodicSleeper(iv.update_time, 1 / NESClockFPS)

run = True

while run:

    run = iv.run

    clock.tick(60)
    iv.draw()
    iv.update()

pygame.quit()