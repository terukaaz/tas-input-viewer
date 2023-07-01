import datetime
import pygame

def get_inputs(line):

    inputs = line.split("|")

    real_inputs = []

    for input in inputs:
        if input == "" or input == "0" or input == "1" or input == "2" or input == "3" or input == "4" or input == "\n":
            continue

        real_inputs.append(input)

    return real_inputs

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
        self.player_count = 1
        self.run = True

        self.load()

    def load(self):

        # this works only with .fm2!!

        with open(self.input_file) as f:

            contents = f.readlines()
            self.file_contents = contents

            for i in range(len(contents)):
                if contents[i].endswith("||\n"):
                    self.playing_offset = i
                    self.player_count = get_inputs(contents[i]).__len__()
                    print(self.player_count)
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

        if not self.finished:
            for k in range(self.player_count):
                screen.blit(self.font.render("RLDUTSBA", True, (100, 100, 100)), (80 + (k * 170), y))

        # I hate Python
        try:
            t = datetime.datetime.strptime(str(datetime.timedelta(milliseconds=self.total_play_time_ms)), "%H:%M:%S.%f")
        except ValueError:
            t = datetime.datetime.strptime(str(datetime.timedelta(milliseconds=self.total_play_time_ms)), "%H:%M:%S")

        screen.blit(self.font.render(f"| {self.frame} / {t.strftime('%M:%S.%f')[:-3]} {('(F)' if self.finished else '')}", True, (255, 255, 255)), (50 + self.player_count * 170, y))

        for i in range(30):

            try:
                line = self.file_contents[i + self.playing_offset + self.frame - 1]

                if not any(str(line).startswith(prefix) for prefix in ["|0|", "|1|", "|2|", "|3|", "|4|"]):
                    continue

            except IndexError:

                if not self.pre_finished:
                    line = "Movie end"

                    self.last_line = i + self.playing_offset + self.frame - 1
                    self.pre_finished = True
                else:
                    line = ""

            if i + self.playing_offset + self.frame - 1 == self.last_line:
                line = "Movie end"

            real_inputs = get_inputs(line)

            for j in range(real_inputs.__len__()):

                display_inputs = real_inputs[j]

                if j == 0 and i == 0:
                    screen.blit(self.font.render(">", True, (255, 255, 255)), (50, y))

                display_inputs = display_inputs.replace(".", " ")
                screen.blit(self.font.render(display_inputs, True, (255, 255, 255)), (80 + (j * 170), y + i * 30))

        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.run = False
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.playing = not self.playing
                elif event.key == pygame.K_r:
                    self.frame = 0

    def update_time(self):
        if self.playing:
            self.frame += 1

            if not self.finished:
                self.total_play_time_ms = (self.frame / (39375000 / 655171)) * 1000
