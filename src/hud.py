import pygame
import toolbox

class HUD():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.state = 'mainmenu'

        self.hud_font = pygame.font.SysFont("consolas", 20)
        self.hud_font_big = pygame.font.SysFont("consolas", 120)

        self.score_text = self.hud_font.render("HUD Test", True, (255, 255, 255))
        
        self.title_image = pygame.image.load("../assets/title.png")
        self.start_blink_timer_max = 80
        self.start_blink_timer = self.start_blink_timer_max
        self.start_text = self.hud_font.render("Press any key to start", True, (255, 255, 255))
        self.tutorial_text = self.hud_font.render("WASD to move, CLICK to shoot, SPACE for crate, RIGHT CLICK for explosive crate", True, (255, 255, 255))

        self.game_over_text = self.hud_font_big.render("Game Over", True, (255, 255, 255))
        self.reset_button = pygame.image.load("../assets/BtnReset.png")
        
        self.crate_icon = pygame.image.load("../assets/Crate.png")
        self.explosive_crate_icon = pygame.image.load("../assets/ExplosiveBarrel.png")
        self.split_shot_icon = pygame.image.load("../assets/iconSplitGreen.png")
        self.stream_shot_icon = pygame.image.load("../assets/iconStream.png")
        self.burst_shot_icon = pygame.image.load("../assets/iconBurst.png")
        self.normal_shot_icon = pygame.image.load("../assets/BalloonSmall2.png")
        
        self.crate_ammo_tile = AmmoTile(self.screen, self.crate_icon, self.hud_font)
        self.explosive_crate_ammo_tile = AmmoTile(self.screen, self.explosive_crate_icon, self.hud_font)
        self.balloon_ammo_tile = AmmoTile(self.screen, self.normal_shot_icon, self.hud_font)
        
    def update(self):
        if self.state == 'ingame':
            self.score_text = self.hud_font.render("Score: " + str(self.player.score), True, (255, 255, 255))
            self.screen.blit(self.score_text, (10, 10))
            
            tile_x = 0
            self.crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.crate_ammo)
            tile_x += self.crate_ammo_tile.width
            self.explosive_crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.explosive_crate_ammo)
            tile_x += self.explosive_crate_ammo_tile.width
            if self.player.shot_type == 'normal':
                self.balloon_ammo_tile.icon = self.normal_shot_icon
            elif self.player.shot_type == 'split':
                self.balloon_ammo_tile.icon = self.split_shot_icon
            elif self.player.shot_type == 'burst':
                self.balloon_ammo_tile.icon = self.burst_shot_icon
            elif self.player.shot_type == 'stream':
                self.balloon_ammo_tile.icon = self.stream_shot_icon

            self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), self.player.special_ammo)

        elif self.state == 'mainmenu':
            self.start_blink_timer -= 1
            if self.start_blink_timer <= 0:
                self.start_blink_timer = self.start_blink_timer_max
            title_x, title_y = toolbox.centeringCoords(self.title_image, self.screen)
            title_y -= 40
            self.screen.blit(self.title_image, (title_x, title_y))
            text_x, text_y = toolbox.centeringCoords(self.start_text, self.screen)
            text_y += 110
            if self.start_blink_timer > 30:
                self.screen.blit(self.start_text, (text_x, text_y+150))
            text_x, text_y = toolbox.centeringCoords(self.tutorial_text, self.screen)
            text_y = self.screen.get_height() - 50
            self.screen.blit(self.tutorial_text, (text_x, text_y))
            
        elif self.state == 'gameover':
            text_x, text_y = toolbox.centeringCoords(self.game_over_text, self.screen)
            text_y -= 60
            self.screen.blit(self.game_over_text, (text_x, text_y))
            self.score_text = self.hud_font.render("Final Score: " + str(self.player.score), True, (255, 255, 255))
            text_x, text_y = toolbox.centeringCoords(self.score_text, self.screen)
            text_y += 0
            self.screen.blit(self.score_text, (text_x, text_y))
            button_x, button_y = toolbox.centeringCoords(self.reset_button, self.screen)
            button_y += 100
            button_rect = self.screen.blit(self.reset_button, (button_x, button_y))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_position):
                        self.state = 'mainmenu'
                        
class AmmoTile():
    def __init__(self, screen, icon, font):
        self.screen = screen
        self.icon = icon
        self.font = font
        self.bg_image = pygame.image.load("../assets/hudTile.png")
        self.width = self.bg_image.get_width()

    def update(self, x, y, ammo):
        tile_rect = self.bg_image.get_rect()
        tile_rect.bottomleft = (x, y)
        self.screen.blit(self.bg_image, tile_rect)
        icon_rect = self.icon.get_rect()
        icon_rect.center = tile_rect.center
        self.screen.blit(self.icon, icon_rect)
        ammo_text = self.font.render(str(ammo), True, (255, 255, 255))
        self.screen.blit(ammo_text, tile_rect.topleft)
