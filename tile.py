import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
  def __init__(self, pos, surf, groups):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_rect(topleft = pos)
    self.hitbox = self.rect

  def check_collide(self, player):
    if self.rect.colliderect(player.rect):
      return True
    return False

  def update(self):
    pass