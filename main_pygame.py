import os, time
import datetime as dt

import pygame
import random

a_time = dt.datetime.now()

# настройка папки ассетов
game_folder = os.path.dirname(__file__)

img_folder = os.path.join(game_folder, 'img')
snd_dir = os.path.join(game_folder, 'sound')
msc_dir = os.path.join(game_folder, 'music')

pygame.mixer.init()

shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pew.wav'))
shoot_sound.set_volume(0.1)

# expl_sounds = []
# for snd in ['expl3.wav', 'expl6.wav']:
#     expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, snd)))

expl_sound1 = pygame.mixer.Sound(os.path.join(snd_dir, 'expl3.wav'))
expl_sound2 = pygame.mixer.Sound(os.path.join(snd_dir, 'expl6.wav'))

expl_sound1.set_volume(0.2)
expl_sound2.set_volume(0.2)

music = ['Zombies_also_love_to_play_the_fool.mp3']
# 'Heroes_Theme.mp3'

# for msc in ['Zombies_also_love_to_play_the_fool.mp3', 'Chocolate_Soul_Fifty.mp3', 'Heroes_Theme.mp3']:
#     music.append(pygame.mixer.music.load(os.path.join(msc_dir, msc)))

pygame.mixer.music.load(os.path.join(msc_dir, random.choice(music)))
pygame.mixer.music.set_volume(0.8)


FPS = 60
WIDTH = 1080
HEIGHT = 720
# size = [640, 480]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

