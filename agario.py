# @author brandon, an agario clone using squares made for numworks calculator
# OOP approach compared to most numworks script
from kandinsky import *
from ion import *
import random
import time

# Global Constants
# TODO: implement a camera system, so we can go beyond the given 320x240
WIDTH = 320
HEIGHT = 240
MAX_FOOD = 20

FPS = 20
SECOND_PER_FRAME = 1/FPS

class Game:
    def __init__(self, player):
        self.player = player # We only have on player
        self.foods = []
        self.bots = []

    def draw_game(self, color=(255,255,255)):
        fill_rect(0, 0, WIDTH, HEIGHT, color) # clear screen
        for food in self.foods:
            # Checking if the player is overlapping any of the squares
            if self.player.contains(food):
                self.remove_food(food)
                self.player.size += food.size // 2
                continue
            food.draw_self()
        self.player.draw_self()
        draw_string("Score:{}".format(self.player.size), 0, 0)

    def events(self):
        speed = self.player.speed
        # Input Listeners
        if keydown(KEY_DOWN):
            self.player.y += speed
        if keydown(KEY_RIGHT):
            self.player.x += speed
        if keydown(KEY_LEFT):
            self.player.x -= speed
        if keydown(KEY_UP):
            self.player.y -= speed

    def add_bots(self, player):
        self.bots.append(player)

    def gen_food(self):
        for i in range(MAX_FOOD):
            rand_x, rand_y = random.randint(0, 320), random.randint(0, 240)
            food = Food(rand_x, rand_y)
            self.add_food(food)

    def add_food(self, food):
        self.foods.append(food)

    def remove_food(self, food):
        self.foods.remove(food)

class Square: # all squares
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size # width and height
        self.color = color # a Tuple of rgb values (255, 255, 255)

    def draw_self(self):
        fill_rect(self.x, self.y, self.size, self.size, self.color)

class Player(Square):
    def __init__(self, x, y, color, size=20, speed=5):
        super().__init__(x, y, size, color)
        self.speed = speed

    def contains(self, entity):
        return (entity.x + entity.size) < (self.x + self.size) and (entity.x > self.x) and (entity.y > self.y) and (entity.y + entity.size) < (self.y + self.size)

class Food(Square):
    def __init__(self, x, y, size=10):
        # Not much different from Square object but gives us a default size and color
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        super().__init__(x, y, size, color)

def main():
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    player = Player(WIDTH // 2, HEIGHT // 2, color)
    game = Game(player)
    game.gen_food()
    spf = SECOND_PER_FRAME
    while game.player.size < 100:
        if time.monotonic()-spf >= SECOND_PER_FRAME:
            spf = time.monotonic()
            game.events()
            game.draw_game()
    draw_string("Congratulations", 0, 20)
    draw_string("you beat the game!", 0, 40)
    draw_string("Agario by Brandon", 0, 60)

main()
