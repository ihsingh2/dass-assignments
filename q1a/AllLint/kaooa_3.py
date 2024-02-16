import sys
import math
import time
import pygame
import logging
from rich.logging import RichHandler
from enum import Enum

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SEGMENT_WIDTH = [
    2 * SCREEN_WIDTH // 9,
    2 * SCREEN_WIDTH // 9,
    2 * SCREEN_WIDTH // 9,
    SCREEN_WIDTH // 3
]
SEGMENT_HEIGHT = 30

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (250, 206, 53)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

class PlayerClass(Enum):
    VULTURE = 0
    CROW = 1

class Game:
    spots = [None for i in range(10)]
    players = None
    winner = None
    start_time = None
    finish_time = None
    moves = 1
    turn = PlayerClass.CROW
    crows_captured = 0
    segments = []
    font = None

    def init():
        vulture = Vulture('V', 100, 400, 26.5)
        crow1 = Crow('C1', 1100, 100, 26.5)
        crow2 = Crow('C2', 1100, 200, 26.5)
        crow3 = Crow('C3', 1100, 300, 26.5)
        crow4 = Crow('C4', 1100, 400, 26.5)
        crow5 = Crow('C5', 1100, 500, 26.5)
        crow6 = Crow('C6', 1100, 600, 26.5)
        crow7 = Crow('C7', 1100, 700, 26.5)

        Game.players = pygame.sprite.Group()
        Game.players.add(vulture, crow1, crow2, crow3, crow4, crow5, crow6, crow7)

        for i in range(4):
            x_coord = sum(SEGMENT_WIDTH[:i])
            y_coord = SCREEN_HEIGHT - SEGMENT_HEIGHT
            rect = pygame.Rect(x_coord, y_coord, SEGMENT_WIDTH[i], SEGMENT_HEIGHT)
            Game.segments.append(rect)

        Game.font = pygame.font.Font(None, 26)
        Game.start_time = time.time()

    def declare_winner(plclass):
        Game.winner = plclass
        Game.finish_time = time.time()

    def handle_event(event):
        for player in Game.players:
            player.handle_event(event)

    def restart():
        Game.winner = None
        Game.spots = [None for i in range(10)]
        for player in Game.players:
            player.show()
        Game.moves = 1
        Game.turn = PlayerClass.CROW
        Game.crows_captured = 0
        Game.start_time = time.time()
        Game.finish_time = None

    def update():
        Game.update_rectangles()
        Game.update_fonts()
        Game.players.draw(screen)
        Game.players.update()

    def update_rectangles():
        pygame.draw.rect(screen, YELLOW, Game.segments[0])
        if Game.turn == PlayerClass.VULTURE:
            pygame.draw.rect(screen, RED, Game.segments[1])
        else:
            pygame.draw.rect(screen, BLUE, Game.segments[1])
        pygame.draw.rect(screen, YELLOW, Game.segments[2])
        pygame.draw.rect(screen, GRAY, Game.segments[3])

    def update_fonts():
        text = []
        text.append(Game.render_move_num())
        text.append(Game.render_next_move())
        text.append(Game.render_crows_captured())
        text.append(Game.render_time_elapsed())

        for i in range(len(Game.segments)):
            x = Game.segments[i].x + (Game.segments[i].width - text[i].get_width()) // 2
            y = Game.segments[i].y + (Game.segments[i].height - text[i].get_height()) // 2
            screen.blit(text[i], (x,y))

    def render_move_num():
        return Game.font.render(f'MOVE: {Game.moves}', True, BLACK)

    def render_next_move():
        if Game.winner is None:
            return Game.font.render(f'{Game.turn.name}', True, WHITE)
        else:
            return Game.font.render(f'{Game.winner.name} WON!', True, WHITE)

    def render_crows_captured():
        return Game.font.render(f'CROWS CAPTURED: {Game.crows_captured}', True, BLACK)

    def render_time_elapsed():
        if Game.winner is None:
            time_elapsed = time.gmtime(time.time() - Game.start_time)
            time_string = time.strftime("%H:%M:%S", time_elapsed)
            return Game.font.render(f'TIME ELAPSED: {time_string}', True, BLACK)
        else:
            time_elapsed = time.gmtime(Game.finish_time - Game.start_time)
            time_string = time.strftime("%H:%M:%S", time_elapsed)
            return Game.font.render(f'TIME ELAPSED: {time_string}', True, BLACK)

