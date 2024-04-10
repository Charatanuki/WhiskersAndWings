import math
import os
import sys
import random

import pygame

from scripts.entities import Player, Enemy, Bird
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particles import Particles
from scripts.spark import Spark


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Game')
        self.screen = pygame.display.set_mode((1920, 1080))
        self.display = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((1920, 1080))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]
        self.movement_bird = [False, False, False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'egypt_wood': load_images('tiles/egypt_wood'),
            'egypt_border': load_images('tiles/egypt_border'),
            'brick': load_images('tiles/brick'),
            'stone_border': load_images('tiles/stone_border'),
            'traps': load_images('tiles/traps'),
            'barrier': load_images('tiles/barrier'),
            'platform': load_images('tiles/platforms'),
            'button': load_images('tiles/buttons'),
            'lever': load_images('tiles/levers'),
            'chest': load_images('tiles/chest'),
            'door': load_images('tiles/doors'),
            'key': load_images('tiles/key'),
            'arrow_spawner': load_images('tiles/arrow_spawner'),
            'arrow': load_images('tiles/arrows'),
            'player': load_image('entities/player.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'player2/idle': Animation(load_images('entities/player2/idle'), img_dur=6),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }

        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.3)

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (200, 1000), (35, 35))

        self.bird = Bird(self, (1800, 950), (40, 35))

        self.tilemap = Tilemap(self, tile_size=64)

        self.layout = True

        self.level = 0
        self.load_level(0)

        self.screenshake = 0

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos'].copy()
                self.player.air_time = 0
            elif spawner['variant'] == 1:
                self.bird.pos = spawner['pos'].copy()
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/music/' + str((min(self.level, len(os.listdir('data/music')) - 1))) + '.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.player.death = False
        self.bird.death = False

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

    def run(self):

        self.sfx['ambience'].play(-1)

        while True:
            self.display.fill((0, 0, 0, 0))
            self.display_2.fill((0, 140, 233))

            self.screenshake = max(0, self.screenshake - 1)

            if len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1

            if (self.player.death or self.bird.death) and not self.dead:
                self.dead = 1

            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.load_level(self.level)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_width() / 2 - self.scroll[1]) / 30
            render_scroll = (0, 0)  # (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particles(self, 'leaf', pos,
                                                    velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0), (3, 2))
                self.player.render(self.display, offset=render_scroll)
                self.bird.update(self.tilemap, (self.movement_bird[1] - self.movement_bird[0],
                                                self.movement_bird[3] - self.movement_bird[2]), (3, 3))
                self.bird.render(self.display, offset=render_scroll)

            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0],
                                        projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(
                            Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0),
                                  2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.sfx['hit'].play()
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particles(self, 'particle', self.player.rect().center,
                                                            velocity=[math.cos(angle + math.pi) * speed * 0.5,
                                                                      math.sin(angle + math.pi) * speed],
                                                            frame=random.randint(0, 7)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jump():
                            self.sfx['jump'].play()
                    if event.key == pygame.K_x:
                        self.player.dash()
                    if self.layout:
                        if event.key == pygame.K_a:
                            self.movement_bird[0] = True
                        if event.key == pygame.K_w:
                            self.movement_bird[2] = True
                    else:
                        if event.key == pygame.K_q:
                            self.movement_bird[0] = True
                        if event.key == pygame.K_z:
                            self.movement_bird[2] = True
                    if event.key == pygame.K_d:
                        self.movement_bird[1] = True
                    if event.key == pygame.K_s:
                        self.movement_bird[3] = True
                    if event.key == pygame.K_j:
                        self.layout = not self.layout
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if self.layout:
                        if event.key == pygame.K_a:
                            self.movement_bird[0] = False
                        if event.key == pygame.K_w:
                            self.movement_bird[2] = False
                    else:
                        if event.key == pygame.K_q:
                            self.movement_bird[0] = False
                        if event.key == pygame.K_z:
                            self.movement_bird[2] = False
                    if event.key == pygame.K_d:
                        self.movement_bird[1] = False
                    if event.key == pygame.K_s:
                        self.movement_bird[3] = False

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255),
                                   (self.display.get_width() // 2, self.display.get_height() // 2),
                                   (30 - abs(self.transition)) * 40)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            self.display_2.blit(self.display, (0, 0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2,
                                  random.random() * self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()),
                             (screenshake_offset[0], screenshake_offset[1]))
            pygame.display.update()
            self.clock.tick(60)


Game().run()