font_name = pygame.font.match_font('verdana')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_text2(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Octopus Fire", 64, WIDTH / 2, HEIGHT / 4)
    draw_text2(screen, "W-A-S-D", 22, WIDTH / 2 - 70, HEIGHT / 2)
    draw_text(screen, "keys for move", 22, WIDTH / 2 + 70, HEIGHT / 2)
    draw_text2(screen, "N-J-K-L-SPACE", 22, WIDTH / 2 - 80, HEIGHT / 2 + 30)
    draw_text(screen, "keys to fire", 22, WIDTH / 2 + 80, HEIGHT / 2 + 30)
    draw_text2(screen, "ESC", 22, WIDTH / 2 - 40, HEIGHT / 2 + 60)
    draw_text(screen, "for exit", 22, WIDTH / 2 + 40, HEIGHT / 2 + 60)
    draw_text(screen, "Press a SPACE to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            # if event.type == pygame.KEYUP:
            #     waiting = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)

        self.image = player_img
        # self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = 30
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # self.rect.center = (WIDTH / 2, HEIGHT / 2)


        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = 0

        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.now = pygame.time.get_ticks()

    def update(self):
        # self.rect.x += 1
        # self.rect.x += self.speedx
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0

        self.speedx = 0
        self.speedy = 0

        # Здесь проверяются на нажатые клавиши, чтобы не нажимать бесконечно
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_s]:
            self.speedy = 8
        if keystate[pygame.K_w]:
            self.speedy = -8



        if keystate[pygame.K_n]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot_left()
        if keystate[pygame.K_j]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot()
        if keystate[pygame.K_k]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot()
        if keystate[pygame.K_l]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot_right()
        if keystate[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot_down()

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        # now = pygame.time.get_ticks()
        # if now - self.last_shot > self.shoot_delay:
        #     self.last_shot = now
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

    def shoot_down(self):
        # now = pygame.time.get_ticks()
        # if now - self.last_shot > self.shoot_delay:
        #     self.last_shot = now
        bullet_down = Bullet_down(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet_down)
        bullets_down.add(bullet_down)
        shoot_sound.play()

    def shoot_left(self):
        # now = pygame.time.get_ticks()
        # if now - self.last_shot > self.shoot_delay:
        #     self.last_shot = now
        bullet_left = Bullet_left(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet_left)
        bullets_left.add(bullet_left)
        shoot_sound.play()

    def shoot_right(self):
        # now = pygame.time.get_ticks()
        # if now - self.last_shot > self.shoot_delay:
        #     self.last_shot = now
        bullet_right = Bullet_right(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet_right)
        bullets_right.add(bullet_right)
        shoot_sound.play()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        # self.image = pygame.Surface((25, 25))
        # self.image.fill(RED)
        # self.image = meteor_images
        # self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-1, 1)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        # self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = bullet_img
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -8

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

class Bullet_down(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = bullet_img_down
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.top = y + 80
        self.rect.centerx = x
        self.speedy = 10
        # self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

class Bullet_left(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = bullet_img_left
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.top = y + 30
        self.rect.centerx = x - 40
        self.speedy = 0
        self.speedx = -8

    def update(self):
        self.rect.x += self.speedx
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

class Bullet_right(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = bullet_img_right
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.top = y + 30
        self.rect.centerx = x + 40
        self.speedy = 0
        self.speedx = 8

    def update(self):
        self.rect.x += self.speedx
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Инициализация PyGame и звука
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OctopusFire")

background = pygame.image.load(os.path.join(img_folder, '3333.jpg')).convert()
background_rect = background.get_rect(bottomright=(background.get_width() - 740,
               background.get_height() - 460))


player_img = pygame.image.load(os.path.join(img_folder, 'player5.png')).convert()

player_mini_img1 = pygame.image.load(os.path.join(img_folder, 'heart.png')).convert()
player_mini_img = pygame.transform.scale(player_mini_img1, (40, 40))
player_mini_img.set_colorkey(BLACK)

bullet_img = pygame.image.load(os.path.join(img_folder, "bullyell.png")).convert()
bullet_img_down = pygame.image.load(os.path.join(img_folder, "greenbull66.png")).convert()
bullet_img_left = pygame.image.load(os.path.join(img_folder, "left_bullet.png")).convert()
bullet_img_right = pygame.image.load(os.path.join(img_folder, "right_bullet.jpg")).convert()

meteor_images = []
meteor_list = ["bug_re2.png", 'bug.png', 'bug_yellow.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (45, 45))
    explosion_anim['sm'].append(img_sm)

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets_down = pygame.sprite.Group()
bullets_left = pygame.sprite.Group()
bullets_right = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 30
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

for i in range(30):
    newmob()

score = 0
charac_str = ''

# expl_sounds[1].play()

pygame.mixer.music.play(loops=-1)

# Цикл игры ================================================================================
game_over = True
running = True

while running:
    if game_over:
        time_start = 0
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(30):
            newmob()
        score = 0

    time_start = time.monotonic()
    clock.tick(FPS)

    text = f'score: {str(score)}'


    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_a:
            #     player.speedx = -8
            # if event.key == pygame.K_d:
            #     player.speedx = 8
            # if event.key == pygame.K_s:
            #     player.speedy = 8
            # if event.key == pygame.K_w:
            #     player.speedy = -8
            if event.key == pygame.K_SPACE:
                player.shoot_down()
            if event.key == pygame.K_n:
                player.shoot_left()
            if event.key == pygame.K_j:
                player.shoot()
            if event.key == pygame.K_k:
                player.shoot()
            if event.key == pygame.K_l:
                player.shoot_right()
            if event.key == pygame.K_ESCAPE:
                game_over = True
                show_go_screen()

            # if event.type == pygame.KEYDOWN:
            #     if pygame.K_0 < event.key < pygame.K_9:  # checks key pressed
            #         character = chr(event.key)  # conv num to char
            #         charac_str += str(character)  # add num to end of string
            #         screen.blit(charac_str)

        if event.type == pygame.QUIT:
            running = False


    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
        expl_sound2.play()

    hits = pygame.sprite.groupcollide(mobs, bullets_down, True, True)
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
        expl_sound2.play()

    hits = pygame.sprite.groupcollide(mobs, bullets_left, True, True)
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
        expl_sound2.play()

    hits = pygame.sprite.groupcollide(mobs, bullets_right, True, True)
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
        # random.choice(expl_sounds).play()
        expl_sound2.play()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    death_explosion = Explosion(player.rect.center, 'lg')

    for hit in hits:
        expl_sound1.play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        player.shield -= 50
        if player.shield <= 0:
            player.hide()
            player.lives -= 1
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if player.lives > 0:
                player.shield = 100
                player.rect.centerx = WIDTH / 2
                player.rect.bottom = HEIGHT - 10

            elif player.lives == 0:
                    # game_over = True
                    all_sprites.add(death_explosion)
                    player.kill()
                    for mob in mobs:
                        mob.kill()
                    with open('score_table.txt', 'a') as f:
                        print(f'{score:05} - name - {a_time.year}-{a_time.month:02}-{a_time.day:02} {a_time.hour:02}:{a_time.minute:02}', file=f)
                    #     a1 = f.readlines()
                    #     a1.insert(1, f'{score} - name - {a_time.year}-{a_time.month:02}-{a_time.day:02} {a_time.hour:02}:{a_time.minute:02}')
                    #
                    # with open('score_table.txt', 'w') as f2:
                    #     f2.writelines(a1)
                # draw_text(screen, 'Game Over', 30, WIDTH / 2, 10)
                # time.sleep(10)
                # running = False


    # if hits:
    #     if not lives == 1:
    #         lives -= 1
    #         player.rect.centerx = WIDTH / 2
    #         player.rect.bottom = HEIGHT - 10
    #         expl_sounds[0].play()
    #     else:
    #         running = False

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    font_name = pygame.font.match_font('verdana')

    if player.lives == 0:
        draw_text(screen, f"Your score: {score}", 64, WIDTH / 2, HEIGHT / 2)

    draw_text(screen, text, 30, WIDTH / 2, 1)
    draw_shield_bar(screen, 10, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    pygame.display.flip()

pygame.quit()

