import pygame
from settings import player_speed
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()

        ## Player
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        ## player movement
        # store direction(x, y) in which player has to move: (1, 0) = right, (-1, 0) = left, (0, 1) = up, (0, -1) = down
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = player_speed # speed of player
        self.gravity = 0.8
        self.jump_speed = -16

        ## Dust Particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface

        ## player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = 'Game/graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('Game/graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed # self.frame_index = 1, 1.15, 1.30, ...., 2, ..... ; and animation image will change when self.frame_index will be 1, 2, 3, ...; therefore image will change at equal time intervals
        if self.frame_index >= len(animation):
            self.frame_index = 0 
        
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect - to stop player levetatin on floor
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        if self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()

        ## horizontal movement
        if keys[pygame.K_RIGHT]:
            # increase the speed of player in right direction
            self.direction.x += 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            # increase the speed of player in left direction
            self.direction.x -= 1
            self.facing_right = False
        else:
            self.direction.x = 0

        ## vertical movement
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if self.direction.y == 0: # or if self.on_ground:jump only when player is on ground and do not jump when player already is in air
                self.jump()
    
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > (0 + self.gravity): # since when player is on ground gravity still applies on it so dircction.y = 0 + self.gravity
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()