class Player(Game, pygame.sprite.Sprite):
    def __init__(self, id, plclass, color, x, y, radius):
        super().__init__()
        self.id = id
        self.plclass = plclass
        self.color = color
        self.radius = radius
        self.init_position = (x, y)
        self.position = -1
        self.__init_graphics__()

    def __init_graphics__(self):
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        #font = pygame.font.Font(None, 28)
        #text_surface = font.render(self.id, True, (255, 255, 255))
        #text_rect = text_surface.get_rect(center=(self.radius, self.radius))
        #self.image.blit(text_surface, text_rect)
        self.rect = self.image.get_rect()
        self.rect.center = self.init_position
        self.speed = 5
        self.dragging = False

    def show(self):
        self.rect.center = self.init_position
        self.position = -1

    def hide(self):
        self.rect.center = (-1000, -1000)
        self.position = -2

    def update(self):
        if Game.winner is None:
            if self.dragging:
                self.rect.center = pygame.mouse.get_pos()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            point_idx = self.find_new_position()
            if point_idx >= 0 and self.is_legal_move(point_idx):
                if self.position != -1:
                    Game.spots[self.position] = None
                Game.spots[point_idx] = self
                self.rect.center = spot_coords[point_idx]
                self.position = point_idx
                self.complete_turn()
            else:
                if self.position == -1:
                    self.rect.center = self.init_position
                elif self.position == -2:
                    pass
                else:
                    self.rect.center = spot_coords[self.position]

    def find_new_position(self):
        for point_idx in range(len(spot_coords)):
            if point_idx != self.position:
                if math.dist(self.rect.center, spot_coords[point_idx]) < (2 * self.radius):
                    if self.plclass == Game.turn:
                        return point_idx
                    else:
                        log.warning('Movement should be in the player\'s turn.')
        return -1

    def is_legal_move(self, point_idx):
        if Game.spots[point_idx] != None:
            log.warning('Movement must be to a vacant spot.')
            return False
        if self.position == -1:
            return True

    def jump_adjacency(self, point_idx):
        jump = (point_idx - self.position) % 10
        if jump in (1,9):
            return True
        elif jump in (2,8):
            if self.position % 2 == 1:
                return True
        log.warning('Movement must be via a single link jump, except for a capture.')
        return False

    def complete_turn(self):
        if Game.turn == PlayerClass.VULTURE:
            Game.turn = PlayerClass.CROW
        else:
            Game.turn = PlayerClass.VULTURE
        if Game.moves == 14:
            log.info('Dropping phase ends.')
        if Game.crows_captured == 4:
            log.info('Vulture has won the game.')
            Game.declare_winner(PlayerClass.VULTURE)
        elif self.vulture_blocked():
            log.info('Crows have won the game.')
            Game.declare_winner(PlayerClass.CROW)
        else:
            Game.moves += 1

    def vulture_blocked(self):
        vulture_idx = -1
        for player_idx in range(len(Game.spots)):
            if Game.spots[player_idx] is not None:
                if Game.spots[player_idx].plclass == PlayerClass.VULTURE:
                    vulture_idx = player_idx
                    break
        else:
            return False

        bool1 = Game.spots[(vulture_idx - 3) % 10] == None
        bool2 = Game.spots[(vulture_idx - 2) % 10] == None
        bool3 = Game.spots[(vulture_idx - 1) % 10] == None
        bool4 = Game.spots[(vulture_idx + 1) % 10] == None
        bool5 = Game.spots[(vulture_idx + 2) % 10] == None
        bool6 = Game.spots[(vulture_idx + 3) % 10] == None

        if bool1 or bool3 or bool4 or bool6:
            return False
        if vulture_idx % 2 == 1:
            if bool2 or bool4:
                return False
        return True

class Vulture(Player):
    def __init__(self, id, x, y, radius):
        super().__init__(id, PlayerClass.VULTURE, RED, x, y, radius)

    def is_legal_move(self, point_idx):
        ret = super().is_legal_move(point_idx)
        if ret is not None: return ret
        ret = self.find_crow(point_idx)
        if ret is not None: return ret
        return self.jump_adjacency(point_idx)

    def find_crow(self, point_idx):
        if self.position % 2 == 0:
            crow_positions = [(self.position + 1) % 10, (self.position - 1) % 10]
            jump_positions = [(self.position + 3) % 10, (self.position - 3) % 10]
        else:
            crow_positions = [(self.position + 2) % 10, (self.position - 2) % 10]
            jump_positions = [(self.position + 3) % 10, (self.position - 3) % 10]
        can_capture = [
            Game.spots[crow_positions[0]] != None and Game.spots[jump_positions[0]] == None,
            Game.spots[crow_positions[1]] != None and Game.spots[jump_positions[1]] == None
        ]
        if can_capture[0] and point_idx == jump_positions[0]:
            self.capture_crow(crow_positions[0])
            return True
        if can_capture[1] and point_idx == jump_positions[1]:
            self.capture_crow(crow_positions[1])
            return True
        if can_capture[0] or can_capture[1]:
            log.warning('Vulture must capture the crow')
            return False

    def capture_crow(self, crow_idx):
        log.info('Crow captured')
        Game.spots[crow_idx].hide()
        Game.spots[crow_idx] = None
        Game.crows_captured += 1

class Crow(Player):
    def __init__(self, id, x, y, radius):
        super().__init__(id, PlayerClass.CROW, BLUE, x, y, radius)

    def is_legal_move(self, point_idx):
        if Game.moves < 14:
            if self.position != -1:
                log.warning('Position of crows cannot be altered, till all crows are on board.')
                return False
        ret = super().is_legal_move(point_idx)
        if ret is not None: return ret
        return self.jump_adjacency(point_idx)

if __name__ == "__main__":
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
    log = logging.getLogger("rich")

    pygame.init()
    pygame.display.set_caption('Kaooa')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Game.init()

    spot_coords = [
        (600, 100),
        (667, 307),
        (888, 307),
        (708, 433),
        (774, 640),
        (600, 514),
        (426, 640),
        (492, 433),
        (312, 307),
        (532, 307)
    ]

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    Game.restart()

        Game.handle_event(event)

        screen.fill(BLACK)
        for i in range(0, len(spot_coords), 2):
            u = spot_coords[i]
            v = spot_coords[(i + 4) % len(spot_coords)]
            pygame.draw.line(screen, WHITE, u, v, width=5)
        for point in spot_coords:
            pygame.draw.circle(screen, WHITE, point, 30)

        Game.update()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
