import pygame
import random
import time
from player import Player
from projectile import WaterBalloon
from enemy import Enemy
from crate import Crate
from crate import ExplosiveCrate
from explosion import Explosion
from powerup import PowerUp
from hud import HUD

# Start the game
pygame.init()
pygame.mixer.pre_init(buffer=1024)
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

numofbg = random.randint(0,3)
if numofbg == 0:
    background_image = pygame.image.load("../assets/BG_Sand.png")
elif numofbg == 1:    
    background_image = pygame.image.load("../assets/BG_Grass.png")
elif numofbg == 2:
    background_image = pygame.image.load("../assets/BG_SciFi.png")
else:
    background_image = pygame.image.load("../assets/BG_Urban.png")

playerGroup = pygame.sprite.Group()
projectilesGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
cratesGroup = pygame.sprite.Group()
explosionsGroup = pygame.sprite.Group()
powerupsGroup = pygame.sprite.Group()

Player.containers = playerGroup
WaterBalloon.containers = projectilesGroup
Enemy.containers = enemiesGroup
Crate.containers = cratesGroup
Explosion.containers = explosionsGroup
PowerUp.containers = powerupsGroup

enemy_spawn_timer_max = 100
enemy_spawn_timer = 0
enemy_spawn_speedup_timer_max = 400
enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

game_started = False

render_player = Player(screen, game_width/2, game_height/2)

hud = HUD(screen, render_player)

def StartGame():
    global game_started
    global hud
    global render_player
    global enemy_spawn_timer_max
    global enemy_spawn_timer
    global enemy_spawn_speedup_timer

    enemy_spawn_timer_max = 100
    enemy_spawn_timer = 0
    enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max
    
    game_started = True
    hud.state = 'ingame'
    render_player.__init__(screen, game_width/2, game_height/2)

    for i in range(0, 10):
        ExplosiveCrate(screen, random.randint(0, game_width), random.randint(0, game_height), render_player)
        Crate(screen, random.randint(0, game_width), random.randint(0, game_height), render_player)

# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(background_image, (0,0))
    
    if not game_started:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                StartGame()
                break
    
    if game_started:
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            render_player.move(1, 0, cratesGroup)
        if keys[pygame.K_LEFT]:
            render_player.move(-1, 0, cratesGroup)
        if keys[pygame.K_UP]:
            render_player.move(0, -1, cratesGroup)
        if keys[pygame.K_DOWN]:
            render_player.move(0, 1, cratesGroup)
        if pygame.mouse.get_pressed()[0]:
            render_player.shoot()
        if keys[pygame.K_SPACE]:
            render_player.placeCrate()
        if pygame.mouse.get_pressed()[2]:
            render_player.placeExplosiveCrate()

        enemy_spawn_speedup_timer -= 1
        if enemy_spawn_speedup_timer <= 0:
            if enemy_spawn_timer_max > 10:
                enemy_spawn_timer_max -= 10
            enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

        enemy_spawn_timer -= 1
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy(screen, 0, 0, render_player)
            side_to_spawn = random.randint(0, 3)
            if side_to_spawn == 0:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = -new_enemy.image.get_height()
            elif side_to_spawn == 1:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = game_height + new_enemy.image.get_height()
            elif side_to_spawn == 2:
                new_enemy.x = -new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
            elif side_to_spawn == 3:
                new_enemy.x = game_width + new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
            enemy_spawn_timer = enemy_spawn_timer_max

        for explosion in explosionsGroup:
            explosion.update()
        
        for powerup in powerupsGroup:
            powerup.update(render_player)

        for projectile in projectilesGroup:
            projectile.update()

        for enemy in enemiesGroup:
            enemy.update(projectilesGroup, cratesGroup, explosionsGroup)
        
        for crate in cratesGroup:
            crate.update(projectilesGroup, explosionsGroup)

        render_player.update(enemiesGroup, explosionsGroup)

        if not render_player.alive:
            if hud.state == 'ingame':
                hud.state = 'gameover'
            elif hud.state == 'mainmenu':
                game_started = False
                playerGroup.empty()
                enemiesGroup.empty()
                projectilesGroup.empty()
                powerupsGroup.empty()
                explosionsGroup.empty()
                cratesGroup.empty()

    hud.update()

    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("IncursionGO fps: " + str(clock.get_fps()))
