import sys
import math
import time
import logging
from enum import Enum
from rich.logging import RichHandler
import pygame

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

    @classmethod
    def init(cls):
        vulture = Vulture((100, 400), 26.5)
        crow1 = Crow((1100, 100), 26.5)
        crow2 = Crow((1100, 200), 26.5)
        crow3 = Crow((1100, 300), 26.5)
        crow4 = Crow((1100, 400), 26.5)
        crow5 = Crow((1100, 500), 26.5)
        crow6 = Crow((1100, 600), 26.5)
        crow7 = Crow((1100, 700), 26.5)

        Game.players = pygame.sprite.Group()
        Game.players.add(vulture, crow1, crow2, crow3, crow4, crow5, crow6, crow7)

        for idx in range(4):
            x_coord = sum(SEGMENT_WIDTH[:idx])
            y_coord = SCREEN_HEIGHT - SEGMENT_HEIGHT
            rect = pygame.Rect(x_coord, y_coord, SEGMENT_WIDTH[idx], SEGMENT_HEIGHT)
            Game.segments.append(rect)

        Game.font = pygame.font.Font(None, 26)
        Game.start_time = time.time()

    @classmethod
    def declare_winner(cls, plclass):
        Game.winner = plclass
        Game.finish_time = time.time()

    @classmethod
    def handle_event(cls, new_event):
        for player in Game.players:
            player.handle_event(new_event)

    @classmethod
    def restart(cls):
        Game.winner = None
        Game.spots = [None for i in range(10)]
        for player in Game.players:
            player.show()
        Game.moves = 1
        Game.turn = PlayerClass.CROW
        Game.crows_captured = 0
        Game.start_time = time.time()
        Game.finish_time = None

    @classmethod
    def update(cls):
        Game.update_rectangles()
        Game.update_fonts()
        Game.players.draw(screen)
        Game.players.update()

    @classmethod
    def update_rectangles(cls):
        pygame.draw.rect(screen, YELLOW, Game.segments[0])
        if Game.turn == PlayerClass.VULTURE:
            pygame.draw.rect(screen, RED, Game.segments[1])
        else:
            pygame.draw.rect(screen, BLUE, Game.segments[1])
        pygame.draw.rect(screen, YELLOW, Game.segments[2])
        pygame.draw.rect(screen, GRAY, Game.segments[3])

    @classmethod
    def update_fonts(cls):
        text = []
        text.append(Game.render_move_num())
        text.append(Game.render_next_move())
        text.append(Game.render_crows_captured())
        text.append(Game.render_time_elapsed())

        for idx, _ in enumerate(Game.segments):
            x_offset = (Game.segments[idx].width - text[idx].get_width()) // 2
            y_offset = (Game.segments[idx].height - text[idx].get_height()) // 2
            x_coord = Game.segments[idx].x + x_offset
            y_coord = Game.segments[idx].y + y_offset
            screen.blit(text[idx], (x_coord,y_coord))

    @classmethod
    def render_move_num(cls):
        return Game.font.render(f'MOVE: {Game.moves}', True, BLACK)

    @classmethod
    def render_next_move(cls):
        if Game.winner is None:
            font = Game.font.render(f'{Game.turn.name}', True, WHITE)
        else:
            font = Game.font.render(f'{Game.winner.name} WON!', True, WHITE)
        return font

    @classmethod
    def render_crows_captured(cls):
        return Game.font.render(f'CROWS CAPTURED: {Game.crows_captured}', True, BLACK)

    @classmethod
    def render_time_elapsed(cls):
        if Game.winner is None:
            time_elapsed = time.gmtime(time.time() - Game.start_time)
            time_string = time.strftime("%H:%M:%S", time_elapsed)
            font = Game.font.render(f'TIME ELAPSED: {time_string}', True, BLACK)
        else:
            time_elapsed = time.gmtime(Game.finish_time - Game.start_time)
            time_string = time.strftime("%H:%M:%S", time_elapsed)
            font = Game.font.render(f'TIME ELAPSED: {time_string}', True, BLACK)
        return font

