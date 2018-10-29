import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_pine(x, y):
    arcade.draw_triangle_filled(x + 40, y - 40, x, y - 100, x + 80, y - 100, arcade.color.DARK_GREEN)
    arcade.draw_triangle_filled(x + 40, y, x, y - 60, x + 80, y - 60, arcade.color.DARK_GREEN)
    arcade.draw_lrtb_rectangle_filled(x + 30, x + 50, y - 100, y - 140, arcade.color.DARK_BROWN)


def draw_house(x, y):
   arcade.draw_triangle_filled(x + 50, y, x, y - 60, x + 100, y - 60, arcade.color.DARK_RED)
   arcade.draw_lrtb_rectangle_filled(x + 10, x + 90, y - 60, y - 120, arcade.color.DARK_BLUE)


arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "School project")
arcade.set_background_color(arcade.color.GREEN)

arcade.start_render()

for x in range(1, 19):
    xx = random.randint(0, 700)
    draw_house(xx, random.randint(120, 600));

for x in range(1, 19):
    xx = random.randint(0, 720)
    draw_pine(xx, random.randint(140, 600));

arcade.finish_render()
arcade.run()



