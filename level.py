import pygame
from settings import *
from player import Player
from tile import Tile

class Level():
  def __init__(self, tmx_maps):
    self.display_surface = pygame.display.get_surface()
    self.all_sprites = pygame.sprite.Group()
    self.collison_sprites = pygame.sprite.Group()
    self.setup(tmx_maps)

  def setup(self, tmx_maps):
    for x,y, surf in tmx_maps.get_layer_by_name('Tile Layer 1').tiles():
      Tile((x*TILE_SIZE,y*TILE_SIZE), surf,[self.all_sprites,self.collison_sprites])

    for obj in tmx_maps.get_layer_by_name('Object Layer'):
      if obj.name == 'player':
        self.player=Player((obj.x,obj.y),[self.all_sprites],self.collison_sprites)

  def draw(self, target, dt):
    self.offset = pygame.math.Vector2()
    self.offset.x = target[0] - SCREEN_WIDTH / 2
    self.offset.y = target[1] - SCREEN_HEIGHT / 2
    for sprite in self.all_sprites:
      offset_pos = sprite.rect.topleft - self.offset
      self.display_surface.blit(sprite.image,offset_pos)
      # hitbox highligth good for debugging
      # pygame.draw.rect(self.display_surface,(255,0,0), sprite.hitbox, 2)

  def run(self,dt):
    self.display_surface.fill('black')
    self.draw(self.player.hitbox.center, dt)
    for sprite in self.all_sprites:
      if sprite == self.player:
        self.player.update(dt)
      else:
        sprite.update()