class Player(pygame.sprite.Sprite):
    def __init__(self, plclass, color, center, radius):
        super().__init__()
        #self.identifier = identifier
        self.plclass = plclass
        self.color = color
        self.radius = radius
        self.init_position = center
        self.position = -1
        self.dragging = False
        self.__init_graphics__()

    def __init_graphics__(self):
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        #font = pygame.font.Font(None, 28)
        #text_surface = font.render(self.identifier, True, (255, 255, 255))
        #text_rect = text_surface.get_rect(center=(self.radius, self.radius))
        #self.image.blit(text_surface, text_rect)
        self.rect = self.image.get_rect()
        self.rect.center = self.init_position
        self.speed = 5

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

    def handle_event(self, player_event):
        if player_event.type == pygame.MOUSEBUTTONDOWN and player_event.button == 1:
            if self.rect.collidepoint(player_event.pos):
                self.dragging = True
        elif player_event.type == pygame.MOUSEBUTTONUP and player_event.button == 1:
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
        for point_idx, _ in enumerate(spot_coords):
            if point_idx != self.position:
                if math.dist(self.rect.center, spot_coords[point_idx]) < (2 * self.radius):
                    if self.plclass == Game.turn:
                        return point_idx
                    log.warning('Movement should be in the player\'s turn.')
        return -1

    def is_legal_move(self, point_idx):
        if Game.spots[point_idx] is not None:
            log.warning('Movement must be to a vacant spot.')
            return False
        if self.position == -1:
            return True
        return None

    def jump_adjacency(self, point_idx):
        jump = (point_idx - self.position) % 10
        if jump in (1,9):
            return True
        if jump in (2,8):
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
        for player_idx, _ in enumerate(Game.spots):
            if Game.spots[player_idx] is not None:
                if Game.spots[player_idx].plclass == PlayerClass.VULTURE:
                    vulture_idx = player_idx
                    break
        else:
            return False

        bool1 = Game.spots[(vulture_idx - 3) % 10] is None
        bool2 = Game.spots[(vulture_idx - 2) % 10] is None
        bool3 = Game.spots[(vulture_idx - 1) % 10] is None
        bool4 = Game.spots[(vulture_idx + 1) % 10] is None
        bool5 = Game.spots[(vulture_idx + 2) % 10] is None
        bool6 = Game.spots[(vulture_idx + 3) % 10] is None

        if bool1 or bool3 or bool4 or bool6:
            return False
        if vulture_idx % 2 == 1:
            if bool2 or bool5:
                return False
        return True

class Vulture(Player):
    def __init__(self, center, radius):
        super().__init__(PlayerClass.VULTURE, RED, center, radius)

    def is_legal_move(self, point_idx):
        ret = super().is_legal_move(point_idx)
        if ret is not None:
            return ret
        ret = self.find_crow(point_idx)
        if ret is not None:
            return ret
        return self.jump_adjacency(point_idx)

    def find_crow(self, point_idx):
        if self.position % 2 == 0:
            crow_positions = [(self.position + 1) % 10, (self.position - 1) % 10]
            jump_positions = [(self.position + 3) % 10, (self.position - 3) % 10]
        else:
            crow_positions = [(self.position + 2) % 10, (self.position - 2) % 10]
            jump_positions = [(self.position + 3) % 10, (self.position - 3) % 10]
        can_capture = [
            Game.spots[crow_positions[0]] is not None and Game.spots[jump_positions[0]] is None,
            Game.spots[crow_positions[1]] is not None and Game.spots[jump_positions[1]] is None
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
        return None

    def capture_crow(self, crow_idx):
        log.info('Crow captured')
        Game.spots[crow_idx].hide()
        Game.spots[crow_idx] = None
        Game.crows_captured += 1

class Crow(Player):
    def __init__(self, center, radius):
        super().__init__(PlayerClass.CROW, BLUE, center, radius)

    def is_legal_move(self, point_idx):
        if Game.moves < 14:
            if self.position != -1:
                log.warning('Position of crows cannot be altered, till all crows are on board.')
                return False
        ret = super().is_legal_move(point_idx)
        if ret is not None:
            return ret
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
    RUNNING = True

    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    RUNNING = False
                elif event.key == pygame.K_r:
                    Game.restart()
            else:
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
