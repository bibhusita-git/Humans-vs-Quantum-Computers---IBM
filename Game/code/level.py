from curses.ascii import SP
import pygame
from tiles import Tile
from settings import tile_size, player_speed, screen_width
from player import Player

class Level:
    def __init__(self, level_data, surface):

        ## Level setup
        self.display_surface = surface
        self.setup_level(level_data)

        # speed with which the screen is scrolling horizontally: If world_shift is positive then tiles will move forward, if world_shift is negative tiles will move backword
        self.world_shift = 0
        self.current_x = 0

    def setup_level(self, layout):
        
        ## Create sprite group for tiles
        self.tiles = pygame.sprite.Group()

        ## Create sprite group for player
        self.player = pygame.sprite.GroupSingle() # Using 'GroupSingle()' instead of 'Group()' because we will only have one player

        ## Get row and columns from level map
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row): # cell = column = col
                x = col_index * tile_size
                y = row_index * tile_size
                
                # Draw tiles at 'X'
                if cell == 'X':
                    tile = Tile((x, y), tile_size) # create tile
                    self.tiles.add(tile) # add 'tile' to 'tiles' group

                # Draw player at initial Position 'P'
                if cell == 'P':
                    player = Player((x, y), self.display_surface)
                    self.player.add(player)

    # Creating a camera to scroll level/screen in horizontal direction according to player movement
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # using percentage of screen_width for making the game responsive
        leftbar = screen_width / 6 # leftbar: player can't go behind this left limit
        rightbar = screen_width - leftbar # rightbar: player can't go after this right limit: rightbar = screen_width - leftbar = screen_width - [screen_width / 6] = screen_width * (5/6)

        # when player reaches leftbar, player stops and screen scroll starts towards right, hence it seems like player is moving towards left
        if player_x < leftbar and direction_x < 0: 
            self.world_shift = player_speed
            player.speed = 0

        # when player reaches rightbar, player stops and screen scroll starts towards left, hence it seems like player is moving towards right
        elif player_x > rightbar and direction_x > 0: 
            self.world_shift = -player_speed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player_speed

    def horizontal_movement_collision(self):
        player = self.player.sprite
        # move the player
        player.rect.x += player.direction.x * player.speed

        # Check collision of player with every tile in horizontal direction
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # if player is moving towards  left and we have collision, collision will be from left side of player
                if player.direction.x < 0: # player moving left
                    player.rect.left = sprite.rect.right # place the player right of the tile
                    player.direction.x = 0
                    player.on_left = True
                    self.current_x = player.rect.left
                
                # if player is moving towards  right and we have collision, collision will be from right side of player
                elif player.direction.x > 0: # player is moving right
                    player.rect.right = sprite.rect.left # place the player left of the tile
                    player.direction.x = 0 
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    
    def vertical_movement_collision(self):
        player = self.player.sprite
        # move the player
        player.apply_gravity()
        
        # Check collision of player with every tile in vertical direction
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # if player is moving downward and we have collision, collision will be from bottom side of player
                if player.direction.y > 0: # player moving downward
                    player.rect.bottom = sprite.rect.top # place the player above the tile
                    player.direction.y = 0
                    player.on_ground = True

                # if player is moving upward and we have collision, collision will be from top side of player
                elif player.direction.y < 0: # player is moving upward
                    player.rect.top = sprite.rect.bottom # place the player below the tile
                    player.direction.y = 0
                    player.on_ceiling = True
        
        if player.on_ground and player.direction.y < 0 or player.direction.y > 0: # when player is jumping
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0: # when player is falling
            player.on_ceiling = False

    def run(self):

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        