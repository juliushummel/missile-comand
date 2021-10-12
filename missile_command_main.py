from ion import *
from kandinsky import *
from random import randint, choice
from math import floor

'''
move() sets new position, renders it, and deletes the old position
draw() renders the new position
delete() removes the old render
'''

class Pos:
  def __init__(self, pos):
      self.x = pos[0]
      self.y = pos[1]

class Color:
  background = (0, 0, 0)
  ground = (255, 255, 0)
  cursor = (255, 255, 255)
  silo = (0, 255, 0)
  city = (0, 0, 255)
  lock = (255, 255, 255)
  text = (255, 255, 255)
  gray = (50, 50, 50)
  missile = (100, 255, 0)
  anti_missile = (100, 0, 255)
  explosion = [(255, 255, 255), (255, 0, 212)]

  
class Silo:
  def __init__(self, pos, num_of_missiles):
    self.pos = Pos(pos)
    self.num_of_missile = num_of_missiles
    self.size = Pos([10, 30])
    self.cooldown = 0
  
  def draw(self):
    fill_rect(self.pos.x, self.pos.y, self.size.x, self.size.y, Color.silo)
  
  def draw_num_of_missiles(self):
    draw_string(str(self.num_of_missiles), self.pos.x, 1, Color.text, Color.background)
  
  def delete(self):
    fill_rect(self.pos.x, self.pos.y, self.size.x, self.size.y, Color.background)


class Missile:
  def __init__(self, available_targets, speed):
    self.pos = Pos([randint(10, 310), 0])
    self.start_pos = Pos([self.pos[0], self.pos[1]])
    self.target_pos = Pos(choice(available_targets))
    self.speed = speed
    self.movement = (self.target_pos.x - self.pos.x) / (self.target_pos.y - self.pos.y) * self.speed
    self.summon_frame = randint(1, 2500)
    
  def draw(self):
    set_pixel(round(self.pos.x), round(self.pos.y), Color.missile)

  def delete(self):
    delete_pos = [self.start_pos.x, self.start_pos.y]
    for i in range(self.pos.y / self.speed):
      delete_pos.x += self.movement.x
      delete_pos.y += self.movement.y
      set_pixel(round(delete_pos.x), round(delete_pos.y))

  def move(self):
    self.pos.x = self.movement.x
    self.pos.y = self.movement.y
    self.draw()


