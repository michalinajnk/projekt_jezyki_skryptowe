import os
import pygame
import sys
from Login import Game_Info, Register, Login
from TextBox import TextBox
import pygame.freetype
import random
import csv
from Button import Button

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]
TILE = 1
DISTANCE_FOR_I_ENEMIES = SCREEN_WIDTH / 4
# scrolling variables
trshld_SCROLL = 200 #granica kiedy wszysko powinno zacząc sie ruszac
bg_scroll = 0
sc_scroll = 0  # the main one

COLS = 150
ROWS = 16
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
lvl = 1
MAX_LEVELS = 3

# set up font
statFont = pygame.font.Font('amazdoom.ttf', 60)
logFont = pygame.font.Font("PIXEARG_.TTF", 20)
GMFont = pygame.font.Font('amazdoom.ttf', 160)

# creating rate for a gameA
start_clock = pygame.time.Clock()
FPS = 60

# bonuses to take
HEALTH_BOX = 10
AMMO_BOX = 10
GRENADE_BOX = 3

# action of player
move_left = False
move_right = False
shoot = False
grenade = False
grenade_thrown = False
start_game = False
logged = False
# ACTION INDICATORS
IDLE = 0
RUN = 1
JUMP = 2
DEATH = 3

# colour
BG_default = (100, 200, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

GRAVITY = 0.75
map_action = {0: 'Idle', 1: 'Run', 2: 'Jump', 3: 'Death'}

# images

# buttons
start_img = pygame.image.load('img/start.png')
restart_img = pygame.image.load('img/restart.png')
exit_img = pygame.image.load('img/exit.png')
login_img = pygame.image.load('img/login.png')
sign_up_img = pygame.image.load('img/sign_up.png')
try_again_img = pygame.image.load('img/try_again.png')
inst_img = pygame.image.load('img/instruction.png')
stats_img = pygame.image.load('img/stats.png')
confirm_img = pygame.image.load('img/confirm.png')

# amunition
bullet_img = pygame.image.load('img/icons/bullet.png')
grenade_img = pygame.image.load('img/icons/grenade.png')
# boxes
health_box_img = pygame.image.load('img/icons/health_box.png')
ammo_box_img = pygame.image.load('img/icons/ammo_box.png')
grenade_box_img = pygame.image.load('img/icons/grenade_box.png')
boxes = {'Health': health_box_img, 'Ammo': ammo_box_img, 'Grenade': grenade_box_img}

# store tiles in  a list
tiles = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{i}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tiles.append(img)
# bg img
shooter = pygame.image.load('img/shoot_or_die.png')
# shooter = pygame.transform.scale(shooter, (800, 800))
forest_img = pygame.image.load('img/Background/bg.png')
mountain_img = pygame.image.load('img/Background/mountain.png')
sky_img = pygame.image.load('img/Background/sky.png')
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# crating game window

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("SHOOTER GAME")


def draw_txt(text, colour, x, y):
    image = statFont.render(text, True, colour, (x, y))
    screen.blit(image, (x, y))


def draw_stats(ammo, grenades):
    ammo_txt = statFont.render('Ammo:' + str(ammo), True, WHITE)
    screen.blit(ammo_txt, (10, 46))
    grenades_txt = statFont.render('Grenades:' + str(grenades), True, WHITE)
    screen.blit(grenades_txt, (10, 104))


def draw_background_update():
    screen.fill(BG_default)
    width = sky_img.get_width()
    screen.blit(sky_img, (0, 0)) #width - bg_scroll * 0.5
    draw_stats(player.ammo, player.grenades)

    if not player.alive:
        time_since_enter = pygame.time.get_ticks() - start_clock.get_time()
        player.user.update_score(int(1000 * ((lvl * player.ammo) + player.health) / time_since_enter))
        GAME_OVER = GMFont.render('GAME OVER', True, (255, 25, 100))
        screen.blit(GAME_OVER, (200, 200))

def draw_menu_game():
    screen.fill(WHITE)
    screen.blit(sky_img, (0, 0))
    screen.blit(shooter, (90, 200))
    number = 2
    soldier = pygame.image.load(f'img\player\Run\{number}.png')
    soldier = pygame.transform.scale(soldier, (60, 60))
    screen.blit(soldier, (90, 170))
    screen.blit(soldier, (360, 170))
    screen.blit(soldier, (600, 170))


def draw_starter():
    screen.fill(WHITE)
    screen.blit(sky_img, (0, 0))

def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data

class Player(pygame.sprite.Sprite):

    def __init__(self, char_type, x, y, scale, speed, ammo, grenades, user=None):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.grenades = grenades
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.dir = 1
        self.velocity_y = 0
        self.flip = False
        self.jump = False
        self.in_air = True

        if self.char_type == 'enemy':
            self.user = None
        else:
            self.user = user
        # creating motion
        self.animation_list = []
        self.anim_index = 0
        self.action = 0
        # updating a animation |measure the time
        self.update_time = pygame.time.get_ticks()

        self.load_all_animation(scale)
        self.image = self.animation_list[self.action][self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # for intelligent enemies
        self.move_counter = 0
        self.idle = False
        self.idling_counter = 0
        self.eye_sight = pygame.Rect(0, 0, 150, 20)  # if bigger better eye sight

    def set_user(self, usr):
        self.user = usr

    def load_all_animation(self, scale):
        for action in map_action.values():
            list_one_action = []
            num_of_photos = len(os.listdir(f'img/{self.char_type}/{action}'))
            for i in range(num_of_photos):
                img = pygame.image.load(f'img/{self.char_type}/{action}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                list_one_action.append(img)
            self.animation_list.append(list_one_action)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, move_left, move_right):
        sc_scroll = 0
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if move_left:
            dx = -self.speed
            self.flip = True
            self.dir = -1
        if move_right:
            dx = self.speed
            self.flip = False
            self.dir = 1

        # jump
        if self.jump and not self.in_air:
            self.velocity_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y
        dy += self.velocity_y

        for obstacle in world.obstacles:  # detect collision earlier
            if obstacle[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0  # (stop moving)
                # if enemy hit the wall turn him around
                if self.char_type == 'enemy':
                    self.dir *= -1
                    self.move_counter = 0
            # collision in the y direction
            if obstacle[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.velocity_y < 0:  # if below the ground
                    self.velocity_y = 0
                    dy = obstacle[1].bottom - self.rect.top
                elif self.velocity_y >= 0:  # if above the ground
                    self.velocity_y = 0
                    self.in_air = False
                    dy = obstacle[1].top - self.rect.bottom

        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

            # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
        # CHECK IF WE ARE ON THE SCREEN

        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # update player position
        self.rect.x += dx
        self.rect.y += dy

        # scrolling due to position of the player
        if self.char_type == 'player':
            if self.rect.right > SCREEN_WIDTH - trshld_SCROLL or self.rect.left < trshld_SCROLL:
                self.rect.x -= dx
                sc_scroll = -dx  # opposite movement of screen to player

        return sc_scroll, level_complete

    def let_idle(self):
        if random.randint(1, 200) == 1 and not self.idle:
            self.update_action(IDLE)
            self.idle = True
            self.idling_counter = 50

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.85 * self.rect.size[0] * self.dir), self.rect.centery)
            bullet_group.add(bullet)
            # reduce ammo
            self.ammo -= 1

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.anim_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.anim_index += 1
        # if the animation has run out the reset back to the start
        if self.anim_index >= len(self.animation_list[self.action]):
            if self.action == DEATH:
                self.anim_index = len(self.animation_list[self.action]) - 1
            else:
                self.anim_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.anim_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(DEATH)

    def intelligent_moves(self):
        if self.alive and player.alive:
            self.let_idle()
            # check if the player is in the eye_sight of enemy:
            if self.eye_sight.colliderect(player.rect):
                self.update_action(IDLE)
                self.shoot()
            else:
                if not self.idle:
                    if self.dir == 1:
                        i_move_right = True
                    else:
                        i_move_right = False
                    i_move_left = not i_move_right
                    self.move(i_move_left, i_move_right)
                    self.update_action(RUN)
                    self.move_counter += 1
                    # update eyesight
                    self.eye_sight.center = (self.rect.centerx + 75 * self.dir, self.rect.centery)
                    if self.move_counter > TILE_SIZE:
                        self.dir *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idle = False
        # scroll enemies
        self.rect.x += sc_scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Platform(object):
    def __init__(self):
        self.obstacles = []  # loaded rock to jump

    def read_data(self, data):  # iterate through csv file
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = tiles[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if 0 <= tile <= 8:
                        self.obstacles.append(tile_data)
                    elif 9 <= tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif 11 <= tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)  # decoration
                    elif tile == 15:  # player
                        player = Player('player', x * TILE_SIZE, y * TILE_SIZE, 2, 5, 20, 6)
                        health_bar = Health_stats(10, 10, player.health, player.health)
                    elif tile == 16:  # enemy
                        enemy = Player('enemy', x * TILE_SIZE, y * TILE_SIZE, 2, 3, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:  # ammo_box
                        ammo_box = Box('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        box_group.add(ammo_box)
                    elif tile == 18:  # grenade box
                        grenade_box = Box('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        box_group.add(grenade_box)
                    elif tile == 19:
                        health_box = Box('Health', x * TILE_SIZE, y * TILE_SIZE)
                        box_group.add(health_box)
                    elif tile == 20:  # exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar

    def draw(self):
        for obstacle in self.obstacles:
            obstacle[1][0] += sc_scroll  # changing x position of a obstacles
            screen.blit(obstacle[0], obstacle[1])  # image and rectangle


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += sc_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += sc_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += sc_scroll




class Health_stats():
    def __init__(self, x, y, health, max_health):
        self.health = health
        self.max_health = max_health
        self.x = x
        self.y = y

    def draw(self, health):
        self.health = health
        percent = self.health / self.max_health
        pygame.draw.rect(screen, WHITE, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, (255, 25, 100), (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * percent, 20))


class Box(pygame.sprite.Sprite):
    def __init__(self, box_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.box_type = box_type
        self.image = boxes[box_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE // 2, y + (TILE - self.image.get_height()))

    def update(self):
        self.rect.x += sc_scroll
        if pygame.sprite.collide_rect(self, player):
            if player.alive:
                if self.box_type == 'Health':
                    player.health += HEALTH_BOX
                    if player.health >= player.max_health:
                        player.health = player.max_health
                elif self.box_type == 'Ammo':
                    player.ammo += AMMO_BOX
                else:
                    player.grenades += GRENADE_BOX
                self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # pos of bullet
        self.direction = player.dir

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed) + sc_scroll
        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # collision with rocks
        for obstacle in world.obstacles:
            if obstacle[1].colliderect(self.rect):
                self.kill()
        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
            self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
            self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.timer_to_blow = 100

        self.velocity_y = -10
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.center = (x, y)  # pos of grenade
        self.direction = player.dir

    def update(self):
        self.velocity_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.velocity_y

        # check collision with the level
        for obstacle in world.obstacles:
            if obstacle[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed

        for obstacle in world.obstacles:  # detect collision earlier
            if obstacle[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0  # (stop moving)
            if obstacle[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.velocity_y < 0:  # going upwards
                    self.velocity_y = 0  # drop back to the ground
                    dy = obstacle[1].bottom - self.rect.top
                elif self.velocity_y > 0:  # if above the ground
                    self.velocity_y = 0
                    self.in_air = False  # falling down
                    dy = obstacle[1].top - self.rect.bottom

        self.rect.x += dx + sc_scroll
        self.rect.y += dy + sc_scroll

        # explosion BOOM
        self.timer_to_blow -= 1
        if self.timer_to_blow <= 0:
            self.kill()  # killing grenade
            boom = Boom(self.rect.x, self.rect.y, 2.0)
            explosion_group.add(boom)


class Boom(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.timer_to_blow = 100
        self.boom_list = []
        self.load_boom_animation(scale)
        self.velocity_y = -10
        self.speed = 7
        self.anim_index = 0
        self.image = self.boom_list[self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # pos of grenade
        self.anim_counter = 0  # controlling animation to change the anim index

    def load_boom_animation(self, scale):
        num_of_photos = len(os.listdir(f'img/explosion/'))
        for i in range(1, num_of_photos + 1):
            img = pygame.image.load(f'img/explosion/exp{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.boom_list.append(img)

    def update(self):
        self.rect.x += sc_scroll
        if pygame.sprite.spritecollide(player, explosion_group, False):
            if player.alive:
                player.health -= 5
        for en in enemy_group:
            if pygame.sprite.spritecollide(en, explosion_group, False):
                if en.alive:
                    en.health -= 50
        boom_speed = 4
        self.timer_to_blow += 1
        if self.timer_to_blow >= boom_speed:
            self.timer_to_blow = 0
            self.anim_index += 1
            # if explosion completed
            if self.anim_index >= len(self.boom_list):
                self.kill()  # deleting image
            else:
                self.image = self.boom_list[self.anim_index]




# groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# buttons
start_btn = Button(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 + 90, start_img, 0.5)
exit_btn = Button(SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 100, exit_img, 0.625)

confirm_btn = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, confirm_img, 1.0)

login_btn = Button(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 + 90, login_img, 1.0)
sign_up_btn = Button(SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 100, sign_up_img, 1.0)
try_again_btn = Button(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 + 90, try_again_img, 0.5)
instruction_btn = Button(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 + 90, inst_img, 0.5)

restart_btn = Button(600, 30, restart_img, 0.5)
stats_btn = Button(600, 60, stats_img, 0.5)
exit_btn_2 = Button(600, 90, exit_img, 0.625)

# text_boxes
login_boxes = []
login_txt_box = TextBox(100, 260, 300, 50, logFont, border=2)
password_txt_box = TextBox(100, 320, 300, 50, logFont, border=2)
login_boxes.append(login_txt_box)
login_boxes.append(password_txt_box)




# list of lists of -1 (empty spaces)
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'level{lvl}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = Platform()
player, health_bar = world.read_data(world_data)


run = True
while run:
    start_clock.tick(FPS)  # start a clock with FPS frequency of movement
    game_info = Game_Info('users.csv')
    draw_starter()
    click_login = login_btn.draw(screen)
    click_sign_up = sign_up_btn.draw(screen)
    login = ''
    password = ''

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
    iterator = 0
    if click_login and not logged:
        done = False
        iterator += 1
        print(str(iterator))
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not logged and event.type == pygame.MOUSEBUTTONDOWN:
                    for box in login_boxes:
                        box.check_click(pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN:
                    for box in login_boxes:  # adding text
                        if box.active:
                            box.add_text(event.key)

            screen.fill((54, 54, 54))
            click_confirm = confirm_btn.draw(screen)
            for box in login_boxes:
                box.draw(screen)
            pygame.display.flip()

            if click_confirm:
                print("Klinknales confirm")
                login = login_txt_box.return_input()
                password = password_txt_box.return_input()
                done = True
                print(game_info.user_exist(login))
                if game_info.user_exist(login):
                    log_vals = Login(login, game_info)
                    if log_vals.check_pass(password):
                        user = game_info.get_user(login)
                        player.set_user(user)
                        logged = True
                        print("Zalogowales sie")
                    else:
                        print("Nieprawidlowe haslo")


                elif not game_info.user_exist(login):
                    print('Nie ma twojego konta')

    elif click_sign_up and not logged:
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not logged and event.type == pygame.MOUSEBUTTONDOWN:
                    for box in login_boxes:
                        box.check_click(pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN:
                    for box in login_boxes:  # adding text
                        if box.active:
                            box.add_text(event.key)

            screen.fill((54, 54, 54))
            click_confirm = confirm_btn.draw(screen)
            for box in login_boxes:
                box.draw(screen)
            pygame.display.flip()

            if click_confirm:
                print("Klinknales confirm")
                login = login_txt_box.return_input()
                password = password_txt_box.return_input()
                done = True

        new_register = Register(login, password, game_info)
        print("Rejestrujesz się")
        player.set_user(game_info.get_user(login))
        logged = True

    if not start_game and logged:
        draw_menu_game()
        click_start = start_btn.draw(screen)
        click_exit = exit_btn.draw(screen)
        if click_start:
            start_game = True
        if click_exit:
            run = False

    if start_game and logged:
        draw_background_update()
        world.draw()
        health_bar.draw(player.health)
        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.intelligent_moves()
            enemy.update()
            enemy.draw()

        box_group.update()
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        water_group.update()
        decoration_group.update()
        exit_group.update()

        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        box_group.draw(screen)
        water_group.draw(screen)
        decoration_group.draw(screen)
        exit_group.draw(screen)

        # ---------------------------------------------------------------------------------------------------------
        # update player actions
        if player.alive:
            if shoot:  # shoot bullets
                player.shoot()
            elif grenade and not grenade_thrown and player.grenades > 0:  # trigger for creating grenades
                grenade = Grenade(player.rect.centerx + (0.6 * player.rect.size[0] * player.dir),
                                  player.rect.top)
                grenade_group.add(grenade)
                player.grenades -= 1
                grenade_thrown = True
            if player.in_air:
                player.update_action(2)  # 2: jump
            elif move_left or move_right:
                player.update_action(1)  # 1: run

            else:

                player.update_action(0)  # 0: idle
            sc_scroll, level_complete = player.move(move_left, move_right)
            #bg_scroll -= sc_scroll

            if level_complete:
                lvl += 1
                #bg_scroll = 0
                world_data = reset_level()
                if lvl <= MAX_LEVELS:
                    # load in level data and create world
                    with open(f'level{lvl}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = Platform()
                    player, health_bar = world.read_data(world_data)
        else:
            sc_scroll = 0
            if restart_btn.draw(screen):
                world_data = reset_level()
                # load in level data and create world
                with open(f'level{lvl}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = Platform()
                player, health_bar = world.read_data(world_data)
            elif exit_btn_2.draw(screen):
                print('klikniety exit')
                don = False
                while not don:
                    print('jestem w pętli exit')
                    screen.fill((54, 54, 54))
                    stats = logFont.render(game_info.get_stats(), True, (255, 25, 100))
                    screen.blit(stats_img, (300, 30))
                    screen.blit(stats, (30, 100))
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            don = True
                            pygame.quit()
                            sys.exit()
            print('juz po petli exit')

    pygame.display.update()
pygame.quit()
