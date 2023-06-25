import datetime
import pygame

class InputViewer:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.playing_offset = 0
        self.frame = 0
        self.total_play_time_ms = 0.00
        self.input_file = "input.txt"
        self.current_line = ""
        self.file_contents = []
        self.font = pygame.font.Font("font.ttf", 25)
        self.playing = False
        self.pre_finished = False
        self.finished = False
        self.last_line = 0
        self.run = True

        self.load()

    def load(self):
        # this works only with .fm2!!

        with open(self.input_file) as f:

            contents = f.readlines()
            self.file_contents = contents

            for i in range(len(contents)):
                if contents[i].startswith("|0|"):
                    self.playing_offset = i
                    break
                else:
                    continue

            print(f"Input playing detected @ pos {self.playing_offset}, (0 is first line)")

    def draw(self):

        screen = self.screen

        screen.fill((0, 0, 0))

        y = 30

        if self.playing_offset + self.frame == self.last_line:
            self.finished = True

        if not self.pre_finished:
            screen.blit(self.font.render("  RLDUTSBA", True, (100, 100, 100)), (50, y))

        # I hate Python
        try:
            t = datetime.datetime.strptime(str(datetime.timedelta(milliseconds=self.total_play_time_ms)), "%H:%M:%S.%f")
        except ValueError:
            t = datetime.datetime.strptime(str(datetime.timedelta(milliseconds=self.total_play_time_ms)), "%H:%M:%S")

        screen.blit(self.font.render(f"           | {self.frame} / {t.strftime('%M:%S.%f')[:-3]}", True, (255, 255, 255)), (50, y))

        for i in range(30):

            try:
                line = self.file_contents[i + self.playing_offset + self.frame - 1]

                if not str(line).startswith("|0|"):
                    continue

            except IndexError as e:

                if not self.pre_finished:
                    line = "Movie end"

                    self.last_line = i + self.playing_offset + self.frame - 1
                    self.pre_finished = True
                else:
                    line = ""

            if i + self.playing_offset + self.frame - 1 == self.last_line:
                line = "Movie end"

            line = line.replace(".", " ").replace("|0|", "").replace("|||", "").replace("\n", "")

            if i == 0:
                line = f"> {line}"
            else:
                line = f"  {line}"

            screen.blit(self.font.render(line, True, (255, 255, 255)), (50, y + i * 30))

        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.run = False
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.playing = not self.playing

    def update_time(self):
        if self.playing:
            self.frame += 1

            if not self.finished:
                self.total_play_time_ms = (self.frame / (39375000 / 655171)) * 1000
