# python standard library modules
import os
import random
import sys

# pygame
import pygame
from pygame.locals import *

# our modules
from classes import *
from globals import *
from skills import *

# set window starting position for my desktop which has multiple monitors, this
# is a convenience thing for me.  You guys can add your own setting here if
# it's useful for you
if os.environ['COMPUTERNAME'] == 'BRIAN-DESKTOP':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(1920, 90)
if os.environ['COMPUTERNAME'] == 'MAX-LT':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(50, 30)

# @PYGAMERUNSPECIAL  setting for my IDE
# -------------------------------------------------------------------------


class GameLoop:
    def __init__(self):
        def _setup_display():
            # set the window size - can add the NOFRAME arg if we don't want a
            # window frame but then we have to figure out how to move the
            # window since it won't have a menu bar to grab
            pygame.display.set_mode((1280, 600))
            pygame.display.set_caption('Famished Tournament')
            self.surface = pygame.display.get_surface()

        def _setup_time():
            self.clock = pygame.time.Clock()
            self.fps = 30
            pygame.time.set_timer(TIME_TICK_EVENT, 250)
            pygame.time.set_timer(REGENERATION_EVENT, 1000)
            self.game_time = GameTime()

        def _setup_input():
            pygame.key.set_repeat(100, 10)  # allow multiple KEYDOWN events
            self.input = Input()

        def _setup_Rects():
            self.window = self.surface.get_rect()
            self.window_border = Rect2(left=0, top=0, width=1278, height=600)
            self.play_area_border = Rect2(left=40, top=0, width=1200, height=500)
            self.player1 = Player(id=1, left=200, top=150, width=30, height=40)
            self.player1_eyeball = Rect2(left=200, top=150, width=5, height=5)
            # self.player2 = Player(id=2, left=1080, top=150, width=30, height=40)
            # self.player2_eyeball = Rect2(left=1080, top=150, width=5, height=5)

            self.arena = random.choice((arena1, arena2))
            self.arena = random.choice((arena1,))

        def _setup_fonts():
            self.timer_font = pygame.font.Font('data/viner-hand-itc.ttf', 36)
            self.timer_font_xy = 605, 500
            self.health_font = pygame.font.Font('data/viner-hand-itc.ttf', 55)
            self.health_font_xy = 60, 490
            self.energy_font = pygame.font.Font('data/viner-hand-itc.ttf', 55)
            self.energy_font_xy = 80, 535
            self.pause_font = pygame.font.Font('data/viner-hand-itc.ttf', 200)
            self.pause_font_xy = font_position_center(self.window, self.pause_font, '-PAUSE-')
            self.debug_font_small = pygame.font.SysFont('consolas', 10)  # monospace
            self.debug_font_small_2 = pygame.font.SysFont('lucidasans', 12)  # monospace
            self.debug_font = pygame.font.SysFont('consolas', 20)  # monospace
            self.debug_font_xy1 = 1000, 505
            self.debug_font_xy2 = 1000, 520
            self.debug_font_xy3 = 1000, 540
            self.debug_font_xy4 = 1000, 560
            self.debug_font_xy5 = 800, 505
            # Scrolling text font
            self.st_font = pygame.font.Font('data/viner-hand-itc.ttf', 30)

        def _setup_particles():
            self.active_particles = []

        def _setup_monsters():
            self.active_monsters = []
            self.active_monsters.append(Monster(MONSTER_TABLE[WEAK], 400, 150, self.player1, self.player1))
            self.active_monsters.append(Monster(MONSTER_TABLE[MEDIUM], 400, 150, self.player1, self.player1))
            self.active_monsters.append(Monster(MONSTER_TABLE[ULTIMATE], 400, 150, self.player1, self.player1))
            self.spawn_monsters = False
            pygame.event.post(pygame.event.Event(MONSTER_SPAWN_EVENT))

        def _setup_music():
            pygame.mixer.init()
            pygame.mixer.music.load('data/404error.mp3')
            pygame.mixer.music.play(loops=-1)

        def _setup_rain():
            self.rain_particles = []
            self.rain = Rect2(left=0, top=0, width=1, height=3)
            self.make_rain = False
            pygame.event.post(pygame.event.Event(MORE_RAIN_EVENT))

        def _setup_mouse():
            pygame.mouse.set_visible(False)

        pygame.init()
        initialize_skill_table()
        _setup_display()
        _setup_time()
        _setup_input()
        _setup_Rects()
        _setup_monsters()
        _setup_fonts()
        _setup_particles()
        _setup_music()
        _setup_rain()
        _setup_mouse()

    # ------------------------------------------------------------------------
    def __call__(self):
        while True:
            if not self.input.PAUSED:
                self.handle_input()
                self.handle_monsters()
                self.handle_particles()
                self.draw_screen()
                self.handle_event_queue()
                self.clock.tick(self.fps)
            else:
                self.handle_input()
                self.handle_event_queue()

    # -------------------------------------------------------------------------
    def handle_input(self):

        def _handle_special_input():
            if self.input.PAUSED:
                rendered_font = self.pause_font.render('-PAUSE-', True, RED)
                self.surface.blit(rendered_font, self.pause_font_xy)
                pygame.display.update()

            # if self.input.DEBUG:
            #     try:
            #         exec(input('\nEnter something to exec: '))
            #     except Exception as err:
            #         print('>> {}: {} <<'.format(type(err).__name__, err))

            if self.input.RESET and not self.input.PAUSED:
                self.player1.topleft = self.player1.topleft_initial

            if self.input.EXIT:
                # Add the QUIT event to the pygame event queue to be handled
                # later, at the same time the QUIT event from clicking the
                # window X is handled
                pygame.event.post(pygame.event.Event(QUIT))

        def _handle_player_input():
            if not self.input.PAUSED:
                self.player1(self.input, self.arena)

        self.input.refresh()
        _handle_player_input()
        _handle_special_input()

    # -------------------------------------------------------------------------
    def handle_particles(self):

        def _update_active_particles():
            if self.player1.new_particle:
                if isinstance(self.player1.new_particle, list):
                    for p in self.player1.new_particle:
                        self.active_particles.append(p)
                else:
                    self.active_particles.append(self.player1.new_particle)
                self.player1.new_particle = None
                # Added this part into player inputs; causing bugs if skill doesn't create particle
                # pygame.time.set_timer(USEREVENT + 2, self.player1.new_particle.cooldown)

        def _update_particles():
            for p in self.active_particles:
                if p.expired:
                    self.active_particles.remove(p)
                else:
                    p.update(self.game_time.msec)

        def _check_particle_collisions():
            for p in self.active_particles:
                # opposite = self.player2 if p.belongs_to == self.player1 else \
                #           self.player1
                if isinstance(p, RangeParticle):
                    all_terrain_hit_i = p.p_collidelistall(self.arena.rects)
                    if all_terrain_hit_i:  # False if empty list
                        self.active_particles.remove(p)
                        for i in all_terrain_hit_i:
                            self.arena.rects[i].hits_to_destroy -= 1
                            if self.arena.rects[i].hits_to_destroy == 0:
                                self.arena.rects.pop(i)
                    else:
                        first_hit = p.collidelist(self.active_monsters)
                        if first_hit != -1:
                            p.on_hit(self.active_monsters[first_hit], self.game_time.msec)
                            self.active_particles.remove(p)
                        # else:
                        #    if p.colliderect(opposite):
                        #        p.on_hit(opposite, self.game_time.msec)
                        #        self.active_particles.remove(p)
                else:
                    all_monsters_hit_i = p.collidelistall(self.active_monsters)
                    for i in all_monsters_hit_i:
                        p.on_hit(self.active_monsters[i], self.game_time.msec)

                    first_terrain_hit_i = p.collidelist(self.arena.rects)
                    if first_terrain_hit_i != -1:
                        self.arena.rects[first_terrain_hit_i].hits_to_destroy -= 1
                        if self.arena.rects[first_terrain_hit_i].hits_to_destroy == 0:
                            self.arena.rects.pop(first_terrain_hit_i)
                    # if p.colliderect(opposite):
                    #    p.on_hit(opposite, self.game_time.msec)

        _update_active_particles()
        _update_particles()
        _check_particle_collisions()

    # -------------------------------------------------------------------------
    def handle_monsters(self):
        if self.spawn_monsters and len(self.active_monsters) < self.arena.max_monsters:
            spawn_point = random.choice(list(filter(lambda x: x.spawn_point, self.arena)))  # pick a random spawn point
            self.active_monsters.append(Monster(MONSTER_TABLE[WEAK], spawn_point.left, spawn_point.top, self.player1, self.player1))

        for m in self.active_monsters:
            if m.is_dead():
                self.active_monsters.remove(m)
            else:
                m(self.game_time.msec, self.arena)

        self.spawn_monsters = False

    # -------------------------------------------------------------------------
    def draw_screen(self):
        def _draw_ui():
            self.surface.fill(DGREY)  # dark grey background
            pygame.draw.rect(self.surface, GREEN, self.window_border, 1)  # thin green border
            pygame.draw.rect(self.surface, DKRED, self.play_area_border)  # thick red border

            # font for player's health and energy
            health_display = self.health_font.render(str(self.player1.hit_points), True, RED)
            energy_display = self.energy_font.render(str(int(self.player1.energy)), True, YELLOW)
            self.surface.blit(health_display, self.health_font_xy)
            self.surface.blit(energy_display, self.energy_font_xy)

        def _draw_timer():
            time_display = self.timer_font.render(str(self.game_time), True, BLUE)
            self.surface.blit(time_display, self.timer_font_xy)

        def _draw_debug():
            if self.input.debug_text_on:
                x = '| x:{:>8.2f}|'.format(self.player1.x)
                y = '| y:{:>8.2f}|'.format(self.player1.y)
                dx = '|dx:{:>8.2f}|'.format(self.player1.dx)
                dy = '|dy:{:>8.2f}|'.format(self.player1.dy)
                debug_font_1 = self.debug_font.render(x, True, GREEN)
                debug_font_2 = self.debug_font.render(y, True, GREEN)
                debug_font_3 = self.debug_font.render(dx, True, GREEN)
                debug_font_4 = self.debug_font.render(dy, True, GREEN)
                self.surface.blit(debug_font_1, self.debug_font_xy1)
                self.surface.blit(debug_font_2, self.debug_font_xy2)
                self.surface.blit(debug_font_3, self.debug_font_xy3)
                self.surface.blit(debug_font_4, self.debug_font_xy4)

                num_monsters = '|monsters:{:>2}|'.format(len(self.active_monsters))
                debug_font_m = self.debug_font.render(num_monsters, True, GREEN)
                self.surface.blit(debug_font_m, self.debug_font_xy5)

        def _draw_map():
            for rect in self.arena:
                if rect.color is not None:
                    pygame.draw.rect(self.surface, rect.color, rect)

        def _draw_destructible_terrain_debug_text():
            for rect in filter(lambda x: x.hits_to_destroy > 0, self.arena):
                rendered_debug_font = self.debug_font_small_2.render(str(rect.hits_to_destroy), True, BLACK)
                pos = font_position_center(rect, self.debug_font_small_2, str(rect.hits_to_destroy))
                self.surface.blit(rendered_debug_font, pos)

        def _draw_players():
            pygame.draw.rect(self.surface, LBLUE, self.player1)
            if self.player1.facing_direction == LEFT:
                self.player1_eyeball.topleft = self.player1.topleft
                self.player1_eyeball.move_ip((+3, 3))
            else:
                self.player1_eyeball.topright = self.player1.topright
                self.player1_eyeball.move_ip((-3, 3))
            pygame.draw.rect(self.surface, DKRED, self.player1_eyeball)

        def _draw_monsters():
            for m in self.active_monsters:
                pygame.draw.rect(self.surface, ORANGE, m)
                health_bar = Rect2(left=m.left, top=m.top - 8, width=m.width, height=6)
                health_bar_width = round(m.width * (m.hit_points / m.hit_points_max))
                health_bar_life = Rect2(left=m.left, top=m.top - 8, width=health_bar_width, height=6)

                pygame.draw.rect(self.surface, WHITE, health_bar)
                pygame.draw.rect(self.surface, RED, health_bar_life)
                pygame.draw.rect(self.surface, BLACK, health_bar, 1)

        def _draw_particles():
            for p in self.active_particles:
                pygame.draw.rect(self.surface, p.color, p)

        def _draw_scrolling_text():
            for t in self.player1.st_buffer:
                self.surface.blit(self.st_font.render('-' + str(int(t[0])), True, RED),
                (self.player1.centerx, self.player1.top - (3000 - t[1] + self.game_time.msec) / 50))
                if t[1] <= self.game_time.msec:
                    self.player1.st_buffer.remove(t)
            # for t in self.player2.st_buffer:
            #    self.surface.blit(self.st_font.render("-"+str(int(t[0])), True, RED), \
            #    (self.player2.centerx, self.player2.top - (3000 - t[1] + self.game_time.msec)/50))
            #    if t[1] <= self.game_time.msec:
            #        self.player2.st_buffer.remove(t)
            for m in self.active_monsters:
                for t in m.st_buffer:
                    self.surface.blit(self.st_font.render('-' + str(int(t[0])), True, RED),
                    (m.centerx, m.top - (3000 - t[1] + self.game_time.msec) / 50))
                    if t[1] <= self.game_time.msec:
                        m.st_buffer.remove(t)

        def _draw_rain():
            if self.make_rain:
                for i in range(5, self.arena.play_area_rect.width, 10):
                    rain_copy = self.rain.copy()
                    rain_copy.left = i + self.arena.play_area_rect.left
                    self.rain_particles.append(rain_copy)

            for r in self.rain_particles:
                r.move_ip((0, 5))
                pygame.draw.rect(self.surface, BLUE, r)

            for r in self.rain_particles[:]:
                if r.top > self.arena.play_area_rect.height:
                    self.rain_particles.remove(r)
            self.make_rain = False

        def _draw_mouse_text():
            mouse_pos = pygame.mouse.get_pos()
            play_area_mouse_pos = mouse_pos[0] - self.arena.play_area_rect.left, mouse_pos[1]
            if 0 <= play_area_mouse_pos[0] <= self.arena.play_area_rect.width and \
                    0 <= play_area_mouse_pos[1] <= self.arena.play_area_rect.height:
                pygame.draw.circle(self.surface, BLACK, mouse_pos, 2, 1)
                rendered_debug_font = self.debug_font_small.render(str(play_area_mouse_pos), True, BLACK)
                self.surface.blit(rendered_debug_font, mouse_pos)

        _draw_ui()
        _draw_timer()
        _draw_debug()
        _draw_map()
        _draw_destructible_terrain_debug_text()
        _draw_monsters()
        _draw_players()
        _draw_particles()
        _draw_scrolling_text()
        # _draw_rain()
        _draw_mouse_text()
        pygame.display.update()

    # -------------------------------------------------------------------------
    def handle_event_queue(self):

        def _handle_time_tick_event():
            for event in pygame.event.get(TIME_TICK_EVENT):
                if event.type == TIME_TICK_EVENT:
                    self.game_time.inc()

                    # Player 1 conditions
                    for k, v in self.player1.conditions.items():
                        for e in v:
                            if e.is_expired(self.game_time.msec):
                                self.player1.conditions[k].remove(e)

                    # Player 2 conditions
                    # for k,v in self.player2.conditions.items():
                    #    for e in v:
                    #        if e.is_expired(self.game_time.msec):
                    #            self.player2.conditions[k].remove(e)

                    # Monster conditions
                    for m in self.active_monsters:
                        for k,v in m.conditions.items():
                            for e in v:
                                if e.is_expired(self.game_time.msec):
                                    m.conditions[k].remove(e)

        def _handle_regeneration_event():
            for event in pygame.event.get(REGENERATION_EVENT):
                if event.type == REGENERATION_EVENT:
                    if self.player1.conditions[WOUNDED] and not self.player1.conditions[INVIGORATED]:
                        self.player1.hit_points += self.player1.level / 20
                    elif not self.player1.conditions[WOUNDED] and self.player1.conditions[INVIGORATED]:
                        self.player1.hit_points += self.player1.level / 5
                    else:
                        self.player1.hit_points += self.player1.level / 10
                    if self.player1.hit_points > 100:
                        self.player1.hit_points = 100

                    if self.player1.conditions[WEAKENED] and not self.player1.conditions[EMPOWERED]:
                        self.player1.energy += self.player1.level / 10
                    elif not self.player1.conditions[WEAKENED] and self.player1.conditions[EMPOWERED]:
                        self.player1.energy += self.player1.level / 2.5
                    else:
                        self.player1.energy += self.player1.level / 5
                    if self.player1.energy > 10:
                        self.player1.energy = 10

        def _handle_player_lock_events():
            for event in pygame.event.get(PLAYER1_LOCK_EVENT):
                # player 1 skill lock timer
                if event.type == PLAYER1_LOCK_EVENT:
                    self.player1.attack_cooldown_expired = True
                    pygame.time.set_timer(PLAYER1_LOCK_EVENT, 0)

        def _handle_player_meditate_events():
            for event in pygame.event.get(PLAYER1_MEDITATE_EVENT):
                if event.type == PLAYER1_MEDITATE_EVENT:
                    self.player1.energy += 5
                    if self.player1.energy > 10:
                        self.player1.energy = 10
                    pygame.time.set_timer(PLAYER1_MEDITATE_EVENT, 0)

        def _handle_rain_event():
            for event in pygame.event.get(MORE_RAIN_EVENT):
                if event.type == MORE_RAIN_EVENT:
                    self.make_rain = True
                    pygame.time.set_timer(MORE_RAIN_EVENT, 150)

        def _handle_monster_spawn_event():
            for event in pygame.event.get(MONSTER_SPAWN_EVENT):
                if event.type == MONSTER_SPAWN_EVENT:
                    self.spawn_monsters = True
                    pygame.time.set_timer(MONSTER_SPAWN_EVENT, 10000)

        def _handle_quit_event():
            for event in pygame.event.get(QUIT):
                # QUIT event occurs when click X on window bar
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

        if not self.input.PAUSED:
            _handle_time_tick_event()
            _handle_regeneration_event()
            _handle_player_lock_events()
            _handle_player_meditate_events()
            _handle_rain_event()
            _handle_monster_spawn_event()
            _handle_quit_event()
            pygame.event.clear()
        else:
            _handle_quit_event()
            self.input._handle_keyboard_updown_events()
            pygame.event.clear()

# -------------------------------------------------------------------------
if __name__ == '__main__':
    GameLoop()()