class AntiMissile:
  def __init__(self, pos, target_pos) -> None:
    self.pos = Pos(pos)
    self.start_pos = Pos(pos)
    self.target_pos = Pos(target_pos)
    self.lock = LockOnTarget(target_pos)
    self.movement = Pos([None, None])
    self.exploded = False
    self.num_of_moves = 0
    self.explosion_width = 0
    self.explosion_frame_index = 1

    if abs(self.target_pos.x - self.pos.x) > abs(self.target_pos.y - self.pos.y):
      if self.target_pos.x - self.pos.x < 0:
        self.movement.x = -1
      else:
        self.movement.x = 1
      self.movement.y = (self.target_pos.y - self.pos.y) / abs(self.target_pos.x - self.pos.x)
    else:
      self.movement.y = -1
      self.movement.x = (self.target_pos.x - self.pos.x) / abs(self.target_pos.y - self.pos.y)

  def move(self):
    for i in range(0, 2):
      self.pos.x += self.movement.x
      self.pos.y += self.movement.y
      self.draw()
      self.num_of_moves += 1
    
  def draw(self):
    set_pixel(round(self.pos.x), round(self.pos.y), Color.anti_missile)
  
  def delete(self):
    delete = self.start_pos
    for i in self.num_of_moves:
      delete.x += self.movement.x
      delete.y += self.movement.y
      set_pixel(round(delete.x), round(delete.y), Color.background)
    self.exploded = True

  def draw_explosion(self):
    self.explosion_width += 1 if self.explosion_width < 20 else 0
    fill_rect(
      round(self.pos.x - self.explosion_width / 2),
      round(self.pos.y - self.explosion_width / 2),
      self.explosion_width,
      self.explosion_width,
      Color.explosion[self.explosion_frame_index // 2]
    )
    self.explosion_frame_index += 1

  def delete_explosion(self):
    fill_rect(
      round(self.pos.x - self.explosion_width / 2),
      round(self.pos.y - self.explosion_width / 2),
      self.explosion_width,
      self.explosion_width,
      Color.background
    )


class City:
  def __init__(self, pos, destroyed=False) -> None:
    self.pos = Pos(pos)
    self.size = Pos([25, 7])
    self.destroyed = destroyed

  def draw(self):
    fill_rect(self.pos.x, self.pos.y, self.size.x, self.size.y, Color.city)
  
  def delete(self):
    fill_rect(self.pos.x, self.pos.y, self.size.x, self.size.y, Color.background)


class Cursor:
  def __init__(self, pos, size) -> None:
    self.pos = Pos(pos)
    self.last_pos = Pos(pos)
    self.size = size
  
  def draw(self):
    fill_rect(self.pos.x, self.pos.y - self.size, 1, self.size, Color.cursor)
    fill_rect(self.pos.x, self.pos.y + 1, 1, self.size, Color.cursor)
    fill_rect(self.pos.x + 1, self.pos.y, self.size, 1, Color.cursor)
    fill_rect(self.pos.x - self.size, self.pos.y, self.size, 1, Color.cursor)
  
  def delete(self):
    fill_rect(self.last_pos.x, self.last_pos.y - self.size, 1, self.size, Color.cursor)
    fill_rect(self.last_pos.x, self.last_pos.y + 1, 1, self.size, Color.cursor)
    fill_rect(self.last_pos.x + 1, self.last_pos.y, self.size, 1, Color.cursor)
    fill_rect(self.last_pos.x - self.size, self.last_pos.y, self.size, 1, Color.cursor)

  def move(self):
    self.last_pos = Pos([self.pos.x, self.pos.y])
    if keydown(KEY_RIGHT) and self.pos.x < 320 - self.size:
      self.pos.x += 1
    if keydown(KEY_LEFT) and self.pos.x > self.size:
      self.pos.x -= 1
    if keydown(KEY_UP) and self.pos.y > self.size:
      self.pos.y -= 1
    if keydown(KEY_DOWN) and self.pos.y < 222 - 30:
      self.pos.y += 1
    
    if self.last_pos.x != self.pos.x and self.last_pos.y != self.pos.y:
      self.delete()
    self.draw()


class LockOnTarget:
  def __init__(self, pos) -> None:
    self.pos = Pos(pos)
    self.size = 6
    self.frames = 0

  def draw(self):
    if self.frames % 4 == 0:
      for i in range(0, self.size):
        set_pixel(i + self.pos.x - 4, i - self.pos.y + 4, Color.lock)
        set_pixel(i - self.pos.x + 4, i - self.pos.y + 4, Color.lock)
    elif self.frames % 4 == 2:
      for i in range(0, self.size):
        set_pixel(i + self.pos.x - 4, i - self.pos.y + 4, Color.background)
        set_pixel(i - self.pos.x + 4, i - self.pos.y + 4, Color.background)
    self.frames += 1


def draw_background():
  fill_rect(0, 0, 320, 218, Color.background)
  fill_rect(0, 219, 340, 5, Color.ground)

def create_cities():
  possible_x_positions = [46, 79, 112, 183, 216, 249]
  cities = []
  for pos in possible_x_positions:
    city = City([pos, 210])
    city.draw()
    cities.append(city)
  return cities

def create_silos():
  possible_x_positions = [8, 145, 282]
  silos = []
  for pos in possible_x_positions:
    silo = Silo([pos, 208], 10)
    silos.append(silo)
  return silos

# Setup
draw_background()
cursor = Cursor([100, 100], 3)
cities = create_cities()
silos = create_silos()
targets = cities + silos

# Main Loop
while True:

  # Reset Silos
  for silo in silos:
    silo.draw()
    silo.missiles = 10
    silo.cooldown = 0
  antimissiles = []
  
  # Initialise missiles
  active_missiles = []
  inactive_missiles = []
  for i in range(randint(15, 23)):
    missile = Missile(targets, 0.25)
    inactive_missiles.append(missile)

  # Wave Loop
  for frame in range(3000):
    for silo in silos:
      silo.cooldown += 1
    
    # Summon missiles
    for missile in inactive_missiles:
      if missile.summon_frame == frame:
        active_missiles.append(missile)
        inactive_missiles.remove(missile)

    # Move and Draw missiles
    for missile in active_missiles:
      missile.move()

    # Shoot antimissiles
    if keydown(KEY_ONE) == True and silos[0].missiles > 0 and silos[0].cooldown >= 10: active_silo = silos[0]
    if keydown(KEY_TWO) == True and silos[1].missiles > 0 and silos[1].cooldown >= 10: active_silo = silos[1]
    if keydown(KEY_THREE) == True and silos[2].missiles > 0 and silos[2].cooldown >= 10: active_silo = silos[2]
    
    antimissile = AntiMissile([active_silo.pos.x + 15, active_silo.pos.y], [cursor.pos.x, cursor.pos.y])
    antimissiles.append(antimissile)
    silo.cooldown = 0
    silo.missiles -= 1

    # Move antimissiles
    for am in antimissiles:
      if not am.exploded:
        am.move()
        if am.target_pos.x - 1 < am.pos.x < am.target_pos.x + 1 and am.target_pos.y - 1 < am.pos.y < am.target_pos.y + 1:
          am.delete()
      else:
        am.draw_explosion()
        if am.explosion_frame_index > 70:
          am.delete_explosion()
          antimissiles.remove(am)
          del am
      
      # Collision
      for missile in active_missiles:
        if am.pos.x - am.explosion_width / 2 < missile.pos.x < am.pos.x + am.explosion_width and am.pos.y - am.explosion_width / 2 < missile.pos.y < am.pos.y + am.explosion_width:
          missile.delete()
          active_missiles.remove(missile)
          del missile
          
    for missile in active_missiles:
      missile.move()

    # City Loop
    for city in cities:
      for missile in active_missiles:
        if missile.pos.y >= city.pos.y and city.pos.x <= missile.pos.x <= city.pos.x + city.size.x:
          city.delete()
          city.destroyed = True
          missile.delete()
          active_missiles.remove(missile)
          del missile
    
    # Silo Loop
    for silo in silos:
      if frame % 10 == 0:
        silo.draw_num_of_missiles()
      for missile in active_missiles:
        if missile.pos.y >= silo.pos.y and silo.pos.x <= missile.pos.x <= silo.pos.x + silo.size.x:
          silo.delete()
          silo.missiles = 0
          missile.delete()
          active_missiles.remove(missile)
          del missile
    
    # Cursor
    cursor.move()
    for am in antimissiles:
      am.lock.draw()
