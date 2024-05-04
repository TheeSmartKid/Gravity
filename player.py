import pygame
from settings import *
from debug import debug

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, groups, collide_sprites):
    super().__init__(groups)
    self.image = pygame.Surface((15, 20))
    self.image.fill('blue')
    self.rect = self.image.get_rect(topleft = pos)
    self.hitbox = self.rect.inflate(0,-10)
    self.collision_sprites = collide_sprites

    self.direction = pygame.math.Vector2()
    self.pos = pygame.math.Vector2(self.rect.center)
    self.speed = PLAYER_SPEED

    self.gravity_direction = 'down'
    self.gravity_changable = True
    self.yg = Y_GRAVITY
    self.xg = 0
    self.g_inc_x = 0
    self.g_inc_y = 0.4
    self.g_direction = 'down'
    self.g_count = 0

  def input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
      self.direction.x = -1
      self.gravity_direction = 'left'
    elif keys[pygame.K_d]:
      self.direction.x = 1
      self.gravity_direction = 'right'
    else:
      self.direction.x = 0

    if keys[pygame.K_w]:
      self.gravity_direction = 'up'
      self.direction.y = -1
    elif keys[pygame.K_s]:
      self.direction.y = 1
      self.gravity_direction = 'down'
    else:
      self.direction.y = 0

    if keys[pygame.K_k]:
      self.change_gravity(self.gravity_direction)
      self.gravity_changable = False
      self.g_count = pygame.time.get_ticks()

    if keys[pygame.K_i]:
      self.change_gravity('stop')
      self.g_direction = 'GRAVITYLESS'

  def move(self, dt):
    self.pos.x += self.direction.x * self.speed * dt
    self.hitbox.centerx = round(self.pos.x)
    self.rect.centerx = self.hitbox.centerx
    self.collide('horizontal')

    self.pos.y += self.direction.y * self.speed * dt
    self.hitbox.centery = round(self.pos.y)
    self.rect.centery = self.hitbox.centery
    self.collide('vertical')

  def get_gravity_direction(self):
    if self.xg > 0 and self.yg==0:
      self.g_direction = 'right'
    elif self.xg < 0 and self.yg==0:
      self.g_direction = 'left'
    elif self.xg==0 and self.yg > 0:
      self.g_direction = 'down'
    elif self.xg==0 and self.yg < 0:
      self.g_direction = 'up'

    if self.xg>0 and self.yg>0:
      self.g_direction = 'bottom-right'
    elif self.xg>0 and self.yg<0:
      self.g_direction = 'top-right'
    elif self.xg<0 and self.yg>0:
      self.g_direction = 'bottom-left'
    elif self.xg<0 and self.yg<0:
      self.g_direction = 'top-left'

  def gravity(self, dt):
    if self.xg < 0:
      self.xg -= self.g_inc_x
    elif self.xg > 0:
      self.xg += self.g_inc_x

    if self.yg < 0:
      self.yg -= self.g_inc_y
    elif self.yg > 0:
      self.yg += self.g_inc_y

    if self.direction.y >= MAX_Y_GRAVITY:
      self.direction.y = MAX_Y_GRAVITY
      self.yg = 0
      self.g_inc_y = 0
    elif self.direction.y <= -MAX_Y_GRAVITY:
      self.direction.y = -MAX_Y_GRAVITY
      self.yg = 0
      self.g_inc_y = 0
    if self.direction.x >= MAX_X_GRAVITY:
      self.direction.x = MAX_X_GRAVITY
      self.xg = 0
      self.g_inc_x = 0
    elif self.direction.x <= -MAX_X_GRAVITY:
      self.direction.x = -MAX_X_GRAVITY
      self.xg = 0
      self.g_inc_x = 0

    if self.xg >= 1000:
      self.xg = 1000
    elif self.xg <= -1000:
      self.xg = -1000
    if self.yg >= 1000:
      self.yg = 1000
    elif self.yg <= -1000:
      self.yg = -1000

    self.direction.x += self.xg *dt
    self.direction.y += self.yg *dt

  def change_gravity(self, direction):
    if self.gravity_changable:
      if direction == 'up':
        self.g_inc_x = 0
        self.g_inc_y = 0.4
        self.yg = -Y_GRAVITY
      elif direction == 'down':
        self.g_inc_x = 0
        self.g_inc_y = 0.4
        self.yg = Y_GRAVITY

      if direction == 'left':
        self.g_inc_x = 0.4
        self.g_inc_y = 0
        self.xg = -X_GRAVITY
      elif direction == 'right':
        self.g_inc_x = 0.4
        self.g_inc_y = 0
        self.xg = X_GRAVITY

      if direction == 'stop':
        self.xg = 0
        self.yg = 0
        self.g_inc_x = 0
        self.g_inc_y = 0

    self.gravity_changable = False

  def collide(self, direction):
    for sprite in self.collision_sprites:
      if hasattr(sprite, 'hitbox'):
        if sprite.hitbox.colliderect(self.hitbox):
          if direction == 'horizontal':

            if self.direction.x > 0: # moving right
              self.hitbox.right = sprite.hitbox.left
            if self.direction.x < 0: # moving left
              self.hitbox.left = sprite.hitbox.right
            self.rect.centerx = self.hitbox.centerx
            self.pos.x = self.hitbox.centerx

          if direction == 'vertical':

            if self.direction.y > 0: # moving down
              self.hitbox.bottom = sprite.hitbox.top
            if self.direction.y < 0: # moving up
              self.hitbox.top = sprite.hitbox.bottom
            self.rect.centery = self.hitbox.centery
            self.pos.y = self.hitbox.centery

  def countdown(self):
    if pygame.time.get_ticks() - self.g_count > 500:
      self.gravity_changable = True

  def update(self, dt):
    self.countdown()
    self.input()
    self.get_gravity_direction()
    self.gravity(dt)
    self.move(dt)
    # self.change_gravity(self.gravity_direction)
    debug((self.direction))
    debug("gravity direction: ",30,10)
    debug((self.g_direction), 30, 200)
    debug("ur direction: ",30,400)
    debug((self.gravity_direction), 30, 540)
    debug("can change gravity?", 10, 250)
    debug((self.gravity_changable), 10, 460)