from ion import *
from kandinsky import *
from random import randint
from math import floor

class Color:
  self.background = (0, 0, 0)
  self.silo = (0, 255, 0)
  self.text = (255, 255, 255)
  self.gray = (50, 50, 50)
  
class Silo:
  def __init__(self, x, y, num_of_missile):
    self.x = x
    self.y = y
    self.num_of_missile = num_of_missiles
    self.height = 10
    self.width = 30
  
  def draw(self):
    fill_rect(self.x, self.y, self.width, self.height, Color.silo)
  
  def draw_num_of_missiles(self):
    draw_string(str(self.num_of_missiles), self.x, 1, Color.text, Color.background)
  
  def delete(self):
    fill_rect(self.x, self.y, self.width, self.height, Color.background)

class Missile:
  def __init__(self, target, speed):
    self.pos = [randint(10, 310), 0]
    self.start_pos = [self.pos[0], self.pos[1]]
    self.target_pos = [randint(10, 310), 3]
    self.speed = speed
    self.movement = (self.target_pos[0] - self.pos[0]) / (self.target_pos[1] - self.pos[1]) * self.speed
    self.summon_frame = randint(1, 2500)
    
    
  
